from enum import Enum


class GetCopilotInfoResponse200WebSearchProvider(str, Enum):
    DEEPSEEK = "deepseek"
    EXA = "exa"
    LINKUP = "linkup"
    TAVILY = "tavily"

    def __str__(self) -> str:
        return str(self.value)
