from enum import StrEnum

class ManagedAgentsHttpapiAutomationWebhookTriggerType(StrEnum):
    WEBHOOK = "webhook"

    def __str__(self) -> str:
        return str(self.value)
