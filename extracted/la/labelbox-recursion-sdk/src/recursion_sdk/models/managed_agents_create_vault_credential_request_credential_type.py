from enum import StrEnum

class ManagedAgentsCreateVaultCredentialRequestCredentialType(StrEnum):
    BEARER_TOKEN = "bearer_token"
    ENV_VAR = "env_var"
    INTEGRATION = "integration"
    WEBHOOK_SECRET = "webhook_secret"

    def __str__(self) -> str:
        return str(self.value)
