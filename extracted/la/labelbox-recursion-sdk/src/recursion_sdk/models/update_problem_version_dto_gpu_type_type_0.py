from enum import StrEnum

class UpdateProblemVersionDtoGpuTypeType0(StrEnum):
    A100 = "A100"
    A10G = "A10G"
    H100 = "H100"
    L4 = "L4"
    T4 = "T4"

    def __str__(self) -> str:
        return str(self.value)
