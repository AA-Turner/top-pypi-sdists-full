from enum import StrEnum

class RunEventsSnapshotDtoStatusType0LiveType0PerRolloutItemPhaseType0(StrEnum):
    GENERATING = "generating"
    GRADING = "grading"

    def __str__(self) -> str:
        return str(self.value)
