from enum import Enum


class SetupCustomInstanceDbJsonBodyTag(str, Enum):
    DATATABLE = "datatable"
    DUCKLAKE = "ducklake"

    def __str__(self) -> str:
        return str(self.value)
