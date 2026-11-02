from enum import Enum


class RuntimeDesiredStatus(str, Enum):
    DELETING = "deleting"
    PAUSED = "paused"
    RUNNING = "running"
    SHUTDOWN = "shutdown"
    SUSPENDED = "suspended"

    def __str__(self) -> str:
        return str(self.value)
