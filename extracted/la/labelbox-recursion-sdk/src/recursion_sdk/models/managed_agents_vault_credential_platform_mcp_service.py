from enum import StrEnum

class ManagedAgentsVaultCredentialPlatformMcpService(StrEnum):
    SLACK_TOOLS = "slack_tools"

    def __str__(self) -> str:
        return str(self.value)
