from enum import StrEnum

class ManagedAgentsFileType(StrEnum):
    FILE = "file"

    def __str__(self) -> str:
        return str(self.value)
