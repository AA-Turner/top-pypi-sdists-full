from enum import StrEnum

class BuiltInSynthesizerDtoKind(StrEnum):
    BUILT_IN = "built-in"

    def __str__(self) -> str:
        return str(self.value)
