from enum import Enum


class FlowModuleValue2Type3ParallelismType1Type(str, Enum):
    JAVASCRIPT = "javascript"

    def __str__(self) -> str:
        return str(self.value)
