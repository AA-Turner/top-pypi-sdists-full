from enum import Enum


class GetCiTestResultsBatchJsonBodyItemsItemKind(str, Enum):
    FLOW = "flow"
    RESOURCE = "resource"
    SCRIPT = "script"

    def __str__(self) -> str:
        return str(self.value)
