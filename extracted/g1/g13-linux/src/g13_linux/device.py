import fcntl
import glob
import os

G13_VENDOR_ID = 0x046D
G13_PRODUCT_ID = 0xC21C


def _hidiocsfeature(length):
    """HIDIOCSFEATURE ioctl for setting feature reports."""
    return 0xC0004806 | (length << 16)


def _hidiocgfeature(length):
    """HIDIOCGFEATURE ioctl for getting feature reports."""
    return 0xC0004807 | (length << 16)


class HidrawDevice:
    """Wrapper for hidraw device file to provide consistent interface."""

    def __init__(self, path):
        self.path = path
        self._fd = None
        self._file = None

    def open(self):
        self._file = open(self.path, "rb+", buffering=0)
        self._fd = self._file.fileno()
        os.set_blocking(self._fd, False)

    def read(self, size):
        try:
            data = self._file.read(size)
            return list(data) if data else None
        except BlockingIOError:
            return None

    def write(self, data):
        """Write an output report to the device."""
        return self._file.write(bytes(data))

    def send_feature_report(self, data):
        """
        Send a HID feature report to the device.

        Args:
            data: Report data (first byte should be report ID)

        Returns:
            Number of bytes written
        """
        if self._fd is None:
            raise RuntimeError("Device not open")

        buf = bytes(data)
        return fcntl.ioctl(self._fd, _hidiocsfeature(len(buf)), buf)

    def get_feature_report(self, report_id, size):
        """
        Get a HID feature report from the device.

        Args:
            report_id: Report ID to request
            size: Expected report size

        Returns:
            Report data as bytes
        """
        if self._fd is None:
            raise RuntimeError("Device not open")

        buf = bytearray(size)
        buf[0] = report_id
        fcntl.ioctl(self._fd, _hidiocgfeature(size), buf)
        return bytes(buf)

    def close(self):
        if self._file:
            self._file.close()
            self._file = None
            self._fd = None


def find_g13_hidraw():
    """Find the hidraw device path for the G13."""
    for hidraw in glob.glob("/sys/class/hidraw/hidraw*"):
        uevent_path = os.path.join(hidraw, "device", "uevent")
        try:
            with open(uevent_path) as f:
                content = f.read()
                # Check for G13 HID_ID (format: 0003:0000046D:0000C21C)
                if "0000046D" in content.upper() and "0000C21C" in content.upper():
                    device_name = os.path.basename(hidraw)
                    return f"/dev/{device_name}"
        except OSError:
            continue
    return None


def open_g13():
    """Open the G13 device and return a handle."""
    hidraw_path = find_g13_hidraw()
    if not hidraw_path:
        raise RuntimeError("Logitech G13 not found")

    device = HidrawDevice(hidraw_path)
    device.open()
    return device


def read_event(handle):
    """Read a HID report from the device."""
    data = handle.read(64)
    return data if data else None


class LibUSBDevice:
    """
    Direct libusb access for G13 input reading.

    Required because hid-generic kernel driver consumes input reports
    and doesn't pass them to hidraw. This requires root/sudo to detach
    the kernel driver.

    Note: Linux kernel 6.19+ will have proper hid-lg-g15 support for G13.
    """

    ENDPOINT_IN = 0x81  # EP 1 IN for button/joystick data
    ENDPOINT_OUT = 0x02  # EP 2 OUT for LCD data
    REPORT_SIZE = 8  # 7 bytes data + 1 byte report ID

    def __init__(self):
        self._dev = None
        self._reattach = False

    def open(self):
        """Open G13 via libusb, detaching kernel driver."""
        try:
            import usb.core
            import usb.util
        except ImportError as err:
            raise RuntimeError("pyusb not installed. Run: pip install pyusb") from err

        self._dev = usb.core.find(idVendor=G13_VENDOR_ID, idProduct=G13_PRODUCT_ID)
        if self._dev is None:
            raise RuntimeError("G13 not found")

        # Detach kernel driver from all interfaces
        for intf_num in range(2):
            try:
                if self._dev.is_kernel_driver_active(intf_num):
                    self._dev.detach_kernel_driver(intf_num)
                    self._reattach = True
            except OSError:
                pass  # Driver may not be attached

        # Set configuration
        try:
            self._dev.set_configuration()
        except OSError:
            pass  # May already be configured

        # Claim both interfaces
        import usb.util

        for intf_num in range(2):
            try:
                usb.util.claim_interface(self._dev, intf_num)
            except OSError:
                pass  # May already be claimed

        # Get endpoints from interface 0
        cfg = self._dev.get_active_configuration()
        intf = cfg[(0, 0)]

        self._ep_in = usb.util.find_descriptor(
            intf,
            custom_match=lambda e: (
                usb.util.endpoint_direction(e.bEndpointAddress) == usb.util.ENDPOINT_IN
            ),
        )
        self._ep_out = usb.util.find_descriptor(
            intf,
            custom_match=lambda e: (
                usb.util.endpoint_direction(e.bEndpointAddress) == usb.util.ENDPOINT_OUT
            ),
        )

    def read(self, timeout_ms=100):
        """
        Read button/joystick report.

        Returns:
            List of bytes or None on timeout
        """
        try:
            data = self._ep_in.read(64, timeout=timeout_ms)
            return list(data) if data else None
        except (OSError, ValueError):
            return None

    def write(self, data):
        """
        Write output data (for LCD) via interrupt transfer.

        Uses endpoint 0x02 OUT which is the LCD data endpoint.
        """
        # Use direct interrupt write to endpoint 0x02
        return self._dev.write(self.ENDPOINT_OUT, bytes(data), timeout=1000)

    def send_feature_report(self, data):
        """Send feature report via control transfer."""
        report_id = data[0]
        return self._dev.ctrl_transfer(
            0x21,  # bmRequestType: Host-to-device, Class, Interface
            0x09,  # bRequest: SET_REPORT
            0x0300 | report_id,  # wValue: Feature report + report ID
            0,  # wIndex: Interface 0
            bytes(data),
            1000,  # timeout
        )

    def close(self):
        """Close device and reattach kernel driver."""
        if self._dev:
            import usb.util

            # Release both interfaces
            for intf_num in range(2):
                try:
                    usb.util.release_interface(self._dev, intf_num)
                except OSError:
                    pass  # Best-effort cleanup

            # Reattach kernel drivers
            if self._reattach:
                for intf_num in range(2):
                    try:
                        self._dev.attach_kernel_driver(intf_num)
                    except OSError:
                        pass  # Best-effort cleanup

            self._dev = None


def open_g13_libusb():
    """
    Open G13 using libusb for input reading.

    Requires root/sudo to detach kernel driver.
    Use this when you need button/joystick input.
    """
    device = LibUSBDevice()
    device.open()
    return device
