from enum import StrEnum

class IssueDetailsKind(StrEnum):
    ISSUE = "issue"
    PULLREQUEST = "pullRequest"

    def __str__(self) -> str:
        return str(self.value)
