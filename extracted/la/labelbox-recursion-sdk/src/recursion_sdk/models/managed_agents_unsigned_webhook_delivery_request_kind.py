from enum import StrEnum

class ManagedAgentsUnsignedWebhookDeliveryRequestKind(StrEnum):
    WEBHOOK = "webhook"

    def __str__(self) -> str:
        return str(self.value)
