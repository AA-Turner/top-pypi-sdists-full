from enum import Enum


class CreateExternalInstancePgDatabaseJsonBodyTag(str, Enum):
    DATATABLE = "datatable"
    DUCKLAKE = "ducklake"

    def __str__(self) -> str:
        return str(self.value)
