from enum import Enum


class JobType1RawFlowModulesItemSleepType1Type(str, Enum):
    JAVASCRIPT = "javascript"

    def __str__(self) -> str:
        return str(self.value)
