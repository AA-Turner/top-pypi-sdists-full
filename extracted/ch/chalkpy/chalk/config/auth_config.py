from __future__ import annotations

import os
from functools import lru_cache
from pathlib import Path
from typing import TYPE_CHECKING, Mapping, Optional

import yaml

if TYPE_CHECKING:
    from pydantic import BaseModel
else:
    try:
        from pydantic.v1 import BaseModel
    except ImportError:
        from pydantic import BaseModel

from chalk.config.project_config import load_project_config
from chalk.utils.log_with_context import get_logger

_logger = get_logger(__name__)


class TokenConfig(BaseModel):
    name: Optional[str] = None
    clientId: str
    clientSecret: str
    apiServer: Optional[str] = None
    activeEnvironment: Optional[str] = None


class AuthConfig(BaseModel):
    tokens: Optional[Mapping[str, TokenConfig]]


def _load_global_config_uncached() -> AuthConfig | None:
    path = None
    p = os.path.join(os.getenv("XDG_CONFIG_HOME", os.path.expanduser("~")), ".chalk.yml")
    if os.path.exists(p):
        path = p

    if path is None:
        return None

    with open(path, "r") as f:
        parsed = yaml.safe_load(f)
        return AuthConfig(**parsed)


# using lru_cache for 3.8 compat
@lru_cache(maxsize=None)
def _load_global_config() -> AuthConfig | None:
    return _load_global_config_uncached()


def _en(current_env_name: str, old_env_name: str | None = None) -> str | None:
    old_env_name = old_env_name or f"_{current_env_name}"
    # Backwards compatability for old env vars.
    deprecated = os.getenv(old_env_name)
    current = os.getenv(current_env_name)
    if deprecated and current:
        _logger.warning(
            f"Using both deprecated '{old_env_name}' and new '{current_env_name}' environment variables. Choosing '{current_env_name}'"
        )
    return current or deprecated


def load_token(
    client_id: Optional[str],
    client_secret: Optional[str],
    active_environment: Optional[str],
    api_server: Optional[str],
    skip_cache: bool = False,
) -> TokenConfig | None:
    token_name = "Explicit" if client_id and client_secret else "Environment"

    client_id = client_id or _en("CHALK_CLIENT_ID")
    client_secret = client_secret or _en("CHALK_CLIENT_SECRET")
    api_server = api_server or _en("CHALK_API_SERVER")
    active_environment = active_environment or _en("CHALK_ENVIRONMENT", "_CHALK_ACTIVE_ENVIRONMENT")

    if client_id is not None and client_secret is not None:
        return TokenConfig(
            name=token_name,
            clientId=client_id,
            clientSecret=client_secret,
            apiServer=api_server or "https://api.chalk.ai",
            activeEnvironment=active_environment,
        )

    global_cfg = _load_global_config_uncached() if skip_cache else _load_global_config()
    if global_cfg is None:
        return None

    absdir = Path(os.getcwd()).absolute().resolve()
    project_config = load_project_config()
    if project_config:
        absdir = Path(project_config.local_path).parent
    tokens: Mapping[str, TokenConfig] = global_cfg.tokens or {}
    token_config = tokens.get(str(absdir)) or tokens.get("default")
    if token_config is None:
        return None

    return TokenConfig(
        name=token_config.name,
        clientId=client_id or token_config.clientId,
        clientSecret=client_secret or token_config.clientSecret,
        apiServer=api_server or token_config.apiServer or "https://api.chalk.ai",
        activeEnvironment=active_environment or token_config.activeEnvironment,
    )
