from enum import Enum


class ListRunnablesOrderBy(str, Enum):
    NAME = "name"
    UPDATED = "updated"

    def __str__(self) -> str:
        return str(self.value)
