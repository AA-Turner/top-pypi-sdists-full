from enum import Enum


class AiAgentType(str, Enum):
    AIAGENT = "aiagent"

    def __str__(self) -> str:
        return str(self.value)
