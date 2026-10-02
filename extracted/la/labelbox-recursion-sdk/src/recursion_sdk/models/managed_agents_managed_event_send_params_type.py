from enum import StrEnum

class ManagedAgentsManagedEventSendParamsType(StrEnum):
    HANDOFF_RESOLVED = "handoff_resolved"
    SYSTEM_MESSAGE = "system.message"
    USER_MESSAGE = "user.message"

    def __str__(self) -> str:
        return str(self.value)
