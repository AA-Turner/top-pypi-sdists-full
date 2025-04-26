from enum import Enum


class ListScriptsResponse200ItemKind(str, Enum):
    APPROVAL = "approval"
    COMMAND = "command"
    FAILURE = "failure"
    PREPROCESSOR = "preprocessor"
    SCRIPT = "script"
    TRIGGER = "trigger"

    def __str__(self) -> str:
        return str(self.value)
