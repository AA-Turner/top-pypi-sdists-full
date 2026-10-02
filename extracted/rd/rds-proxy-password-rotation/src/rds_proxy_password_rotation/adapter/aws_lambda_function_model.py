from enum import Enum

from pydantic import BaseModel, Field

from rds_proxy_password_rotation.model import RotationStep


class AwsRotationStep(Enum):
    CREATE_SECRET = "create_secret"
    """Create a new version of the secret"""
    SET_SECRET = "set_secret"
    """Change the credentials in the database or service"""
    TEST_SECRET = "test_secret"
    """Test the new secret version"""
    FINISH_SECRET = "finish_secret"
    """Finish the rotation"""

    def to_rotation_step(self) -> RotationStep:
        match self:
            case AwsRotationStep.CREATE_SECRET:
                return RotationStep.CREATE_SECRET
            case AwsRotationStep.SET_SECRET:
                return RotationStep.SET_SECRET
            case AwsRotationStep.TEST_SECRET:
                return RotationStep.TEST_SECRET
            case AwsRotationStep.FINISH_SECRET:
                return RotationStep.FINISH_SECRET
            case _:
                raise ValueError(f"Invalid rotation step: {self.value}")


class AwsSecretManagerRotationEvent(BaseModel):
    step: AwsRotationStep = Field(alias='Step')
    """The rotation step: create_secret, set_secret, test_secret, or finish_secret. For more information, see Four steps in a rotation function."""

    secret_id: str = Field(alias='SecretId')
    """The ARN of the secret to rotate."""

    client_request_token: str = Field(alias='ClientRequestToken')
    """A unique identifier for the new version of the secret. This value helps ensure idempotency. For more information, see PutSecretValue: ClientRequestToken in the AWS Secrets Manager API Reference."""

    rotation_token: str = Field(alias='RotationToken')
    """A unique identifier that indicates the source of the request. Required for secret rotation using an assumed role or cross-account rotation, in which you rotate a secret in one account by using a Lambda rotation function in another account. In both cases, the rotation function assumes an IAM role to call Secrets Manager and then Secrets Manager uses the rotation token to validate the IAM role identity."""
