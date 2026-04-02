from enum import Enum


class WidgetEnum(str, Enum):
    ATTACHED_INSTANCE = "attached_instance"
    CSV = "csv"
    FILESIZE = "filesize"

    def __str__(self) -> str:
        return str(self.value)
