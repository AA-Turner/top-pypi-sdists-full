from enum import Enum


class GetCiTestResultsKind(str, Enum):
    FLOW = "flow"
    RESOURCE = "resource"
    SCRIPT = "script"

    def __str__(self) -> str:
        return str(self.value)
