"""OCI Credentials Secret Type"""
from dataclasses import dataclass
from typing import Any, Dict, Optional

from mcli.models import Secret
from mcli.models.mcli_secret import SECRET_MOUNT_PATH_PARENT


@dataclass
class MCLIOCISecret(Secret):
    """
    Secret class for OCI config and pem filew.
    """
    mount_directory: Optional[str] = None
    key_file: Optional[str] = None
    config: Optional[str] = None

    def __post_init__(self):
        if self.mount_directory is None:
            self.mount_directory = str(SECRET_MOUNT_PATH_PARENT / self.name)

    @property
    def mapi_data(self) -> Dict[str, Any]:
        return {
            'ociSecret': {
                'name': self.name,
                'metadata': {
                    'mountDirectory': self.mount_directory
                },
                'value': {
                    'config': self.config,
                    'keyFile': self.key_file,
                },
            }
        }
