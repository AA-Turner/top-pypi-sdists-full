"""Models for `plato vault app`: a vendor OAuth app and its grant, kept per vault account.

One record holds ONE grant for every kind it lists (``api``, ``mcp``): Canva refresh tokens work one
time only, and a second use of a spent refresh token can revoke the whole grant.
Secrets are ``SecretStr``. Only the store reveals them, with ``context={"reveal": True}``.
Commands print only :class:`AppCredentialsPresence` (prefixes and lengths).
"""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
from enum import StrEnum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, SecretStr, SerializationInfo, field_serializer

from plato.cli.vault.prompts import GoalTemplate
from plato.cli.vault.sign_in_models import CANVA_SIGN_IN, SignInRecipe

# How much of a value `show` prints: enough to tell `cnv...` from `eyJ...`.
SECRET_PREFIX_LEN = 3
CLIENT_ID_PREFIX_LEN = 5


class AppVendor(StrEnum):
    canva = "canva"


class CredentialKind(StrEnum):
    """What a grant serves: the vendor's REST API, or its remote MCP server."""

    api = "api"
    mcp = "mcp"


class ClientAuth(StrEnum):
    """How the token call sends the client secret (RFC 6749 2.3.1)."""

    basic = "client_secret_basic"
    post = "client_secret_post"


class PkceMethod(StrEnum):
    """RFC 7636 code challenge methods. Only S256: ``plain`` sends the verifier itself."""

    s256 = "S256"


class ConsentBrowser(StrEnum):
    """``--browser`` of `plato vault app create`, `plato vault app consent` and
    `plato vault totp enroll`: which browser the portal steps use."""

    ego = "ego"  # ego-browser on this Mac, and an agent clicks Allow
    # Chromium on pi5-2 (the office Pi), driven from this machine over ssh: code through
    # CDP, the agent through the `computer` MCP server over VNC (cli/vault/pi_browser.py)
    pi = "pi"
    none = "none"  # consent only: the command prints the URL; a person opens it in any browser


class CredentialSource(StrEnum):
    """How the client secret got into the store."""

    portal = "portal"  # `plato vault app create`: code read it from the portal page
    imported = "import"  # `plato vault app import`: from an env file
    typed = "typed"  # typed at a getpass prompt (the --manual portal path)


class VendorRecipe(BaseModel):
    """Everything vendor-specific about one vendor's OAuth app. Data, not code:
    a second vendor is a second recipe plus its goal templates (cli/vault/prompts/)."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    vendor: AppVendor
    portal_url: str
    authorize_url: str
    token_url: str
    client_auth: ClientAuth
    pkce: bool
    redirect_uri: str
    user_check_url: str
    mcp_url: str
    access_token_s: int
    app_name_max: int
    client_id_prefix: str
    scopes: dict[CredentialKind, list[str]]
    env_prefix: dict[CredentialKind, str]
    # The portal switch (under Integration methods) that turns each kind on.
    switches: dict[CredentialKind, str]
    # The portal agent's goal ($space_id, $portal_url, $app_step, $switches, $scopes,
    # $redirect_uri, $no_files) and the consent agent's ($space_id, $app, $button,
    # $redirect_base, $no_files): template files in cli/vault/prompts/, filled in by
    # app_portal. The portal goal ends BEFORE "Generate secret": code clicks that
    # button, so no model sees the secret.
    portal_template: GoalTemplate
    consent_template: GoalTemplate
    # The same two goals for `--browser pi`: the agent has the `computer` screen tools
    # only. The same slots as above, minus $space_id, and $screen_rule in place of
    # $no_files.
    pi_portal_template: GoalTemplate
    pi_consent_template: GoalTemplate
    # The accessible name of the consent page's grant button. Code clicks it
    # (app_portal.click_consent); the consent agent runs only when that fails.
    consent_button: str
    # The vendor's sign-in pages: code fills them from the vault item (cli/vault/sign_in.py).
    sign_in: SignInRecipe

    def scopes_for(self, kinds: list[CredentialKind]) -> list[str]:
        """The union of the kinds' scopes, in recipe order, no repeats."""
        out: list[str] = []
        for kind in kinds:
            for scope in self.scopes[kind]:
                if scope not in out:
                    out.append(scope)
        return out


class PkcePair(BaseModel):
    """RFC 7636: the verifier stays in this process; only the challenge leaves it."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    verifier: SecretStr
    challenge: str
    method: PkceMethod = PkceMethod.s256


class TokenGrant(BaseModel):
    """A token endpoint reply (RFC 6749 5.1). Extra keys are ignored: a vendor may add some."""

    model_config = ConfigDict(extra="ignore")

    access_token: SecretStr
    token_type: str = "Bearer"
    expires_in: int | None = None
    refresh_token: SecretStr | None = None
    scope: str | None = None


class VendorUser(BaseModel):
    """Who the grant signs in as, from the vendor's user check (Canva `users/me`)."""

    model_config = ConfigDict(extra="forbid")

    user_id: str | None = None
    team_id: str | None = None


class AppCredentials(BaseModel):
    """The stored record. Never print it: print :meth:`presence` instead."""

    model_config = ConfigDict(extra="forbid")

    vendor: AppVendor
    login_key: str
    account: str
    kinds: list[CredentialKind]
    app_id: str | None = None
    app_name: str | None = None
    client_id: str
    client_secret: SecretStr
    client_auth: ClientAuth
    source: CredentialSource
    redirect_uri: str
    scopes: list[str] = Field(default_factory=list)
    refresh_token: SecretStr | None = None
    access_token: SecretStr | None = None
    expires_at: datetime | None = None
    user: VendorUser | None = None
    created_at: datetime
    updated_at: datetime

    @field_serializer("client_secret", "refresh_token", "access_token")
    def _reveal(self, value: SecretStr | None, info: SerializationInfo) -> str | None:
        """Plain text only for the store (``context={"reveal": True}``); masked otherwise."""
        if value is None:
            return None
        if info.context and info.context.get("reveal"):
            return value.get_secret_value()
        return str(value)

    def seconds_left(self, now: datetime | None = None) -> float | None:
        """Seconds until the access token expires; None when there is no token or no expiry."""
        if self.access_token is None or self.expires_at is None:
            return None
        return (self.expires_at - (now or datetime.now(UTC))).total_seconds()

    def fresh_for(self, min_left_s: float, now: datetime | None = None) -> bool:
        left = self.seconds_left(now)
        return left is not None and left >= min_left_s

    def with_grant(self, grant: TokenGrant, now: datetime | None = None) -> AppCredentials:
        """This record after a token call. A grant with no refresh token keeps the
        old one (RFC 6749 6 allows that); Canva always sends a new one."""
        now = now or datetime.now(UTC)
        update: dict = {
            "access_token": grant.access_token,
            "expires_at": now + timedelta(seconds=grant.expires_in) if grant.expires_in else None,
            "updated_at": now,
        }
        if grant.refresh_token is not None:
            update["refresh_token"] = grant.refresh_token
        if grant.scope:
            update["scopes"] = grant.scope.split()
        return self.model_copy(update=update)

    def presence(self, store_path: str | None = None, now: datetime | None = None) -> AppCredentialsPresence:
        left = self.seconds_left(now)
        return AppCredentialsPresence(
            vendor=self.vendor,
            login_key=self.login_key,
            account=self.account,
            kinds=self.kinds,
            app_id=self.app_id,
            app_name=self.app_name,
            source=self.source,
            client_id=ValuePresence.of(self.client_id, CLIENT_ID_PREFIX_LEN),
            client_secret=ValuePresence.of(self.client_secret),
            refresh_token=ValuePresence.of(self.refresh_token),
            access_token=ValuePresence.of(self.access_token),
            expires_at=self.expires_at,
            expires_in_s=int(left) if left is not None else None,
            scopes=self.scopes,
            redirect_uri=self.redirect_uri,
            user=self.user,
            updated_at=self.updated_at,
            store_path=store_path,
        )


class ValuePresence(BaseModel):
    """What may be shown about one value: whether it is there, its first characters, its length."""

    model_config = ConfigDict(extra="forbid")

    present: bool
    prefix: str | None = None
    length: int | None = None

    @classmethod
    def of(cls, value: SecretStr | str | None, prefix_len: int = SECRET_PREFIX_LEN) -> ValuePresence:
        if value is None:
            return cls(present=False)
        raw = value.get_secret_value() if isinstance(value, SecretStr) else value
        return cls(present=bool(raw), prefix=raw[:prefix_len] if raw else None, length=len(raw))

    def __str__(self) -> str:
        return f"{self.prefix}... ({self.length} chars)" if self.present else "-"


class AppCredentialsPresence(BaseModel):
    """`show` output: no secret, only presence, prefixes, lengths and the expiry."""

    model_config = ConfigDict(extra="forbid")

    vendor: AppVendor
    login_key: str
    account: str
    kinds: list[CredentialKind]
    app_id: str | None
    app_name: str | None
    source: CredentialSource
    client_id: ValuePresence
    client_secret: ValuePresence
    refresh_token: ValuePresence
    access_token: ValuePresence
    expires_at: datetime | None
    expires_in_s: int | None
    scopes: list[str]
    redirect_uri: str
    user: VendorUser | None
    updated_at: datetime
    store_path: str | None = None


class McpCheck(BaseModel):
    """The MCP probe: ``initialize`` then ``tools/list`` with the access token."""

    model_config = ConfigDict(extra="forbid")

    url: str
    initialize_status: int
    tools_status: int | None = None
    tool_count: int | None = None
    error: str | None = None

    @property
    def ok(self) -> bool:
        """Both calls got 200 and tools/list gave a readable ``result.tools`` list."""
        return (
            self.initialize_status == 200
            and self.tools_status == 200
            and self.error is None
            and self.tool_count is not None
        )


class TokenFileReport(BaseModel):
    """`token` output: the names written, never their values."""

    model_config = ConfigDict(extra="forbid")

    path: str
    names: list[str]
    refreshed: bool
    expires_at: datetime | None


class VaultLine(BaseModel):
    """One ``@@VAULT {json}`` result line from an ego-browser script or a portal agent.
    Every other output line is ignored. No field can carry a secret: the secret
    script prints the client id's prefix and the secret's length only, and the
    TOTP scripts print counts only."""

    model_config = ConfigDict(extra="ignore")

    space_id: int | None = None
    ready_for_secret: bool | None = None
    allowed: bool | None = None
    need_person: str | None = None
    reason: str | None = None
    error: str | None = None
    generate_buttons: int | None = None
    allow_buttons: int | None = None
    clicks: int | None = None
    written: bool | None = None
    client_id_prefix: str | None = None
    secret_len: int | None = None
    app_id: str | None = None
    # `plato vault totp` (totp_portal): counts and results only, never a key or a code.
    ready_for_key: bool | None = None
    uri_count: int | None = None
    key_count: int | None = None
    inputs: int | None = None
    typed: bool | None = None
    clicked: bool | None = None
    result: str | None = None
    codes: int | None = None
    finished: bool | None = None
    # The signed-in check (totp_portal): the account emails the page shows. Not a secret.
    emails: list[str] | None = None
    # The sign-in step (sign_in): the detect or fill result (counts and flags, never a value).
    sign_in: Any = None


class PortalSecretFile(BaseModel):
    """What the secret script writes to the private temp file, read back once and deleted."""

    model_config = ConfigDict(extra="forbid")

    client_id: str
    client_secret: SecretStr


_CANVA_REST_SCOPES = [
    "asset:read",
    "asset:write",
    "brandtemplate:content:read",
    "brandtemplate:content:write",
    "brandtemplate:meta:read",
    "comment:read",
    "comment:write",
    "design:content:read",
    "design:content:write",
    "design:meta:read",
    "design:meta:write",
    "folder:read",
    "folder:write",
    "profile:read",
]

CANVA = VendorRecipe(
    vendor=AppVendor.canva,
    portal_url="https://www.canva.com/developers/apps",
    authorize_url="https://www.canva.com/api/oauth/authorize",
    token_url="https://api.canva.com/rest/v1/oauth/token",
    client_auth=ClientAuth.basic,
    pkce=True,
    # 127.0.0.1 is allowed, localhost is not.
    redirect_uri="http://127.0.0.1:8765/callback",
    user_check_url="https://api.canva.com/rest/v1/users/me",
    # The portal-app MCP server (mcp.canva.com is for waitlist clients, with its own sign-in server).
    mcp_url="https://api.canva.com/connect/v1/mcp",
    access_token_s=14400,
    app_name_max=18,
    client_id_prefix="OC-",
    scopes={
        CredentialKind.api: _CANVA_REST_SCOPES,
        # The same scope names, plus the three that the MCP server's own scope list
        # adds: brandkit:read and the two help:answers scopes.
        CredentialKind.mcp: [*_CANVA_REST_SCOPES, "brandkit:read", "help:answers:read", "help:answers:write"],
    },
    env_prefix={CredentialKind.api: "CANVA_API", CredentialKind.mcp: "CANVA_MCP"},
    switches={CredentialKind.api: "Canva REST APIs", CredentialKind.mcp: "Canva MCP"},
    portal_template=GoalTemplate.canva_portal,
    consent_template=GoalTemplate.canva_consent,
    pi_portal_template=GoalTemplate.canva_pi_portal,
    pi_consent_template=GoalTemplate.canva_pi_consent,
    consent_button="Allow",
    sign_in=CANVA_SIGN_IN,
)

RECIPES: dict[AppVendor, VendorRecipe] = {AppVendor.canva: CANVA}
