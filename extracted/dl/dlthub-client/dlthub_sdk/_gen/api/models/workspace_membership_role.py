from enum import Enum


class WorkspaceMembershipRole(str, Enum):
    DEVELOPER = "developer"
    OWNER = "owner"
    VIEWER = "viewer"

    def __str__(self) -> str:
        return str(self.value)
