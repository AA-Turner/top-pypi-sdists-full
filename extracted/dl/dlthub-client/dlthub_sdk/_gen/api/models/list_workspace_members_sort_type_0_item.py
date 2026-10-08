from enum import Enum


class ListWorkspaceMembersSortType0Item(str, Enum):
    CREATED_AT = "created_at"
    EMAIL = "email"

    def __str__(self) -> str:
        return str(self.value)
