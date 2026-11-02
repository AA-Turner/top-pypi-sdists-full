from enum import Enum


class FlowModuleValue2Type5DefaultItemSleepType1Type(str, Enum):
    JAVASCRIPT = "javascript"

    def __str__(self) -> str:
        return str(self.value)
