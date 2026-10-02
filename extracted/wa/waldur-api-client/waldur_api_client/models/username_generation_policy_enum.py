from enum import Enum


class UsernameGenerationPolicyEnum(str, Enum):
    ANONYMIZED = "anonymized"
    FREEIPA = "freeipa"
    FULL_NAME = "full_name"
    IDENTITY_CLAIM = "identity_claim"
    SERVICE_PROVIDER = "service_provider"
    WALDUR_USERNAME = "waldur_username"

    def __str__(self) -> str:
        return str(self.value)
