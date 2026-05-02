"""Tests for WindowMonitorThread and window detection."""

import subprocess
from unittest.mock import MagicMock, patch


class TestWindowInfo:
    """Tests for WindowInfo dataclass."""

    def test_window_info_creation(self):
        """Test creating WindowInfo."""
        from g13_linux.gui.models.window_monitor import WindowInfo

        info = WindowInfo(window_id="12345", name="Test Window", wm_class="test-app")

        assert info.window_id == "12345"
        assert info.name == "Test Window"
        assert info.wm_class == "test-app"

    def test_window_info_equality_same_id(self):
        """Test equality by window_id."""
        from g13_linux.gui.models.window_monitor import WindowInfo

        info1 = WindowInfo(window_id="12345", name="Name 1", wm_class="class1")
        info2 = WindowInfo(window_id="12345", name="Name 2", wm_class="class2")

        assert info1 == info2  # Same ID means same window

    def test_window_info_inequality_different_id(self):
        """Test inequality with different window_id."""
        from g13_linux.gui.models.window_monitor import WindowInfo

        info1 = WindowInfo(window_id="12345", name="Name", wm_class="class")
        info2 = WindowInfo(window_id="67890", name="Name", wm_class="class")

        assert info1 != info2

    def test_window_info_inequality_non_window_info(self):
        """Test inequality with non-WindowInfo object."""
        from g13_linux.gui.models.window_monitor import WindowInfo

        info = WindowInfo(window_id="12345", name="Name", wm_class="class")

        assert info != "12345"
        assert info is not None
        assert info != {"window_id": "12345"}


class TestIsXdotoolAvailable:
    """Tests for xdotool availability check."""

    def test_xdotool_available(self):
        """Test when xdotool is installed."""
        from g13_linux.gui.models.window_monitor import is_xdotool_available

        with patch("shutil.which", return_value="/usr/bin/xdotool"):
            assert is_xdotool_available() is True

    def test_xdotool_not_available(self):
        """Test when xdotool is not installed."""
        from g13_linux.gui.models.window_monitor import is_xdotool_available

        with patch("shutil.which", return_value=None):
            assert is_xdotool_available() is False


class TestIsWayland:
    """Tests for Wayland detection."""

    def test_is_wayland_true(self):
        """Test when running under Wayland."""
        from g13_linux.gui.models.window_monitor import is_wayland

        with patch.dict("os.environ", {"XDG_SESSION_TYPE": "wayland"}):
            assert is_wayland() is True

    def test_is_wayland_false_x11(self):
        """Test when running under X11."""
        from g13_linux.gui.models.window_monitor import is_wayland

        with patch.dict("os.environ", {"XDG_SESSION_TYPE": "x11"}):
            assert is_wayland() is False

    def test_is_wayland_false_not_set(self):
        """Test when XDG_SESSION_TYPE is not set."""
        from g13_linux.gui.models.window_monitor import is_wayland

        with patch.dict("os.environ", {}, clear=True):
            assert is_wayland() is False


class TestGetActiveWindowInfo:
    """Tests for get_active_window_info function."""

    def test_get_active_window_success(self):
        """Test successful window info retrieval."""
        from g13_linux.gui.models.window_monitor import get_active_window_info

        def mock_run(args, **kwargs):
            result = MagicMock()
            result.returncode = 0
            if args[1] == "getwindowfocus":
                result.stdout = "12345678\n"
            elif args[1] == "getwindowname":
                result.stdout = "Firefox\n"
            elif args[1] == "getwindowclassname":
                result.stdout = "firefox\n"
            return result

        with patch("subprocess.run", side_effect=mock_run):
            info = get_active_window_info()

            assert info is not None
            assert info.window_id == "12345678"
            assert info.name == "Firefox"
            assert info.wm_class == "firefox"

    def test_get_active_window_no_focus(self):
        """Test when no window is focused."""
        from g13_linux.gui.models.window_monitor import get_active_window_info

        result = MagicMock()
        result.returncode = 1
        result.stdout = ""

        with patch("subprocess.run", return_value=result):
            info = get_active_window_info()
            assert info is None

    def test_get_active_window_empty_id(self):
        """Test when window ID is empty."""
        from g13_linux.gui.models.window_monitor import get_active_window_info

        result = MagicMock()
        result.returncode = 0
        result.stdout = ""

        with patch("subprocess.run", return_value=result):
            info = get_active_window_info()
            assert info is None

    def test_get_active_window_timeout(self):
        """Test timeout handling."""
        from g13_linux.gui.models.window_monitor import get_active_window_info

        with patch("subprocess.run", side_effect=subprocess.TimeoutExpired("xdotool", 1)):
            info = get_active_window_info()
            assert info is None

    def test_get_active_window_not_installed(self):
        """Test when xdotool is not installed."""
        from g13_linux.gui.models.window_monitor import get_active_window_info

        with patch("subprocess.run", side_effect=FileNotFoundError):
            info = get_active_window_info()
            assert info is None

    def test_get_active_window_generic_exception(self):
        """Test generic exception handling."""
        from g13_linux.gui.models.window_monitor import get_active_window_info

        with patch("subprocess.run", side_effect=Exception("Something went wrong")):
            info = get_active_window_info()
            assert info is None

    def test_get_active_window_partial_failure(self):
        """Test when name/class retrieval fails but ID succeeds."""
        from g13_linux.gui.models.window_monitor import get_active_window_info

        call_count = [0]

        def mock_run(args, **kwargs):
            call_count[0] += 1
            result = MagicMock()
            if call_count[0] == 1:  # getwindowfocus
                result.returncode = 0
                result.stdout = "12345\n"
            else:  # getwindowname or getwindowclassname
                result.returncode = 1
                result.stdout = ""
            return result

        with patch("subprocess.run", side_effect=mock_run):
            info = get_active_window_info()

            assert info is not None
            assert info.window_id == "12345"
            assert info.name == ""
            assert info.wm_class == ""


class TestWindowMonitorThread:
    """Tests for WindowMonitorThread."""

    def test_monitor_init(self, qapp):
        """Test monitor initialization."""
        from g13_linux.gui.models.window_monitor import WindowMonitorThread

        monitor = WindowMonitorThread(poll_interval_ms=100)

        assert monitor.poll_interval_ms == 100
        assert monitor._running is False
        assert monitor._last_window is None

    def test_monitor_is_available_xdotool_missing(self, qapp):
        """Test is_available when xdotool is missing."""
        from g13_linux.gui.models.window_monitor import WindowMonitorThread

        monitor = WindowMonitorThread()

        with patch("g13_linux.gui.models.window_monitor.is_xdotool_available", return_value=False):
            with patch("g13_linux.gui.models.window_monitor.is_wayland", return_value=False):
                assert monitor.is_available is False

    def test_monitor_is_available_wayland(self, qapp):
        """Test is_available under Wayland."""
        from g13_linux.gui.models.window_monitor import WindowMonitorThread

        monitor = WindowMonitorThread()

        with patch("g13_linux.gui.models.window_monitor.is_xdotool_available", return_value=True):
            with patch("g13_linux.gui.models.window_monitor.is_wayland", return_value=True):
                assert monitor.is_available is False

    def test_monitor_is_available_success(self, qapp):
        """Test is_available when everything works."""
        from g13_linux.gui.models.window_monitor import WindowMonitorThread

        monitor = WindowMonitorThread()

        with patch("g13_linux.gui.models.window_monitor.is_xdotool_available", return_value=True):
            with patch("g13_linux.gui.models.window_monitor.is_wayland", return_value=False):
                assert monitor.is_available is True

    def test_monitor_stop(self, qapp):
        """Test stopping the monitor."""
        from g13_linux.gui.models.window_monitor import WindowMonitorThread

        monitor = WindowMonitorThread()
        monitor._running = True

        with patch.object(monitor, "wait"):
            monitor.stop()

        assert monitor._running is False

    def test_monitor_get_current_window(self, qapp):
        """Test get_current_window method."""
        from g13_linux.gui.models.window_monitor import WindowInfo, WindowMonitorThread

        monitor = WindowMonitorThread()

        mock_info = WindowInfo("123", "Test", "test")
        with patch(
            "g13_linux.gui.models.window_monitor.get_active_window_info", return_value=mock_info
        ):
            result = monitor.get_current_window()
            assert result == mock_info

    def test_monitor_run_wayland_error(self, qapp):
        """Test run() emits error under Wayland."""
        from g13_linux.gui.models.window_monitor import WindowMonitorThread

        monitor = WindowMonitorThread()
        error_messages = []
        monitor.monitor_error.connect(lambda msg: error_messages.append(msg))

        with patch("g13_linux.gui.models.window_monitor.is_wayland", return_value=True):
            monitor.run()

        assert len(error_messages) == 1
        assert "Wayland" in error_messages[0]
        assert monitor._available is False

    def test_monitor_run_xdotool_missing_error(self, qapp):
        """Test run() emits error when xdotool missing."""
        from g13_linux.gui.models.window_monitor import WindowMonitorThread

        monitor = WindowMonitorThread()
        error_messages = []
        monitor.monitor_error.connect(lambda msg: error_messages.append(msg))

        with patch("g13_linux.gui.models.window_monitor.is_wayland", return_value=False):
            with patch(
                "g13_linux.gui.models.window_monitor.is_xdotool_available", return_value=False
            ):
                monitor.run()

        assert len(error_messages) == 1
        assert "xdotool" in error_messages[0]
        assert monitor._available is False

    def test_monitor_run_emits_window_changed(self, qapp):
        """Test run() emits window_changed signal."""
        from g13_linux.gui.models.window_monitor import WindowInfo, WindowMonitorThread

        monitor = WindowMonitorThread(poll_interval_ms=10)
        changes = []
        monitor.window_changed.connect(lambda wid, name, cls: changes.append((wid, name, cls)))

        call_count = [0]

        def mock_get_window():
            call_count[0] += 1
            if call_count[0] >= 3:
                monitor._running = False  # Stop after a few iterations
            return WindowInfo("123", "Test Window", "test-class")

        with patch("g13_linux.gui.models.window_monitor.is_wayland", return_value=False):
            with patch(
                "g13_linux.gui.models.window_monitor.is_xdotool_available", return_value=True
            ):
                with patch(
                    "g13_linux.gui.models.window_monitor.get_active_window_info",
                    side_effect=mock_get_window,
                ):
                    monitor.run()

        assert len(changes) == 1  # Should only emit once (no change after first)
        assert changes[0] == ("123", "Test Window", "test-class")

    def test_monitor_run_no_emit_same_window(self, qapp):
        """Test run() doesn't emit for same window."""
        from g13_linux.gui.models.window_monitor import WindowInfo, WindowMonitorThread

        monitor = WindowMonitorThread(poll_interval_ms=10)
        # Pre-set the last window
        monitor._last_window = WindowInfo("123", "Old Name", "old-class")

        changes = []
        monitor.window_changed.connect(lambda wid, name, cls: changes.append((wid, name, cls)))

        call_count = [0]

        def mock_get_window():
            call_count[0] += 1
            if call_count[0] >= 2:
                monitor._running = False
            return WindowInfo("123", "Test Window", "test-class")  # Same ID

        with patch("g13_linux.gui.models.window_monitor.is_wayland", return_value=False):
            with patch(
                "g13_linux.gui.models.window_monitor.is_xdotool_available", return_value=True
            ):
                with patch(
                    "g13_linux.gui.models.window_monitor.get_active_window_info",
                    side_effect=mock_get_window,
                ):
                    monitor.run()

        assert len(changes) == 0  # No change - same window ID

    def test_monitor_run_no_emit_none_window(self, qapp):
        """Test run() doesn't emit for None window."""
        from g13_linux.gui.models.window_monitor import WindowMonitorThread

        monitor = WindowMonitorThread(poll_interval_ms=10)
        changes = []
        monitor.window_changed.connect(lambda wid, name, cls: changes.append((wid, name, cls)))

        call_count = [0]

        def mock_get_window():
            call_count[0] += 1
            if call_count[0] >= 2:
                monitor._running = False
            return None

        with patch("g13_linux.gui.models.window_monitor.is_wayland", return_value=False):
            with patch(
                "g13_linux.gui.models.window_monitor.is_xdotool_available", return_value=True
            ):
                with patch(
                    "g13_linux.gui.models.window_monitor.get_active_window_info",
                    side_effect=mock_get_window,
                ):
                    monitor.run()

        assert len(changes) == 0
