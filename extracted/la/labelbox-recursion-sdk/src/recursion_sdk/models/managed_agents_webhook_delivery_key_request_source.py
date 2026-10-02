from enum import StrEnum

class ManagedAgentsWebhookDeliveryKeyRequestSource(StrEnum):
    BODY = "body"
    HEADER = "header"

    def __str__(self) -> str:
        return str(self.value)
