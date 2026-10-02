from enum import StrEnum

class SynthesizerJobDtoKind(StrEnum):
    USER = "user"

    def __str__(self) -> str:
        return str(self.value)
