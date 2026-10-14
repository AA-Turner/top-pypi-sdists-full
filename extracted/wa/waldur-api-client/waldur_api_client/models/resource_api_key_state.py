from enum import Enum


class ResourceApiKeyState(str, Enum):
    CREATING = "Creating"
    DELETED = "Deleted"
    DELETING = "Deleting"
    ERRED = "Erred"
    OK = "OK"
    PAUSED = "Paused"
    UPDATING = "Updating"

    def __str__(self) -> str:
        return str(self.value)
