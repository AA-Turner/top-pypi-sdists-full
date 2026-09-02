from enum import Enum


class OpenFlowValueModulesItemSleepType2Type(str, Enum):
    AI = "ai"

    def __str__(self) -> str:
        return str(self.value)
