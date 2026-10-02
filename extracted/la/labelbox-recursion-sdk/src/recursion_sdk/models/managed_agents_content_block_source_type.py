from enum import StrEnum

class ManagedAgentsContentBlockSourceType(StrEnum):
    FILE = "file"

    def __str__(self) -> str:
        return str(self.value)
