
# Import pyvirtualdisplay conditionally
from dataclasses import dataclass
import logging
import platform
from typing import Optional


try:
    from pyvirtualdisplay import Display
    PYVIRTUALDISPLAY_AVAILABLE = True
except ImportError:
    PYVIRTUALDISPLAY_AVAILABLE = False
    class Display:
        """Dummy Display class for when pyvirtualdisplay is not installed."""
        def __init__(self, *args, **kwargs): pass
        def start(self): pass
        def stop(self): pass
        @property
        def is_started(self): return False
        @property
        def backend(self): return "none (pyvirtualdisplay not installed)"
        

@dataclass
class DisplayConfig:
    """Configuration settings for the virtual display."""
    width: int = 1920
    height: int = 1080
    depth: int = 24
    visible: bool = False
    backend: Optional[str] = None

class DisplayManager:
    """Manages the lifecycle of a virtual display using pyvirtualdisplay."""
    def __init__(self, config: Optional[DisplayConfig] = None):
        self.config = config or DisplayConfig()
        self._display: Optional[Display] = None
        self.logger = logging.getLogger("DisplayManager")
        self._is_supported_os = platform.system() != "Windows" and PYVIRTUALDISPLAY_AVAILABLE
        if platform.system() == "Windows":
            self.logger.warning("Running on Windows. pyvirtualdisplay not supported.")
        elif not PYVIRTUALDISPLAY_AVAILABLE:
             self.logger.warning("pyvirtualdisplay not found. Install it to enable virtual display.")

    def start(self) -> bool:
        if not self._is_supported_os:
            self.logger.info("Skipping virtual display start: Unsupported environment.")
            return True
        if self._display and getattr(self._display, 'is_started', False):
             self.logger.info("Virtual display already running.")
             return True
        self.logger.info("Attempting to start virtual display...")
        try:
            self._display = Display(
                visible=self.config.visible,
                size=(self.config.width, self.config.height),
                color_depth=self.config.depth,
                backend=self.config.backend
            )
            self._display.start()
            self.logger.info(
                f"Started virtual display: {self.config.width}x{self.config.height}x{self.config.depth} "
                f"(backend: {getattr(self._display, 'backend', 'N/A')})"
            )
            return True
        except Exception as e:
            self.logger.error(f"Failed to start virtual display: {e}", exc_info=True)
            self._display = None
            return False

    def stop(self) -> None:
        if self._display:
            self.logger.info("Attempting to stop virtual display...")
            try:
                self._display.stop()
                self.logger.info("Stopped virtual display.")
            except Exception as e:
                self.logger.error(f"Error stopping virtual display: {e}", exc_info=True)
            finally:
                self._display = None

    @property
    def is_active(self) -> bool:
        return (
            self._is_supported_os and
            self._display is not None and
            getattr(self._display, 'is_started', False)
        )

    def __enter__(self) -> 'DisplayManager':
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.stop()
