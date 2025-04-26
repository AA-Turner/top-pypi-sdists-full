""" Creates an EnvVar Secret """
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Optional, Type

from mcli.models import MCLIGenericSecret, SecretType


@dataclass
class MCLIEnvVarSecret(MCLIGenericSecret):
    """Secret class for generic secrets that will be added as environment variables
    """
    key: Optional[str] = None

    @property
    def mapi_data(self) -> Dict[str, Any]:
        return {
            'envVarSecret': {
                'name': self.name,
                'metadata': {
                    'key': self.key
                },
                'value': self.value,
            },
        }

    @classmethod
    def from_generic_secret(
        cls: Type[MCLIEnvVarSecret],
        generic_secret: MCLIGenericSecret,
        key: str,
    ) -> MCLIEnvVarSecret:
        return cls(
            name=generic_secret.name,
            value=generic_secret.value,
            secret_type=SecretType.environment,
            key=key,
        )


@dataclass
class HuggingFaceSecret(MCLIEnvVarSecret):
    token: Optional[str] = None
    key: Optional[str] = "HF_TOKEN"

    @property
    def mapi_data(self) -> Dict[str, Any]:
        self.value = self.token
        return super().mapi_data
