from enum import StrEnum

class ManagedAgentsApiErrorSlackInstallationMismatchCode(StrEnum):
    SLACK_INSTALLATION_MISMATCH = "slack_installation_mismatch"

    def __str__(self) -> str:
        return str(self.value)
