from enum import Enum


class HideRecentRunItemsJsonBodyItemsItemKind(str, Enum):
    AGENT = "agent"
    FLOW = "flow"
    SCRIPT = "script"

    def __str__(self) -> str:
        return str(self.value)
