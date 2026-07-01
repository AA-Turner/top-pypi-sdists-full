""" Docker Registry Secret Type """
from dataclasses import dataclass
from typing import Any, Dict, Optional

from mcli.models import Secret


@dataclass
class MCLIDockerRegistrySecret(Secret):
    """Secret class for docker image pull secrets
    """
    username: Optional[str] = None
    password: Optional[str] = None
    email: Optional[str] = None
    server: Optional[str] = None

    @property
    def mapi_data(self) -> Dict[str, Any]:
        return {
            'dockerRegistrySecret': {
                'name': self.name,
                'value': {
                    'username': self.username,
                    'password': self.password,
                    'email': self.email,
                    'server': self.server,
                }
            },
        }
