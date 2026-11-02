from enum import Enum


class AiAgentInputTransformsMemoryType1Type(str, Enum):
    JAVASCRIPT = "javascript"

    def __str__(self) -> str:
        return str(self.value)
