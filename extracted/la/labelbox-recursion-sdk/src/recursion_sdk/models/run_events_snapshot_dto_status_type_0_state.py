from enum import StrEnum

class RunEventsSnapshotDtoStatusType0State(StrEnum):
    COMPLETED = "completed"
    FAILED = "failed"
    IDLE = "idle"
    RUNNING = "running"
    STALLED = "stalled"

    def __str__(self) -> str:
        return str(self.value)
