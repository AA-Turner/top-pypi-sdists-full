from enum import Enum


class TJobDefinitionIncrementalModeType0(str, Enum):
    INTERVAL = "interval"
    PIPELINE = "pipeline"

    def __str__(self) -> str:
        return str(self.value)
