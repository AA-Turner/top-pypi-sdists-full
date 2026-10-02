from enum import StrEnum

class ManagedAgentsIntegrationEventSourceDeliveryKind(StrEnum):
    INTEGRATION = "integration"

    def __str__(self) -> str:
        return str(self.value)
