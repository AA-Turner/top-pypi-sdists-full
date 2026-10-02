from enum import StrEnum

class RunEventsSnapshotDtoPropertiesBlocksItemsPropertiesBlocksItemsPillsDataGroupsItemSlotsItemTone(StrEnum):
    ACCUMULATING = "accumulating"
    COMPLETE = "complete"
    CONSTANT = "constant"

    def __str__(self) -> str:
        return str(self.value)
