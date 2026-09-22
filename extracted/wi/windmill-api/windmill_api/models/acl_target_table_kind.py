from enum import Enum


class AclTargetTableKind(str, Enum):
    TABLE = "table"

    def __str__(self) -> str:
        return str(self.value)
