from enum import StrEnum

class ManagedAgentsHttpapiAutomationWebhookTriggerRequestType(StrEnum):
    WEBHOOK = "webhook"

    def __str__(self) -> str:
        return str(self.value)
