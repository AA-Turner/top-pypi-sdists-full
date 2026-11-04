from enum import Enum


class ListRecentRunsFailedIdsKind(str, Enum):
    AGENT = "agent"
    FLOW = "flow"
    SCRIPT = "script"

    def __str__(self) -> str:
        return str(self.value)
