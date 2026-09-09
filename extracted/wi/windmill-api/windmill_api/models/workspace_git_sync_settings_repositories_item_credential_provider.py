from enum import Enum


class WorkspaceGitSyncSettingsRepositoriesItemCredentialProvider(str, Enum):
    GITLAB = "gitlab"

    def __str__(self) -> str:
        return str(self.value)
