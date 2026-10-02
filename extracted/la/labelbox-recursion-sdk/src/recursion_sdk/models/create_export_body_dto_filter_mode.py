from enum import StrEnum

class CreateExportBodyDtoFilterMode(StrEnum):
    FILTER = "filter"

    def __str__(self) -> str:
        return str(self.value)
