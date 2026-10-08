from enum import Enum


class ListOrganizationsSortType0Item(str, Enum):
    CREATED_AT = "created_at"
    NAME = "name"

    def __str__(self) -> str:
        return str(self.value)
