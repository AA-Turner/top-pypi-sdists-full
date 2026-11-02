from enum import Enum


class ListRunAssetsResponse200AssetsItemAccessType(str, Enum):
    R = "r"
    RW = "rw"
    W = "w"

    def __str__(self) -> str:
        return str(self.value)
