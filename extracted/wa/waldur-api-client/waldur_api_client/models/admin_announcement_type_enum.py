from enum import Enum


class AdminAnnouncementTypeEnum(str, Enum):
    DANGER = "danger"
    INFORMATION = "information"
    WARNING = "warning"

    def __str__(self) -> str:
        return str(self.value)
