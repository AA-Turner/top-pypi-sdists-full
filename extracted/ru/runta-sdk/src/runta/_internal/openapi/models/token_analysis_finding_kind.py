from enum import Enum


class TokenAnalysisFindingKind(str, Enum):
    LARGE_OUTPUT = "large_output"
    REPEATED_CALL = "repeated_call"
    REPEATED_KEYS = "repeated_keys"
    REPEATED_LINES = "repeated_lines"
    REPEATED_PATHS = "repeated_paths"

    def __str__(self) -> str:
        return str(self.value)
