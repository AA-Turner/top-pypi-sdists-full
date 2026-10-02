from enum import StrEnum

class RunEventsSnapshotDtoPropertiesBlocksItemsPropertiesBlocksItemsTablePageDataKind(StrEnum):
    EVAL = "eval"
    TRAIN = "train"

    def __str__(self) -> str:
        return str(self.value)
