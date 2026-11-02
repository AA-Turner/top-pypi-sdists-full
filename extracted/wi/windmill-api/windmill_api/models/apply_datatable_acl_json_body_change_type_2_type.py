from enum import Enum


class ApplyDatatableAclJsonBodyChangeType2Type(str, Enum):
    REVOKE = "revoke"

    def __str__(self) -> str:
        return str(self.value)
