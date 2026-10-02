from enum import StrEnum

class ImportResponseListDtoItemErrorsItemSeverity(StrEnum):
    ERROR = "error"
    WARNING = "warning"

    def __str__(self) -> str:
        return str(self.value)
