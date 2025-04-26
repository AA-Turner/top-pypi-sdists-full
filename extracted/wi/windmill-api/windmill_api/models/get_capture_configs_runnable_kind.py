from enum import Enum


class GetCaptureConfigsRunnableKind(str, Enum):
    FLOW = "flow"
    SCRIPT = "script"

    def __str__(self) -> str:
        return str(self.value)
