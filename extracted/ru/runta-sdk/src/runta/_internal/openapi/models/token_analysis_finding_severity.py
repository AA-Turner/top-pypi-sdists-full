from enum import Enum


class TokenAnalysisFindingSeverity(str, Enum):
    DANGER = "danger"
    INFO = "info"
    WARNING = "warning"

    def __str__(self) -> str:
        return str(self.value)
