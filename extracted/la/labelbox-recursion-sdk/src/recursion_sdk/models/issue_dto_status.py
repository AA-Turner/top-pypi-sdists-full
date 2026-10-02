from enum import StrEnum

class IssueDtoStatus(StrEnum):
    CLOSED = "closed"
    OPEN = "open"

    def __str__(self) -> str:
        return str(self.value)
