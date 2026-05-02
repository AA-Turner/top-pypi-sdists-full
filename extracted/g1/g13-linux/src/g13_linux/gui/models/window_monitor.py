"""Window monitor for per-application profile switching.

Monitors active window changes using xdotool and emits signals
when the focused application changes.
"""

import shutil
import subprocess
from dataclasses import dataclass

from PyQt6.QtCore import QThread, pyqtSignal


@dataclass
class WindowInfo:
    """Information about an X11 window."""

    window_id: str
    name: str
    wm_class: str

    def __eq__(self, other):
        if not isinstance(other, WindowInfo):
            return False
        # Compare by window_id only - name can change (e.g., browser tabs)
        return self.window_id == other.window_id


def is_xdotool_available() -> bool:
    """Check if xdotool is installed."""
    return shutil.which("xdotool") is not None


def is_wayland() -> bool:
    """Check if running under Wayland (xdotool won't work)."""
    import os

    return os.environ.get("XDG_SESSION_TYPE") == "wayland"


def get_active_window_info() -> WindowInfo | None:
    """Get information about the currently focused window.

    Returns None if no window is focused or on error.
    """
    try:
        # Get focused window ID
        result = subprocess.run(
            ["xdotool", "getwindowfocus"],
            capture_output=True,
            text=True,
            timeout=1,
        )
        if result.returncode != 0:
            return None

        window_id = result.stdout.strip()
        if not window_id:
            return None

        # Get window name
        result = subprocess.run(
            ["xdotool", "getwindowname", window_id],
            capture_output=True,
            text=True,
            timeout=1,
        )
        window_name = result.stdout.strip() if result.returncode == 0 else ""

        # Get WM_CLASS
        result = subprocess.run(
            ["xdotool", "getwindowclassname", window_id],
            capture_output=True,
            text=True,
            timeout=1,
        )
        wm_class = result.stdout.strip() if result.returncode == 0 else ""

        return WindowInfo(window_id=window_id, name=window_name, wm_class=wm_class)

    except subprocess.TimeoutExpired:
        return None
    except FileNotFoundError:
        # xdotool not installed
        return None
    except Exception:
        return None


class WindowMonitorThread(QThread):
    """Background thread that monitors active window changes.

    Emits window_changed signal when the focused window changes.
    Uses xdotool for X11 window detection.

    Signals:
        window_changed(window_id, name, wm_class): Emitted when focus changes
        monitor_error(message): Emitted on error (e.g., xdotool not available)
    """

    window_changed = pyqtSignal(str, str, str)  # window_id, name, wm_class
    monitor_error = pyqtSignal(str)

    def __init__(self, poll_interval_ms: int = 500, parent=None):
        """Initialize the window monitor.

        Args:
            poll_interval_ms: How often to check for window changes (default 500ms)
            parent: Parent QObject
        """
        super().__init__(parent)
        self.poll_interval_ms = poll_interval_ms
        self._running = False
        self._last_window: WindowInfo | None = None
        self._available = True

    @property
    def is_available(self) -> bool:
        """Check if window monitoring is available."""
        return self._available and is_xdotool_available() and not is_wayland()

    def run(self):
        """Main thread loop - polls for window changes."""
        # Check availability before starting
        if is_wayland():
            self.monitor_error.emit(
                "Window monitoring not available under Wayland. Per-application profiles disabled."
            )
            self._available = False
            return

        if not is_xdotool_available():
            self.monitor_error.emit("xdotool not installed. Install with: sudo apt install xdotool")
            self._available = False
            return

        self._running = True
        self._available = True

        while self._running:
            window_info = get_active_window_info()

            if window_info and window_info != self._last_window:
                self._last_window = window_info
                self.window_changed.emit(
                    window_info.window_id,
                    window_info.name,
                    window_info.wm_class,
                )

            # Sleep for poll interval
            self.msleep(self.poll_interval_ms)

    def stop(self):
        """Stop the monitor thread."""
        self._running = False
        self.wait(1000)  # Wait up to 1 second for thread to finish

    def get_current_window(self) -> WindowInfo | None:
        """Get the current window info (for testing/debugging)."""
        return get_active_window_info()
