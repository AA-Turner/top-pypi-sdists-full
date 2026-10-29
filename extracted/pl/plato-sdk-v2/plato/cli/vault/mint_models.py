"""Models for `plato vault mint token` (:mod:`app_mint`): the agent's tool inputs, what code
keeps in memory, and the report. No field the agent sees holds a secret: tool replies carry
names, lengths and HTTP statuses only.
"""

from __future__ import annotations

from datetime import datetime
from enum import StrEnum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, SecretStr

from plato.cli.vault.app_models import ClientAuth

# A value name the agent picks for read_value.
VALUE_NAME_PATTERN = r"^[a-z][a-z0-9_]{0,39}$"
# A Chronos grant kind (plato chronos/models/login_vault_grants.py GRANT_KIND_PATTERN).
GRANT_KIND_PATTERN = r"^[a-z][a-z0-9_]{0,39}$"


class SignInField(StrEnum):
    username = "username"
    password = "password"
    totp = "totp"
    email_code = "email_code"  # the code the vendor just emailed to the login email, read from its inbox


class FillInput(BaseModel):
    field: SignInField = Field(description="Which vault value code types into the input that has focus now")


class ReadInput(BaseModel):
    name: str = Field(pattern=VALUE_NAME_PATTERN, description="client_id or client_secret")
    secret: bool = Field(
        default=True,
        description="False only for a value that is no secret (a client id): code then also reads plain text",
    )


class OAuthStartInput(BaseModel):
    authorize_url: str = Field(description="The vendor's authorization endpoint (https), from its docs")
    token_url: str = Field(description="The vendor's token endpoint (https), from its docs")
    scopes: list[str] = Field(default_factory=list, description="The scopes to ask for, as the docs name them")
    scope_separator: str = Field(default=" ", description="How the vendor joins scopes in the URL (most: a space)")
    extra_params: dict[str, str] = Field(
        default_factory=dict,
        description="Other authorize parameters the docs require, e.g. audience or prompt (never a secret, "
        "nor one code sets: state, redirect_uri, client_id, response_type, PKCE, scope)",
    )
    pkce: bool = Field(default=True, description="Send a PKCE S256 challenge (false if the docs say it is refused)")
    client_auth: ClientAuth = Field(
        default=ClientAuth.post,
        description="How the token call sends the client secret: client_secret_post (in the body), "
        "client_secret_basic (HTTP Basic) or none (a registered public client: register_client says which)",
    )


class RegisterInput(BaseModel):
    server_url: str = Field(
        description="The https URL of the vendor's server to register a client with: its hosted MCP server "
        "URL (as an MCP client connects to it), or its OAuth server"
    )


class OAuthFinishInput(BaseModel):
    timeout_s: int = Field(default=300, ge=10, le=900, description="How long code waits for the consent redirect")


class CheckInput(BaseModel):
    url: str = Field(
        description="A GET endpoint (https) of the vendor's API that answers who the token signs in as; "
        "with mcp_tool: the MCP server URL"
    )
    mcp_tool: str | None = Field(
        default=None,
        description="For an MCP server: a tool the server marks read-only that takes no input and returns the "
        "signed-in user (e.g. a 'current user info' tool). Code runs initialize, tools/list and this tools/call",
    )


class FocusedInput(BaseModel):
    """The focused element as the sign-in fill checks it (FOCUSED_JS); ``frame`` when focus is in a frame."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    frame: bool = False
    tag: str = ""
    type: str = ""
    autocomplete: str = ""
    usable: bool = False
    protocol: str = ""
    host: str = ""


class CheckIdentity(BaseModel):
    """The identity fields a check reply may show the agent (one level deep, or under one object)."""

    model_config = ConfigDict(extra="forbid")

    id: str | None = None
    account_id: str | None = None
    accountId: str | None = None
    user_id: str | None = None
    login: str | None = None
    username: str | None = None
    handle: str | None = None
    email: str | None = None
    emailAddress: str | None = None
    name: str | None = None
    displayName: str | None = None

    def emails(self) -> set[str]:
        return {v.casefold() for v in self.model_dump(exclude_none=True).values() if "@" in v}

    def names_account(self) -> bool:
        """Whether the reply says whose account it is: an email or a user id or login."""
        return bool(self.emails() or self.user_id_value() or self.username or self.handle)

    def user_id_value(self) -> str | None:
        """The vendor's user id for the grant: the first of the id-like fields the reply had."""
        return self.account_id or self.accountId or self.id or self.user_id or self.login


class RegisteredServer(BaseModel):
    """What register_client tells the agent: the discovered endpoints (no secret)."""

    model_config = ConfigDict(extra="forbid")

    authorize_url: str
    token_url: str
    client_auth: ClientAuth
    scopes_supported: list[str] = Field(default_factory=list)


class ToolReply(BaseModel):
    """A `vault` tool's answer to the agent: names, counts and statuses, never a value."""

    model_config = ConfigDict(extra="forbid")

    ok: bool
    error: str | None = None
    next: str | None = None
    warning: str | None = None
    filled: SignInField | None = None
    name: str | None = None
    length: int | None = None
    starts_with: str | None = Field(default=None, description="read_value of a non-secret: its first 4 characters")
    has_refresh_token: bool | None = None
    expires_in: int | None = None
    scopes: int | None = None
    status: int | None = None
    identity: CheckIdentity | None = None
    tools: int | None = Field(default=None, description="An MCP check: the tools the server listed")
    server: RegisteredServer | None = None


class RpcReply(BaseModel):
    """A JSON-RPC reply of an MCP server: its result, or that it answered an error (the error's text
    is never kept: it can quote the request)."""

    model_config = ConfigDict(extra="ignore")

    id: int | str | None = None
    result: dict[str, Any] | None = None
    error: dict[str, Any] | None = None


class McpToolAnnotations(BaseModel):
    model_config = ConfigDict(extra="ignore")

    readOnlyHint: bool | None = None


class McpInputSchema(BaseModel):
    model_config = ConfigDict(extra="ignore")

    required: list[str] = Field(default_factory=list)


class McpTool(BaseModel):
    model_config = ConfigDict(extra="ignore")

    name: str
    annotations: McpToolAnnotations | None = None
    inputSchema: McpInputSchema = Field(default_factory=McpInputSchema)


class McpToolList(BaseModel):
    """A tools/list result page."""

    model_config = ConfigDict(extra="ignore")

    tools: list[McpTool] = Field(default_factory=list)
    nextCursor: str | None = None


class McpContent(BaseModel):
    model_config = ConfigDict(extra="ignore")

    type: str
    text: str | None = None


class McpToolResult(BaseModel):
    """A tools/call result: a tool error comes back as a result with ``isError``."""

    model_config = ConfigDict(extra="ignore")

    content: list[McpContent] = Field(default_factory=list)
    structuredContent: dict[str, Any] | None = None
    isError: bool = False


class CheckResult(BaseModel):
    """A check's HTTP status and the identity fields of its JSON reply (never a token)."""

    status: int | None = None
    error: str | None = None
    identity: CheckIdentity = Field(default_factory=CheckIdentity)
    tools: int | None = None

    @property
    def ok(self) -> bool:
        # An MCP tool error comes back as HTTP 200 with an error set.
        return self.status is not None and 200 <= self.status < 300 and self.error is None


class OAuthSpec(BaseModel):
    """The agent's OAuth settings once it started the consent. No secret."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    authorize_url: str
    token_url: str
    scopes: list[str]
    client_auth: ClientAuth
    # RFC 8707: sent on the authorize and every token call (a registered client's resource metadata).
    resource: str | None = None


class OAuthTokens(BaseModel):
    """The exchange's result. Never print it."""

    model_config = ConfigDict(extra="forbid")

    access_token: SecretStr
    refresh_token: SecretStr | None = None
    expires_at: datetime | None = None
    scope: str | None = None
    client_id: SecretStr = Field(description="The client id the exchange used")
    client_secret: SecretStr | None = Field(description="The client secret the exchange used (none: a public client)")


class VaultItem(BaseModel):
    """The vault item's sign-in values, read once. Never print it."""

    model_config = ConfigDict(extra="forbid")

    username: str | None = None
    password: SecretStr | None = None
    totp_seed: SecretStr | None = None
    login_url: str | None = None
    # Picks the inbox an emailed code is read from (plato.vault.mail_route); Chronos answers the
    # username when it is unset and the username is an address.
    login_email: str | None = None


class MintOutcome(StrEnum):
    verified = "verified"  # the grant was there and its token read answered: nothing minted
    minted = "minted"  # the agent made an OAuth app and a consent; the grant is new


class DocsPlan(BaseModel):
    """What the docs step found: how a user of this vendor gets an OAuth app with a refresh token.
    For this run's walker only; never stored."""

    model_config = ConfigDict(extra="forbid")

    portal_url: str = Field(description="Where a user makes an OAuth app (the developer console)")
    steps: list[str] = Field(description="The few steps there, one short line each")
    scopes: list[str] = Field(default_factory=list, description="Scopes that read and write the account's data")
    refresh_token: str | None = Field(default=None, description="What the vendor needs to issue a refresh token")
    authorize_url: str | None = None
    token_url: str | None = None
    check_url: str | None = Field(default=None, description='A "who am I" GET endpoint that names the user')
    docs: list[str] = Field(min_length=1, description="The doc pages used")


class DocsReply(BaseModel):
    model_config = ConfigDict(extra="ignore")

    plan: DocsPlan | None
    reason: str | None = None


class MintReport(BaseModel):
    """What `mint token` prints: names, lengths and statuses only."""

    login_key: str
    account: str
    kind: str
    outcome: MintOutcome | None = None
    why_mint: str | None = Field(default=None, description="Why the stored grant did not pass, when it was minted")
    docs_pages: int | None = Field(default=None, description="Doc pages the docs step's plan used (none: no plan)")
    docs_note: str | None = Field(default=None, description="Why the walker had no docs plan")
    summary: str | None = None
    values: dict[str, int] = Field(default_factory=dict, description="read values: name -> length")
    state: str | None = None
    generation: int | None = None
    refreshed: bool | None = None
    expires_at: datetime | None = None
    scopes: int | None = None
    check_url: str | None = None
    agent_check: CheckResult | None = None
    stored_check: CheckResult | None = None
