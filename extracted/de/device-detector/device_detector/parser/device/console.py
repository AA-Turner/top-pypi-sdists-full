from device_detector.enums import DeviceType

from .base import BaseDeviceParser


class Console(BaseDeviceParser):
    __slots__ = ()
    DEVICE_TYPE = DeviceType.Console

    fixture_files = ('upstream/device/consoles.yml',)


__all__ = [
    'Console',
]
