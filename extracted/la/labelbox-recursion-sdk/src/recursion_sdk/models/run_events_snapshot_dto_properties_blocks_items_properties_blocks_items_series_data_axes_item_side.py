from enum import StrEnum

class RunEventsSnapshotDtoPropertiesBlocksItemsPropertiesBlocksItemsSeriesDataAxesItemSide(StrEnum):
    LEFT = "left"
    RIGHT = "right"

    def __str__(self) -> str:
        return str(self.value)
