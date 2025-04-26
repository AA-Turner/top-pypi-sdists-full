""" GCP Credentials Secret Type """
from dataclasses import dataclass
from typing import Any, Dict

from mcli.objects.secrets.mounted import MCLIMountedSecret


@dataclass
class MCLIGCPSecret(MCLIMountedSecret):
    """Secret class for GCP credentials
    """

    @property
    def mapi_data(self) -> Dict[str, Any]:
        return {
            'gcpSecret': {
                'name': self.name,
                'metadata': {
                    'mountPath': self.mount_path
                },
                'value': self.value,
            }
        }
