from enum import Enum


class SIDEBARSTYLEEnum(str, Enum):
    ACCENT = "accent"
    ACCENT_LIGHT = "accent-light"
    AUTO = "auto"
    DARK = "dark"
    LIGHT = "light"
    PRIMARY = "primary"

    def __str__(self) -> str:
        return str(self.value)
