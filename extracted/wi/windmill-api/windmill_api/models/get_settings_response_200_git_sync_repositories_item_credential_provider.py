from enum import Enum


class GetSettingsResponse200GitSyncRepositoriesItemCredentialProvider(str, Enum):
    GITLAB = "gitlab"

    def __str__(self) -> str:
        return str(self.value)
