from enum import Enum


class TokenAnalysisIssueKind(str, Enum):
    PARSE_ERROR = "parse_error"
    TRUNCATED_CAPTURE = "truncated_capture"

    def __str__(self) -> str:
        return str(self.value)
