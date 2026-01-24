from enum import Enum


class GroupRole(str, Enum):
    maintainer = "maintainer"
    member = "member"
    pending = "pending"
