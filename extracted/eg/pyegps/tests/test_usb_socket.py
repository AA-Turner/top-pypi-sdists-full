"""Main pyEGPS tests."""
from __future__ import annotations

from array import array
import pytest
from unittest.mock import patch
import usb.core


from pyegps.usb.eg_powerstrip import PowerStripUSB
from pyegps.exceptions import MaximumConnectionTriesReached, MissingLibrary


def test_main(fakeUsbDevice):
    """Dummy Test."""
    # check that all device impl have a unique id
    ps = PowerStripUSB(fakeUsbDevice)
    assert ps.manufacturer == "AllFake"

    with pytest.raises(MaximumConnectionTriesReached):
        _ = ps.device_id

    with patch.object(
        fakeUsbDevice, "ctrl_transfer", return_value=array("B", [1, 2, 3])
    ):
        assert ps.device_id == ":".join(
            [ps.get_implementation_id()] + [format(x, "02x") for x in [1, 2, 3]]
        )


def test_main_error_check(fakeUsbDevice):
    """Dummy Test."""
    # check that all device impl have a unique id
    ps = PowerStripUSB(fakeUsbDevice)

    with patch.object(
        fakeUsbDevice,
        "ctrl_transfer",
        return_value=array("B", [1, 2, 3]),
        side_effect=usb.core.USBError("Error"),
    ):
        with pytest.raises(MaximumConnectionTriesReached):
            _ = ps.device_id

    with patch("usb.core.find", side_effect=usb.core.NoBackendError("Error")):
        with pytest.raises(MissingLibrary):
            PowerStripUSB.search_for_devices()
