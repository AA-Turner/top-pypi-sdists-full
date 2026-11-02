from enum import Enum


class AiDecisionInputTransformsProviderType1Type(str, Enum):
    JAVASCRIPT = "javascript"

    def __str__(self) -> str:
        return str(self.value)
