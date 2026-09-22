from enum import Enum


class AclTargetDatabaseKind(str, Enum):
    DATABASE = "database"

    def __str__(self) -> str:
        return str(self.value)
