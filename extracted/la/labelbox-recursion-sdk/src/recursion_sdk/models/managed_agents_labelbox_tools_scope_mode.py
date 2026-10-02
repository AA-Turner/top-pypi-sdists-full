from enum import StrEnum

class ManagedAgentsLabelboxToolsScopeMode(StrEnum):
    ORGANIZATION = "organization"
    PROJECTS = "projects"

    def __str__(self) -> str:
        return str(self.value)
