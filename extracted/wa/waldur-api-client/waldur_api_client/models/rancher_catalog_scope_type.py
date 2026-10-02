from enum import Enum


class RancherCatalogScopeType(str, Enum):
    CLUSTER = "cluster"
    GLOBAL = "global"
    PROJECT = "project"

    def __str__(self) -> str:
        return str(self.value)
