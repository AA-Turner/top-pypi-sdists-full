from enum import Enum


class AclChangeRequestChangeType2Type(str, Enum):
    REVOKE = "revoke"

    def __str__(self) -> str:
        return str(self.value)
