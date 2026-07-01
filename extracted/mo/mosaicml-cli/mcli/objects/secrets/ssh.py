""" SSH Secret Type """
from dataclasses import dataclass
from typing import Any, Dict, Optional

from mcli.objects.secrets.mounted import MCLIMountedSecret


@dataclass
class MCLISSHSecret(MCLIMountedSecret):
    """Secret class for ssh private keys that will be mounted to run pods as a file
    """

    @property
    def mapi_data(self) -> Dict[str, Any]:
        return {
            'sshSecret': {
                'name': self.name,
                'metadata': {
                    'mountPath': self.mount_path,
                },
                'value': self.value,
            },
        }


@dataclass
class MCLIGitSSHSecret(MCLISSHSecret):
    """Secret class for git-related ssh private keys

    The ssh key will be mounted to a file and the environment variable GIT_SSH_COMMAND
    will be pointed toward it
    """

    @property
    def mapi_data(self) -> Dict[str, Any]:
        return {
            'gitSSHSecret': {
                'name': self.name,
                'metadata': {
                    'mountPath': self.mount_path,
                },
                'value': self.value,
            },
        }


@dataclass
class MCLISFTPSSHSecret(MCLISSHSecret):
    """Secret class for sftp-related ssh private keys

    The sftp ssh key will be mounted to a file and the environment variable COMPOSER_SFTP_KEY_FILE
    will be pointed toward it
    """

    known_hosts: Optional[str] = None

    @property
    def mapi_data(self) -> Dict[str, Any]:
        return {
            'sftpSSHSecret': {
                'name': self.name,
                'metadata': {
                    'mountPath': self.mount_path,
                },
                'value': self.value,
            },
        }
