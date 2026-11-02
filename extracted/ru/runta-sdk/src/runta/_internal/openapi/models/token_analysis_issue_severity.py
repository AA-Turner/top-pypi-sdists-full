from enum import Enum


class TokenAnalysisIssueSeverity(str, Enum):
    DANGER = "danger"
    INFO = "info"
    WARNING = "warning"

    def __str__(self) -> str:
        return str(self.value)
