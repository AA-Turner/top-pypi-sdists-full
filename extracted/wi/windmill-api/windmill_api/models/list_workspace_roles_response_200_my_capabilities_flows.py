from enum import Enum


class ListWorkspaceRolesResponse200MyCapabilitiesFlows(str, Enum):
    COMPOSE = "compose"
    FULL = "full"
    NONE = "none"

    def __str__(self) -> str:
        return str(self.value)
