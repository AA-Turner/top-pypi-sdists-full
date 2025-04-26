from enum import Enum


class JobType1RawFlowModulesItemSleepType0Type(str, Enum):
    JAVASCRIPT = "javascript"

    def __str__(self) -> str:
        return str(self.value)
