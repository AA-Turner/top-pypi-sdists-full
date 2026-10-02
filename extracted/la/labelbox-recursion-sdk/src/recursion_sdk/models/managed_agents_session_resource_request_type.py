from enum import StrEnum

class ManagedAgentsSessionResourceRequestType(StrEnum):
    FILE = "file"

    def __str__(self) -> str:
        return str(self.value)
