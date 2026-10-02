from enum import StrEnum

class RunEventsSnapshotDtoTerminalType0Type1Status(StrEnum):
    COMPLETED = "completed"
    FAILED = "failed"

    def __str__(self) -> str:
        return str(self.value)
