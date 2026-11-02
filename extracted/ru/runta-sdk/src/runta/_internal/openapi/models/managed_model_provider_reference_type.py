from enum import Enum


class ManagedModelProviderReferenceType(str, Enum):
    MANAGED = "managed"

    def __str__(self) -> str:
        return str(self.value)
