from enum import Enum


class TJobDefinitionIncrementalMode(str, Enum):
    INTERVAL = "interval"
    PIPELINE = "pipeline"

    def __str__(self) -> str:
        return str(self.value)
