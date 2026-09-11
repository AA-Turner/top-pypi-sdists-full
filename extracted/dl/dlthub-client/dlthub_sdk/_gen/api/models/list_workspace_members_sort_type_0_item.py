from enum import Enum


class ListWorkspaceMembersSortType0Item(str, Enum):
    DATE_ADDED = "date_added"
    EMAIL = "email"

    def __str__(self) -> str:
        return str(self.value)
