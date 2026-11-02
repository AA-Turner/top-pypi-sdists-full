from enum import Enum


class PlanDatatableAclJsonBodyTargetType0Kind(str, Enum):
    DATABASE = "database"

    def __str__(self) -> str:
        return str(self.value)
