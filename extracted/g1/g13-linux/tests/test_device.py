"""Tests for g13_linux.device module."""

from unittest.mock import MagicMock, patch

import pytest

from g13_linux.device import (
    G13_PRODUCT_ID,
    G13_VENDOR_ID,
    HidrawDevice,
    LibUSBDevice,
    _hidiocgfeature,
    _hidiocsfeature,
    find_g13_hidraw,
    open_g13,
    open_g13_libusb,
    read_event,
)


class TestIoctlHelpers:
    """Tests for ioctl helper functions."""

    def test_hidiocsfeature(self):
        result = _hidiocsfeature(5)
        assert result == 0xC0004806 | (5 << 16)

    def test_hidiocgfeature(self):
        result = _hidiocgfeature(8)
        assert result == 0xC0004807 | (8 << 16)


class TestHidrawDevice:
    """Tests for HidrawDevice class."""

    def test_init(self):
        device = HidrawDevice("/dev/hidraw0")
        assert device.path == "/dev/hidraw0"
        assert device._fd is None

    def test_open(self):
        mock_file = MagicMock()
        mock_file.fileno.return_value = 42

        with patch("builtins.open", return_value=mock_file):
            with patch("os.set_blocking") as mock_blocking:
                device = HidrawDevice("/dev/hidraw0")
                device.open()
                assert device._fd == 42
                mock_blocking.assert_called_once_with(42, False)

    def test_read_success(self):
        mock_file = MagicMock()
        mock_file.read.return_value = b""
        device = HidrawDevice("/dev/hidraw0")
        device._file = mock_file
        result = device.read(64)
        assert result == [1, 2, 3]

    def test_read_empty(self):
        mock_file = MagicMock()
        mock_file.read.return_value = b""
        device = HidrawDevice("/dev/hidraw0")
        device._file = mock_file
        result = device.read(64)
        assert result is None

    def test_read_blocking_error(self):
        mock_file = MagicMock()
        mock_file.read.side_effect = BlockingIOError()
        device = HidrawDevice("/dev/hidraw0")
        device._file = mock_file
        result = device.read(64)
        assert result is None

    def test_write(self):
        mock_file = MagicMock()
        mock_file.write.return_value = 5
        device = HidrawDevice("/dev/hidraw0")
        device._file = mock_file
        result = device.write([1, 2, 3, 4, 5])
        assert result == 5

    def test_send_feature_report_not_open(self):
        device = HidrawDevice("/dev/hidraw0")
        with pytest.raises(RuntimeError, match="Device not open"):
            device.send_feature_report([0x00, 0x01])

    def test_send_feature_report(self):
        device = HidrawDevice("/dev/hidraw0")
        device._fd = 42
        with patch("fcntl.ioctl", return_value=3):
            result = device.send_feature_report([0x00, 0x01])
            assert result == 3

    def test_get_feature_report_not_open(self):
        device = HidrawDevice("/dev/hidraw0")
        with pytest.raises(RuntimeError, match="Device not open"):
            device.get_feature_report(0x01, 8)

    def test_get_feature_report(self):
        device = HidrawDevice("/dev/hidraw0")
        device._fd = 42
        with patch("fcntl.ioctl"):
            result = device.get_feature_report(0x01, 8)
            assert len(result) == 8

    def test_close(self):
        mock_file = MagicMock()
        device = HidrawDevice("/dev/hidraw0")
        device._file = mock_file
        device._fd = 42
        device.close()
        mock_file.close.assert_called_once()
        assert device._file is None

    def test_close_when_not_open(self):
        device = HidrawDevice("/dev/hidraw0")
        device.close()


class TestFindG13Hidraw:
    """Tests for find_g13_hidraw function."""

    def test_find_g13_success(self, tmp_path):
        hidraw0 = tmp_path / "hidraw0" / "device"
        hidraw0.mkdir(parents=True)
        (hidraw0 / "uevent").write_text("HID_ID=0003:0000046D:0000C21C\n")
        with patch("glob.glob", return_value=[str(tmp_path / "hidraw0")]):
            result = find_g13_hidraw()
            assert result == "/dev/hidraw0"

    def test_find_g13_not_found(self):
        with patch("glob.glob", return_value=[]):
            result = find_g13_hidraw()
            assert result is None

    def test_find_g13_wrong_device(self, tmp_path):
        hidraw0 = tmp_path / "hidraw0" / "device"
        hidraw0.mkdir(parents=True)
        (hidraw0 / "uevent").write_text("HID_ID=0003:00001234:00005678\n")
        with patch("glob.glob", return_value=[str(tmp_path / "hidraw0")]):
            result = find_g13_hidraw()
            assert result is None

    def test_find_g13_io_error(self, tmp_path):
        hidraw0 = tmp_path / "hidraw0" / "device"
        hidraw0.mkdir(parents=True)
        with patch("glob.glob", return_value=[str(tmp_path / "hidraw0")]):
            result = find_g13_hidraw()
            assert result is None


class TestOpenG13:
    """Tests for open_g13 function."""

    def test_open_g13_success(self):
        with patch("g13_linux.device.find_g13_hidraw", return_value="/dev/hidraw0"):
            with patch.object(HidrawDevice, "open"):
                device = open_g13()
                assert isinstance(device, HidrawDevice)

    def test_open_g13_not_found(self):
        with patch("g13_linux.device.find_g13_hidraw", return_value=None):
            with pytest.raises(RuntimeError, match="G13 not found"):
                open_g13()


class TestReadEvent:
    """Tests for read_event function."""

    def test_read_event_success(self):
        mock_handle = MagicMock()
        mock_handle.read.return_value = [1, 2, 3, 4]
        result = read_event(mock_handle)
        assert result == [1, 2, 3, 4]

    def test_read_event_no_data(self):
        mock_handle = MagicMock()
        mock_handle.read.return_value = None
        result = read_event(mock_handle)
        assert result is None


class TestLibUSBDevice:
    """Tests for LibUSBDevice class."""

    def test_init(self):
        device = LibUSBDevice()
        assert device._dev is None
        assert device._reattach is False

    def test_open_no_pyusb(self):
        device = LibUSBDevice()
        with patch.dict("sys.modules", {"usb.core": None, "usb.util": None}):
            with patch("builtins.__import__", side_effect=ImportError("No module")):
                with pytest.raises(RuntimeError, match="pyusb not installed"):
                    device.open()

    def test_open_device_not_found(self):
        """Test open raises when G13 not found via libusb."""
        mock_core = MagicMock()
        mock_util = MagicMock()
        mock_core.find.return_value = None  # Device not found

        device = LibUSBDevice()
        with patch.dict("sys.modules", {"usb.core": mock_core, "usb.util": mock_util}):
            with pytest.raises(RuntimeError, match="G13 not found"):
                device.open()

    def test_open_success(self):
        """Test successful device open with kernel driver."""
        mock_core = MagicMock()
        mock_util = MagicMock()
        mock_dev = MagicMock()
        mock_core.find.return_value = mock_dev
        mock_dev.is_kernel_driver_active.return_value = True
        mock_intf = MagicMock()
        mock_cfg = MagicMock()
        mock_cfg.__getitem__ = MagicMock(return_value=mock_intf)
        mock_dev.get_active_configuration.return_value = mock_cfg
        mock_ep_in = MagicMock()
        mock_ep_out = MagicMock()
        mock_util.find_descriptor.side_effect = [mock_ep_in, mock_ep_out]
        mock_util.ENDPOINT_IN = 0x80
        mock_util.endpoint_direction.return_value = 0x80

        device = LibUSBDevice()
        with patch.dict("sys.modules", {"usb.core": mock_core, "usb.util": mock_util}):
            device.open()
            assert device._dev is mock_dev
            assert device._reattach is True
            assert device._ep_in is mock_ep_in

    def test_open_no_kernel_driver(self):
        """Test handling when no kernel driver is attached."""
        mock_core = MagicMock()
        mock_util = MagicMock()
        mock_dev = MagicMock()
        mock_core.find.return_value = mock_dev
        mock_dev.is_kernel_driver_active.return_value = False  # No kernel driver
        mock_intf = MagicMock()
        mock_cfg = MagicMock()
        mock_cfg.__getitem__ = MagicMock(return_value=mock_intf)
        mock_dev.get_active_configuration.return_value = mock_cfg
        mock_ep_in = MagicMock()
        mock_ep_out = MagicMock()
        mock_util.find_descriptor.side_effect = [mock_ep_in, mock_ep_out]
        mock_util.ENDPOINT_IN = 0x80
        mock_util.endpoint_direction.return_value = 0x80

        device = LibUSBDevice()
        with patch.dict("sys.modules", {"usb.core": mock_core, "usb.util": mock_util}):
            device.open()
            assert device._reattach is False

    def test_open_detach_exception(self):
        """Test open handles detach exception gracefully."""
        mock_core = MagicMock()
        mock_util = MagicMock()
        mock_dev = MagicMock()
        mock_core.find.return_value = mock_dev
        mock_dev.is_kernel_driver_active.return_value = True
        mock_dev.detach_kernel_driver.side_effect = OSError("Detach failed")
        mock_intf = MagicMock()
        mock_cfg = MagicMock()
        mock_cfg.__getitem__ = MagicMock(return_value=mock_intf)
        mock_dev.get_active_configuration.return_value = mock_cfg
        mock_ep_in = MagicMock()
        mock_ep_out = MagicMock()
        mock_util.find_descriptor.side_effect = [mock_ep_in, mock_ep_out]
        mock_util.ENDPOINT_IN = 0x80
        mock_util.endpoint_direction.return_value = 0x80

        device = LibUSBDevice()
        with patch.dict("sys.modules", {"usb.core": mock_core, "usb.util": mock_util}):
            # Should not raise - exception is caught
            device.open()
            assert device._dev is mock_dev

    def test_open_set_configuration_exception(self):
        """Test open handles set_configuration exception."""
        mock_core = MagicMock()
        mock_util = MagicMock()
        mock_dev = MagicMock()
        mock_core.find.return_value = mock_dev
        mock_dev.is_kernel_driver_active.return_value = False
        mock_dev.set_configuration.side_effect = OSError("Config failed")
        mock_intf = MagicMock()
        mock_cfg = MagicMock()
        mock_cfg.__getitem__ = MagicMock(return_value=mock_intf)
        mock_dev.get_active_configuration.return_value = mock_cfg
        mock_ep_in = MagicMock()
        mock_ep_out = MagicMock()
        mock_util.find_descriptor.side_effect = [mock_ep_in, mock_ep_out]
        mock_util.ENDPOINT_IN = 0x80
        mock_util.endpoint_direction.return_value = 0x80

        device = LibUSBDevice()
        with patch.dict("sys.modules", {"usb.core": mock_core, "usb.util": mock_util}):
            # Should not raise - exception is caught
            device.open()
            assert device._dev is mock_dev

    def test_open_claim_interface_exception(self):
        """Test open handles claim_interface exception."""
        mock_core = MagicMock()
        mock_util = MagicMock()
        mock_dev = MagicMock()
        mock_core.find.return_value = mock_dev
        mock_dev.is_kernel_driver_active.return_value = False
        mock_intf = MagicMock()
        mock_cfg = MagicMock()
        mock_cfg.__getitem__ = MagicMock(return_value=mock_intf)
        mock_dev.get_active_configuration.return_value = mock_cfg
        mock_util.claim_interface.side_effect = OSError("Claim failed")
        mock_ep_in = MagicMock()
        mock_ep_out = MagicMock()
        mock_util.find_descriptor.side_effect = [mock_ep_in, mock_ep_out]
        mock_util.ENDPOINT_IN = 0x80
        mock_util.endpoint_direction.return_value = 0x80

        device = LibUSBDevice()
        with patch.dict("sys.modules", {"usb.core": mock_core, "usb.util": mock_util}):
            # Should not raise - exception is caught
            device.open()
            assert device._dev is mock_dev

    def test_read_success(self):
        device = LibUSBDevice()
        device._ep_in = MagicMock()
        device._ep_in.read.return_value = [1, 2, 3, 4]
        result = device.read(100)
        assert result == [1, 2, 3, 4]

    def test_read_timeout(self):
        device = LibUSBDevice()
        device._ep_in = MagicMock()
        device._ep_in.read.side_effect = OSError("Timeout")
        result = device.read(100)
        assert result is None

    def test_read_empty(self):
        device = LibUSBDevice()
        device._ep_in = MagicMock()
        device._ep_in.read.return_value = []
        result = device.read(100)
        assert result is None

    def test_write(self):
        device = LibUSBDevice()
        device._dev = MagicMock()
        device._dev.write.return_value = 5
        result = device.write([1, 2, 3, 4, 5])
        assert result == 5

    def test_send_feature_report(self):
        device = LibUSBDevice()
        device._dev = MagicMock()
        device._dev.ctrl_transfer.return_value = 3
        result = device.send_feature_report([0x01, 0x02, 0x03])
        assert result == 3

    def test_close(self):
        mock_util = MagicMock()
        device = LibUSBDevice()
        device._dev = MagicMock()
        device._reattach = True
        with patch.dict("sys.modules", {"usb.util": mock_util}):
            device.close()
            assert device._dev is None

    def test_close_no_reattach(self):
        mock_util = MagicMock()
        device = LibUSBDevice()
        device._dev = MagicMock()
        device._reattach = False
        with patch.dict("sys.modules", {"usb.util": mock_util}):
            device.close()

    def test_close_release_exception(self):
        mock_util = MagicMock()
        mock_util.release_interface.side_effect = OSError("Error")
        device = LibUSBDevice()
        device._dev = MagicMock()
        device._reattach = False
        with patch.dict("sys.modules", {"usb.util": mock_util}):
            device.close()

    def test_close_attach_exception(self):
        mock_util = MagicMock()
        device = LibUSBDevice()
        device._dev = MagicMock()
        device._dev.attach_kernel_driver.side_effect = OSError("Error")
        device._reattach = True
        with patch.dict("sys.modules", {"usb.util": mock_util}):
            device.close()

    def test_close_when_not_open(self):
        device = LibUSBDevice()
        device.close()


class TestOpenG13Libusb:
    """Tests for open_g13_libusb function."""

    def test_open_g13_libusb(self):
        with patch.object(LibUSBDevice, "open"):
            device = open_g13_libusb()
            assert isinstance(device, LibUSBDevice)


class TestConstants:
    """Test module constants."""

    def test_vendor_id(self):
        assert G13_VENDOR_ID == 0x046D

    def test_product_id(self):
        assert G13_PRODUCT_ID == 0xC21C
