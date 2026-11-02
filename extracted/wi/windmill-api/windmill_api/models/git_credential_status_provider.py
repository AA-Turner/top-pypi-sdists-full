from enum import Enum


class GitCredentialStatusProvider(str, Enum):
    GITLAB = "gitlab"

    def __str__(self) -> str:
        return str(self.value)
