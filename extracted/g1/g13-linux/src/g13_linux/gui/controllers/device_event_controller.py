"""
Device Event Thread Controller

Background thread for reading G13 USB events.
"""

from PyQt6.QtCore import QThread, pyqtSignal

from ...device import LibUSBDevice, read_event


class DeviceEventThread(QThread):
    """Background thread for reading device events"""

    event_received = pyqtSignal(bytes)
    error_occurred = pyqtSignal(str)

    def __init__(self, device_handle):
        super().__init__()
        self.device_handle = device_handle
        self.running = True
        # Check if this is a libusb device (has different read method)
        self._is_libusb = isinstance(device_handle, LibUSBDevice)

    def run(self):
        """Event loop - runs in background thread"""
        while self.running:
            try:
                if self._is_libusb:
                    # LibUSBDevice.read() returns list or None
                    data = self.device_handle.read(timeout_ms=100)
                else:
                    # HidrawDevice via read_event()
                    data = read_event(self.device_handle)

                if data:
                    self.event_received.emit(bytes(data))
            except Exception as e:
                self.error_occurred.emit(f"Event read error: {e}")
                self.running = False

    def stop(self):
        """Stop event loop"""
        self.running = False
        self.wait(1000)  # Wait up to 1 second for thread to finish
