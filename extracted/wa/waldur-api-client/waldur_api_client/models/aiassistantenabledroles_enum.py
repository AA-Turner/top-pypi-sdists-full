from enum import Enum


class AIASSISTANTENABLEDROLESEnum(str, Enum):
    ALL = "all"
    ANONYMOUS = "anonymous"
    DISABLED = "disabled"
    STAFF = "staff"
    STAFF_AND_SUPPORT = "staff_and_support"

    def __str__(self) -> str:
        return str(self.value)
