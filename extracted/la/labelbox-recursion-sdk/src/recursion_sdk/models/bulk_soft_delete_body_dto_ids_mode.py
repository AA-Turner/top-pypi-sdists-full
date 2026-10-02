from enum import StrEnum

class BulkSoftDeleteBodyDtoIdsMode(StrEnum):
    IDS = "ids"

    def __str__(self) -> str:
        return str(self.value)
