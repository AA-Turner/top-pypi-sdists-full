from enum import Enum


class ListAllExperimentsResponse200ItemScoresItemKind(str, Enum):
    AGENT = "agent"
    SCRIPT = "script"

    def __str__(self) -> str:
        return str(self.value)
