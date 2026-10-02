from enum import StrEnum

class RunEventsSnapshotDtoTerminalType0Type0Status(StrEnum):
    COMPLETED = "completed"
    FAILED = "failed"

    def __str__(self) -> str:
        return str(self.value)
