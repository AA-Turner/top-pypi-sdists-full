from enum import Enum


class ResourceApiKeyAction(str, Enum):
    CREATE = "create"
    DELETE = "delete"
    PAUSE = "pause"
    RESUME = "resume"
    ROTATE = "rotate"
    UPDATE = "update"

    def __str__(self) -> str:
        return str(self.value)
