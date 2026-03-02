from enum import Enum


class WorkspaceMembershipRole(str, Enum):
    OWNER = "owner"
    VIEWER = "viewer"

    def __str__(self) -> str:
        return str(self.value)
