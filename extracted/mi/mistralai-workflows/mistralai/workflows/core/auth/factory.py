from pydantic import SecretStr

from mistralai.workflows.core.auth.file_provider import FileTokenProvider
from mistralai.workflows.core.auth.provider import TokenProvider
from mistralai.workflows.core.auth.static_provider import StaticTokenProvider
from mistralai.workflows.core.config.config import config


def get_token_provider(explicit_key: str | SecretStr | None = None) -> TokenProvider | None:
    """Select the active token provider.

    An explicit per-service key wins (wrapped as a ``StaticTokenProvider``). Otherwise a
    service-account token path takes precedence over a static API key so that deployments mounting
    an SA token automatically pick up rotation.
    """
    if explicit_key:
        key = explicit_key.get_secret_value() if isinstance(explicit_key, SecretStr) else explicit_key
        return StaticTokenProvider(key)
    if config.common.mistral_sa_token_path:
        return FileTokenProvider(config.common.mistral_sa_token_path)
    if config.common.mistral_api_key:
        return StaticTokenProvider(config.common.mistral_api_key.get_secret_value())
    return None
