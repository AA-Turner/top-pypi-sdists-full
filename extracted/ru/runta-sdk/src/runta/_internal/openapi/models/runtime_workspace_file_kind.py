from enum import Enum


class RuntimeWorkspaceFileKind(str, Enum):
    DIRECTORY = "directory"
    FILE = "file"
    IMAGE = "image"
    TEXT = "text"
    VIDEO = "video"

    def __str__(self) -> str:
        return str(self.value)
