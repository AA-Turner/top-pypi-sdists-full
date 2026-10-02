from enum import StrEnum

class ManagedAgentsEventsAcceptedResponseDeliveryState(StrEnum):
    QUEUED = "queued"
    RESUMED = "resumed"
    SIGNALED = "signaled"
    STORED = "stored"

    def __str__(self) -> str:
        return str(self.value)
