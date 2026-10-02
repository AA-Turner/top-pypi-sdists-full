from enum import StrEnum

class ManagedAgentsEventSourceStatusResponseHealth(StrEnum):
    CONNECTION_UNAVAILABLE = "connection_unavailable"
    HEALTHY = "healthy"
    NEVER_RECEIVED = "never_received"
    PAUSED = "paused"
    SETUP_REQUIRED = "setup_required"

    def __str__(self) -> str:
        return str(self.value)
