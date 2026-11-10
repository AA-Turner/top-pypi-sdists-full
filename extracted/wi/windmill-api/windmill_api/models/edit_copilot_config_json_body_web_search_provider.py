from enum import Enum


class EditCopilotConfigJsonBodyWebSearchProvider(str, Enum):
    DEEPSEEK = "deepseek"
    EXA = "exa"
    LINKUP = "linkup"
    TAVILY = "tavily"

    def __str__(self) -> str:
        return str(self.value)
