from enum import Enum


class UpdateEvalDatasetJsonBodyScorersItemKind(str, Enum):
    AGENT = "agent"
    SCRIPT = "script"

    def __str__(self) -> str:
        return str(self.value)
