from enum import Enum


class OpenFlowWPathValueModulesItemSleepType0Type(str, Enum):
    STATIC = "static"

    def __str__(self) -> str:
        return str(self.value)
