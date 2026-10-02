from enum import Enum


class DiagnoseCheckStatusEnum(str, Enum):
    FAIL = "fail"
    OK = "ok"
    SKIP = "skip"
    WARN = "warn"

    def __str__(self) -> str:
        return str(self.value)
