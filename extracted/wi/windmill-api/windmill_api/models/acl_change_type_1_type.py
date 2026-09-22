from enum import Enum


class AclChangeType1Type(str, Enum):
    GRANT = "grant"

    def __str__(self) -> str:
        return str(self.value)
