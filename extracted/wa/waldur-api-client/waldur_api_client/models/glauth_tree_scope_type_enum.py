from enum import Enum


class GlauthTreeScopeTypeEnum(str, Enum):
    PROJECT = "project"
    RESOURCE = "resource"
    RESOURCE_PROJECT = "resource_project"
    USER = "user"

    def __str__(self) -> str:
        return str(self.value)
