from enum import StrEnum

class ManagedAgentsWebhookDeliveryKeySource(StrEnum):
    BODY = "body"
    HEADER = "header"

    def __str__(self) -> str:
        return str(self.value)
