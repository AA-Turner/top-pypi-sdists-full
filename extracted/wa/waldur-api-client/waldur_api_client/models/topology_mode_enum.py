from enum import Enum


class TopologyModeEnum(str, Enum):
    CUSTOMER_CHOICE = "customer_choice"
    VALUE_0 = "1-datacenter"
    VALUE_1 = "3-datacenter"

    def __str__(self) -> str:
        return str(self.value)
