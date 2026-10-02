from enum import StrEnum

class ManagedAgentsEventSourceSignedPartKind(StrEnum):
    BODY = "body"

    def __str__(self) -> str:
        return str(self.value)
