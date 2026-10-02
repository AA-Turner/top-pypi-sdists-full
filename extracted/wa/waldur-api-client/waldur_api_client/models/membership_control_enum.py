from enum import Enum


class MembershipControlEnum(str, Enum):
    LOCKED = "locked"
    MEMBERS_ONLY = "members_only"
    OPEN = "open"
    ROLES_ONLY = "roles_only"

    def __str__(self) -> str:
        return str(self.value)
