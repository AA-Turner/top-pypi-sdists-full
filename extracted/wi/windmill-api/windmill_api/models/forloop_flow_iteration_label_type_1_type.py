from enum import Enum


class ForloopFlowIterationLabelType1Type(str, Enum):
    JAVASCRIPT = "javascript"

    def __str__(self) -> str:
        return str(self.value)
