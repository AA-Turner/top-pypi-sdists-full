from enum import Enum


class GetFlowByPathWithDraftResponse200DraftValueNotesItemType(str, Enum):
    FREE = "free"
    GROUP = "group"

    def __str__(self) -> str:
        return str(self.value)
