from enum import Enum


class HubScriptKind(str, Enum):
    APPROVAL = "approval"
    FAILURE = "failure"
    SCRIPT = "script"
    TRIGGER = "trigger"

    def __str__(self) -> str:
        return str(self.value)
