import os
from typing import List
from .app_config import AppConfig, AppConfigError
from .secrets import SecretRetriever, SecretNotFound


def secrets_validator(secrets: List[str]):
    secret_retriever = SecretRetriever()
    for secret in secrets:
        try:
            secret_retriever.get_secret_as_dict(secret)
        except SecretNotFound:
            raise Exception(f"Secret named `{secret}` not found")


def run_validations(app_config: AppConfig):
    pass
