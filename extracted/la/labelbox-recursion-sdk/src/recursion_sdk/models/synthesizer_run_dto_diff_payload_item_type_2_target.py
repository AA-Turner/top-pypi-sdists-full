from enum import StrEnum

class SynthesizerRunDtoDiffPayloadItemType2Target(StrEnum):
    GRADERSUPPORTFILES = "graderSupportFiles"
    PROBLEMFILES = "problemFiles"
    SUPPORTINGFILES = "supportingFiles"

    def __str__(self) -> str:
        return str(self.value)
