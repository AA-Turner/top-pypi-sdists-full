from enum import Enum


class ProjectPosixGroupKindEnum(str, Enum):
    PROJECT_GROUP = "project_group"
    ROLE_GROUP = "role_group"

    def __str__(self) -> str:
        return str(self.value)
