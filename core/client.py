# -*- coding: utf-8 -*-
"""
Module for interacting with Chrome DevTools Protocol (CDP), including
managing virtual displays and handling CDP connections, sessions, and events.

Includes a base class for CDP controllers and a specific WebSocket implementation.
"""

import abc # Abstract Base Classes module
import json
import logging
import threading
import time
import websocket
from typing import Dict, Generator, Optional, Any, TypeVar, Type, Callable, List
from dataclasses import dataclass # Keep dataclass if used elsewhere, remove if only for removed Session
from urllib.parse import urlparse

# Import Chrome DevTools Protocol library components
from cdp.util import _event_parsers, parse_json_event, CDPClient

# Generic TypeVar for typing
T = TypeVar('T')

# Configure basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


def get_devtools_urls(base_url: str, target_id: str, use_secure: bool = None) -> tuple[str, str]:
    """
    Returns (websocket_url, frontend_url) for a given DevTools target ID.

    Args:
        base_url (str): Base URL (e.g. ws://localhost:9222/devtools/browser/UUID).
        target_id (str): Target ID from /json/list.
        use_secure (bool, optional): Force wss/https if True, ws/http if False. Auto-detect if None.

    Returns:
        tuple: (websocket_url, frontend_url)

    Raises:
        RuntimeError: If the base_url is invalid.
    """
    parsed = urlparse(base_url)
    if not parsed.hostname or not parsed.port:
        raise RuntimeError(f"Invalid URL: {base_url}")

    inferred_secure = parsed.scheme in ("wss", "https")
    secure = use_secure if use_secure is not None else inferred_secure

    ws_scheme = "wss" if secure else "ws"
    http_scheme = "https" if secure else "http"

    hostname = parsed.hostname
    port = parsed.port

    websocket_url = f"{ws_scheme}://{hostname}:{port}/devtools/page/{target_id}"
    frontend_url = f"{http_scheme}://{hostname}:{port}/devtools/page/{target_id}"

    return websocket_url, frontend_url

class CDPConnectionError(Exception):
    """Custom exception raised for failures during CDP connection attempts."""
    pass

class CDPError(Exception):
    """Custom exception raised for failures during CDP execution."""
    pass

# --- Abstract Base Class for CDP Controllers ---

class BaseCDPClient(CDPClient, abc.ABC):
    """
    Abstract Base Class defining the interface for a CDP Controller.

    A CDP Controller manages communication with a *single* Chrome DevTools Protocol endpoint.
    Implementations should handle connection, command sending/receiving, and event dispatching.
    """

    def __init__(self, websocket_url: str):
        """
        Initializes the base client.

        Args:
            websocket_url (str): The WebSocket URL to connect to.
        """
        self.ws_url = websocket_url
        # Base logger, can be customized by subclasses
        self.logger = logging.getLogger(f"{self.__class__.__name__}({websocket_url.split('/')[-1]})")

    @property
    @abc.abstractmethod
    def is_connected(self) -> bool:
        """Checks if the connection is currently established and active."""
        raise NotImplementedError

    @abc.abstractmethod
    def connect(self) -> None:
        """Establishes the connection to the endpoint."""
        raise NotImplementedError

    @abc.abstractmethod
    def disconnect(self) -> None:
        """Disconnects from the endpoint and cleans up resources."""
        raise NotImplementedError

    @abc.abstractmethod
    def send(self, cmd_generator: Generator[Dict[str, Any], Optional[Dict[str, Any]], T], _response_timeout: Optional[float] = 30.0) -> Any:
        """
        Executes a CDP command synchronously and waits for its response.

        Args:
            cmd_generator: The generator from a `cdp` command function.
            _response_timeout: Maximum time in seconds to wait for the response.

        Returns:
            The parsed result object from the command's response.

        Raises:
            RuntimeError: If not connected, or for various protocol/communication errors.
            TimeoutError: If the response is not received within the tibmeout.
            Exception: For CDP-reported errors or other unexpected issues.
        """
        raise NotImplementedError

    def get_event_name(self, event_cls: Type[T]) -> str:
        """
        Finds the CDP event method name (string) for a given event class type.
        Relies on the cdp_ast_generated library's internal mapping.
        """
        for method, cls in _event_parsers.items():
            if cls == event_cls:
                return method
        raise ValueError(f"Event class {event_cls.__name__} not registered in cdp_ast_generated.")

    @abc.abstractmethod
    def add_event_listener(self, event_type: Type[T], callback: Callable[[T], None]) -> None:
        """Registers a callback for a specific CDP event type."""
        raise NotImplementedError

    @abc.abstractmethod
    def remove_event_listener(self, event_type: Type[T], callback: Callable[[T], None]) -> None:
        """Removes a previously registered callback for a specific CDP event type."""
        raise NotImplementedError

    # --- Context Manager Protocol (Implemented using abstract methods) ---

    def __enter__(self) -> 'BaseCDPClient':
        """Context manager entry point: connects the client."""
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Context manager exit point: disconnects the client."""
        self.disconnect()


# --- Concrete WebSocket-based CDP Controller Implementation ---

class DevToolsClient(BaseCDPClient):
    """
    Manages communication with a *single* Chrome DevTools Protocol endpoint via WebSocket.

    This class provides a concrete implementation of BaseCDPClient using the
    'websocket-client' library. It handles:
    - Establishing and maintaining the WebSocket connection.
    - Sending CDP commands and receiving responses synchronously for this specific connection.
    - Receiving and dispatching CDP events from this connection to registered listeners.

    It does NOT handle:
    - Target discovery (finding new tabs/pages).
    - Managing connections to multiple targets.
    - Explicit CDP session management (`attachToTarget`, etc.). Commands are sent directly
      over the established WebSocket connection, targeting the entity associated with that
      connection's URL.
    """

    def __init__(self, websocket_url: str, target_id_hint: Optional[str] = None, connection_timeout: float = 10.0, auto_connect=True):
        """
        Initializes the DevToolsClient for a single WebSocket endpoint.

        Args:
            websocket_url (str): The 'webSocketDebuggerUrl' to connect to.
            target_id_hint (Optional[str]): An optional identifier (like TargetID) associated
                                            with this connection, primarily for logging/debugging.
                                            This client does *not* use it for protocol logic.
            connection_timeout (float): Maximum time in seconds to wait for the initial
                                        WebSocket connection to establish.
        """
        # Initialize BaseCDPClient first
        super().__init__(websocket_url=websocket_url)

        # Override logger with more specific name if hint is provided
        self.logger = logging.getLogger(f"DevToolsClient({target_id_hint or websocket_url.split('/')[-1]})")

        self.connection_timeout = connection_timeout

        # Internal state for command management
        self._command_id: int = 0
        self._command_events: Dict[int, threading.Event] = {}
        self._command_results: Dict[int, Any] = {}
        self._lock = threading.Lock() # Protects access to command state & listeners

        # WebSocket and connection state
        self._websocket: Optional[websocket.WebSocket] = None
        self._receiver_thread: Optional[threading.Thread] = None
        self._running: bool = False
        self._connection_event = threading.Event()

        # Event handling
        self._event_listeners: Dict[str, List[Callable[[Any], None]]] = {}

        # Store the hint for reference/debugging if needed
        self._target_id_hint = target_id_hint

        if auto_connect:
            self.connect()

    @property
    def is_connected(self) -> bool:
        """Checks if the WebSocket connection is currently established and running."""
        # Ensure receiver thread is active and connection event is set
        return self._running and self._websocket is not None and self._connection_event.is_set()

    def connect(self) -> None:
        """
        Establishes the WebSocket connection to the configured endpoint.

        Raises:
            CDPConnectionError: If the connection cannot be established within the timeout.
            RuntimeError: If already connected or attempting to connect while stopping.
        """
        # Implementation remains the same as the original class
        if self.is_connected:
            self.logger.warning("Already connected.")
            return
        if self._running and not self._connection_event.is_set():
            raise RuntimeError("Cannot connect while in a disconnecting state.")

        start_time = time.time()
        self.logger.info(f"Attempting to connect to {self.ws_url}...")

        self._running = True
        self._connection_event.clear()

        while time.time() - start_time < self.connection_timeout:
            if not self._running:
                raise CDPConnectionError(f"Connection attempt aborted for {self.ws_url}.")

            try:
                self._websocket = websocket.create_connection(self.ws_url, timeout=5)
                self._websocket.settimeout(1)

                self._connection_event.set()

                self._receiver_thread = threading.Thread(
                    target=self._receive_messages,
                    name=f"cdp_receiver_{self._target_id_hint or 'target'}",
                    daemon=True
                )
                self._receiver_thread.start()

                self.logger.info(f"Successfully connected to {self.ws_url}")
                return

            except Exception as e:
                self.logger.warning(f"Connection attempt failed: {e}. Retrying...")
                if self._websocket:
                    try: self._websocket.close()
                    except: pass
                    self._websocket = None
                time.sleep(1)

        self._running = False
        raise CDPConnectionError(
            f"Failed to connect to {self.ws_url} after {self.connection_timeout} seconds"
        )

    def disconnect(self) -> None:
        """
        DisconDnects from the WebSocket endpoint and cleans up resources.
        """
        # Implementation remains the same as the original class
        if not self._running and not self._websocket:
            self.logger.info("Already disconnected or not connected.")
            return

        self.logger.info(f"Disconnecting from {self.ws_url}...")
        self._running = False
        self._connection_event.clear()

        ws = self._websocket
        self._websocket = None
        if ws:
            try:
                ws.close()
                self.logger.info("WebSocket connection closed.")
            except Exception as e:
                self.logger.warning(f"Error closing websocket: {e}", exc_info=True)

        rt = self._receiver_thread
        self._receiver_thread = None
        if rt and rt.is_alive():
            self.logger.debug("Waiting for receiver thread to join...")
            rt.join(timeout=2.0)
            if rt.is_alive():
                self.logger.warning("Receiver thread did not join cleanly.")

        with self._lock:
            self.logger.debug("Clearing pending command events and results.")
            for cmd_id, event in self._command_events.items():
                self._command_results.setdefault(cmd_id, {'error': {'message': 'Connection closed during command execution'}})
                event.set()
            self._command_events.clear()
            self._command_results.clear()

        self.logger.info(f"Disconnected successfully from {self.ws_url}.")


    def _receive_messages(self) -> None:
        """Background thread loop for receiving messages."""
        # Implementation remains the same as the original class
        self.logger.debug("Receiver thread started.")
        ws = self._websocket
        while self._running and ws:
            try:
                message = ws.recv()
                if not message:
                    if self._running:
                        self.logger.warning("Received empty message, assuming connection closed by remote.")
                        self._handle_connection_lost()
                    break

                try:
                    data = json.loads(message)
                except json.JSONDecodeError:
                    self.logger.error(f"Invalid JSON received: {message[:200]}...")
                    continue

                if 'id' in data:
                    cmd_id = data['id']
                    self.logger.debug(f"Received response for command ID: {cmd_id}")
                    with self._lock:
                        if cmd_id in self._command_events:
                            self._command_results[cmd_id] = data
                            self._command_events[cmd_id].set()
                        else:
                            self.logger.warning(f"Received response for unknown/timed-out command ID: {cmd_id}")
                elif 'method' in data:
                    self.logger.debug(f"Received event: {data.get('method')}")
                    self._handle_event(data)
                else:
                    self.logger.warning(f"Received unexpected message format: {data}")

            except websocket.WebSocketTimeoutException:
                continue
            except (websocket.WebSocketConnectionClosedException, OSError) as e:
                if self._running:
                    self.logger.error(f"WebSocket connection closed unexpectedly: {type(e).__name__} {e}")
                    self._handle_connection_lost()
                break
            except Exception as e:
                if self._running:
                    self.logger.error(f"Error in message receiver loop: {e}", exc_info=True)
                break

        ws = None
        self.logger.debug("Receiver thread finished.")

    def _handle_connection_lost(self):
        """Handles unexpected connection loss."""
        # Implementation remains the same as the original class
        if not self._running:
            return

        self.logger.warning("Connection lost unexpectedly.")
        self._running = False
        self._connection_event.clear()
        self._websocket = None

        with self._lock:
            self.logger.debug("Notifying pending commands about connection loss.")
            for cmd_id, event in list(self._command_events.items()):
                if cmd_id not in self._command_results:
                    self._command_results[cmd_id] = {'error': {'message': 'Connection lost'}}
                event.set()
            self._command_events.clear()


    def _handle_event(self, data: dict) -> None:
        """Processes and dispatches a received CDP event."""
        # Implementation remains the same as the original class
        method = data.get("method")
        if not method:
            self.logger.warning(f"Event data missing 'method': {data}")
            return

        listeners: List[Callable[[Any], None]] = []
        with self._lock:
            listeners = self._event_listeners.get(method, []).copy()

        if not listeners:
            return

        try:
            event_object = parse_json_event(data)
        except Exception as e:
            self.logger.error(f"Failed to parse event {method}: {e} - Data: {data}", exc_info=True)
            return

        self.logger.debug(f"Dispatching event {method} to {len(listeners)} listener(s)")
        for callback in listeners:
            try:
                callback(event_object)
            except Exception as e:
                self.logger.error(
                    f"Error in callback {getattr(callback, '__name__', 'unknown')} for event {method}: {e}",
                    exc_info=True
                )

    # get_event_name is inherited from BaseCDPClient

    def add_event_listener(self, event_type: Type[T], callback: Callable[[T], None]) -> None:
        """Registers a callback for a specific CDP event type."""
        # Uses inherited get_event_name
        try:
            event_name = self.get_event_name(event_type)
        except ValueError as e:
            self.logger.error(f"Failed to add listener: {e}")
            raise

        with self._lock: # Lock protects listener dict access
            if event_name not in self._event_listeners:
                self._event_listeners[event_name] = []
            if callback not in self._event_listeners[event_name]:
                self._event_listeners[event_name].append(callback)
                self.logger.info(f"Added listener for {event_name} ({getattr(callback, '__name__', 'unknown')})")
            else:
                self.logger.warning(f"Callback {getattr(callback, '__name__', 'unknown')} already registered for {event_name}")

    def remove_event_listener(self, event_type: Type[T], callback: Callable[[T], None]) -> None:
        """Removes a previously registered callback for a specific CDP event type."""
        # Uses inherited get_event_name
        try:
            event_name = self.get_event_name(event_type)
        except ValueError as e:
            self.logger.error(f"Failed to remove listener: {e}")
            raise

        with self._lock: # Lock protects listener dict access
            if event_name in self._event_listeners:
                try:
                    self._event_listeners[event_name].remove(callback)
                    self.logger.info(f"Removed listener for {event_name} ({getattr(callback, '__name__', 'unknown')})")
                    # Optional: if not self._event_listeners[event_name]: del self._event_listeners[event_name]
                except ValueError:
                    self.logger.warning(f"Callback {getattr(callback, '__name__', 'unknown')} not found for {event_name}")
            else:
                self.logger.warning(f"No listeners found for event {event_name}")


    def send(self, cmd_generator: Generator[Dict[str, Any], Optional[Dict[str, Any]], T], _response_timeout: Optional[float] = 30.0) -> Any:
        """
        Executes a CDP command synchronously and waits for its response on this connection.
        Implementation remains the same as the original class.
        """
        # Implementation remains the same as the original class
        if not self.is_connected:
            raise RuntimeError("Not connected. Cannot execute command.")
        if not self._websocket:
            raise RuntimeError("WebSocket is not initialized. Cannot execute command.")

        try:
            request: Dict[str, Any] = next(cmd_generator)
        except StopIteration:
            raise RuntimeError("Command generator did not yield a request payload.")
        except Exception as e:
            raise RuntimeError(f"Error obtaining command request from generator: {e}") from e

        with self._lock:
            self._command_id += 1
            current_id = self._command_id
            request['id'] = current_id
            response_event = threading.Event()
            self._command_events[current_id] = response_event
            self._command_results.pop(current_id, None)

        command_name = request.get('method', 'Unknown Command')
        self.logger.debug(f"Sending command ID {current_id}: {command_name}")

        try:
            #print(request)
            payload = json.dumps(request)
            ws = self._websocket
            if not ws:
                raise RuntimeError("Connection closed before command could be sent.")
            ws.send(payload)

            if not response_event.wait(_response_timeout):
                self.logger.error(f"Command ID {current_id} ({command_name}) timed out after {_response_timeout} seconds.")
                with self._lock:
                    self._command_events.pop(current_id, None)
                    self._command_results.pop(current_id, None)
                raise TimeoutError(f"Command '{command_name}' timed out after {_response_timeout} seconds")

            with self._lock:
                response_data = self._command_results.pop(current_id, None)
                self._command_events.pop(current_id, None)

            if response_data is None:
                if not self.is_connected:
                    raise RuntimeError(f"Connection lost after command {current_id} ({command_name}) was sent, response may be missing.")
                else:
                    self.logger.error(f"Internal Error: Command ID {current_id} ({command_name}) response event set, but no result found.")
                    raise RuntimeError(f"No response data found for command {current_id} despite event signal.")

            if 'error' in response_data:
                error_details = response_data['error']
                msg = error_details.get('message', 'No message')
                code = error_details.get('code', 'N/A')
                self.logger.error(f"Command ID {current_id} ({command_name}) failed: {msg} (Code: {code})")
                raise CDPError(f"CDP Error ({code}): {msg}")

            try:
                cmd_generator.send(response_data.get("result"))
                self.logger.error(f"Command {command_name} generator yielded again after sending result.")
                raise RuntimeError(f"Generator for {command_name} did not stop after receiving result.")
            except StopIteration as si:
                self.logger.debug(f"Command ID {current_id} ({command_name}) completed successfully.")
                return si.value
            except Exception as e:
                self.logger.error(f"Error processing result for {command_name} (ID: {current_id}): {e}", exc_info=True)
                raise RuntimeError(f"Error processing command result: {e}") from e

        except websocket.WebSocketConnectionClosedException:
            self.logger.error(f"Connection closed while executing command {command_name} (ID: {current_id}).")
            if self._running:
                self._handle_connection_lost()
            raise RuntimeError(f"Connection closed during command {command_name} execution.")
        except Exception as e:
            self.logger.error(f"Unexpected error executing {command_name} (ID: {current_id}): {e}", exc_info=True)
            with self._lock:
                self._command_events.pop(current_id, None)
                self._command_results.pop(current_id, None)
            raise

    def wait_for_event(self, event_type: Type[T], timeout: float = 30.0) -> T:
        """
        Waits synchronously for a specific CDP event to occur within a given timeout.

        Args:
            event_type (Type[T]): The type of the CDP event to wait for (e.g., cdp.target.TargetCreatedEvent).
            timeout (float): The maximum time in seconds to wait for the event.

        Returns:
            T: The parsed event object when the event is received.

        Raises:
            TimeoutError: If the event is not received within the specified timeout.
            RuntimeError: If the client is not connected.
            ValueError: If the event_type is not a recognized CDP event.
        """
        if not self.is_connected:
            raise RuntimeError("Not connected. Cannot wait for event.")

        event_name: str
        try:
            event_name = self.get_event_name(event_type)
        except ValueError as e:
            self.logger.error(f"Cannot wait for unknown event type: {e}")
            raise

        received_event_data: Optional[T] = None
        event_arrived = threading.Event()

        def _temporary_listener(event: T):
            nonlocal received_event_data
            nonlocal event_arrived
            self.logger.debug(f"Temporary listener caught event {event_name}.")
            received_event_data = event
            event_arrived.set()

        self.logger.debug(f"Waiting for event {event_name} with timeout {timeout}s...")
        self.add_event_listener(event_type, _temporary_listener)

        try:
            if not event_arrived.wait(timeout=timeout):
                self.logger.warning(f"Timeout waiting for event {event_name} after {timeout} seconds.")
                raise TimeoutError(f"Timed out waiting for CDP event: {event_name}")
            else:
                self.logger.debug(f"Event {event_name} received.")
                return received_event_data # type: ignore (Guaranteed to be T by now)
        finally:
            self.remove_event_listener(event_type, _temporary_listener)

    
    def wait_for_event_where(self, event_type: Type[T], predicate: Callable[[T], bool], timeout: float = 30.0) -> T:
        """
        Waits synchronously for a specific CDP event that satisfies a given predicate.

        Args:
            event_type (Type[T]): The type of the CDP event to wait for.
            predicate (Callable[[T], bool]): A function that takes an event object and returns True if it matches criteria.
            timeout (float): The maximum time in seconds to wait for the event.

        Returns:
            T: The parsed event object when the event is received and satisfies the predicate.

        Raises:
            TimeoutError: If no matching event is received within the specified timeout.
            RuntimeError: If the client is not connected.
            ValueError: If the event_type is not a recognized CDP event.
        """
        if not self.is_connected:
            raise RuntimeError("Not connected. Cannot wait for event.")

        event_name: str
        try:
            event_name = self.get_event_name(event_type)
        except ValueError as e:
            self.logger.error(f"Cannot wait for unknown event type: {e}")
            raise

        received_event_data: Optional[T] = None
        event_arrived = threading.Event()

        def _temporary_listener(event: T):
            nonlocal received_event_data
            nonlocal event_arrived
            try:
                if predicate(event):
                    self.logger.debug(f"Temporary listener caught and matched event {event_name}.")
                    received_event_data = event
                    event_arrived.set()
                else:
                    self.logger.debug(f"Temporary listener caught event {event_name} but predicate not met.")
            except Exception as e:
                self.logger.error(f"Error in predicate for event {event_name}: {e}", exc_info=True)
                # Decide if a predicate error should prevent the wait or be ignored
                # For now, it just logs and continues waiting.
                pass # Continue waiting if predicate itself fails

        self.logger.debug(f"Waiting for event {event_name} (with predicate) with timeout {timeout}s...")
        self.add_event_listener(event_type, _temporary_listener)

        try:
            if not event_arrived.wait(timeout=timeout):
                self.logger.warning(f"Timeout waiting for event {event_name} (with predicate) after {timeout} seconds.")
                raise TimeoutError(f"Timed out waiting for CDP event: {event_name} (with predicate)")
            else:
                self.logger.debug(f"Matching event {event_name} received.")
                return received_event_data # type: ignore
        finally:
            self.remove_event_listener(event_type, _temporary_listener)