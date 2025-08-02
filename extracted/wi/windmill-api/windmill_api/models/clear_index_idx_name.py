from enum import Enum


class ClearIndexIdxName(str, Enum):
    JOBINDEX = "JobIndex"
    SERVICELOGINDEX = "ServiceLogIndex"

    def __str__(self) -> str:
        return str(self.value)
