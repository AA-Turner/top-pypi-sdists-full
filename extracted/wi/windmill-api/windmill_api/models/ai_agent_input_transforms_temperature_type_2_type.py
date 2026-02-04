from enum import Enum


class AiAgentInputTransformsTemperatureType2Type(str, Enum):
    AI = "ai"

    def __str__(self) -> str:
        return str(self.value)
