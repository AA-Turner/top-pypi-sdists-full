from enum import Enum


class MatrixTicketDraftStateEnum(str, Enum):
    CANCELLED = "cancelled"
    EXPIRED = "expired"
    PENDING = "pending"
    SENT = "sent"

    def __str__(self) -> str:
        return str(self.value)
