"""Creators for gcp secrets"""
from pathlib import Path
from typing import Callable, Optional

from mcli.models import SecretType
from mcli.objects.secrets import MCLIGCPSecret
from mcli.objects.secrets.create.base import SecretCreator, SecretValidationError
from mcli.objects.secrets.create.generic import FileSecretFiller, FileSecretValidator
from mcli.utils.utils_interactive import file_prompt
from mcli.utils.utils_string_functions import validate_existing_filename


class GCPSecretFiller(FileSecretFiller):
    """Interactive filler for gcp secret data
    """

    @staticmethod
    def fill_file(prompt: str, validate: Callable[[str], bool]) -> str:
        return file_prompt(prompt, validate=validate)

    @classmethod
    def fill_credentials(cls, validate: Callable[[str], bool]) -> str:
        return cls.fill_file(
            'Where is your GCP credentials file located?',
            validate,
        )


class GCPSecretValidator(FileSecretValidator):
    """Validation methods for secret data

    Raises:
        SecretValidationError: Raised for any validation error for secret data
    """

    @staticmethod
    def validate_file_exists(path: str) -> bool:
        if not validate_existing_filename(path):
            raise SecretValidationError(f'File does not exist. File path {path} does not exist or is not a file.')
        return True


class GCPSecretCreator(GCPSecretFiller, GCPSecretValidator):
    """Creates gcp secrets for the CLI
    """

    def create(
        self,
        name: Optional[str] = None,
        mount_path: Optional[str] = None,
        credentials_file: Optional[str] = None,
    ) -> MCLIGCPSecret:

        # Validate mount path and files
        if mount_path:
            self.validate_mount_absolute(mount_path)

        if credentials_file:
            self.validate_file_exists(credentials_file)

        base_creator = SecretCreator()
        secret = base_creator.create(SecretType.gcp, name=name)
        assert isinstance(secret, MCLIGCPSecret)

        if not credentials_file:
            credentials_file = self.fill_credentials(self.validate_file_exists)

        if not mount_path:
            mount_path = self.get_mount_path(secret.name)
        secret.mount_path = mount_path

        with open(Path(credentials_file).expanduser().absolute(), 'r', encoding='utf8') as fh:
            secret.value = fh.read()

        return secret
