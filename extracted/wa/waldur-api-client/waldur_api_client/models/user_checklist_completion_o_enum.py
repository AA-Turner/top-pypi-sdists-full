from enum import Enum


class UserChecklistCompletionOEnum(str, Enum):
    IS_COMPLETED = "is_completed"
    MODIFIED = "modified"
    VALUE_0 = "-is_completed"
    VALUE_1 = "-modified"

    def __str__(self) -> str:
        return str(self.value)
