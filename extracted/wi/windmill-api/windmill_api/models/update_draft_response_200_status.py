from enum import Enum


class UpdateDraftResponse200Status(str, Enum):
    CONFLICT = "conflict"
    SAVED = "saved"

    def __str__(self) -> str:
        return str(self.value)
