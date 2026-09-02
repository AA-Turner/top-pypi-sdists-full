from enum import Enum


class ExperimentResultsResponse200ExperimentScoresItemKind(str, Enum):
    AGENT = "agent"
    SCRIPT = "script"

    def __str__(self) -> str:
        return str(self.value)
