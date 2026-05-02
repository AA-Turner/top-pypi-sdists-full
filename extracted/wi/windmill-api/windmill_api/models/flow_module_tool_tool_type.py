from enum import Enum


class FlowModuleToolToolType(str, Enum):
    FLOWMODULE = "flowmodule"

    def __str__(self) -> str:
        return str(self.value)
