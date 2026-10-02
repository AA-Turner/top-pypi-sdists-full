from enum import StrEnum

class ComputeCreationInProgressBodyDtoCode(StrEnum):
    COMPUTE_CREATION_IN_PROGRESS = "compute_creation_in_progress"

    def __str__(self) -> str:
        return str(self.value)
