from enum import StrEnum

class ListWorkspaceEntriesResponseDtoItemsItemType(StrEnum):
    DIRECTORY = "directory"
    FILE = "file"

    def __str__(self) -> str:
        return str(self.value)
