from enum import Enum


class GetSharedAiArtifactResponse200Kind(str, Enum):
    HTML = "html"
    MD = "md"

    def __str__(self) -> str:
        return str(self.value)
