from enum import Enum


class ListDeploymentsSortType0Item(str, Enum):
    CREATED_AT = "created_at"
    VERSION = "version"

    def __str__(self) -> str:
        return str(self.value)
