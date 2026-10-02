from enum import StrEnum

class CreateRunConfigRunDtoCompletionMode(StrEnum):
    GENERIC = "generic"
    TRAINING = "training"

    def __str__(self) -> str:
        return str(self.value)
