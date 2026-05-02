from enum import Enum


class ListDataTablesResponse200ItemResourceType(str, Enum):
    INSTANCE = "instance"
    POSTGRES = "postgres"

    def __str__(self) -> str:
        return str(self.value)
