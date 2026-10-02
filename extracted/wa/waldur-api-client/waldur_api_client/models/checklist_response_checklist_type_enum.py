from enum import Enum


class ChecklistResponseChecklistTypeEnum(str, Enum):
    CUSTOMER = "customer"
    INTENT = "intent"

    def __str__(self) -> str:
        return str(self.value)
