"""Creators for ssh secrets"""
import logging
import subprocess
from pathlib import Path
from typing import Callable, Optional

from mcli.models import SecretType
from mcli.objects.secrets import MCLISSHSecret
from mcli.objects.secrets.create.base import SecretCreator, SecretValidationError
from mcli.objects.secrets.create.generic import FileSecretFiller, FileSecretValidator
from mcli.objects.secrets.ssh import MCLISFTPSSHSecret
from mcli.utils.utils_interactive import file_prompt, query_yes_no, simple_prompt
from mcli.utils.utils_logging import WARN, console
from mcli.utils.utils_string_functions import ensure_rfc1123_compatibility, validate_existing_filename

logger = logging.getLogger(__name__)


def _get_known_hosts_str(host_name: str) -> str:
    try:
        result = subprocess.run(["ssh-keyscan", host_name], capture_output=True, check=True)
        known_hosts_str = result.stdout.decode("utf-8")
        return known_hosts_str
    except subprocess.CalledProcessError as e:
        raise SecretValidationError(
            'ssh-keyscan failed. '
            'Please ensure that your hostname was spelled correctly and has an ssh port open on port 22.') from e
    except FileNotFoundError as e:
        raise SecretValidationError(
            'ssh-keyscan failed. Please ensure that you have ssh installed on your machine.') from e


class SSHSecretFiller(FileSecretFiller):
    """Interactive filler for SSH secret data
    """

    @staticmethod
    def fill_private_key(validate: Callable[[str], bool]) -> str:
        return file_prompt('Where is your private SSH key located?', validate=validate)

    @staticmethod
    def fill_sftp_host_name(validate: Callable[[str], bool]) -> str:
        return simple_prompt('What is your SFTP server host name?', validate=validate)


class SSHSecretValidator(FileSecretValidator):
    """Validation methods for SSH secret data

    Raises:
        SecretValidationError: Raised for any validation error for secret data
    """

    @staticmethod
    def validate_private_key(key_path: str) -> bool:

        if not validate_existing_filename(key_path):
            raise SecretValidationError(f'File does not exist. File path {key_path} does not exist or is not a file.')
        return True

    @staticmethod
    def validate_host_name(host_name: str) -> bool:
        if not host_name:
            raise SecretValidationError('Host name must be specified.')
        return True


class SSHSecretCreator(SSHSecretFiller, SSHSecretValidator):
    """Creates SSH secrets for the CLI
    """

    def create(self,
               name: Optional[str] = None,
               mount_path: Optional[str] = None,
               ssh_private_key: Optional[str] = None,
               git: bool = False,
               sftp: bool = False,
               host_name: Optional[str] = None,
               no_host_check: Optional[bool] = None) -> MCLISSHSecret:

        if no_host_check:
            logger.warning(
                f'{WARN} WARNING: Disabling host checking when adding SSH keys is a security risk. Use with caution.')

        # Validate mount and ssh key
        if mount_path:
            self.validate_mount_absolute(mount_path)

        if ssh_private_key:
            self.validate_private_key(ssh_private_key)

        # Fill ssh private key
        if not ssh_private_key:
            ssh_private_key = self.fill_private_key(self.validate_private_key)

        # Fill in SFTP information
        known_hosts = ''
        if sftp:
            if not host_name:
                host_name = self.fill_sftp_host_name(self.validate_host_name)

            with console.status(f'Retrieving host fingerprints for host name {host_name}...'):
                known_hosts = _get_known_hosts_str(host_name)

            # If the user specified --no-host-check then do not confirm fingerprints
            if not no_host_check:
                confirm_hosts = query_yes_no(
                    f'Found host fingerprints:\n\n{known_hosts}\nAre you sure you want to add the above hosts to '
                    f'the ssh known_hosts when running your job?')
                if not confirm_hosts:
                    raise SecretValidationError(
                        'Must confirm known hosts to configure SFTP SSH. '
                        'If the host fingerprints are not correct please contact your server administrator.')

        # Default name based on private key path
        make_name_unique = False
        if not name:
            name = ensure_rfc1123_compatibility(Path(ssh_private_key).stem)
            make_name_unique = True

        base_creator = SecretCreator()
        if git:
            secret_type = SecretType.git
        elif sftp:
            secret_type = SecretType.sftp
        else:
            secret_type = SecretType.ssh
        secret = base_creator.create(secret_type, name=name, make_name_unique=make_name_unique)
        assert isinstance(secret, MCLISSHSecret)

        if isinstance(secret, MCLISFTPSSHSecret):
            secret.known_hosts = known_hosts

        if not mount_path:
            mount_path = self.get_mount_path(secret.name)
        secret.mount_path = mount_path

        with open(Path(ssh_private_key).expanduser().absolute(), 'r', encoding='utf8') as fh:
            secret.value = fh.read()

        return secret
