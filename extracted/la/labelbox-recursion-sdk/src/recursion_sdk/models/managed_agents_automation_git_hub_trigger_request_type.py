from enum import StrEnum

class ManagedAgentsAutomationGitHubTriggerRequestType(StrEnum):
    GITHUB = "github"

    def __str__(self) -> str:
        return str(self.value)
