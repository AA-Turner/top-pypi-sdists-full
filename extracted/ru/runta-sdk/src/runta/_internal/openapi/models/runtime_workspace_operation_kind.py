from enum import Enum


class RuntimeWorkspaceOperationKind(str, Enum):
    LIST_DIRECTORY = "list_directory"
    LIST_PORTS = "list_ports"
    READ_MEDIA = "read_media"
    READ_TEXT = "read_text"
    SEARCH_FILES = "search_files"

    def __str__(self) -> str:
        return str(self.value)
