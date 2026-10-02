from enum import Enum


class AccessTypeEnum(str, Enum):
    STAFF = "staff"
    STAFF_AND_SUPPORT = "staff_and_support"
    SUPPORT = "support"

    def __str__(self) -> str:
        return str(self.value)
