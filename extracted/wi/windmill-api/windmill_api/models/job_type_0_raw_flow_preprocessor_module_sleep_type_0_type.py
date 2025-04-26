from enum import Enum


class JobType0RawFlowPreprocessorModuleSleepType0Type(str, Enum):
    JAVASCRIPT = "javascript"

    def __str__(self) -> str:
        return str(self.value)
