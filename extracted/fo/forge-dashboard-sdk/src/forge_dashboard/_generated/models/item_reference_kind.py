from enum import StrEnum

class ItemReferenceKind(StrEnum):
    ISSUE = "issue"
    PULLREQUEST = "pullRequest"

    def __str__(self) -> str:
        return str(self.value)
