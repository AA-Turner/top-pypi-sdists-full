from enum import Enum


class ContentTypeInputEnum(str, Enum):
    RESOURCE = "resource"
    RESOURCE_PROJECT = "resource_project"

    def __str__(self) -> str:
        return str(self.value)
