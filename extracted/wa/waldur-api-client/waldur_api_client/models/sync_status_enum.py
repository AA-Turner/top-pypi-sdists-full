from enum import Enum


class SyncStatusEnum(str, Enum):
    IN_SYNC = "in_sync"
    OUT_OF_SYNC = "out_of_sync"
    SYNC_FAILED = "sync_failed"

    def __str__(self) -> str:
        return str(self.value)
