from enum import Enum


class PlanDatatableAclJsonBodyTargetType2Kind(str, Enum):
    TABLE = "table"

    def __str__(self) -> str:
        return str(self.value)
