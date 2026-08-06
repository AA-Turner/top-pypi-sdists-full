"""The registry PAT's own lifecycle: introspection, rotation, creation link.

Why a personal access token and not the token ``glab`` holds: the latter is an
OAuth access token whose ``/oauth/token/info`` lifetime is about 34 minutes
(``glab`` keeps renewing it with its refresh token), so writing it into a
configuration file yields an access that expires within the hour. The PyPI
index rejects it even while fresh, because it authenticates over HTTP Basic,
where GitLab only accepts a PAT, a deploy token or a job token.

Expiry is read from GitLab (``GET /personal_access_tokens/self``) rather than
stored locally, so a token revoked or rotated elsewhere is detected instead of
trusted. Rotation goes through ``POST /personal_access_tokens/self/rotate``,
which requires the ``self_rotate`` scope and **invalidates the old token** — so
every consumer must be rewritten right after (see
:mod:`pysae_ai_tools.install.registry_credential`).

The token is only ever sent as a request header: never in a URL, never logged.
"""

from dataclasses import dataclass
from datetime import date

# ``httpx`` is imported inside the two functions that call GitLab, not at module
# level: ``env/config.py`` reads this module's constants and ``creation_url``,
# which are pure, and it sits on the import path of most CLI commands. A
# top-level httpx would add roughly 250ms to every one of them.

# read_api covers the Python and npm package endpoints, read_registry the
# container registry, self_rotate the renewal below.
REQUIRED_SCOPES: tuple[str, ...] = ("read_api", "read_registry", "self_rotate")

# Name pre-filled in the creation link, so a token this CLI manages is
# recognisable in the user's GitLab settings.
TOKEN_NAME = "pysae-ai-tools-registry"

# Rotate this many days before expiry. Wide enough that a developer who runs
# the CLI weekly never hits an expired credential.
ROTATION_THRESHOLD_DAYS = 14

_TIMEOUT = 10.0


@dataclass(frozen=True)
class TokenInfo:
    """What GitLab reports about the token presented to it."""

    token_id: int
    name: str
    scopes: tuple[str, ...]
    expires_at: date | None
    active: bool
    revoked: bool

    @property
    def missing_scopes(self) -> tuple[str, ...]:
        """Recommended scopes this token lacks — a warning, never a veto.

        Each missing scope costs one capability rather than the whole credential:
        without ``read_registry`` only Docker fails, without ``self_rotate`` only
        the renewal does. (``read_api`` is not really optional — a token lacking
        it cannot even introspect itself, so it never reaches here.)
        """
        return tuple(scope for scope in REQUIRED_SCOPES if scope not in self.scopes)

    @property
    def usable(self) -> bool:
        """True when GitLab accepted the token and it is neither revoked nor expired.

        Scope breadth is deliberately not part of this: GitLab is the authority
        on what a token may do, and a service token carrying a broader scope
        (``api``) would fail a literal scope-list check while working perfectly.
        """
        return self.active and not self.revoked

    @property
    def can_rotate(self) -> bool:
        """True when the token may renew itself — rotation needs ``self_rotate``."""
        return "self_rotate" in self.scopes

    def days_left(self, today: date | None = None) -> int | None:
        """Days until expiry, or ``None`` for a non-expiring token."""
        if self.expires_at is None:
            return None
        return (self.expires_at - (today or date.today())).days

    def needs_rotation(self, today: date | None = None, threshold: int = ROTATION_THRESHOLD_DAYS) -> bool:
        remaining = self.days_left(today)
        return remaining is not None and remaining <= threshold


def creation_url(host: str, name: str = TOKEN_NAME, scopes: tuple[str, ...] = REQUIRED_SCOPES) -> str:
    """GitLab token-creation page with the name and scopes pre-filled.

    A link rather than an API call because GitLab has no self-serve endpoint
    that can mint this token. ``POST /user/personal_access_tokens`` does accept
    the OAuth token ``glab`` holds, but only grants a whitelist of scopes
    (``self_rotate``, ``k8s_proxy``); ``read_api``, ``read_registry`` and even
    ``api`` come back ``400 scopes does not have a valid value`` — including
    when the calling token itself carries ``api``. Creating the credential is
    therefore the developer's own action, which also matches the rule that they
    create and hold their own PAT.
    """
    return f"https://{host}/-/user_settings/personal_access_tokens?name={name}&scopes={','.join(scopes)}"


def _parse_expiry(raw: object) -> date | None:
    if not isinstance(raw, str) or not raw:
        return None
    try:
        return date.fromisoformat(raw[:10])
    except ValueError:
        return None


def token_info(token: str, host: str) -> TokenInfo | None:
    """Introspect ``token`` against ``host``, or ``None`` when it cannot be read.

    ``None`` covers every reason indistinguishable from the caller's point of
    view — revoked or invalid token (401), a PAT without ``read_api``, GitLab
    unreachable — all of which mean "this credential cannot be relied on".
    """
    if not token:
        return None

    import httpx

    try:
        response = httpx.get(
            f"https://{host}/api/v4/personal_access_tokens/self",
            headers={"PRIVATE-TOKEN": token},
            timeout=_TIMEOUT,
            follow_redirects=True,
        )
    except httpx.HTTPError:
        return None
    if response.status_code != httpx.codes.OK:
        return None
    try:
        data = response.json()
    except ValueError:
        return None
    if not isinstance(data, dict):
        return None

    raw_scopes = data.get("scopes")
    scopes = tuple(str(s) for s in raw_scopes) if isinstance(raw_scopes, list) else ()
    return TokenInfo(
        token_id=int(data.get("id") or 0),
        name=str(data.get("name") or ""),
        scopes=scopes,
        expires_at=_parse_expiry(data.get("expires_at")),
        active=bool(data.get("active", True)),
        revoked=bool(data.get("revoked", False)),
    )


def rotate(token: str, host: str) -> str | None:
    """Rotate ``token`` and return its replacement, or ``None`` on failure.

    The old token stops working the moment this succeeds, so the caller owns
    re-applying the returned value everywhere it was posed.
    """
    if not token:
        return None

    import httpx

    try:
        response = httpx.post(
            f"https://{host}/api/v4/personal_access_tokens/self/rotate",
            headers={"PRIVATE-TOKEN": token},
            timeout=_TIMEOUT,
            follow_redirects=True,
        )
    except httpx.HTTPError:
        return None
    if response.status_code not in (httpx.codes.OK, httpx.codes.CREATED):
        return None
    try:
        data = response.json()
    except ValueError:
        return None
    if not isinstance(data, dict):
        return None
    rotated = data.get("token")
    return str(rotated) if isinstance(rotated, str) and rotated else None
