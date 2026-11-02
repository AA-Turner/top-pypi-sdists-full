from enum import Enum


class GcpTriggerDataDeliveryType(str, Enum):
    PULL = "pull"
    PUSH = "push"

    def __str__(self) -> str:
        return str(self.value)
