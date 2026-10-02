from enum import StrEnum

class ComputeAlreadyActiveBodyDtoCode(StrEnum):
    COMPUTE_ALREADY_ACTIVE = "compute_already_active"

    def __str__(self) -> str:
        return str(self.value)
