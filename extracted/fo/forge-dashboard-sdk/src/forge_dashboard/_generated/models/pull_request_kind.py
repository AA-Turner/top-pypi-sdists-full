from enum import StrEnum

class PullRequestKind(StrEnum):
    DEPENDENCY = "dependency"
    REGULAR = "regular"
    RELEASE = "release"

    def __str__(self) -> str:
        return str(self.value)
