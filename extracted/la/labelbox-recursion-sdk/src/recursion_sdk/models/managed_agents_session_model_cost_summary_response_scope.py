from enum import StrEnum

class ManagedAgentsSessionModelCostSummaryResponseScope(StrEnum):
    SELF = "self"
    SUBTREE = "subtree"
    TREE = "tree"

    def __str__(self) -> str:
        return str(self.value)
