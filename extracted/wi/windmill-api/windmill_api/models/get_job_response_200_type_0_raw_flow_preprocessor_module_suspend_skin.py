from enum import Enum


class GetJobResponse200Type0RawFlowPreprocessorModuleSuspendSkin(str, Enum):
    DETAILED = "detailed"
    MINIMAL = "minimal"

    def __str__(self) -> str:
        return str(self.value)
