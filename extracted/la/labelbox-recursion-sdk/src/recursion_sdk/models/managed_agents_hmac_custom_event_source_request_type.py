from enum import StrEnum

class ManagedAgentsHmacCustomEventSourceRequestType(StrEnum):
    CUSTOM_WEBHOOK = "custom_webhook"

    def __str__(self) -> str:
        return str(self.value)
