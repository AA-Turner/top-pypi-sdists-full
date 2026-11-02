from enum import StrEnum

class AutoUpdateSource(StrEnum):
    PULLREQUEST = "pullRequest"
    REPO = "repo"

    def __str__(self) -> str:
        return str(self.value)
