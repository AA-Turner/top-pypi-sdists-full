from enum import Enum


class AclTargetType1Kind(str, Enum):
    SCHEMA = "schema"

    def __str__(self) -> str:
        return str(self.value)
