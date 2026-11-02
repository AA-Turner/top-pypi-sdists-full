from enum import Enum


class QueuedJobRawFlowModulesItemSleepType0Type(str, Enum):
    STATIC = "static"

    def __str__(self) -> str:
        return str(self.value)
