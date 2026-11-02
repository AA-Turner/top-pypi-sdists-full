from enum import Enum


class SharedAiArtifactInfoKind(str, Enum):
    HTML = "html"
    MD = "md"

    def __str__(self) -> str:
        return str(self.value)
