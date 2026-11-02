from enum import Enum


class FlowModuleValue2Type8ToolsItemValueType2ToolType(str, Enum):
    WEBSEARCH = "websearch"

    def __str__(self) -> str:
        return str(self.value)
