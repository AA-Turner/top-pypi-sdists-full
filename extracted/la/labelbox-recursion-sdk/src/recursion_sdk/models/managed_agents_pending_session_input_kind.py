from enum import StrEnum

class ManagedAgentsPendingSessionInputKind(StrEnum):
    INTERRUPT = "interrupt"
    MESSAGE = "message"

    def __str__(self) -> str:
        return str(self.value)
