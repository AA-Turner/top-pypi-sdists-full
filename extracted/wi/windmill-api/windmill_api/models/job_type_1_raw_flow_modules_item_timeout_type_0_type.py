from enum import Enum


class JobType1RawFlowModulesItemTimeoutType0Type(str, Enum):
    STATIC = "static"

    def __str__(self) -> str:
        return str(self.value)
