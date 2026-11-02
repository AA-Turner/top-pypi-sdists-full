from enum import Enum


class GetAiArtifactShareStatusResponse200ShareKind(str, Enum):
    HTML = "html"
    MD = "md"

    def __str__(self) -> str:
        return str(self.value)
