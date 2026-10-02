from enum import StrEnum

class SynthesizerRunDtoDiffPayloadItemType2Kind(StrEnum):
    FILE = "file"

    def __str__(self) -> str:
        return str(self.value)
