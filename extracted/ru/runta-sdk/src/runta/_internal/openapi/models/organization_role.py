from enum import Enum


class OrganizationRole(str, Enum):
    ADMIN = "admin"
    DEVELOPER = "developer"
    OWNER = "owner"
    UNSCOPED = "unscoped"

    def __str__(self) -> str:
        return str(self.value)
