from enum import Enum


class RunFlowPreviewJsonBodyValuePreprocessorModuleSuspendSkin(str, Enum):
    DETAILED = "detailed"
    MINIMAL = "minimal"

    def __str__(self) -> str:
        return str(self.value)
