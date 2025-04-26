from enum import Enum


class GetGcpTriggerResponse200DeliveryType(str, Enum):
    PULL = "pull"
    PUSH = "push"

    def __str__(self) -> str:
        return str(self.value)
