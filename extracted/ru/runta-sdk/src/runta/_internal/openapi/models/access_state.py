from enum import Enum


class AccessState(str, Enum):
    ACTIVE = "active"
    PAST_DUE = "past_due"
    RESTRICTED = "restricted"

    def __str__(self) -> str:
        return str(self.value)
