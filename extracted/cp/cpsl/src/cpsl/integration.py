"""Integration declarations for Capsule apps.

Integrations are user-facing connections declared at the app level via
``app.add_integration()``. Three modes:

- **OAuth** (``gmail``, ``github``, …): user completes an OAuth redirect.
- **Secret** (``tailscale``, ``aws``, …): user submits credentials via a form.
- **Pipedream**: user connects any supported Pipedream app; Capsule stores the
  Pipedream account reference and app code uses its own client.

At runtime, credentials are available on ``session.integrations``. For
scheduled handlers and background tasks without an explicit session
parameter, use ``cpsl.current_session()`` to access the active runtime
session and its integrations.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Union

from .secret import Secret


# ---------------------------------------------------------------------------
# OAuth integration types
# ---------------------------------------------------------------------------

INTEGRATION_GOOGLE = "google"
INTEGRATION_GMAIL = "gmail"
INTEGRATION_GCAL = "gcal"
INTEGRATION_GDRIVE = "gdrive"
INTEGRATION_OUTLOOK = "outlook"
INTEGRATION_GITHUB = "github"
INTEGRATION_LINEAR = "linear"

# ---------------------------------------------------------------------------
# Secret-based integration types and their field schemas
# ---------------------------------------------------------------------------

INTEGRATION_TAILSCALE = "tailscale"
INTEGRATION_AWS = "aws"

KNOWN_SECRET_INTEGRATIONS: dict[str, list[str]] = {
    INTEGRATION_TAILSCALE: ["auth_key"],
    INTEGRATION_AWS: ["access_key_id", "secret_access_key", "region"],
}

MODE_OAUTH = "oauth"
MODE_SECRET = "secret"
MODE_PIPEDREAM = "pipedream"


class Integration(str, Enum):
    """Built-in integration type names.

    Values match the wire-format strings used by the Capsule API.
    """

    GOOGLE = INTEGRATION_GOOGLE
    GMAIL = INTEGRATION_GMAIL
    GCAL = INTEGRATION_GCAL
    GDRIVE = INTEGRATION_GDRIVE
    OUTLOOK = INTEGRATION_OUTLOOK
    GITHUB = INTEGRATION_GITHUB
    LINEAR = INTEGRATION_LINEAR
    TAILSCALE = INTEGRATION_TAILSCALE
    AWS = INTEGRATION_AWS


def integration_type(value: object) -> str:
    """Return the wire-format integration type for enum/config/string input."""
    if isinstance(value, IntegrationConfig):
        return value.type
    if isinstance(value, Integration):
        return value.value
    return str(value)


@dataclass
class IntegrationConfig:
    """Describes an integration the app requires from end users.

    For OAuth integrations supply ``client_id`` / ``client_secret``.
    For secret-based integrations (Tailscale, AWS, or custom) just pass the
    type name — fields are inferred — or supply ``fields`` explicitly.
    For Pipedream-backed integrations use :func:`Pipedream`.
    """

    type: str | Integration
    client_id: Union[str, Secret] = ""
    client_secret: Union[str, Secret] = ""
    scopes: list[str] = field(default_factory=list)
    fields: list[str] | None = None
    mode: str = ""

    def __post_init__(self) -> None:
        self.type = integration_type(self.type)
        if not self.mode:
            if self.fields or self.type in KNOWN_SECRET_INTEGRATIONS:
                self.mode = MODE_SECRET
            else:
                self.mode = MODE_OAUTH
        if self.mode == MODE_SECRET and self.fields is None:
            self.fields = list(KNOWN_SECRET_INTEGRATIONS.get(self.type, []))

    def to_dict(self) -> dict:
        cid = self.client_id
        cs = self.client_secret
        d: dict = {
            "type": self.type,
            "mode": self.mode,
        }
        if self.mode == MODE_OAUTH:
            d["scopes"] = list(self.scopes)
            d["client_id_secret"] = cid._name if isinstance(cid, Secret) else cid
            d["client_secret_secret"] = cs._name if isinstance(cs, Secret) else cs
        else:
            d["fields"] = list(self.fields or [])
        return d


IntegrationLike = Union[str, Integration, IntegrationConfig]


def _oauth_config(
    integration: Integration,
    *,
    client_id: Union[str, Secret],
    client_secret: Union[str, Secret],
    scopes: list[str] | None = None,
) -> IntegrationConfig:
    return IntegrationConfig(
        type=integration,
        client_id=client_id,
        client_secret=client_secret,
        scopes=scopes or [],
        mode=MODE_OAUTH,
    )


def Google(
    *,
    client_id: Union[str, Secret],
    client_secret: Union[str, Secret],
    scopes: list[str] | None = None,
) -> IntegrationConfig:
    return _oauth_config(
        Integration.GOOGLE, client_id=client_id, client_secret=client_secret, scopes=scopes
    )


def Gmail(
    *,
    client_id: Union[str, Secret],
    client_secret: Union[str, Secret],
    scopes: list[str] | None = None,
) -> IntegrationConfig:
    return _oauth_config(
        Integration.GMAIL, client_id=client_id, client_secret=client_secret, scopes=scopes
    )


def GoogleCalendar(
    *,
    client_id: Union[str, Secret],
    client_secret: Union[str, Secret],
    scopes: list[str] | None = None,
) -> IntegrationConfig:
    return _oauth_config(
        Integration.GCAL, client_id=client_id, client_secret=client_secret, scopes=scopes
    )


def GoogleDrive(
    *,
    client_id: Union[str, Secret],
    client_secret: Union[str, Secret],
    scopes: list[str] | None = None,
) -> IntegrationConfig:
    return _oauth_config(
        Integration.GDRIVE, client_id=client_id, client_secret=client_secret, scopes=scopes
    )


def Outlook(
    *,
    client_id: Union[str, Secret],
    client_secret: Union[str, Secret],
    scopes: list[str] | None = None,
) -> IntegrationConfig:
    resolved_scopes = list(scopes or [])
    if "offline_access" not in resolved_scopes:
        resolved_scopes.append("offline_access")
    return _oauth_config(
        Integration.OUTLOOK,
        client_id=client_id,
        client_secret=client_secret,
        scopes=resolved_scopes,
    )


def GitHub(
    *,
    client_id: Union[str, Secret],
    client_secret: Union[str, Secret],
    scopes: list[str] | None = None,
) -> IntegrationConfig:
    return _oauth_config(
        Integration.GITHUB, client_id=client_id, client_secret=client_secret, scopes=scopes
    )


def Linear(
    *,
    client_id: Union[str, Secret],
    client_secret: Union[str, Secret],
    scopes: list[str] | None = None,
) -> IntegrationConfig:
    return _oauth_config(
        Integration.LINEAR, client_id=client_id, client_secret=client_secret, scopes=scopes
    )


def Tailscale() -> IntegrationConfig:
    return IntegrationConfig(type=Integration.TAILSCALE, mode=MODE_SECRET)


def AWS() -> IntegrationConfig:
    return IntegrationConfig(type=Integration.AWS, mode=MODE_SECRET)


def Pipedream(
    app_slug: str,
    *,
    client_id: Union[str, Secret] = "",
    client_secret: Union[str, Secret] = "",
    project_id: Union[str, Secret] = "",
    environment: str = "development",
    api_base_url: str = "",
) -> IntegrationConfig:
    """Declare a Pipedream-managed account connection.

    ``app_slug`` must match Pipedream's app ``name_slug`` (for example
    ``gmail``, ``slack``, or ``google_sheets``). Capsule handles the end-user
    Connect flow and exposes Pipedream account metadata at runtime via
    ``session.integrations[app_slug].fields``.

    By default Capsule can use platform-managed Pipedream credentials. To bring
    your own Pipedream project, pass ``client_id``, ``client_secret``, and
    ``project_id`` as workspace secrets.
    """
    if not app_slug or not str(app_slug).strip():
        raise ValueError("Pipedream app slug must not be empty")
    has_byo = bool(client_id or client_secret or project_id)
    if has_byo and not (client_id and client_secret and project_id):
        raise ValueError(
            "Pipedream BYO config requires client_id, client_secret, and project_id"
        )
    fields: list[str] = []
    if project_id:
        project_secret = project_id._name if isinstance(project_id, Secret) else str(project_id)
        fields.append(f"project_id_secret:{project_secret}")
    if environment:
        fields.append(f"environment:{environment}")
    if api_base_url:
        fields.append(f"api_base_url:{api_base_url}")
    return IntegrationConfig(
        type=str(app_slug).strip(),
        client_id=client_id,
        client_secret=client_secret,
        fields=fields,
        mode=MODE_PIPEDREAM,
    )


@dataclass
class IntegrationCredentials:
    """Decrypted credentials provided on the session at runtime.

    For OAuth integrations ``access_token`` contains the bearer token.
    For secret-based integrations ``fields`` holds the submitted values
    and ``access_token`` is empty.
    """

    access_token: str = ""
    token_type: str = "Bearer"
    scopes: list[str] = field(default_factory=list)
    expires_at: int = 0
    fields: dict[str, str] = field(default_factory=dict)

    def __bool__(self) -> bool:
        return bool(self.access_token or self.fields)
