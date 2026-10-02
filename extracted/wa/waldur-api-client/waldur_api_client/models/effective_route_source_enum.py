from enum import Enum


class EffectiveRouteSourceEnum(str, Enum):
    CONNECTED = "connected"
    DEFAULT = "default"
    STATIC = "static"

    def __str__(self) -> str:
        return str(self.value)
