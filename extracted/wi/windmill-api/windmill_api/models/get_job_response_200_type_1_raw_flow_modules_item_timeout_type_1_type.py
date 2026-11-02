from enum import Enum


class GetJobResponse200Type1RawFlowModulesItemTimeoutType1Type(str, Enum):
    JAVASCRIPT = "javascript"

    def __str__(self) -> str:
        return str(self.value)
