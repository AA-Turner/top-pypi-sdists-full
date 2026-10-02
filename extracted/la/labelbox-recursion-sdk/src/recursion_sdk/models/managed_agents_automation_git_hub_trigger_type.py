from enum import StrEnum

class ManagedAgentsAutomationGitHubTriggerType(StrEnum):
    GITHUB = "github"

    def __str__(self) -> str:
        return str(self.value)
