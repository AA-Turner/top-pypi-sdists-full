from enum import StrEnum

class ManagedAgentsGithubEventSourceRequestType(StrEnum):
    GITHUB_WEBHOOK = "github_webhook"

    def __str__(self) -> str:
        return str(self.value)
