from .display import Display

from pydantic import BaseModel
from .keyboard_info import KeyboardInformation


class DeviceHardwareInfo(BaseModel):
    """
    The Device Hardware Information object contains details and specifications of
    the physical components that make up a device. This information provides an
    overview of the hardware capabilities, configuration, and characteristics of the
    device.
    """

    # Optional:
    bios_date: str | None = None
    bios_manufacturer: str | None = None
    bios_ver: str | None = None
    chassis: str | None = None
    cpu_bits: int | None = None
    cpu_count: int | None = None
    cpu_cores: int | None = None
    cpu_speed: int | None = None
    cpu_type: str | None = None
    desktop_display: Display | None = None
    keyboard_info: KeyboardInformation | None = None
    ram_size: int | None = None
    serial_number: str | None = None # The device manufacturer serial number.
