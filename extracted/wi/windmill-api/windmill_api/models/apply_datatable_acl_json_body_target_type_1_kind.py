from enum import Enum


class ApplyDatatableAclJsonBodyTargetType1Kind(str, Enum):
    SCHEMA = "schema"

    def __str__(self) -> str:
        return str(self.value)
