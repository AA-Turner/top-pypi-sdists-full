from enum import Enum


class ApplyDatatableAclJsonBodyTargetType0Kind(str, Enum):
    DATABASE = "database"

    def __str__(self) -> str:
        return str(self.value)
