from enum import Enum


class ShareAiArtifactResponse200Kind(str, Enum):
    HTML = "html"
    MD = "md"

    def __str__(self) -> str:
        return str(self.value)
