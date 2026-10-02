from enum import Enum


class ResourceApiKeyState(str, Enum):
    CREATING = "Creating"
    ERRED = "Erred"
    OK = "OK"
    UPDATING = "Updating"

    def __str__(self) -> str:
        return str(self.value)
