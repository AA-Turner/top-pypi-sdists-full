"""Tests for DeviceEventThread controller."""

import time
from unittest.mock import MagicMock, patch


class TestDeviceEventThreadInit:
    """Tests for DeviceEventThread initialization."""

    def test_init_with_hidraw_device(self, qtbot):
        """Test init with hidraw device handle."""
        from g13_linux.gui.controllers.device_event_controller import DeviceEventThread

        mock_handle = MagicMock()

        thread = DeviceEventThread(mock_handle)

        assert thread.device_handle is mock_handle
        assert thread.running is True
        assert thread._is_libusb is False

    def test_init_with_libusb_device(self, qtbot):
        """Test init with LibUSBDevice."""
        from g13_linux.device import LibUSBDevice
        from g13_linux.gui.controllers.device_event_controller import DeviceEventThread

        mock_handle = MagicMock(spec=LibUSBDevice)

        thread = DeviceEventThread(mock_handle)

        assert thread.device_handle is mock_handle
        assert thread._is_libusb is True


class TestDeviceEventThreadRun:
    """Tests for run() method."""

    def test_run_with_libusb_device(self, qtbot):
        """Test run loop with LibUSB device."""
        from g13_linux.device import LibUSBDevice
        from g13_linux.gui.controllers.device_event_controller import DeviceEventThread

        mock_handle = MagicMock(spec=LibUSBDevice)
        # Return data once, then stop
        call_count = [0]

        def mock_read(timeout_ms=100):
            call_count[0] += 1
            if call_count[0] == 1:
                return [0x01, 0x02, 0x03]
            else:
                thread.running = False
                return None

        mock_handle.read.side_effect = mock_read

        thread = DeviceEventThread(mock_handle)

        events = []
        thread.event_received.connect(events.append)

        thread.run()

        assert len(events) == 1
        assert events[0] == bytes([0x01, 0x02, 0x03])

    def test_run_with_hidraw_device(self, qtbot):
        """Test run loop with hidraw device."""
        from g13_linux.gui.controllers.device_event_controller import DeviceEventThread

        mock_handle = MagicMock()
        call_count = [0]

        def mock_read_event(handle):
            call_count[0] += 1
            if call_count[0] == 1:
                return bytes([0xAA, 0xBB])
            else:
                thread.running = False
                return None

        thread = DeviceEventThread(mock_handle)

        events = []
        thread.event_received.connect(events.append)

        with patch(
            "g13_linux.gui.controllers.device_event_controller.read_event",
            side_effect=mock_read_event,
        ):
            thread.run()

        assert len(events) == 1
        assert events[0] == bytes([0xAA, 0xBB])

    def test_run_emits_error_on_exception(self, qtbot):
        """Test run emits error on exception."""
        from g13_linux.device import LibUSBDevice
        from g13_linux.gui.controllers.device_event_controller import DeviceEventThread

        mock_handle = MagicMock(spec=LibUSBDevice)
        mock_handle.read.side_effect = Exception("USB read failed")

        thread = DeviceEventThread(mock_handle)

        errors = []
        thread.error_occurred.connect(errors.append)

        thread.run()

        assert len(errors) == 1
        assert "USB read failed" in errors[0]
        assert thread.running is False

    def test_run_continues_on_empty_data(self, qtbot):
        """Test run loop continues when data is None/empty."""
        from g13_linux.device import LibUSBDevice
        from g13_linux.gui.controllers.device_event_controller import DeviceEventThread

        mock_handle = MagicMock(spec=LibUSBDevice)
        call_count = [0]

        def mock_read(timeout_ms=100):
            call_count[0] += 1
            if call_count[0] < 3:
                return None  # Empty read
            elif call_count[0] == 3:
                return [0xFF]  # Valid data
            else:
                thread.running = False
                return None

        mock_handle.read.side_effect = mock_read

        thread = DeviceEventThread(mock_handle)

        events = []
        thread.event_received.connect(events.append)

        thread.run()

        # Should only emit once (the valid data)
        assert len(events) == 1
        assert call_count[0] >= 3


class TestDeviceEventThreadStop:
    """Tests for stop() method."""

    def test_stop_sets_running_false(self, qtbot):
        """Test stop sets running to False."""
        from g13_linux.gui.controllers.device_event_controller import DeviceEventThread

        mock_handle = MagicMock()
        thread = DeviceEventThread(mock_handle)

        assert thread.running is True

        # Mock wait to avoid actual waiting
        with patch.object(thread, "wait"):
            thread.stop()

        assert thread.running is False

    def test_stop_waits_for_thread(self, qtbot):
        """Test stop waits for thread to finish."""
        from g13_linux.gui.controllers.device_event_controller import DeviceEventThread

        mock_handle = MagicMock()
        thread = DeviceEventThread(mock_handle)

        with patch.object(thread, "wait") as mock_wait:
            thread.stop()

            mock_wait.assert_called_once_with(1000)


class TestDeviceEventThreadSignals:
    """Tests for signal emission."""

    def test_event_received_signal_exists(self, qtbot):
        """Test event_received signal exists."""
        from g13_linux.gui.controllers.device_event_controller import DeviceEventThread

        mock_handle = MagicMock()
        thread = DeviceEventThread(mock_handle)

        assert hasattr(thread, "event_received")

    def test_error_occurred_signal_exists(self, qtbot):
        """Test error_occurred signal exists."""
        from g13_linux.gui.controllers.device_event_controller import DeviceEventThread

        mock_handle = MagicMock()
        thread = DeviceEventThread(mock_handle)

        assert hasattr(thread, "error_occurred")


class TestDeviceEventThreadIntegration:
    """Integration tests for DeviceEventThread."""

    def test_thread_stops_cleanly(self, qtbot):
        """Test thread can be started and stopped cleanly."""
        from g13_linux.device import LibUSBDevice
        from g13_linux.gui.controllers.device_event_controller import DeviceEventThread

        mock_handle = MagicMock(spec=LibUSBDevice)

        def slow_read(timeout_ms=100):
            time.sleep(0.01)
            return None

        mock_handle.read.side_effect = slow_read

        thread = DeviceEventThread(mock_handle)

        # Start in background
        thread.start()

        # Give it time to start
        time.sleep(0.05)

        # Stop it
        thread.stop()

        # Thread should have stopped
        assert thread.running is False
