from enum import Enum


class FlowModuleValue2Type8ToolsItemValueType3ToolType(str, Enum):
    QUESTION = "question"

    def __str__(self) -> str:
        return str(self.value)
