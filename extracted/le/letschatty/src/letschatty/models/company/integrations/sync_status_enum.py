from enum import Enum


class SyncStatusEnum(str, Enum):
    STARTED = "STARTED"
    RUNNING = "RUNNING"
    FINISHED = "FINISHED"
    FAILED = "FAILED"

