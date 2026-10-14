from enum import Enum


class AnnouncementTypeEnum(str, Enum):
    INFORMATION = "information"
    WARNING = "warning"

    def __str__(self) -> str:
        return str(self.value)
