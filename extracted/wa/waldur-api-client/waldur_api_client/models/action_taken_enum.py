from enum import Enum


class ActionTakenEnum(str, Enum):
    ALLOW = "allow"
    BLOCK = "block"
    FLAG = "flag"
    REDACT = "redact"
    WARN = "warn"

    def __str__(self) -> str:
        return str(self.value)
