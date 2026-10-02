from enum import StrEnum

class ManagedAgentsLabelboxScopeRequestMode(StrEnum):
    ORGANIZATION = "organization"
    PROJECTS = "projects"

    def __str__(self) -> str:
        return str(self.value)
