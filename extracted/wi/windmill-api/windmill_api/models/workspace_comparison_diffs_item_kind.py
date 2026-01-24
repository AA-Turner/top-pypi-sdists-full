from enum import Enum


class WorkspaceComparisonDiffsItemKind(str, Enum):
    APP = "app"
    FLOW = "flow"
    RESOURCE = "resource"
    SCRIPT = "script"
    VARIABLE = "variable"

    def __str__(self) -> str:
        return str(self.value)
