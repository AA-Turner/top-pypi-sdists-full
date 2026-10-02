from enum import StrEnum

class ListJobsForEnvironmentSortDirection(StrEnum):
    ASC = "asc"
    DESC = "desc"

    def __str__(self) -> str:
        return str(self.value)
