from enum import Enum


class InviteStatus(str, Enum):
    ACCEPTED = "accepted"
    PENDING = "pending"
    REVOKED = "revoked"

    def __str__(self) -> str:
        return str(self.value)
