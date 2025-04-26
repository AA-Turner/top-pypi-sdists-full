from enum import Enum


class JobType0FlowStatusModulesItemBranchChosenType(str, Enum):
    BRANCH = "branch"
    DEFAULT = "default"

    def __str__(self) -> str:
        return str(self.value)
