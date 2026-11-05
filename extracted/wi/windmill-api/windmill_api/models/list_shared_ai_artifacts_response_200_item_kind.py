from enum import Enum


class ListSharedAiArtifactsResponse200ItemKind(str, Enum):
    HTML = "html"
    MD = "md"

    def __str__(self) -> str:
        return str(self.value)
