from enum import Enum


class ListGcpTriggersResponse200ItemDeliveryType(str, Enum):
    PULL = "pull"
    PUSH = "push"

    def __str__(self) -> str:
        return str(self.value)
