from enum import Enum


class WorkspaceItemDiffKind(str, Enum):
    APP = "app"
    FLOW = "flow"
    RESOURCE = "resource"
    RESOURCE_TYPE = "resource_type"
    SCRIPT = "script"
    VARIABLE = "variable"

    def __str__(self) -> str:
        return str(self.value)
