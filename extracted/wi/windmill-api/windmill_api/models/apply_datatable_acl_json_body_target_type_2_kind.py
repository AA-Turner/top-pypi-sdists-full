from enum import Enum


class ApplyDatatableAclJsonBodyTargetType2Kind(str, Enum):
    TABLE = "table"

    def __str__(self) -> str:
        return str(self.value)
