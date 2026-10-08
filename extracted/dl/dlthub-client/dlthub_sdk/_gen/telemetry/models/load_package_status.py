from enum import Enum


class LoadPackageStatus(str, Enum):
    ABORTED = "aborted"
    EXTRACTED = "extracted"
    LOADED = "loaded"
    NEW = "new"
    NORMALIZED = "normalized"

    def __str__(self) -> str:
        return str(self.value)
