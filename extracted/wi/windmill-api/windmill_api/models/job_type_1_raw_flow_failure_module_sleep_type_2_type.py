from enum import Enum


class JobType1RawFlowFailureModuleSleepType2Type(str, Enum):
    AI = "ai"

    def __str__(self) -> str:
        return str(self.value)
