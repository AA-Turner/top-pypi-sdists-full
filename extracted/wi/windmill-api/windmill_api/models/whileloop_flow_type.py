from enum import Enum


class WhileloopFlowType(str, Enum):
    WHILELOOPFLOW = "whileloopflow"

    def __str__(self) -> str:
        return str(self.value)
