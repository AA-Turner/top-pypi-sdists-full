from enum import Enum


class GetScriptByPathWithDraftResponse200AssetsItemAltAccessType(str, Enum):
    R = "r"
    RW = "rw"
    W = "w"

    def __str__(self) -> str:
        return str(self.value)
