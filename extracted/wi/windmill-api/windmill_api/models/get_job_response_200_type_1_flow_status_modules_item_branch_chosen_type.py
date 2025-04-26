from enum import Enum


class GetJobResponse200Type1FlowStatusModulesItemBranchChosenType(str, Enum):
    BRANCH = "branch"
    DEFAULT = "default"

    def __str__(self) -> str:
        return str(self.value)
