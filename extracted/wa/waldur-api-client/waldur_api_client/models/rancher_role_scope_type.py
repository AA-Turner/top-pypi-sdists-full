from enum import Enum


class RancherRoleScopeType(str, Enum):
    CLUSTER = "cluster"
    PROJECT = "project"

    def __str__(self) -> str:
        return str(self.value)
