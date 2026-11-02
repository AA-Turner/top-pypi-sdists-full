from enum import Enum


class CloudAgentPromptImageType(str, Enum):
    IMAGE = "image"

    def __str__(self) -> str:
        return str(self.value)
