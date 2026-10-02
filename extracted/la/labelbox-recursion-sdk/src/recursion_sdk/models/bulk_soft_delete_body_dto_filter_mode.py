from enum import StrEnum

class BulkSoftDeleteBodyDtoFilterMode(StrEnum):
    FILTER = "filter"

    def __str__(self) -> str:
        return str(self.value)
