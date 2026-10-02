import boto3
from aws_lambda_powertools import Logger
from dependency_injector import containers, providers

from rds_proxy_password_rotation.adapter.aws_secrets_manager import AwsSecretsManagerService
from rds_proxy_password_rotation.password_rotation_application import PasswordRotationApplication


class Container(containers.DeclarativeContainer):
    config = providers.Configuration()

    logger = providers.Singleton(
        Logger,
    )

    boto3_secrets_manager = boto3.client(service_name='secretsmanager')

    secrets_manager = providers.Singleton(
        AwsSecretsManagerService,
        boto3_secrets_manager=boto3_secrets_manager,
    )

    password_rotation_application = providers.Singleton(
        PasswordRotationApplication,
        secrets_manager=secrets_manager,
        logger=logger,
    )
