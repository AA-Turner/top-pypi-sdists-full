from enum import StrEnum

class ListSessionResourceSamplesResolution(StrEnum):
    MINUTE = "minute"
    RAW = "raw"

    def __str__(self) -> str:
        return str(self.value)
