"""Creators for OCI secrets"""
import configparser
import os
import tempfile
from pathlib import Path
from typing import Callable, Optional

from mcli.models import SecretType
from mcli.objects.secrets import MCLIOCISecret
from mcli.objects.secrets.create.base import SecretCreator, SecretValidationError
from mcli.objects.secrets.create.generic import FileSecretFiller, FileSecretValidator
from mcli.utils.utils_interactive import file_prompt
from mcli.utils.utils_string_functions import validate_existing_filename


class OCISecretFiller(FileSecretFiller):
    """Interactive filler for OCI secrets
    """

    @staticmethod
    def fill_file(prompt: str, validate: Callable[[str], bool]) -> str:
        return file_prompt(prompt, validate=validate)

    @classmethod
    def fill_config(cls, validate: Callable[[str], bool]) -> str:
        return cls.fill_file(
            'Where is your OCI config file located?',
            validate,
        )

    @classmethod
    def fill_key_file(cls, validate: Callable[[str], bool]) -> str:
        return cls.fill_file(
            'Where is your OCI API key file located?',
            validate,
        )


class OCISecretValidator(FileSecretValidator):
    """Validation class for OCI secret files

    Raises:
        SecretValidationError: Raised for any validation error for secret data
    """

    @staticmethod
    def validate_file_exists(path: str) -> bool:
        if not validate_existing_filename(path):
            raise SecretValidationError(f'File does not exist. File path {path} does not exist or is not a file.')
        return True


class OCISecretCreator(OCISecretFiller, OCISecretValidator):
    """Creates OCI secrets for the CLI.
    """

    def create(self,
               name: Optional[str] = None,
               mount_directory: Optional[str] = None,
               key_file: Optional[str] = None,
               config_file: Optional[str] = None) -> MCLIOCISecret:

        # Validate mount directory and files
        if mount_directory:
            self.validate_mount_absolute(mount_directory)

        if key_file:
            self.validate_file_exists(key_file)

        if config_file:
            self.validate_file_exists(config_file)

        base_creator = SecretCreator()
        secret = base_creator.create(SecretType.oci, name=name)
        assert isinstance(secret, MCLIOCISecret)

        if not config_file:
            config_file = self.fill_config(self.validate_file_exists)

        if not key_file:
            key_file = self.fill_key_file(self.validate_file_exists)

        if not mount_directory:
            mount_directory = self.get_mount_path(secret.name)
        secret.mount_directory = mount_directory

        oci_config_parser = configparser.ConfigParser()
        try:
            oci_config_parser.read(Path(config_file).expanduser().absolute(), encoding='utf8')
        except Exception as ex:
            raise SecretValidationError(
                f"Configparser couldn't read the config file. Please ensure {config_file} is a valid OCI config file."
            ) from ex

        default_kw = oci_config_parser.default_section
        #TODO HEK-1930 loop through all parts of config and set key path not just default section
        if 'key_file' in oci_config_parser[default_kw]:
            oci_config_parser[default_kw]['key_file'] = f'{secret.mount_directory}/key_file'

        tmp_fd, tmp_path = tempfile.mkstemp()
        try:
            with os.fdopen(tmp_fd, 'w') as tmp:
                oci_config_parser.write(tmp)
            with open(tmp_path, 'r', encoding='utf-8') as cf:
                secret.config = cf.read()
        finally:
            os.remove(tmp_path)

        with open(Path(key_file).expanduser().absolute(), 'r', encoding='utf8') as fh:
            secret.key_file = fh.read()

        return secret
