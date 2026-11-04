from enum import Enum


class AccessReasonType(str, Enum):
    FOLDER = "folder"
    GROUP = "group"
    GROUP_PATH = "group_path"
    OWN = "own"
    USER = "user"

    def __str__(self) -> str:
        return str(self.value)
