from enum import Enum


class OfferingUserPosixGroupKindEnum(str, Enum):
    PROJECT_GROUP = "project_group"
    PROVIDER_PROJECT_GROUP = "provider_project_group"

    def __str__(self) -> str:
        return str(self.value)
