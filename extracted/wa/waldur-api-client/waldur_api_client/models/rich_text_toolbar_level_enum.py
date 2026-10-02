from enum import Enum


class RichTextToolbarLevelEnum(str, Enum):
    EXTENDED = "extended"
    MINIMAL = "minimal"
    STANDARD = "standard"

    def __str__(self) -> str:
        return str(self.value)
