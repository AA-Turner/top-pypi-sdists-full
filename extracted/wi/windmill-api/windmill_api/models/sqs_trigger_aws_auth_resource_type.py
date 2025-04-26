from enum import Enum


class SqsTriggerAwsAuthResourceType(str, Enum):
    CREDENTIALS = "credentials"
    OIDC = "oidc"

    def __str__(self) -> str:
        return str(self.value)
