from enum import Enum


class ToolValueType2ToolType(str, Enum):
    WEBSEARCH = "websearch"

    def __str__(self) -> str:
        return str(self.value)
