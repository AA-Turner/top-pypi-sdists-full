from enum import Enum


class FlowModuleValue2Type4ModulesItemSleepType1Type(str, Enum):
    JAVASCRIPT = "javascript"

    def __str__(self) -> str:
        return str(self.value)
