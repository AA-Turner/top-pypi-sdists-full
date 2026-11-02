from enum import Enum


class FlowModuleValue2Type8Type(str, Enum):
    AIAGENT = "aiagent"

    def __str__(self) -> str:
        return str(self.value)
