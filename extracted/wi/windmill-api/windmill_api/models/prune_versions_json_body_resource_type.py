from enum import Enum


class PruneVersionsJsonBodyResourceType(str, Enum):
    APPS = "apps"
    FLOWS = "flows"
    RESOURCES = "resources"
    SCRIPTS = "scripts"

    def __str__(self) -> str:
        return str(self.value)
