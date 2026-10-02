from enum import StrEnum

class TaigaImageListDtoItemsItemBuildStatus(StrEnum):
    BUILDING = "building"
    FAILED = "failed"
    PENDING = "pending"
    READY = "ready"

    def __str__(self) -> str:
        return str(self.value)
