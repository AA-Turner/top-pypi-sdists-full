from enum import Enum


class ListAiUsageScope(str, Enum):
    SELF = "self"
    WORKSPACE = "workspace"

    def __str__(self) -> str:
        return str(self.value)
