from enum import Enum


class ComponentUserUsageOEnum(str, Enum):
    COMPONENT_USAGE_BILLING_PERIOD = "component_usage__billing_period"
    USAGE = "usage"
    USERNAME = "username"
    VALUE_0 = "-component_usage__billing_period"
    VALUE_1 = "-usage"
    VALUE_2 = "-username"

    def __str__(self) -> str:
        return str(self.value)
