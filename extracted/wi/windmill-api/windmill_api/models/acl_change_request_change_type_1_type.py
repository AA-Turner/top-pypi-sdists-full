from enum import Enum


class AclChangeRequestChangeType1Type(str, Enum):
    GRANT = "grant"

    def __str__(self) -> str:
        return str(self.value)
