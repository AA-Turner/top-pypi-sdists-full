from enum import Enum


class GetSettingsResponse200AutoInviteMode(str, Enum):
    ADD = "add"
    INVITE = "invite"

    def __str__(self) -> str:
        return str(self.value)
