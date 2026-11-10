from enum import Enum


class AIConfigWebSearchProvider(str, Enum):
    DEEPSEEK = "deepseek"
    EXA = "exa"
    LINKUP = "linkup"
    TAVILY = "tavily"

    def __str__(self) -> str:
        return str(self.value)
