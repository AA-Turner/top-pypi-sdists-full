from enum import Enum


class MigrateLegacyDraftJsonBodyAction(str, Enum):
    ASSIGN_TO_SELF = "assign_to_self"
    DELETE = "delete"

    def __str__(self) -> str:
        return str(self.value)
