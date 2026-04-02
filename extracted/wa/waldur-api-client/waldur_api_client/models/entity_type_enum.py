from enum import Enum


class EntityTypeEnum(str, Enum):
    COMPANY = "company"
    GOVERNMENT = "government"
    NONPROFIT = "nonprofit"
    OTHER = "other"
    STARTUP = "startup"

    def __str__(self) -> str:
        return str(self.value)
