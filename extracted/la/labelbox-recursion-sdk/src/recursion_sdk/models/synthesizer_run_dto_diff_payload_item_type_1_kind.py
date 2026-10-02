from enum import StrEnum

class SynthesizerRunDtoDiffPayloadItemType1Kind(StrEnum):
    ROW = "row"

    def __str__(self) -> str:
        return str(self.value)
