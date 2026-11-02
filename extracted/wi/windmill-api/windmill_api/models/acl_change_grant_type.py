from enum import Enum


class AclChangeGrantType(str, Enum):
    GRANT = "grant"

    def __str__(self) -> str:
        return str(self.value)
