from enum import Enum


class NodeDiskDriverEnum(str, Enum):
    SD = "sd"
    VD = "vd"

    def __str__(self) -> str:
        return str(self.value)
