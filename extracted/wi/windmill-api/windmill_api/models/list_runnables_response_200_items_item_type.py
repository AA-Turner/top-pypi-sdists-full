from enum import Enum


class ListRunnablesResponse200ItemsItemType(str, Enum):
    APP = "app"
    FLOW = "flow"
    SCRIPT = "script"

    def __str__(self) -> str:
        return str(self.value)
