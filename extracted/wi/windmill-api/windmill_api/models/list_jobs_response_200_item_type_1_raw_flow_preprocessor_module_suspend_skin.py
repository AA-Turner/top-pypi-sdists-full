from enum import Enum


class ListJobsResponse200ItemType1RawFlowPreprocessorModuleSuspendSkin(str, Enum):
    DETAILED = "detailed"
    MINIMAL = "minimal"

    def __str__(self) -> str:
        return str(self.value)
