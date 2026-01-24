from enum import Enum


class CompareWorkspacesResponse200DiffsItemKind(str, Enum):
    APP = "app"
    FLOW = "flow"
    RESOURCE = "resource"
    SCRIPT = "script"
    VARIABLE = "variable"

    def __str__(self) -> str:
        return str(self.value)
