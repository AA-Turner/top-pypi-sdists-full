from enum import Enum


class AiAgentInputTransformsProviderType2Type(str, Enum):
    AI = "ai"

    def __str__(self) -> str:
        return str(self.value)
