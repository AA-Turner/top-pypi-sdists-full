"""Per-environment Auth0/API configuration for the Pysae API client.

Two Pysae environments are supported: ``dev`` and ``prod``. The Auth0 domain
and API audience are stable, public values (mirrored from the front-end
``op`` config and the ``infra-cluster`` Terraform). The **OAuth client id**
is the only piece that is not known ahead of time: it belongs to the
dedicated ``pysae-ai-tools`` Auth0 native client created in
``infra-cluster/modules/auth0`` and is minted at ``terraform apply`` time.

Client-id resolution order (first hit wins):

1. ``--client-id`` passed explicitly on the command line.
2. Environment variable ``PYSAE_API_CLIENT_ID_DEV`` / ``PYSAE_API_CLIENT_ID_PROD``
   (or the generic ``PYSAE_API_CLIENT_ID``).
3. The persisted config file ``pysae-api.json`` (written by ``auth configure``).
4. The baked-in default below (empty until the client is provisioned).
"""

import json
import os
from dataclasses import dataclass

from ....config import CONFIG_DIR, DATA_DIR

CONFIG_PATH = CONFIG_DIR / "pysae-api.json"
# The client id is config; the token set is persistent auth state (rotating refresh token) → data dir.
TOKENS_PATH = DATA_DIR / "pysae-api-tokens.json"

# OAuth scope requested at login. ``offline_access`` is what yields a refresh
# token; the resource server enables it (``allow_offline_access = true``).
OAUTH_SCOPE = "openid profile email offline_access"

# Local redirect ports tried in order for the authorization-code (PKCE) flow.
# These MUST match the ``callbacks`` registered on the Auth0 client in
# ``infra-cluster/modules/auth0/main.tf`` (path ``/callback``).
CALLBACK_PORTS = (8765, 8766, 8767)
CALLBACK_PATH = "/callback"


@dataclass(frozen=True)
class Auth0Env:
    """Stable, public configuration for one Pysae environment."""

    name: str
    api_base: str
    auth0_domain: str
    audience: str
    default_client_id: str

    @property
    def token_endpoint(self) -> str:
        return f"https://{self.auth0_domain}/oauth/token"

    @property
    def authorize_endpoint(self) -> str:
        return f"https://{self.auth0_domain}/authorize"

    @property
    def device_endpoint(self) -> str:
        return f"https://{self.auth0_domain}/oauth/device/code"

    @property
    def logout_endpoint(self) -> str:
        return f"https://{self.auth0_domain}/v2/logout"


ENVS: dict[str, Auth0Env] = {
    "dev": Auth0Env(
        name="dev",
        api_base="https://api.dev.pysae.com",
        auth0_domain="auth.dev.pysae.com",
        audience="https://dev.pysae.com/api",
        # Public client id of the `pysae-ai-tools` Auth0 native client (dev
        # tenant). Public identifier, not a secret — same nature as the `op`
        # SPA clientId shipped in the front-end bundle.
        default_client_id="K5HJsjKsCkLP2491leOQuUBqk9XbvYTo",
    ),
    "prod": Auth0Env(
        name="prod",
        api_base="https://api.pysae.com",
        auth0_domain="auth.pysae.com",
        audience="https://pysae.com/api",
        # Public client id of the `pysae-ai-tools` Auth0 native client (prod
        # tenant). Public identifier, not a secret.
        default_client_id="0BxBIcouT4q2lKpjhxwkEgNbL9rQGlTA",
    ),
}


def get_env(name: str) -> Auth0Env:
    """Return the :class:`Auth0Env` for ``name`` or raise ``KeyError``-style error."""
    try:
        return ENVS[name]
    except KeyError:
        raise ValueError(f"unknown environment '{name}' (expected one of: {', '.join(ENVS)})") from None


def _load_config() -> dict[str, dict[str, str]]:
    try:
        raw = CONFIG_PATH.read_text(encoding="utf-8")
    except (FileNotFoundError, OSError):
        return {}
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        return {}
    if not isinstance(data, dict):
        return {}
    return data


def _save_config(data: dict[str, dict[str, str]]) -> None:
    CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
    fd = os.open(CONFIG_PATH, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    with os.fdopen(fd, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, sort_keys=True)


def set_client_id(env: str, client_id: str) -> None:
    """Persist the OAuth client id for ``env`` to the config file."""
    data = _load_config()
    data.setdefault(env, {})["client_id"] = client_id
    _save_config(data)


def resolve_client_id(env: Auth0Env, override: str | None = None) -> str:
    """Resolve the OAuth client id for ``env`` following the documented order.

    Raises ``RuntimeError`` with actionable guidance when no client id can be
    found — typically because the Terraform client has not been applied yet,
    or its id has not been configured locally.
    """
    if override:
        return override

    per_env = os.environ.get(f"PYSAE_API_CLIENT_ID_{env.name.upper()}")
    if per_env:
        return per_env
    generic = os.environ.get("PYSAE_API_CLIENT_ID")
    if generic:
        return generic

    persisted = _load_config().get(env.name, {}).get("client_id")
    if persisted:
        return persisted

    if env.default_client_id:
        return env.default_client_id

    raise RuntimeError(
        f"no Auth0 client id configured for env '{env.name}'.\n"
        "The dedicated `pysae-ai-tools` Auth0 client lives in "
        "infra-cluster/modules/auth0. Once it is applied, grab its id from the "
        "Terraform `client_ids` output and run:\n"
        f"  pysae-ai-tools pysae api auth configure --env {env.name} --client-id <CLIENT_ID>\n"
        f"or set PYSAE_API_CLIENT_ID_{env.name.upper()}."
    )
