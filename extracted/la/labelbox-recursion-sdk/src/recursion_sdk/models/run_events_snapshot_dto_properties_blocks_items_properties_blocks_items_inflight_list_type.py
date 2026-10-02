from enum import StrEnum

class RunEventsSnapshotDtoPropertiesBlocksItemsPropertiesBlocksItemsInflightListType(StrEnum):
    INFLIGHT_LIST = "inflight-list"

    def __str__(self) -> str:
        return str(self.value)
