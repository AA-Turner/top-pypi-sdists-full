from enum import Enum


class InvitationStateEnum(str, Enum):
    ACCEPTED = "accepted"
    CANCELED = "canceled"
    EXPIRED = "expired"
    PENDING = "pending"
    PROJECT = "project"
    REJECTED = "rejected"
    REQUESTED = "requested"

    def __str__(self) -> str:
        return str(self.value)
