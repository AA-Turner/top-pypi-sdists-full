from enum import StrEnum

class ManagedAgentsWebhookEventSourceDeliveryKind(StrEnum):
    WEBHOOK = "webhook"

    def __str__(self) -> str:
        return str(self.value)
