from enum import StrEnum

class CreateComputeRequestDtoAcceleratorType(StrEnum):
    GPU = "gpu"

    def __str__(self) -> str:
        return str(self.value)
