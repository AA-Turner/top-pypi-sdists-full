from enum import Enum


class FlowStatusPreprocessorModuleBranchChosenType(str, Enum):
    BRANCH = "branch"
    DEFAULT = "default"

    def __str__(self) -> str:
        return str(self.value)
