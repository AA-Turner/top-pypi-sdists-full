from enum import Enum


class OrganizationMembershipRole(str, Enum):
    COLLABORATOR = "collaborator"
    MEMBER = "member"
    OWNER = "owner"

    def __str__(self) -> str:
        return str(self.value)
