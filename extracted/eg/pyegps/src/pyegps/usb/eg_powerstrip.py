"""Implementation of USB PowerStrips by Energenie."""
from __future__ import annotations
import logging

from array import array
import usb.core
from usb.core import Device as UsbDevice, NoBackendError
from usb.util import (
    CTRL_IN,
    CTRL_OUT,
    CTRL_TYPE_CLASS,
    CTRL_RECIPIENT_INTERFACE,
    dispose_resources,
)

from ..device import Device
from ..powerstrip import PowerStrip

from ..exceptions import (
    MissingLibrary,
    MaximumConnectionTriesReached,
    UnsupportedProducId,
)

_logger = logging.getLogger(__name__)

USB_VENDOR_ID = 0x04B4
USB_PRODUCT_IDS = [0xFD10, 0xFD11, 0xFD12, 0xFD13, 0xFD15]
PRODUCT_SOCKET_RANGES = [(0, 0), (1, 1), (1, 4), (1, 4), (1, 4)]

USB_CTRL_TRANSFER_TRIES = 5
USB_CTRL_TRANSFER_TIMEOUT = 500

USB_HID_GET_REPORT = 0x01
USB_HID_SET_REPORT = 0x09
USB_HID_REPORT_INPUT = 0x01
USB_HID_REPORT_OUTPUT = 0x02
USB_HID_REPORT_FEATURE = 0x03


class PowerStripUSB(PowerStrip):
    """Represents an Energenie Power-Strip."""

    opened_devices: dict[str, Device] = {}
    port_dev_mapping: dict[str, str] = {}

    def __init__(self, dev: UsbDevice) -> None:
        """Initiate PowerStripUSB device.

        :param dev: usb device instance
        :type dev: usb.core.Device
        :raises UNSUPPORTED_PRODUCT_ID: Given usb device has unsupported product id.
        """
        self.productId: int = dev.idProduct

        if self.productId not in USB_PRODUCT_IDS:
            raise UnsupportedProducId

        self._dev: UsbDevice = dev
        self._uid: str | None = None

        _logger.debug(f"active kernel driver: {str(dev.is_kernel_driver_active(0))}")
        _logger.debug(f"address: {dev.address} bus: {dev.bus} ")

        minAddr, maxAddr = PRODUCT_SOCKET_RANGES[USB_PRODUCT_IDS.index(self.productId)]
        self._addrMapping: range = range(minAddr, maxAddr + 1)

    def release(self) -> None:
        """Release the usb device."""
        PowerStripUSB.opened_devices.pop(self.device_id, None)
        PowerStripUSB.port_dev_mapping.pop(f"{self._dev.bus}_{self._dev.address}", None)
        try:
            dispose_resources(self._dev)
        except Exception:
            pass

    @classmethod
    def get_implementation_id(cls) -> str:
        """Return an identifier for this implementation."""
        return "EGPS-USB"

    @property
    def uid(self) -> str:
        """Return an identifier for PowerStripUSB devices, read from firmware."""
        if self._uid is None:
            self._uid = self._read_device_id()
        return self._uid

    @property
    def manufacturer(self) -> str:
        """Return the manufacturer as read from the device."""
        return self._dev.manufacturer

    @property
    def name(self) -> str:
        """Return the product name as read from the device."""
        return self._dev.product

    @property
    def numberOfSockets(self) -> int:
        """Return number of controllable sockets."""
        return len(self._addrMapping)

    def get_status(self, socket: int) -> bool:
        """
        Get the status of the socket given by 'socket'.

        @param socket: socket number
        @return: status
        """
        super().get_status(socket)

        addr = self._addrMapping[socket]
        buf: bytes = self._get_feature_report(3 * addr)
        return (1 & buf[1]) == 1

    def switch_off(self, socket: int) -> None:
        """
        Switch the socket with the given id off.

        @param socket: socket number
        """
        super().switch_off(socket)

        addr = self._addrMapping[socket]
        buf = bytes([3 * addr, 0x00])
        self._set_feature_report(3 * addr, buf)

    def switch_on(self, socket: int) -> None:
        """
        Switch the socket with the given id on.

        @param socket: socket number
        """
        super().switch_on(socket)

        addr = self._addrMapping[socket]
        buf = bytes([3 * addr, 0x03])
        self._set_feature_report(3 * addr, buf)

    def _read_device_id(self) -> str:
        report_id: int = 0x01
        id = self._get_feature_report(report_id)
        _logger.debug(f"The device id is: {id!r}")
        return ":".join([format(x, "02x") for x in id])

    def _get_feature_report(self, report_id: int) -> bytes:
        bmRequestType: int = CTRL_IN | CTRL_TYPE_CLASS | CTRL_RECIPIENT_INTERFACE
        bRequest: int = USB_HID_GET_REPORT
        wValue: int = (USB_HID_REPORT_FEATURE << 8) | (report_id & 255)
        wIndex: int = 0
        wLength: int = 5
        ret = self._retry_ctrl_transfer(
            bmRequestType, bRequest, wValue, wIndex, wLength
        )
        assert isinstance(ret, bytes)
        return ret

    def _set_feature_report(self, report_id: int, data: bytes) -> int:
        bmRequestType: int = CTRL_OUT | CTRL_TYPE_CLASS | CTRL_RECIPIENT_INTERFACE
        bRequest: int = USB_HID_SET_REPORT
        wValue: int = (USB_HID_REPORT_FEATURE << 8) | (report_id & 255)
        wIndex: int = 0
        ret = self._retry_ctrl_transfer(bmRequestType, bRequest, wValue, wIndex, data)
        assert isinstance(ret, int)
        return ret

    def _retry_ctrl_transfer(
        self,
        bmRequestType: int,
        bRequest: int,
        wValue: int,
        wIndex: int,
        data_or_wLength: bytes | int,
    ) -> int | bytes:
        """Perform ctrl transfer and retry if not successful.

        The parameters bmRequestType, bRequest, wValue and wIndex are the same
        of the USB Standard Control Request format.

        Return the number of bytes written (for OUT transfers) or the data
        read (for IN transfers), as an array.array object.
        """
        _logger.debug(
            f"ctrl_transfer: {bmRequestType}, {bRequest}, {wValue}, {data_or_wLength!r}"
        )
        req_in: bool = (bmRequestType & CTRL_IN) == CTRL_IN
        for i in range(USB_CTRL_TRANSFER_TRIES):
            try:
                buf_or_len: bytes | int = self._dev.ctrl_transfer(
                    bmRequestType,
                    bRequest,
                    wValue,
                    wIndex,
                    data_or_wLength,
                    USB_CTRL_TRANSFER_TIMEOUT,
                )
            except usb.core.USBError as e:
                _logger.debug(f"ctrl_transfer: try number {i}, usb error: {e}")
                continue
            if req_in:
                assert isinstance(buf_or_len, array)
                if len(buf_or_len) == 0:
                    continue
                return bytes(buf_or_len)

            return int(buf_or_len)

        raise MaximumConnectionTriesReached

    @classmethod
    def search_for_devices(cls) -> list[PowerStripUSB]:
        """List the usb devices which have a known EG-PM product_id."""
        devices = []
        for prodId in USB_PRODUCT_IDS:
            try:
                devices += [
                    cls(dev)
                    for dev in usb.core.find(
                        find_all=True, idVendor=USB_VENDOR_ID, idProduct=prodId
                    )
                    if f"{dev.bus}_{dev.address}" not in cls.port_dev_mapping
                ]
            except NoBackendError:
                raise MissingLibrary
        return devices

    @classmethod
    def get_device(cls, device_id: str) -> Device | None:
        """Try to locate a specific EG-PM device.

        :param deviceId: The device specific firmware id.
        :type deviceId: str
        :return: _description_
        :rtype: PowerStripUSB | None
        """
        if device_id in cls.opened_devices:
            return cls.opened_devices[device_id]
        candidates = cls.search_for_devices()
        for dev in candidates:
            if dev.device_id == device_id:
                cls.opened_devices[device_id] = dev
                cls.port_dev_mapping[f"{dev._dev.bus}_{dev._dev.address}"] = device_id
                return dev
        return None
