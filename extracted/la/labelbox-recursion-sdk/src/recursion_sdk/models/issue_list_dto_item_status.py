from enum import StrEnum

class IssueListDtoItemStatus(StrEnum):
    CLOSED = "closed"
    OPEN = "open"

    def __str__(self) -> str:
        return str(self.value)
