import subprocess
import time
import os
import json
import signal
import platform
import tempfile
import shutil
import requests
import logging
from pathlib import Path
from typing import Dict, List, Optional, Union, Tuple
from dataclasses import dataclass
from datetime import datetime

@dataclass
class ChromeProfile:
    """Represents a Chrome profile configuration"""
    name: str
    path: Path
    created_at: datetime
    last_used: datetime
    is_temporary: bool = False

class ProfileManager:
    """Handles Chrome profile management with proper state handling and validation"""
    
    def __init__(self, base_dir: Optional[Path] = None):
        default_dir = os.environ.get("CHROME_PROFILE_DIR", "/tmp/.chrome_profiles")
        self.base_dir = Path(base_dir) if base_dir else Path(default_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)
        self.base_dir.mkdir(parents=True, exist_ok=True)
        self._current_profile: Optional[ChromeProfile] = None
        self._temp_dir: Optional[Path] = None
        
    def get_profile_path(self, name: str) -> Path:
        """Get the full path for a profile name"""
        return self.base_dir / name
    
    def create_temporary(self) -> ChromeProfile:
        """Create a new temporary profile"""
        if self._temp_dir and self._temp_dir.exists():
            shutil.rmtree(self._temp_dir)
            
        self._temp_dir = Path(tempfile.mkdtemp(prefix="chrome_profile_"))
        now = datetime.now()
        profile = ChromeProfile(
            name=self._temp_dir.name,
            path=self._temp_dir,
            created_at=now,
            last_used=now,
            is_temporary=True
        )
        self._current_profile = profile
        return profile
    
    def create(self, name: str) -> ChromeProfile:
        """Create a new persistent profile"""
        if not name.isalnum():
            raise ValueError("Profile name must be alphanumeric")
            
        profile_path = self.get_profile_path(name)
        if profile_path.exists():
            raise ValueError(f"Profile '{name}' already exists")
            
        profile_path.mkdir(parents=True)
        now = datetime.now()
        profile = ChromeProfile(
            name=name,
            path=profile_path,
            created_at=now,
            last_used=now
        )
        
        # Save profile metadata
        self._save_metadata(profile)
        self._current_profile = profile
        return profile
    
    def load(self, name: str) -> ChromeProfile:
        """Load an existing profile"""
        profile_path = self.get_profile_path(name)
        if not profile_path.exists():
            raise ValueError(f"Profile '{name}' does not exist")
            
        metadata = self._load_metadata(name)
        if metadata:
            profile = ChromeProfile(
                name=name,
                path=profile_path,
                created_at=metadata['created_at'],
                last_used=datetime.now()
            )
        else:
            # Handle existing profiles that don't have metadata
            now = datetime.now()
            profile = ChromeProfile(
                name=name,
                path=profile_path,
                created_at=now,
                last_used=now
            )
            self._save_metadata(profile)
            
        self._current_profile = profile
        return profile
    
    def list_profiles(self) -> List[ChromeProfile]:
        """List all available persistent profiles"""
        profiles = []
        for path in self.base_dir.iterdir():
            if path.is_dir():
                metadata = self._load_metadata(path.name)
                if metadata:
                    profiles.append(ChromeProfile(
                        name=path.name,
                        path=path,
                        created_at=metadata['created_at'],
                        last_used=metadata['last_used']
                    ))
                else:
                    # Handle profiles without metadata
                    now = datetime.now()
                    profile = ChromeProfile(
                        name=path.name,
                        path=path,
                        created_at=now,
                        last_used=now
                    )
                    self._save_metadata(profile)
                    profiles.append(profile)
        return sorted(profiles, key=lambda p: p.last_used, reverse=True)
    
    def delete(self, name: str) -> None:
        """Delete a profile and its data"""
        if self._current_profile and self._current_profile.name == name:
            raise ValueError("Cannot delete currently active profile")
            
        profile_path = self.get_profile_path(name)
        if not profile_path.exists():
            raise ValueError(f"Profile '{name}' does not exist")
            
        try:
            shutil.rmtree(profile_path)
        except Exception as e:
            raise RuntimeError(f"Failed to delete profile: {e}")
    
    def cleanup(self) -> None:
        """Clean up temporary profile if it exists"""
        if self._temp_dir and self._temp_dir.exists():
            try:
                shutil.rmtree(self._temp_dir)
                self._temp_dir = None
                if self._current_profile and self._current_profile.is_temporary:
                    self._current_profile = None
            except Exception:
                pass  # Best effort cleanup
    
    @property
    def current_profile(self) -> Optional[ChromeProfile]:
        """Get the currently active profile"""
        return self._current_profile
    
    def _save_metadata(self, profile: ChromeProfile) -> None:
        """Save profile metadata"""
        metadata = {
            'name': profile.name,
            'created_at': profile.created_at.isoformat(),
            'last_used': profile.last_used.isoformat(),
            'is_temporary': profile.is_temporary
        }
        metadata_path = profile.path / '.metadata.json'
        with metadata_path.open('w') as f:
            json.dump(metadata, f)
    
    def _load_metadata(self, name: str) -> Optional[Dict]:
        """Load profile metadata"""
        metadata_path = self.get_profile_path(name) / '.metadata.json'
        if not metadata_path.exists():
            return None
            
        try:
            with metadata_path.open('r') as f:
                data = json.load(f)
                return {
                    'name': data['name'],
                    'created_at': datetime.fromisoformat(data['created_at']),
                    'last_used': datetime.fromisoformat(data['last_used']),
                    'is_temporary': data.get('is_temporary', False)
                }
        except (json.JSONDecodeError, KeyError, ValueError):
            return None

class Launcher:
    """
    A class for launching and monitoring Chrome browser instances.
    This class provides functionality to:
    - Launch Chrome with custom arguments
    - Get the WebSocket debugger URL
    - Monitor Chrome process
    - Gracefully terminate Chrome
    """

    def __init__(
        self,
        chrome_path: Optional[str] = None,
        profile_dir: Optional[Union[str, Path]] = None,
        debug_port: int = 9222,
        headless: bool = False,
        log_level: int = logging.INFO
    ):
        """
        Initialize the ChromeLauncher.

        Args:
            chrome_path: Path to Chrome executable. If None, will attempt to find Chrome automatically.
            profile_dir: Base directory for Chrome profiles. If None, uses ~/.chrome_profiles
            debug_port: Port for Chrome's remote debugging protocol.
            headless: Whether to run Chrome in headless mode.
            log_level: Logging level.
        """
        self.logger = logging.getLogger("ChromeLauncher")
        self.chrome_path = chrome_path or self._find_chrome()
        self.debug_port = debug_port
        self.headless = headless
        
        self.profile_manager = ProfileManager(profile_dir)
        self.process = None
        self.websocket_url = None
        self.startup_args = []


    def _find_chrome(self) -> str:
        """
        Find the Chrome executable on the current system.
        
        Returns:
            str: Path to Chrome executable.
            
        Raises:
            FileNotFoundError: If Chrome executable cannot be found.
        """
        system = platform.system()
        possible_paths = []
        
        if system == "Windows":
            possible_paths = [
                os.path.expandvars(r"%ProgramFiles%\Google\Chrome\Application\chrome.exe"),
                os.path.expandvars(r"%ProgramFiles(x86)%\Google\Chrome\Application\chrome.exe"),
                os.path.expandvars(r"%LocalAppData%\Google\Chrome\Application\chrome.exe"),
            ]
        elif system == "Darwin":  # macOS
            possible_paths = [
                "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
                "~/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
            ]
        else:  # Linux and others
            possible_paths = [
                "/usr/bin/google-chrome",
                "/usr/bin/google-chrome-stable",
                "/usr/bin/chromium",
                "/usr/bin/chromium-browser",
            ]
        
        for path in possible_paths:
            expanded_path = os.path.expanduser(path)
            if os.path.isfile(expanded_path) and os.access(expanded_path, os.X_OK):
                self.logger.info(f"Found Chrome at: {expanded_path}")
                return expanded_path
        
        raise FileNotFoundError("Could not find Chrome executable. Please specify chrome_path manually.")

    def _build_args(self, extra_args: Optional[List[str]] = None) -> List[str]:
        """
        Build the arguments list for launching Chrome.
        
        Args:
            extra_args: Additional Chrome arguments.
            
        Returns:
            List[str]: Complete list of arguments for Chrome.
        """
        args = [self.chrome_path]
        
        # Base arguments
        args.extend([
            f"--remote-debugging-port={self.debug_port}",  # Enable remote debugging
            "--no-startup-window",  # Do not open a default browser window on startup
            "--no-first-run",  # Skip the first-run experience
            "--no-default-browser-check",  # Skip default browser check
            "--remote-allow-origins=*",  # Allow remote debugging from any origin
            "--disable-infobars",  # Disable notification bars (e.g., "Chrome is being controlled by automated test software")
            "--disable-notifications",  # Disable web notifications
            "--disable-popup-blocking",  # Disable pop-up blocking (useful for automation)
            "--disable-background-networking",  # Reduce background network requests
            "--disable-sync",  # Disable Chrome sync (accounts, settings, etc.)
            "--disable-translate",  # Disable automatic translation popups
            "--disable-logging",  # Disable logging to prevent extra console logs
            "--disable-gpu",  # Disable GPU hardware acceleration (useful for headless mode)
            "--disable-software-rasterizer",  # Disable software rendering fallback
            "--disable-hang-monitor",  # Prevent "App is not responding" popups
            "--disable-telemetry",  # Disable telemetry data collection
            "--disable-crash-reporter",  # Prevent crash reports from being sent
            "--disable-save-password-bubble",  # Disable "Save password?" prompts
            "--password-store=basic",  # Use basic password storage (avoid OS-level password managers)
            "--disable-prompt-on-repost",  # Skip confirmation dialogs for form resubmissions
            "--start-maximized",  # Start browser in maximized mode
            "--disable-backgrounding-occluded-windows",  # Prevent Chrome from deprioritizing hidden tabs
            "--metrics-recording-only",  # Disable sending usage metrics while still recording them
            "--disable-background-timer-throttling",  # Disable throttling of background JavaScript timers
            "--homepage=about:blank",  # Set the homepage to a blank page
            "--no-service-autorun",  # Prevent Chrome services from starting automatically
            "--disable-ipc-flooding-protection",  # Disable protection against excessive inter-process communication
            "--disable-session-crashed-bubble",  # Disable the "Chrome didn't shut down correctly" message
            "--force-fieldtrials=*BackgroundTracing/default/",  # Force field trials for debugging
            "--disable-breakpad",  # Disable Chrome's crash handling system
            "--disable-features=IsolateOrigins,site-per-process",  # Disable strict site isolation (can improve performance)
            "--disable-client-side-phishing-detection",  # Disable phishing detection mechanisms
            "--use-mock-keychain",  # Use a mock keychain instead of the system keychain
            "--no-pings",  # Disable sending pings when clicking links
            "--disable-renderer-backgrounding",  # Keep background tabs fully active
            "--disable-component-update",  # Disable Chrome's component update mechanism
            "--disable-dev-shm-usage",  # Use /tmp instead of /dev/shm (useful for Docker environments)
            "--disable-default-apps",  # Do not install default Chrome apps
            "--disable-domain-reliability",  # Disable collection of domain reliability data
        ])


        
        if self.headless:
            args.extend([
                "--headless=new",  # Use new headless mode if available
                "--disable-gpu",   # Recommended for headless mode
                #"--proxy-server='direct://'",
                #"--proxy-bypass-list=*",
                #"--ignore-certificate-errors"
            ])
        
        if self.profile_manager.current_profile:
            args.append(f"--user-data-dir={self.profile_manager.current_profile.path}")
        
        # Add any extra arguments
        if extra_args:
            args.extend(extra_args)
        
        self.startup_args = args
        return args

    def launch(self, profile_name: Optional[str] = None, extra_args: Optional[List[str]] = None, timeout: int = 30) -> bool:
        """
        Launch a Chrome browser instance.
        
        Args:
            profile_name: Name of profile to use. If None, creates a temporary profile.
            extra_args: Additional Chrome arguments.
            timeout: Maximum time in seconds to wait for Chrome to start.
            
        Returns:
            bool: True if Chrome launched successfully, False otherwise.
        """
        if self.process and self.process.poll() is None:
            self.logger.warning("Chrome is already running. Use terminate() first.")
            return False
            
        try:
            # Set up profile
            if profile_name:
                try:
                    self.profile_manager.load(profile_name)
                except ValueError:
                    self.profile_manager.create(profile_name)
            else:
                self.profile_manager.create_temporary()
            
            # Launch Chrome
            args = self._build_args(extra_args)
            
            self.logger.info(f"Launching Chrome with arguments: {' '.join(args)}")
            
            # Use DETACHED_PROCESS flag on Windows to avoid cmd window
            if platform.system() == "Windows":
                self.process = subprocess.Popen(
                    args,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    creationflags=subprocess.DETACHED_PROCESS
                )
            else:
                self.process = subprocess.Popen(
                    args,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE
                )
            
            # Wait for Chrome to start and get websocket URL
            start_time = time.time()
            while time.time() - start_time < timeout:
                try:
                    self.websocket_url = self.get_websocket_url()
                    if self.websocket_url:
                        self.logger.info(f"Chrome started successfully with PID: {self.process.pid}")
                        self.logger.info(f"WebSocket URL: {self.websocket_url}")
                        return True
                except requests.exceptions.ConnectionError:
                    # Chrome is not yet ready, wait a bit
                    time.sleep(0.5)
            
            # If we get here, we timed out waiting for Chrome to start
            self.logger.error(f"Timed out waiting for Chrome to start after {timeout} seconds")
            self.terminate()
            return False
            
        except Exception as e:
            self.logger.error(f"Failed to launch Chrome: {str(e)}")
            if self.process:
                self.terminate()
            return False

    def get_websocket_url(self) -> Optional[str]:
        """
        Get the WebSocket URL from Chrome's debugging interface.
        
        Returns:
            Optional[str]: WebSocket URL if successful, None otherwise.
        """
        try:
            response = requests.get(f"http://localhost:{self.debug_port}/json/version")
            data = response.json()
            websocket_url = data.get("webSocketDebuggerUrl")

            return websocket_url
        except (requests.exceptions.RequestException, json.JSONDecodeError) as e:
            self.logger.debug(f"Failed to get WebSocket URL: {str(e)}")
            return None
    
    def get_devtools_url(self) -> Optional[str]:
        """
        Get the WebSocket URL from Chrome's debugging interface.
        
        Returns:
            Optional[str]: WebSocket URL if successful, None otherwise.
        """
        try:
            response = requests.get(f"http://localhost:{self.debug_port}/json/list")
            data = response.json()
            print(data)
            devtools_page = data[0].get("devtoolsFrontendUrl")        
            return devtools_page
    
        except (requests.exceptions.RequestException, json.JSONDecodeError) as e:
            self.logger.debug(f"Failed to get WebSocket URL: {str(e)}")
            return None

    def is_running(self) -> bool:
        """
        Check if Chrome process is still running.
        
        Returns:
            bool: True if Chrome is running, False otherwise.
        """
        if self.process is None:
            return False
        return self.process.poll() is None

    def terminate(self, timeout: int = 5) -> bool:
        """
        Terminate the Chrome process gracefully.
        
        Args:
            timeout: Time to wait for Chrome to terminate gracefully before force killing.
            
        Returns:
            bool: True if termination was successful, False otherwise.
        """
        if not self.process:
            return True
        
        try:
            # Try graceful shutdown first
            if platform.system() == "Windows":
                self.process.terminate()
            else:
                self.process.send_signal(signal.SIGTERM)
            
            # Wait for the process to terminate
            for _ in range(timeout * 2):
                if not self.is_running():
                    break
                time.sleep(0.5)
            
            # If still running, force kill
            if self.is_running():
                self.logger.warning("Chrome did not terminate gracefully, force killing...")
                self.process.kill()
            
            # Cleanup return code
            self.process.wait()
            
            self.profile_manager.cleanup()
            
            self.process = None
            self.websocket_url = None
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error terminating Chrome: {str(e)}")
            return False
    
    def stop(self):
        """Context manager exit."""
        self.terminate()

    def restart(self, profile_name: Optional[str] = None, extra_args: Optional[List[str]] = None, timeout: int = 30) -> bool:
        """
        Restart Chrome with the same or new arguments.

        Args:
            profile_name: Name of the profile to use for the restart.
            extra_args: Additional Chrome arguments for the restart.
            timeout: Maximum time to wait for Chrome to start.

        Returns:
            bool: True if restart was successful, False otherwise.
        """
        if not self.terminate():
            self.logger.error("Failed to terminate Chrome before restart")
            return False

        return self.launch(profile_name, extra_args, timeout)

    def get_process_info(self) -> Dict:
        """
        Get information about the Chrome process.
        
        Returns:
            Dict: Dictionary containing process information.
        """
        if not self.is_running():
            return {"status": "not_running"}
        
        info = {
            "status": "running",
            "pid": self.process.pid,
            "websocket_url": self.websocket_url,
            "debug_port": self.debug_port,
            "user_data_dir": self.profile_manager.current_profile.path if self.profile_manager.current_profile else None,
            "chrome_path": self.chrome_path,
            "headless": self.headless,
            "startup_args": self.startup_args
        }
        
        return info

    def __enter__(self):
        """Context manager entry."""
        self.launch()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.terminate()

    def __del__(self):
        """Ensure Chrome is terminated when the object is garbage collected."""
        self.terminate()

    # Profile management convenience methods
    def create_profile(self, name: str) -> ChromeProfile:
        """Create a new profile"""
        return self.profile_manager.create(name)

    def list_profiles(self) -> List[ChromeProfile]:
        """List all available profiles"""
        return self.profile_manager.list_profiles()

    def delete_profile(self, name: str) -> None:
        """Delete a profile"""
        return self.profile_manager.delete(name)