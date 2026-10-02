from enum import StrEnum

class ManagedAgentsSessionResourceSamplesResponseResolution(StrEnum):
    MINUTE = "minute"
    RAW = "raw"

    def __str__(self) -> str:
        return str(self.value)
