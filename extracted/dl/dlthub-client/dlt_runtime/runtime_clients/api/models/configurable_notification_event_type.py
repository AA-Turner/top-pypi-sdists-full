from enum import Enum


class ConfigurableNotificationEventType(str, Enum):
    RUN_FAILURE = "run.failure"

    def __str__(self) -> str:
        return str(self.value)
