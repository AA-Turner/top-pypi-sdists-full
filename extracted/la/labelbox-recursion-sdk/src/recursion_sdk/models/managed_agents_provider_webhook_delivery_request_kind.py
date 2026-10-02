from enum import StrEnum

class ManagedAgentsProviderWebhookDeliveryRequestKind(StrEnum):
    WEBHOOK = "webhook"

    def __str__(self) -> str:
        return str(self.value)
