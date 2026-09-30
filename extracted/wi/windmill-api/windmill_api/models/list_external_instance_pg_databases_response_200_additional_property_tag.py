from enum import Enum


class ListExternalInstancePgDatabasesResponse200AdditionalPropertyTag(str, Enum):
    DATATABLE = "datatable"
    DUCKLAKE = "ducklake"

    def __str__(self) -> str:
        return str(self.value)
