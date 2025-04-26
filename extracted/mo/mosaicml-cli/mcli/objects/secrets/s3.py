""" S3 Credentials Secret Type """
from dataclasses import dataclass
from typing import Any, Dict, Optional

from mcli.models import Secret
from mcli.models.mcli_secret import SECRET_MOUNT_PATH_PARENT


@dataclass
class MCLIS3Secret(Secret):
    """Secret class for AWS credentials
    """
    mount_directory: Optional[str] = None
    credentials: Optional[str] = None
    config: Optional[str] = None
    profile: Optional[str] = None

    def __post_init__(self):
        if self.mount_directory is None:
            self.mount_directory = str(SECRET_MOUNT_PATH_PARENT / self.name)

    @property
    def mapi_data(self) -> Dict[str, Any]:
        value = {'config': self.config, 'credentials': self.credentials}
        if self.profile:
            value['profile'] = self.profile

        return {
            's3Secret': {
                'name': self.name,
                'metadata': {
                    'mountDirectory': self.mount_directory
                },
                'value': value,
            }
        }
