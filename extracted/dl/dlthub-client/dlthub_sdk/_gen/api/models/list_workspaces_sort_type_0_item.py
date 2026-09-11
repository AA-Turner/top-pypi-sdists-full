from enum import Enum


class ListWorkspacesSortType0Item(str, Enum):
    DATE_ADDED = "date_added"
    NAME = "name"

    def __str__(self) -> str:
        return str(self.value)
