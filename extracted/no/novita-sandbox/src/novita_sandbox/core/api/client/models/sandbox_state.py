from enum import Enum


class SandboxState(str, Enum):
    PAUSED = "paused"
    RUNNING = "running"
    CLONING = "cloning"
    COMMITING = "commiting"
    SNAPSHOTTING = "snapshotting"

    def __str__(self) -> str:
        return str(self.value)
