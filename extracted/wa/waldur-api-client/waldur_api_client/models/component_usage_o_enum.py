from enum import Enum


class ComponentUsageOEnum(str, Enum):
    BILLING_PERIOD = "billing_period"
    USAGE = "usage"
    VALUE_0 = "-billing_period"
    VALUE_1 = "-usage"

    def __str__(self) -> str:
        return str(self.value)
