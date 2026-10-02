from enum import Enum

from aws_lambda_powertools import Logger

from rds_proxy_password_rotation.model import RotationStep, PasswordStage
from rds_proxy_password_rotation.services import PasswordService, DatabaseService


class PasswordRotationResult(Enum):
    NOTHING_TO_ROTATE = "nothing_to_rotate"
    STEP_EXECUTED = "step_executed"


class PasswordRotationApplication:
    def __init__(self, password_service: PasswordService, database_service: DatabaseService, logger: Logger):
        self.password_service = password_service
        self.database_service = database_service
        self.logger = logger

    def rotate_secret(self, step: RotationStep, secret_id: str, token: str) -> PasswordRotationResult:
        if not self.password_service.is_rotation_enabled(secret_id):
            self.logger.warning("Rotation is not enabled for the secret %s", secret_id)
            return PasswordRotationResult.NOTHING_TO_ROTATE

        if step != RotationStep.CREATE_SECRET and not self.password_service.ensure_valid_secret_state(secret_id, token):
            return PasswordRotationResult.NOTHING_TO_ROTATE

        match step:
            case RotationStep.CREATE_SECRET:
                self.__create_secret(secret_id, token)
            case RotationStep.SET_SECRET:
                self.__set_secret(secret_id, token)
            case RotationStep.TEST_SECRET:
                self.__test_secret(secret_id, token)
            case RotationStep.FINISH_SECRET:
                self.__finish_secret(secret_id, token)
            case _:
                raise ValueError(f"Invalid rotation step: {step}")

        return PasswordRotationResult.STEP_EXECUTED

    def __finish_secret(self, secret_id: str, token: str):
        self.password_service.make_new_credentials_current(secret_id, token)

    def __test_secret(self, secret_id: str, token: str):
        pending_credential = self.password_service.get_database_credentials(secret_id, PasswordStage.PENDING, token)
        self.database_service.test_user_credentials(pending_credential)

    def __set_secret(self, secret_id: str, token: str):
        pending_credential = self.password_service.get_database_credentials(secret_id, PasswordStage.PENDING, token)
        current_credential = self.password_service.get_database_credentials(secret_id, PasswordStage.CURRENT)

        proxy_secret_id = None
        proxy_secret = None

        for secret_id in current_credential.proxy_secret_ids:
            proxy_secret = self.password_service.get_user_credentials(secret_id, PasswordStage.CURRENT)
            if proxy_secret.username == pending_credential.username:
                proxy_secret_id = secret_id
                break

        self.database_service.change_user_credentials(current_credential, pending_credential.password)

        # database and proxy user credentials have to be in sync as the proxy user is used to connect to the database
        if proxy_secret_id is not None:
            self.password_service.set_credentials(secret_id, token, proxy_secret)

        self.logger.info(f'set_secret: successfully set password for user {pending_credential.username} for secret {secret_id}')

    def __create_secret(self, secret_id: str, token: str):
        """
        Creates a new version of the secret with the password to rotate to unless a version tagged with AWSPENDING
        already exists.
        """

        if self.password_service.get_database_credentials(secret_id, PasswordStage.PENDING, token) is not None:
            return

        credentials_to_rotate = self.password_service.get_database_credentials(secret_id, PasswordStage.CURRENT)

        self.password_service.set_new_pending_password(secret_id, token, credentials_to_rotate)
