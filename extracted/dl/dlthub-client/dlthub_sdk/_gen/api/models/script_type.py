from enum import Enum


class ScriptType(str, Enum):
    BATCH = "batch"
    INTERACTIVE = "interactive"
    STREAM = "stream"

    def __str__(self) -> str:
        return str(self.value)
