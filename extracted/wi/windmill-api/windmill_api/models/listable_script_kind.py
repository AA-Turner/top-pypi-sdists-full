from enum import Enum


class ListableScriptKind(str, Enum):
    APPROVAL = "approval"
    FAILURE = "failure"
    PREPROCESSOR = "preprocessor"
    SCRIPT = "script"
    TRIGGER = "trigger"

    def __str__(self) -> str:
        return str(self.value)
