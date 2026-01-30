from enum import Enum


class AutoInviteConfigMode(str, Enum):
    ADD = "add"
    INVITE = "invite"

    def __str__(self) -> str:
        return str(self.value)
