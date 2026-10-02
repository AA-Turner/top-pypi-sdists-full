from enum import StrEnum

class ProblemRunResponseListDtoItemProvenanceType0(StrEnum):
    TAIGA = "taiga"
    V2 = "v2"

    def __str__(self) -> str:
        return str(self.value)
