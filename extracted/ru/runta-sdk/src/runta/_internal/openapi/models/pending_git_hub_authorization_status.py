from enum import Enum


class PendingGitHubAuthorizationStatus(str, Enum):
    PENDING = "pending"

    def __str__(self) -> str:
        return str(self.value)
