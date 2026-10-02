from enum import StrEnum

class QaJobPageResponseDtoItemsItemResultType0IssuesItemSeverity(StrEnum):
    ERROR = "error"
    INFO = "info"
    WARNING = "warning"

    def __str__(self) -> str:
        return str(self.value)
