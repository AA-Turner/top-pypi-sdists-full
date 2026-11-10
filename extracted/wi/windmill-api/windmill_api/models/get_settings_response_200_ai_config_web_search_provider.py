from enum import Enum


class GetSettingsResponse200AiConfigWebSearchProvider(str, Enum):
    DEEPSEEK = "deepseek"
    EXA = "exa"
    LINKUP = "linkup"
    TAVILY = "tavily"

    def __str__(self) -> str:
        return str(self.value)
