from enum import Enum


class ConfigurableNotificationEventType(str, Enum):
    RUN_FAILURE = "run.failure"
    RUN_STATUS_CHANGE = "run.status-change"

    def __str__(self) -> str:
        return str(self.value)
