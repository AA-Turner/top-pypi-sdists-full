from enum import Enum


class ApprovedGitHubAuthorizationStatus(str, Enum):
    APPROVED = "approved"

    def __str__(self) -> str:
        return str(self.value)
