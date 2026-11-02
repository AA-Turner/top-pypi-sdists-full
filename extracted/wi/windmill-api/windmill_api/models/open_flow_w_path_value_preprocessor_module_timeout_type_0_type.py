from enum import Enum


class OpenFlowWPathValuePreprocessorModuleTimeoutType0Type(str, Enum):
    STATIC = "static"

    def __str__(self) -> str:
        return str(self.value)
