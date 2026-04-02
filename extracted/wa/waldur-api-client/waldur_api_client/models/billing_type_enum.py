from enum import Enum


class BillingTypeEnum(str, Enum):
    FEW = "few"
    FIXED = "fixed"
    LIMIT = "limit"
    ONE = "one"
    USAGE = "usage"

    def __str__(self) -> str:
        return str(self.value)
