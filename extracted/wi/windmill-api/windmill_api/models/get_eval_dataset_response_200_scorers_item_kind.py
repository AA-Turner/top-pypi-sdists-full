from enum import Enum


class GetEvalDatasetResponse200ScorersItemKind(str, Enum):
    AGENT = "agent"
    SCRIPT = "script"

    def __str__(self) -> str:
        return str(self.value)
