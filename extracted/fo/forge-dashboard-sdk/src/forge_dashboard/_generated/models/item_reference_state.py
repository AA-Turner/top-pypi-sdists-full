from enum import StrEnum

class ItemReferenceState(StrEnum):
    CLOSED = "closed"
    MERGED = "merged"
    OPEN = "open"

    def __str__(self) -> str:
        return str(self.value)
