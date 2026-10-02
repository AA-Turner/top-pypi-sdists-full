from enum import StrEnum

class ManagedAgentsWebhookValueSelectorSource(StrEnum):
    BODY = "body"
    HEADER = "header"

    def __str__(self) -> str:
        return str(self.value)
