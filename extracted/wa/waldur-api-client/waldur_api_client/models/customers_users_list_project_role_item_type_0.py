from enum import Enum


class CustomersUsersListProjectRoleItemType0(str, Enum):
    PROJECT_ADMIN = "PROJECT.ADMIN"
    PROJECT_MANAGER = "PROJECT.MANAGER"
    PROJECT_MEMBER = "PROJECT.MEMBER"

    def __str__(self) -> str:
        return str(self.value)
