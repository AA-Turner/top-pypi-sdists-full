from enum import Enum


class ExtendedJobsJobsItemType0FlowStatusModulesItemBranchChosenType(str, Enum):
    BRANCH = "branch"
    DEFAULT = "default"

    def __str__(self) -> str:
        return str(self.value)
