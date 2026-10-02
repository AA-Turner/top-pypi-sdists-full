from enum import Enum


class GlauthGroupKind(str, Enum):
    PERSONAL = "personal"
    PROJECT = "project"
    RESOURCE_PROJECT_ROLE = "resource_project_role"
    RESOURCE_ROLE = "resource_role"

    def __str__(self) -> str:
        return str(self.value)
