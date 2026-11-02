from enum import Enum


class RunFlowPreviewAndWaitResultJsonBodyValueNotesItemType(str, Enum):
    FREE = "free"
    GROUP = "group"

    def __str__(self) -> str:
        return str(self.value)
