from enum import Enum


class AiAgentInputTransformsUserMessageType1Type(str, Enum):
    JAVASCRIPT = "javascript"

    def __str__(self) -> str:
        return str(self.value)
