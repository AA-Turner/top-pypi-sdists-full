from enum import Enum


class SearchLogsIndexResponse200HitsItemLevel(str, Enum):
    DEBUG = "DEBUG"
    ERROR = "ERROR"
    INFO = "INFO"
    TRACE = "TRACE"
    WARN = "WARN"

    def __str__(self) -> str:
        return str(self.value)
