from enum import Enum


class MatrixRoomStateEnum(str, Enum):
    ACTIVE = "active"
    ARCHIVED = "archived"
    CREATING = "creating"
    DISABLING = "disabling"
    ERROR = "error"

    def __str__(self) -> str:
        return str(self.value)
