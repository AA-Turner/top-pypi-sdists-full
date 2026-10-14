from enum import Enum


class ProjectActionEnum(str, Enum):
    CREATE = "create"
    EXISTING = "existing"
    NOT_RECREATED = "not_recreated"

    def __str__(self) -> str:
        return str(self.value)
