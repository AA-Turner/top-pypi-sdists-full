from enum import Enum


class GetTopHubScriptsResponse200AsksItemKind(str, Enum):
    APPROVAL = "approval"
    FAILURE = "failure"
    SCRIPT = "script"
    TRIGGER = "trigger"

    def __str__(self) -> str:
        return str(self.value)
