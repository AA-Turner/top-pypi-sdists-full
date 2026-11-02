from enum import Enum


class DenylistEgressPolicyMode(str, Enum):
    DENYLIST = "denylist"

    def __str__(self) -> str:
        return str(self.value)
