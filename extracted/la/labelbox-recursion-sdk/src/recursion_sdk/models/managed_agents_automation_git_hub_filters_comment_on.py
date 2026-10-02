from enum import StrEnum

class ManagedAgentsAutomationGitHubFiltersCommentOn(StrEnum):
    ISSUE = "issue"
    PULL_REQUEST = "pull_request"

    def __str__(self) -> str:
        return str(self.value)
