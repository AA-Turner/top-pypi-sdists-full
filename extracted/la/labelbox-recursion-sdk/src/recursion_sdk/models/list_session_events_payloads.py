from enum import StrEnum

class ListSessionEventsPayloads(StrEnum):
    REFS = "refs"

    def __str__(self) -> str:
        return str(self.value)
