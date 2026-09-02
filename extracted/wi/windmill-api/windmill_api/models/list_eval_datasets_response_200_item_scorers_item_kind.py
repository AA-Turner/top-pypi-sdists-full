from enum import Enum


class ListEvalDatasetsResponse200ItemScorersItemKind(str, Enum):
    AGENT = "agent"
    SCRIPT = "script"

    def __str__(self) -> str:
        return str(self.value)
