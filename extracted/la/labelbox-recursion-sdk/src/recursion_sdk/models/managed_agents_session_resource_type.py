from enum import StrEnum

class ManagedAgentsSessionResourceType(StrEnum):
    FILE = "file"

    def __str__(self) -> str:
        return str(self.value)
