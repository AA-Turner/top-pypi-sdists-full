from enum import Enum


class AclChangeRevokeType(str, Enum):
    REVOKE = "revoke"

    def __str__(self) -> str:
        return str(self.value)
