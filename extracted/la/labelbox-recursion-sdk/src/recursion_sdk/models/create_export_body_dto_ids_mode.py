from enum import StrEnum

class CreateExportBodyDtoIdsMode(StrEnum):
    IDS = "ids"

    def __str__(self) -> str:
        return str(self.value)
