from enum import Enum


class MemberSyncStatusEntryStateEnum(str, Enum):
    ERROR = "error"
    MISSING_IN_IDP = "missing_in_idp"
    PENDING = "pending"
    SYNCED = "synced"

    def __str__(self) -> str:
        return str(self.value)
