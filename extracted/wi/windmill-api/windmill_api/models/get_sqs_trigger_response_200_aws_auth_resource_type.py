from enum import Enum


class GetSqsTriggerResponse200AwsAuthResourceType(str, Enum):
    CREDENTIALS = "credentials"
    OIDC = "oidc"

    def __str__(self) -> str:
        return str(self.value)
