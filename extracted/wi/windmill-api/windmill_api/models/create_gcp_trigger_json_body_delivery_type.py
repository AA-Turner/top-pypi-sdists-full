from enum import Enum


class CreateGcpTriggerJsonBodyDeliveryType(str, Enum):
    PULL = "pull"
    PUSH = "push"

    def __str__(self) -> str:
        return str(self.value)
