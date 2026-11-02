from enum import Enum


class RunnableItemType(str, Enum):
    AGENT = "agent"
    APP = "app"
    FLOW = "flow"
    SCRIPT = "script"

    def __str__(self) -> str:
        return str(self.value)
