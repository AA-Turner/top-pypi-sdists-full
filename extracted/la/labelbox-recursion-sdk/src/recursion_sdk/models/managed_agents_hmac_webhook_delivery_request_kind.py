from enum import StrEnum

class ManagedAgentsHmacWebhookDeliveryRequestKind(StrEnum):
    WEBHOOK = "webhook"

    def __str__(self) -> str:
        return str(self.value)
