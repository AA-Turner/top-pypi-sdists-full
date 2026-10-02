from enum import StrEnum

class RunEventsSnapshotDtoPropertiesBlocksItemsPropertiesBlocksItemsSeriesDataAxis(StrEnum):
    STEP = "step"
    TIME = "time"

    def __str__(self) -> str:
        return str(self.value)
