from enum import StrEnum

class ManagedAgentsSessionModelCostDetailResponseScope(StrEnum):
    SELF = "self"
    SUBTREE = "subtree"
    TREE = "tree"

    def __str__(self) -> str:
        return str(self.value)
