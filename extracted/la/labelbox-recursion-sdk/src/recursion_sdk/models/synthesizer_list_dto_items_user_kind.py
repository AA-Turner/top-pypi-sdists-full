from enum import StrEnum

class SynthesizerListDtoItemsUserKind(StrEnum):
    USER = "user"

    def __str__(self) -> str:
        return str(self.value)
