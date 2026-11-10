from enum import Enum


class DeliveryEnum(str, Enum):
    RMQ = "rmq"
    WEBHOOK = "webhook"

    def __str__(self) -> str:
        return str(self.value)
