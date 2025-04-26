from enum import Enum


class WhileloopFlowType(str, Enum):
    FORLOOPFLOW = "forloopflow"

    def __str__(self) -> str:
        return str(self.value)
