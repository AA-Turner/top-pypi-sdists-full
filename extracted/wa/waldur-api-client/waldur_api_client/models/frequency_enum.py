from enum import Enum


class FrequencyEnum(str, Enum):
    BIWEEKLY = "biweekly"
    MONTHLY = "monthly"
    WEEKLY = "weekly"

    def __str__(self) -> str:
        return str(self.value)
