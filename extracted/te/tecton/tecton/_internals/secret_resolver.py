from typing import Dict

from tecton._internals import metadata_service
from tecton_core.errors import TectonNotFoundError
from tecton_core.secret_management import SecretCacheKey
from tecton_core.secret_management import SecretResolver
from tecton_proto.common.secret__client_pb2 import SecretReference
from tecton_proto.secrets.secrets_service__client_pb2 import GetSecretValueRequest


# Singleton local secret store for Notebook development
_local_secret_store: Dict[SecretCacheKey, str] = {}


def set_local_secret(scope: str, key: str, value: str) -> None:
    """Set the secret in Local Secret Store singleton instance."""
    _local_secret_store[SecretCacheKey(scope, key)] = value


class LocalDevSecretResolver(SecretResolver):
    """Secret Resolver for local development. Secrets are retrieved from Secret Service or locally specified values.

    Example:
        db_password = LocalDevSecretResolver().resolve(SecretReference(scope="prod", key="db_password"))
    """

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)  # pylint: disable=no-value-for-parameter
        return cls._instance

    def resolve(self, secret: SecretReference) -> str:
        if secret.is_local:
            return self._fetch_local_secret(secret.scope, secret.key)
        return self._fetch_mds_secret(secret.scope, secret.key)

    @staticmethod
    def _fetch_mds_secret(scope: str, key: str) -> str:
        try:
            request = GetSecretValueRequest(scope=scope, key=key)
            response = metadata_service.instance().GetSecretValue(request)
            return response.value
        except TectonNotFoundError:
            msg = f"Failed to get secret `{key}` in scope `{scope}`. Please check if the secret scope or key exists."
            raise RuntimeError(msg)
        except Exception as e:
            msg = f"Failed to get secret `{key}` in scope `{scope}` with {e}"
            raise RuntimeError(msg)

    @staticmethod
    def _fetch_local_secret(scope: str, key: str) -> str:
        return _local_secret_store[SecretCacheKey(scope, key)]
