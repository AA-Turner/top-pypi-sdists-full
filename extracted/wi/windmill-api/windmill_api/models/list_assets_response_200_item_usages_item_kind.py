from enum import Enum


class ListAssetsResponse200ItemUsagesItemKind(str, Enum):
    FLOW = "flow"
    SCRIPT = "script"

    def __str__(self) -> str:
        return str(self.value)
