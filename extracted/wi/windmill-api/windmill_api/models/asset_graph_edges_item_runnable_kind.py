from enum import Enum


class AssetGraphEdgesItemRunnableKind(str, Enum):
    FLOW = "flow"
    JOB = "job"
    SCRIPT = "script"

    def __str__(self) -> str:
        return str(self.value)
