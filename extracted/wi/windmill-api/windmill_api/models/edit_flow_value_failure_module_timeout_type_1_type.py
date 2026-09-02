from enum import Enum


class EditFlowValueFailureModuleTimeoutType1Type(str, Enum):
    JAVASCRIPT = "javascript"

    def __str__(self) -> str:
        return str(self.value)
