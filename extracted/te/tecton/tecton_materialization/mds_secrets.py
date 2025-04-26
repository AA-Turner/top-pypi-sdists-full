from typing import Dict

from tecton_core import http
from tecton_core.secret_management import SecretCacheKey
from tecton_core.secret_management import SecretReference
from tecton_core.secret_management import SecretResolver


class MDSSecretResolver(SecretResolver):
    """Implementation of SecretsResolver that fetches secrets from the Tecton Secret Service and caches in-memory.

    Example:
        secret_resolver = SecretResolver(secrets_api_service_url="https://example.tecton.ai", api_key="my_api_key")
        db_password = secret_resolver.resolve(SecretReference(scope="prod", key="db_password"))
    """

    def __init__(self, secrets_api_service_url: str, api_key: str) -> None:
        if not api_key:
            msg = "Tecton secrets access API key not found."
            raise RuntimeError(msg)
        self.secrets_api_service_url = secrets_api_service_url
        self.secret_cache: Dict[SecretCacheKey, str] = {}
        self._headers = {"Authorization": f"Tecton-Key {api_key}"}

    def resolve(self, secret: SecretReference) -> str:
        cache_key = SecretCacheKey(secret.scope, secret.key)
        if cache_key not in self.secret_cache:
            self.secret_cache[cache_key] = self._fetch_secret(secret.scope, secret.key)
        return self.secret_cache[cache_key]

    def _fetch_secret(self, scope: str, key: str) -> str:
        """Fetch the secret value from the Secret Manager Service via HTTP."""
        # TODO: Switch to use PureHTTPStub, which allow service proto annotation once TEC-18444 is resolved.
        api_url = f"{self.secrets_api_service_url}/v1/secrets-service/scopes/{scope}/keys/{key}"
        response = http.session().get(api_url, verify=True, headers=self._headers)

        response.raise_for_status()
        response_json = response.json()
        if "value" in response_json:
            return response_json["value"]
        else:
            msg = f"Secret value not found when resolving secret for scope: {scope}, key: {key}"
            raise KeyError(msg)
