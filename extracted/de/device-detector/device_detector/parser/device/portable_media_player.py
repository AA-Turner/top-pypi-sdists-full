from device_detector.enums import DeviceType

from .base import BaseDeviceParser


class PortableMediaPlayer(BaseDeviceParser):
    __slots__ = ()
    DEVICE_TYPE = DeviceType.PortableMediaPlayer

    fixture_files = ('upstream/device/portable_media_player.yml',)


__all__ = [
    'PortableMediaPlayer',
]
