from enum import Enum


class AclChangeRequestTargetType1Kind(str, Enum):
    SCHEMA = "schema"

    def __str__(self) -> str:
        return str(self.value)
