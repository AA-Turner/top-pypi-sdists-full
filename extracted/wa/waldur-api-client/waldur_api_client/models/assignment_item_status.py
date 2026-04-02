from enum import Enum


class AssignmentItemStatus(str, Enum):
    ACCEPTED = "accepted"
    COI_BLOCKED = "coi_blocked"
    DECLINED = "declined"
    EXPIRED = "expired"
    PENDING = "pending"
    REASSIGNED = "reassigned"

    def __str__(self) -> str:
        return str(self.value)
