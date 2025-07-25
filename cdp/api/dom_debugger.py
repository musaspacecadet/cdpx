# # DO NOT EDIT THIS FILE!
# #
# # This file is generated from the CDP specification using AST. If you need to make
# # changes, edit the generator and regenerate all of the modules.

from __future__ import annotations
"""API wrapper for the DOMDebugger domain."""
import typing
from ..util import CDPClient
from .. import dom_debugger as _dom_debugger_module
from .. import dom
from .. import runtime
from deprecated.sphinx import deprecated
None


class DomDebuggerAPI:
    """Provides an API wrapper for the 'DOMDebugger' domain commands.

Domain Description:
DOM debugging allows setting breakpoints on particular DOM operations and events. JavaScript
execution will stop on these operations as if there was a regular breakpoint set."""

    def __init__(self, client: CDPClient) ->None:
        self.client: CDPClient = client

    def get_event_listeners(self, object_id: runtime.RemoteObjectId, depth:
        typing.Optional[int]=None, pierce: typing.Optional[bool]=None,
        _response_timeout: typing.Optional[float]=None) ->typing.List[
        _dom_debugger_module.EventListener]:
        """Returns event listeners of the given object.

NOTE: This is a blocking wrapper method that executes the underlying generator command using the client.


:param ...:

:param object_id: Identifier of the object to return listeners for.

:param depth: *(Optional)* The maximum depth at which Node children should be retrieved, defaults to 1. Use -1 for the entire subtree or provide an integer larger than 0.

:param pierce: *(Optional)* Whether or not iframes and shadow roots should be traversed when returning the subtree (default is false). Reports listeners for all contexts if pierce is enabled.

:param _response_timeout: Optional timeout in seconds for the command.


:returns: Array of relevant listeners."""
        gen = _dom_debugger_module.get_event_listeners(object_id=object_id,
            depth=depth, pierce=pierce)
        return self.client.send(gen, _response_timeout=_response_timeout)

    def remove_dom_breakpoint(self, node_id: dom.NodeId, type_:
        _dom_debugger_module.DOMBreakpointType, _response_timeout: typing.
        Optional[float]=None) ->None:
        """Removes DOM breakpoint that was set using ``setDOMBreakpoint``.

NOTE: This is a blocking wrapper method that executes the underlying generator command using the client.


:param ...:

:param node_id: Identifier of the node to remove breakpoint from.

:param type_: Type of the breakpoint to remove.

:param _response_timeout: Optional timeout in seconds for the command."""
        gen = _dom_debugger_module.remove_dom_breakpoint(node_id=node_id,
            type_=type_)
        return self.client.send(gen, _response_timeout=_response_timeout)

    def remove_event_listener_breakpoint(self, event_name: str, target_name:
        typing.Optional[str]=None, _response_timeout: typing.Optional[float
        ]=None) ->None:
        """Removes breakpoint on particular DOM event.

NOTE: This is a blocking wrapper method that executes the underlying generator command using the client.


:param ...:

:param event_name: Event name.

:param target_name: **(EXPERIMENTAL)** *(Optional)* EventTarget interface name.

:param _response_timeout: Optional timeout in seconds for the command."""
        gen = _dom_debugger_module.remove_event_listener_breakpoint(event_name
            =event_name, target_name=target_name)
        return self.client.send(gen, _response_timeout=_response_timeout)

    @deprecated(version='1.3')
    def remove_instrumentation_breakpoint(self, event_name: str,
        _response_timeout: typing.Optional[float]=None) ->None:
        """Removes breakpoint on particular native event.

NOTE: This is a blocking wrapper method that executes the underlying generator command using the client.

Redirects to command 'EventBreakpoints'.

.. deprecated:: 1.3

**EXPERIMENTAL**


:param ...:

:param event_name: Instrumentation name to stop on.

:param _response_timeout: Optional timeout in seconds for the command."""
        gen = _dom_debugger_module.remove_instrumentation_breakpoint(event_name
            =event_name)
        return self.client.send(gen, _response_timeout=_response_timeout)

    def remove_xhr_breakpoint(self, url: str, _response_timeout: typing.
        Optional[float]=None) ->None:
        """Removes breakpoint from XMLHttpRequest.

NOTE: This is a blocking wrapper method that executes the underlying generator command using the client.


:param ...:

:param url: Resource URL substring.

:param _response_timeout: Optional timeout in seconds for the command."""
        gen = _dom_debugger_module.remove_xhr_breakpoint(url=url)
        return self.client.send(gen, _response_timeout=_response_timeout)

    def set_break_on_csp_violation(self, violation_types: typing.List[
        _dom_debugger_module.CSPViolationType], _response_timeout: typing.
        Optional[float]=None) ->None:
        """Sets breakpoint on particular CSP violations.

NOTE: This is a blocking wrapper method that executes the underlying generator command using the client.

**EXPERIMENTAL**


:param ...:

:param violation_types: CSP Violations to stop upon.

:param _response_timeout: Optional timeout in seconds for the command."""
        gen = _dom_debugger_module.set_break_on_csp_violation(violation_types
            =violation_types)
        return self.client.send(gen, _response_timeout=_response_timeout)

    def set_dom_breakpoint(self, node_id: dom.NodeId, type_:
        _dom_debugger_module.DOMBreakpointType, _response_timeout: typing.
        Optional[float]=None) ->None:
        """Sets breakpoint on particular operation with DOM.

NOTE: This is a blocking wrapper method that executes the underlying generator command using the client.


:param ...:

:param node_id: Identifier of the node to set breakpoint on.

:param type_: Type of the operation to stop upon.

:param _response_timeout: Optional timeout in seconds for the command."""
        gen = _dom_debugger_module.set_dom_breakpoint(node_id=node_id,
            type_=type_)
        return self.client.send(gen, _response_timeout=_response_timeout)

    def set_event_listener_breakpoint(self, event_name: str, target_name:
        typing.Optional[str]=None, _response_timeout: typing.Optional[float
        ]=None) ->None:
        """Sets breakpoint on particular DOM event.

NOTE: This is a blocking wrapper method that executes the underlying generator command using the client.


:param ...:

:param event_name: DOM Event name to stop on (any DOM event will do).

:param target_name: **(EXPERIMENTAL)** *(Optional)* EventTarget interface name to stop on. If equal to ``"*"`` or not provided, will stop on any EventTarget.

:param _response_timeout: Optional timeout in seconds for the command."""
        gen = _dom_debugger_module.set_event_listener_breakpoint(event_name
            =event_name, target_name=target_name)
        return self.client.send(gen, _response_timeout=_response_timeout)

    @deprecated(version='1.3')
    def set_instrumentation_breakpoint(self, event_name: str,
        _response_timeout: typing.Optional[float]=None) ->None:
        """Sets breakpoint on particular native event.

NOTE: This is a blocking wrapper method that executes the underlying generator command using the client.

Redirects to command 'EventBreakpoints'.

.. deprecated:: 1.3

**EXPERIMENTAL**


:param ...:

:param event_name: Instrumentation name to stop on.

:param _response_timeout: Optional timeout in seconds for the command."""
        gen = _dom_debugger_module.set_instrumentation_breakpoint(event_name
            =event_name)
        return self.client.send(gen, _response_timeout=_response_timeout)

    def set_xhr_breakpoint(self, url: str, _response_timeout: typing.
        Optional[float]=None) ->None:
        """Sets breakpoint on XMLHttpRequest.

NOTE: This is a blocking wrapper method that executes the underlying generator command using the client.


:param ...:

:param url: Resource URL substring. All XHRs having this substring in the URL will get stopped upon.

:param _response_timeout: Optional timeout in seconds for the command."""
        gen = _dom_debugger_module.set_xhr_breakpoint(url=url)
        return self.client.send(gen, _response_timeout=_response_timeout)
