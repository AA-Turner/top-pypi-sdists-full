from enum import Enum


class SuspendAndWakeupIdlePolicyMode(str, Enum):
    SUSPEND_AND_WAKEUP = "suspend_and_wakeup"

    def __str__(self) -> str:
        return str(self.value)
