from enum import Enum


class AllowlistEgressPolicyMode(str, Enum):
    ALLOWLIST = "allowlist"

    def __str__(self) -> str:
        return str(self.value)
