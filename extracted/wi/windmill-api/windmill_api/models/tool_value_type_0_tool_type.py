from enum import Enum


class ToolValueType0ToolType(str, Enum):
    FLOWMODULE = "flowmodule"

    def __str__(self) -> str:
        return str(self.value)
