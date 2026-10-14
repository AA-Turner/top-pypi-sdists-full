from enum import Enum


class ComponentUsageOEnum(str, Enum):
    BILLING_PERIOD = "billing_period"
    MISSING_USAGE_POLICY = "missing_usage_policy"
    USAGE = "usage"
    VALUE_0 = "-billing_period"
    VALUE_1 = "-missing_usage_policy"
    VALUE_2 = "-usage"

    def __str__(self) -> str:
        return str(self.value)
