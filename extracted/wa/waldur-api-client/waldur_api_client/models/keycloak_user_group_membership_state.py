from enum import Enum


class KeycloakUserGroupMembershipState(str, Enum):
    ACTIVE = "active"
    PENDING = "pending"

    def __str__(self) -> str:
        return str(self.value)
