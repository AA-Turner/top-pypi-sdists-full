from enum import Enum


class UsageGroupBy(str, Enum):
    WORKSPACE = "workspace"

    def __str__(self) -> str:
        return str(self.value)
