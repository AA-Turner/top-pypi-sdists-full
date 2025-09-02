"""Parser for Medcom BLE devices."""
from __future__ import annotations

import asyncio
import binascii

from collections import namedtuple
from collections.abc import Callable
import dataclasses
from logging import Logger
import re
from typing import Any, Optional

from bleak import BleakClient, BleakError
from bleak.backends.device import BLEDevice
from bleak_retry_connector import establish_connection

from .const import (
    CHAR_UUID_FIRMWARE_REV,
    CHAR_UUID_HARDWARE_REV,
    CHAR_UUID_MANUFACTURER_NAME,
    CHAR_UUID_MODEL_NUMBER_STRING,
    CHAR_UUID_SERIAL_NUMBER_STRING,
    DEVICE_TYPE,
    INSPECTOR_CPM_UUID,
)

Characteristic = namedtuple("Characteristic", ["uuid", "name", "format"])

inspector_gen_1_device_info_characteristics = [
    Characteristic(CHAR_UUID_MANUFACTURER_NAME, "manufacturer", "utf-8"),
    Characteristic(CHAR_UUID_SERIAL_NUMBER_STRING, "serial_nr", "utf-8"),
    Characteristic(CHAR_UUID_FIRMWARE_REV, "firmware_rev", "utf-8"),
    Characteristic(CHAR_UUID_HARDWARE_REV, "hardware_rev", "utf-8"),
]

# List of sensor characteristics that are read via a notification
notifiable_sensors_uuid = [INSPECTOR_CPM_UUID]
notifiable_sensors_uuid_str = [str(x) for x in notifiable_sensors_uuid]


def _decode_re_attr(
    name: str, format_type: str, regexp: re.Pattern
) -> Callable[[bytearray], dict[str, float | None | str]]:
    """Decode an attribute using a regex."""

    def handler(raw_data: bytearray) -> dict[str, float | None | str]:
        res: int | None = None
        str_data = raw_data.decode(format_type)
        val = regexp.findall(str_data)
        if len(val) == 1:
            res = val[0]

        data: dict[str, float | None | str] = {name: res}
        return data

    return handler


# Notifications on Medcom devices contain the entire message, we don't
# have a MTU larger than the BLE notification size.
class NotificationHandler:
    """Helper to receive notifications and decode the data."""

    def __init__(self):
        """Start the handler."""
        self._data = None
        self._event = asyncio.Event()

    def __call__(self, _: Any, data: bytearray) -> None:
        """Receive the callback when a notification arrives."""
        self._data = data
        self._event.set()

    def get_data(self) -> bytearray | None:
        """Return the notification data."""
        return self._data

    async def wait_for_message(self) -> None:
        """Wait for a notification to be received."""
        await self._event.wait()


# Generic way to map sensor characteristics to decoders.
# This is overkill for just one sensor right now, but can be used
# in the future if we add more sensor types.
sensor_decoders: dict[str, Callable[[bytearray], dict[str, float | None | str]],] = {
    str(INSPECTOR_CPM_UUID): _decode_re_attr(
        name="cpm", format_type="ascii", regexp=re.compile("[0-9]+")
    ),
}


@dataclasses.dataclass
class MedcomBleDevice:
    """Data with information about a Medcom BLE device."""

    manufacturer: str = ""
    hw_version: str = ""
    sw_version: str = ""
    model: Optional[str] = None
    model_raw: str = ""
    name: str = ""
    identifier: str = ""

    address: str = ""

    sensors: dict[str, str | float | None] = dataclasses.field(
        default_factory=lambda: {}
    )

    def friendly_name(self) -> str:
        """Generate a name for the device."""

        return f"{self.model}"


class MedcomBleDeviceData:
    """Data for Inspector BLE devices."""

    def __init__(
        self,
        logger: Logger,
        elevation: int | None = None,
        is_metric: bool = True,
    ) -> None:
        """Initialize the device metadata."""
        super().__init__()
        self.logger = logger
        self.is_metric = is_metric
        self.elevation = elevation

    async def _get_device_characteristics(
        self, client: BleakClient, device: MedcomBleDevice
    ) -> MedcomBleDevice:
        """Get the general properties of the device (not the sensor values)."""
        device.address = client.address

        # First of all, get the device model. Future devices might have
        # different behaviour, so we can detect here as well
        try:
            data = await client.read_gatt_char(CHAR_UUID_MODEL_NUMBER_STRING)
        except BleakError as err:
            self.logger.debug("Get device characteristics exception: %s", err)
            return device
        device.model_raw = data.decode("utf-8")
        device.model = DEVICE_TYPE.get(device.model_raw)

        if device.model is None:
            self.logger.debug(
                "Could not map model number to model name, most likely an unsupported device: %s",
                device.model_raw,
            )

        if device.model == "Inspector BLE":
            device_characteristics = inspector_gen_1_device_info_characteristics
        else:
            self.logger.error("Unknown Medcom device: %s", device.model_raw)

        for characteristic in device_characteristics:
            try:
                data = await client.read_gatt_char(characteristic.uuid)
            except BleakError as err:
                self.logger.debug("Get device characteristics exception: %s", err)
                continue
            if characteristic.name == "manufacturer":
                device.manufacturer = data.decode(characteristic.format)
            elif characteristic.name == "hardware_rev":
                device.hw_version = data.decode(characteristic.format)
            elif characteristic.name == "firmware_rev":
                device.sw_version = data.decode(characteristic.format)
            elif characteristic.name == "device_name":
                device.name = data.decode(characteristic.format)
            elif characteristic.name == "serial_nr":
                # The serial number is the BLE MAC address directly, not
                # as a hex string, so we need to massage it a bit.
                device.identifier = binascii.hexlify(data).decode(characteristic.format)
            else:
                self.logger.debug(
                    "Characteristic not handled: %s, %s",
                    characteristic.uuid,
                    characteristic.name,
                )

        # In some cases the device name will be empty, for example when using a Mac.
        if device.name == "":
            device.name = device.friendly_name()

        return device

    async def _get_service_characteristics(
        self, client: BleakClient, device: MedcomBleDevice
    ) -> MedcomBleDevice:
        """Read the sensor values."""
        svcs = client.services
        for service in svcs:
            for characteristic in service.characteristics:
                if characteristic.uuid in notifiable_sensors_uuid_str:
                    decoder = sensor_decoders[characteristic.uuid]
                    handler = NotificationHandler()
                    await client.start_notify(characteristic.uuid, handler)
                    # Wait for up to 4 seconds to see we get a notification.
                    # Inspector devices notify every 3 seconds, so that should
                    # be long enough
                    try:
                        await asyncio.wait_for(handler.wait_for_message(), 4)
                    except asyncio.TimeoutError:
                        self.logger.warning("Timeout getting command data.")

                    data = handler.get_data()
                    if data is not None:
                        val = decoder(data)
                        device.sensors.update(val)
                    else:
                        self.logger.warning("Did not get data for the sensor")

                    await client.stop_notify(characteristic.uuid)

        return device

    async def update_device(self, ble_device: BLEDevice) -> MedcomBleDevice:
        """Connect to the device through BLE and retrieve relevant data."""
        device = MedcomBleDevice()
        client = await establish_connection(BleakClient, ble_device, ble_device.address)
        try:
            device = await self._get_device_characteristics(client, device)
            device = await self._get_service_characteristics(client, device)
        finally:
            await client.disconnect()

        return device
