from enum import StrEnum

class ListAgentMemoriesSort(StrEnum):
    ALPHABETICAL = "alphabetical"
    UPDATED = "updated"

    def __str__(self) -> str:
        return str(self.value)
