from enum import StrEnum

class ManagedAgentsWebhookValueSelectorRequestSource(StrEnum):
    BODY = "body"
    HEADER = "header"

    def __str__(self) -> str:
        return str(self.value)
