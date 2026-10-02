from enum import StrEnum

class ManagedAgentsWebhookEventSourceDeliverySummaryKind(StrEnum):
    WEBHOOK = "webhook"

    def __str__(self) -> str:
        return str(self.value)
