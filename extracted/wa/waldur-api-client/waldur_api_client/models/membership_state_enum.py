from enum import Enum


class MembershipStateEnum(str, Enum):
    BANNED = "banned"
    INVITED = "invited"
    JOINED = "joined"
    LEFT = "left"

    def __str__(self) -> str:
        return str(self.value)
