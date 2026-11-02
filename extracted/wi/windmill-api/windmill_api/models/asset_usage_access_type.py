from enum import Enum


class AssetUsageAccessType(str, Enum):
    R = "r"
    RW = "rw"
    W = "w"

    def __str__(self) -> str:
        return str(self.value)
