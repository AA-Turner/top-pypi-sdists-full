from enum import Enum


class AllocationTimeEnum(str, Enum):
    FIXED_DATE = "fixed_date"
    ON_DECISION = "on_decision"

    def __str__(self) -> str:
        return str(self.value)
