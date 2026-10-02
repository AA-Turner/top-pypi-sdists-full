from uuid import uuid4

from aws_lambda_powertools import Logger
from mypy_boto3_secretsmanager.client import SecretsManagerClient
from mypy_boto3_secretsmanager.type_defs import DescribeSecretResponseTypeDef
from pydantic import ValidationError

from rds_proxy_password_rotation.model import DatabaseCredentials, PasswordStage, UserCredentials, Credentials
from rds_proxy_password_rotation.services import PasswordService


class AwsSecretsManagerService(PasswordService):
    def __init__(self, secretsmanager_client: SecretsManagerClient, logger: Logger):
        self.client = secretsmanager_client
        self.logger = logger

    def is_rotation_enabled(self, secret_id: str) -> bool:
        metadata = self.__get_secret_metadata(secret_id)

        return 'RotationEnabled' in metadata and metadata['RotationEnabled']

    def make_new_credentials_current(self, secret_id: str, token: str):
        metadata = self.__get_secret_metadata(secret_id)
        versions = metadata['VersionIdsToStages']

        current_version = None
        previous_version = None

        for version, stages in versions.items():
            if "AWSCURRENT" in stages:
                if version == token:
                    self.logger.info(f'current secret is already the pending one: {secret_id} and version {version}')
                    return

                current_version = version
            elif "AWSPREVIOUS" in stages:
                previous_version = version

        if previous_version is not None:
            self.client.update_secret_version_stage(
                SecretId=secret_id,
                VersionStage="AWSPREVIOUS",
                MoveToVersionId=current_version,
                RemoveFromVersionId=previous_version
            )
        else:
            self.client.update_secret_version_stage(
                SecretId=secret_id,
                VersionStage="AWSPREVIOUS",
                MoveToVersionId=current_version
            )

        self.client.update_secret_version_stage(
            SecretId=secret_id,
            VersionStage='AWSCURRENT',
            MoveToVersionId=token,
            RemoveFromVersionId=current_version)

        self.client.update_secret_version_stage(
            SecretId=secret_id,
            VersionStage='AWSPENDING',
            RemoveFromVersionId=token)

    def ensure_valid_secret_state(self, secret_id: str, token: str) -> bool:
        metadata = self.__get_secret_metadata(secret_id)
        versions = metadata['VersionIdsToStages']

        if token not in versions:
            self.logger.error("Secret version %s has no stage for rotation of secret %s." % (token, secret_id))
            raise ValueError("Secret version %s has no stage for rotation of secret %s." % (token, secret_id))
        elif "AWSCURRENT" in versions[token]:
            self.logger.info("Secret version %s already set as AWSCURRENT for secret %s." % (token, secret_id))
            return False
        elif "AWSPENDING" not in versions[token]:
            self.logger.error("Secret version %s not set as AWSPENDING for rotation of secret %s." % (token, secret_id))
            raise ValueError("Secret version %s not set as AWSPENDING for rotation of secret %s." % (token, secret_id))
        else:
            return True

    def get_database_credentials(self, secret_id: str, stage: PasswordStage, token: str = None) -> DatabaseCredentials | None:
        try:
            return DatabaseCredentials.model_validate_json(self.__get_secret_value(secret_id, stage, token))
        except ValidationError as e:
            self.logger.error(f"Failed to parse secret value for secret {secret_id} (stage: {stage.name}, token: {token})")

            raise e
        except self.client.exceptions.ResourceNotFoundException:
            self.logger.error(f"Failed to retrieve secret value for secret {secret_id} (stage: {stage.name}, token: {token})")

        return None

    def get_user_credentials(self, secret_id: str, stage: PasswordStage, token: str = None) -> UserCredentials | None:
        try:
            return UserCredentials.model_validate_json(self.__get_secret_value(secret_id, stage, token))
        except ValidationError as e:
            self.logger.error(f"Failed to parse secret value for secret {secret_id} (stage: {stage.name}, token: {token})")

            raise e
        except self.client.exceptions.ResourceNotFoundException:
            self.logger.error(f"Failed to retrieve secret value for secret {secret_id} (stage: {stage.name}, token: {token})")

        return None

    def __get_secret_value(self, secret_id: str, stage: PasswordStage, token: str) -> str:
        stage_string = AwsSecretsManagerService.__get_stage_string(stage)

        if token is None:
            secret = self.client.get_secret_value(SecretId=secret_id, VersionStage=stage_string)
        else:
            secret = self.client.get_secret_value(SecretId=secret_id, VersionId=token, VersionStage=stage_string)

        return secret['SecretString']

    def set_new_pending_password(self, secret_id: str, token: str, credential: DatabaseCredentials):
        if token is None:
            token = str(uuid4())

        new_username = credential.get_next_username()
        pending_credential = credential.model_copy(update={'username': new_username, 'password': self.client.get_random_password(ExcludeCharacters=':/@"\'\\')['RandomPassword']})

        self.client.put_secret_value(
                SecretId=secret_id,
                ClientRequestToken=token,
                SecretString=pending_credential.model_dump_json(),
                VersionStages=[AwsSecretsManagerService.__get_stage_string(PasswordStage.PENDING)])

        self.logger.info(f'new pending secret created: {secret_id} and version {token}')

    def set_credentials(self, secret_id: str, token: str, credentials: Credentials):
        if token is None:
            token = str(uuid4())

        self.client.put_secret_value(
            SecretId=secret_id,
            ClientRequestToken=token,
            SecretString=credentials.model_dump_json(),
            VersionStages=[AwsSecretsManagerService.__get_stage_string(PasswordStage.CURRENT)])

        self.logger.info(f'credentials modified: {secret_id} and version {token}')

    def __get_secret_metadata(self, secret_id: str) -> DescribeSecretResponseTypeDef:
        return self.client.describe_secret(SecretId=secret_id)

    @staticmethod
    def __get_stage_string(stage: PasswordStage) -> str:
        match stage:
            case PasswordStage.CURRENT:
                return "AWSCURRENT"
            case PasswordStage.PENDING:
                return "AWSPENDING"
            case PasswordStage.PREVIOUS:
                return "AWSPREVIOUS"
            case _:
                raise ValueError(f"Invalid stage: {stage}")
