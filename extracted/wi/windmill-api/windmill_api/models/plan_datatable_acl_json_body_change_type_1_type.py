from enum import Enum


class PlanDatatableAclJsonBodyChangeType1Type(str, Enum):
    GRANT = "grant"

    def __str__(self) -> str:
        return str(self.value)
