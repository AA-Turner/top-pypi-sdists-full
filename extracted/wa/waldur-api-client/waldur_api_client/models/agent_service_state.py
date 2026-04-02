from enum import Enum


class AgentServiceState(str, Enum):
    ACTIVE = "Active"
    ERROR = "Error"
    IDLE = "Idle"

    def __str__(self) -> str:
        return str(self.value)
