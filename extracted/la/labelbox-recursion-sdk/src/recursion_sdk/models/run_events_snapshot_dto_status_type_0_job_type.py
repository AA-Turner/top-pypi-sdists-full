from enum import StrEnum

class RunEventsSnapshotDtoStatusType0JobType(StrEnum):
    EVAL = "eval"
    HARVEST = "harvest"
    TRAIN = "train"

    def __str__(self) -> str:
        return str(self.value)
