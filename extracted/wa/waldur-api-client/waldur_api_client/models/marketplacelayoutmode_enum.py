from enum import Enum


class MARKETPLACELAYOUTMODEEnum(str, Enum):
    CAROUSEL = "carousel"
    CLASSIC = "classic"
    SIDEBAR = "sidebar"

    def __str__(self) -> str:
        return str(self.value)
