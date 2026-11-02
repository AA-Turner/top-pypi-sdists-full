from enum import Enum


class EditGitSyncRepositoryJsonBodyRepositoryCredentialProvider(str, Enum):
    GITLAB = "gitlab"

    def __str__(self) -> str:
        return str(self.value)
