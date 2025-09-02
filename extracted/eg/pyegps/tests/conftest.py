"""Fixtures definitions for pyEGPS tests."""
from __future__ import annotations

from array import array
from unittest.mock import MagicMock

import pytest

CTRL_IN = 1 << 7


def get_usb_mock(product_id: int) -> MagicMock:
    """Create a Mock representing a pyusb device."""
    mock = MagicMock()
    mock.idProduct = product_id
    mock.manufacturer = "AllFake"
    mock.product = "Fake-Product"

    def ctrl_transfer(
        bmRequestType,
        bRequest,
        wValue,
        wIndex,
        data_or_wLength,
        USB_CTRL_TRANSFER_TIMEOUT,
    ) -> bytes | int:
        req_in: bool = (bmRequestType & CTRL_IN) == CTRL_IN
        return array("B", []) if req_in else 0

    mock.ctrl_transfer = ctrl_transfer
    return mock


@pytest.fixture
def fakeUsbDevice() -> MagicMock:
    """Return a fake USB device with supported product_id."""
    return get_usb_mock(product_id=0xFD15)


@pytest.fixture
def fakeUnknownUsbDevice() -> MagicMock:
    """Return a fake USB device with unsupported product_id."""
    return get_usb_mock(product_id=0xFD20)
