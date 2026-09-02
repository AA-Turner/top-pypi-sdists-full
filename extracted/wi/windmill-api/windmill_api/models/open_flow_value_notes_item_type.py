from enum import Enum


class OpenFlowValueNotesItemType(str, Enum):
    FREE = "free"
    GROUP = "group"

    def __str__(self) -> str:
        return str(self.value)
