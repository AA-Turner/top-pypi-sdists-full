from enum import Enum


class AvailableChecklistsResponseChecklistTypeEnum(str, Enum):
    ALL = "all"
    CUSTOMER = "customer"
    INTENT = "intent"

    def __str__(self) -> str:
        return str(self.value)
