from enum import Enum


class UserWorkspaceListWorkspacesItemCapabilitiesFlows(str, Enum):
    COMPOSE = "compose"
    FULL = "full"
    NONE = "none"

    def __str__(self) -> str:
        return str(self.value)
