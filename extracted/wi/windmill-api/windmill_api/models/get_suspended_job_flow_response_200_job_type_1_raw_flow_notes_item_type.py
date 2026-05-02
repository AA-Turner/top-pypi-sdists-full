from enum import Enum


class GetSuspendedJobFlowResponse200JobType1RawFlowNotesItemType(str, Enum):
    FREE = "free"
    GROUP = "group"

    def __str__(self) -> str:
        return str(self.value)
