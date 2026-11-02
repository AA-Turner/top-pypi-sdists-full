from enum import Enum


class GetWorkspaceSettingsDocumentSecrets(str, Enum):
    ENCRYPTED = "encrypted"
    REDACTED = "redacted"

    def __str__(self) -> str:
        return str(self.value)
