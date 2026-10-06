from device_detector.enums import AppType

from . import BaseClientParser


class Messaging(BaseClientParser):
    __slots__ = ()
    APP_TYPE = AppType.Messaging


__all__ = [
    'Messaging',
]
