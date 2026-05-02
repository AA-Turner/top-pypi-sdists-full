from enum import Enum


class FlowModuleValue2Type4Type(str, Enum):
    WHILELOOPFLOW = "whileloopflow"

    def __str__(self) -> str:
        return str(self.value)
