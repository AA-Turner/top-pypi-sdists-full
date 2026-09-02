from enum import Enum


class WorkspaceGitSyncSettingsRepositoriesItemAutoPullMode(str, Enum):
    AUTO = "auto"
    POLLING = "polling"
    WEBHOOK = "webhook"

    def __str__(self) -> str:
        return str(self.value)
