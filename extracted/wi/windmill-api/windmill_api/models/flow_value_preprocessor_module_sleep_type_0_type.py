from enum import Enum


class FlowValuePreprocessorModuleSleepType0Type(str, Enum):
    STATIC = "static"

    def __str__(self) -> str:
        return str(self.value)
