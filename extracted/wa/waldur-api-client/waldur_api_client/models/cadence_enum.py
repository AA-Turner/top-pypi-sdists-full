from enum import Enum


class CadenceEnum(str, Enum):
    BIANNUAL = "biannual"
    CUSTOM = "custom"
    MONTHLY = "monthly"
    QUARTERLY = "quarterly"
    YEARLY = "yearly"

    def __str__(self) -> str:
        return str(self.value)
