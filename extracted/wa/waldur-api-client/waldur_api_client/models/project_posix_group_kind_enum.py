from enum import Enum


class ProjectPosixGroupKindEnum(str, Enum):
    PROJECT_GROUP = "project_group"
    PROVIDER_PROJECT_GROUP = "provider_project_group"
    ROLE_GROUP = "role_group"

    def __str__(self) -> str:
        return str(self.value)
