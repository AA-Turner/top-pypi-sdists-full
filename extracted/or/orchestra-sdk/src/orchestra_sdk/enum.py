from enum import Enum


class TaskRunStatus(Enum):
    CANCELLED = "CANCELLED"
    FAILED = "FAILED"
    RUNNING = "RUNNING"
    SUCCEEDED = "SUCCEEDED"
    WARNING = "WARNING"


class WebhookEventType(Enum):
    LOG = "LOG"
    UPDATE_STATUS = "UPDATE_STATUS"
    SET_OUTPUT = "SET_OUTPUT"
