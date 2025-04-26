""" MCLI Mounted Secret """
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Optional, Type

from mcli.models import MCLIGenericSecret, SecretType
from mcli.models.mcli_secret import SECRET_MOUNT_PATH_PARENT


@dataclass
class MCLIMountedSecret(MCLIGenericSecret):
    """Secret class for generic secrets that will be mounted to run pods as files
    """
    mount_path: Optional[str] = None

    def __post_init__(self):
        if self.mount_path is None:
            self.mount_path = str(SECRET_MOUNT_PATH_PARENT / self.name)

    @property
    def mapi_data(self) -> Dict[str, Any]:
        return {
            'mountedSecret': {
                'name': self.name,
                'metadata': {
                    'mountPath': self.mount_path
                },
                'value': self.value,
            },
        }

    @classmethod
    def from_generic_secret(
        cls: Type[MCLIMountedSecret],
        generic_secret: MCLIGenericSecret,
        mount_path: Optional[str] = None,
    ) -> MCLIMountedSecret:
        return cls(
            name=generic_secret.name,
            value=generic_secret.value,
            secret_type=SecretType.mounted,
            mount_path=mount_path,
        )
