from enum import Enum


class RunScriptPreviewAndWaitResultJsonBodyKind(str, Enum):
    CODE = "code"
    HTTP = "http"
    IDENTITY = "identity"

    def __str__(self) -> str:
        return str(self.value)
