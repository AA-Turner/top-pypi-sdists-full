from pydantic import SecretStr

from mistralai.workflows.core.auth.file_provider import FileTokenProvider
from mistralai.workflows.core.auth.provider import TokenProvider
from mistralai.workflows.core.auth.static_provider import StaticTokenProvider
from mistralai.workflows.core.config.config import AppConfig, config


def get_token_provider(
    explicit_key: str | SecretStr | None = None,
    *,
    app_config: AppConfig | None = None,
) -> TokenProvider | None:
    """Select the active bearer token provider for worker HTTP and the Temporal connection.

    An explicit per-service key wins (wrapped as a ``StaticTokenProvider``). Otherwise a
    service-account token path takes precedence over a static API key, so a deployment mounting an SA
    token file picks up rotation automatically -- this is also how a rotating gateway bearer is supplied:
    write the JWT to a file and point ``MISTRAL_SA_TOKEN_PATH`` at it.
    """
    if explicit_key:
        key = explicit_key.get_secret_value() if isinstance(explicit_key, SecretStr) else explicit_key
        return StaticTokenProvider(key)
    resolved_config = app_config if app_config is not None else config
    if resolved_config.common.mistral_sa_token_path:
        return FileTokenProvider(resolved_config.common.mistral_sa_token_path)
    if resolved_config.common.mistral_api_key:
        return StaticTokenProvider(resolved_config.common.mistral_api_key.get_secret_value())
    return None
