"""Creators for s3 secrets"""
import configparser
from pathlib import Path
from typing import Callable, List, Optional

from mcli.models import SecretType
from mcli.objects.secrets import MCLIS3Secret
from mcli.objects.secrets.create.base import SecretCreator, SecretValidationError
from mcli.objects.secrets.create.generic import FileSecretFiller, FileSecretValidator
from mcli.utils.utils_interactive import choose_one, file_prompt
from mcli.utils.utils_string_functions import validate_existing_filename


class S3SecretFiller(FileSecretFiller):
    """Interactive filler for s3 secret data
    """

    @staticmethod
    def fill_file(prompt: str, validate: Callable[[str], bool]) -> str:
        return file_prompt(prompt, validate=validate)

    @classmethod
    def fill_config(cls, validate: Callable[[str], bool]) -> str:
        return cls.fill_file(
            'Where is your S3 config file located?',
            validate,
        )

    @classmethod
    def fill_credentials(cls, validate: Callable[[str], bool]) -> str:
        return cls.fill_file(
            'Where is your S3 credentials file located?',
            validate,
        )


class S3SecretValidator(FileSecretValidator):
    """Validation methods for secret data

    Raises:
        SecretValidationError: Raised for any validation error for secret data
    """

    @staticmethod
    def validate_file_exists(path: str) -> bool:

        if not validate_existing_filename(path):
            raise SecretValidationError(f'File does not exist. File path {path} does not exist or is not a file.')
        return True


class S3SecretCreator(S3SecretFiller, S3SecretValidator):
    """Creates s3 secrets for the CLI
    """

    def create(self,
               name: Optional[str] = None,
               mount_directory: Optional[str] = None,
               credentials_file: Optional[str] = None,
               config_file: Optional[str] = None,
               profile: Optional[str] = None) -> MCLIS3Secret:

        # Validate mount directory and files
        if mount_directory:
            self.validate_mount_absolute(mount_directory)

        if credentials_file:
            self.validate_file_exists(credentials_file)

        if config_file:
            self.validate_file_exists(config_file)

        base_creator = SecretCreator()
        secret = base_creator.create(SecretType.s3, name=name)
        assert isinstance(secret, MCLIS3Secret)

        if not config_file:
            config_file = self.fill_config(self.validate_file_exists)

        if not credentials_file:
            credentials_file = self.fill_credentials(self.validate_file_exists)

        if not mount_directory:
            mount_directory = self.get_mount_path(secret.name)
        secret.mount_directory = mount_directory

        with open(Path(config_file).expanduser().absolute(), 'r', encoding='utf8') as fh:
            secret.config = fh.read()

        with open(Path(credentials_file).expanduser().absolute(), 'r', encoding='utf8') as fh:
            secret.credentials = fh.read()
            profiles = self._parse_aws_profiles(secret.credentials)

        if not profiles:
            raise SecretValidationError('No profiles found in the config file')

        if profile and profile not in profiles:
            profile_list = ', '.join(profiles)
            raise SecretValidationError(
                f'Profile "{profile}" does not exist in the profiles in s3 config, please choose among: {profile_list}')

        if not profile:
            # Fill in value for profile
            if len(profiles) == 1:
                profile = profiles[0]
            elif "default" in profiles:
                profile = "default"
            else:
                profile = choose_one(
                    f'Profile "{profile}" does not exist in the profiles in s3 config, please choose among:', profiles)
        secret.profile = profile

        return secret

    def _parse_aws_profiles(self, credentials: str) -> List[str]:
        """Parse the aws config file and return the set of profiles in the config file"""
        parser = configparser.ConfigParser()
        parser.read_string(credentials)

        # return the set of aws profiles in the config file
        return parser.sections()
