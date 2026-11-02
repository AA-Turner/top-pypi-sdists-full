from enum import Enum


class PublicRuntimeStatus(str, Enum):
    CRASHED = "crashed"
    CREATING = "creating"
    DELETING = "deleting"
    ERROR = "error"
    PAUSED = "paused"
    RUNNING = "running"
    SHUTDOWN = "shutdown"
    SUSPENDED = "suspended"
    UNAVAILABLE = "unavailable"

    def __str__(self) -> str:
        return str(self.value)
