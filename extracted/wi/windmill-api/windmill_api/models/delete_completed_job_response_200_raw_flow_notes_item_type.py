from enum import Enum


class DeleteCompletedJobResponse200RawFlowNotesItemType(str, Enum):
    FREE = "free"
    GROUP = "group"

    def __str__(self) -> str:
        return str(self.value)
