from enum import Enum


class InstalledGitHubAuthorizationStatus(str, Enum):
    INSTALLED = "installed"

    def __str__(self) -> str:
        return str(self.value)
