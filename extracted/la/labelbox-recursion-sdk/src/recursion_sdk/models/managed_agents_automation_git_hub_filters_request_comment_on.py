from enum import StrEnum

class ManagedAgentsAutomationGitHubFiltersRequestCommentOn(StrEnum):
    ISSUE = "issue"
    PULL_REQUEST = "pull_request"

    def __str__(self) -> str:
        return str(self.value)
