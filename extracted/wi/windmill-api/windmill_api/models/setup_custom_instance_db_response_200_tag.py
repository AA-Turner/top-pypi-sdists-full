from enum import Enum


class SetupCustomInstanceDbResponse200Tag(str, Enum):
    DATATABLE = "datatable"
    DUCKLAKE = "ducklake"

    def __str__(self) -> str:
        return str(self.value)
