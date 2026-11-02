from enum import Enum


class ExpiredGitHubAuthorizationStatus(str, Enum):
    EXPIRED = "expired"

    def __str__(self) -> str:
        return str(self.value)
