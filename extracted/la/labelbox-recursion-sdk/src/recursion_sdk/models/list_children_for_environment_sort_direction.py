from enum import StrEnum

class ListChildrenForEnvironmentSortDirection(StrEnum):
    ASC = "asc"
    DESC = "desc"

    def __str__(self) -> str:
        return str(self.value)
