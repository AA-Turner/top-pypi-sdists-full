from enum import Enum


class ListDataTablesResponse200ItemResourceType(str, Enum):
    EXTERNAL_INSTANCE = "external_instance"
    INSTANCE = "instance"
    POSTGRES = "postgres"

    def __str__(self) -> str:
        return str(self.value)
