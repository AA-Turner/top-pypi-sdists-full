from enum import Enum


class FlowModuleValue2Type4Type(str, Enum):
    FORLOOPFLOW = "forloopflow"

    def __str__(self) -> str:
        return str(self.value)
