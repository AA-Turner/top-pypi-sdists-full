"""Pydantic models for the server API."""

from __future__ import annotations

import typing as t

from pydantic import BaseModel, ConfigDict, Field, model_validator

if t.TYPE_CHECKING:
    from datetime import datetime


class WebSearchResult(BaseModel):
    title: str
    url: str
    snippet: str = ""


class WebSearchResponse(BaseModel):
    results: list[WebSearchResult]


# API Models - Complete models for all documented API routes.
# This module contains Pydantic models for all API responses defined in
# API_ROUTES.md, plus additional models used by the SDK for runs, tasks,
# traces, and objects.

AnyDict = dict[str, t.Any]


def _normalize_default_agent_fields(data: t.Any) -> t.Any:
    """Normalize legacy `default` agent/capability inputs to no override."""
    if not isinstance(data, dict):
        return data

    normalized = dict(data)
    for field in ("agent", "capability"):
        value = normalized.get(field)
        if isinstance(value, str) and value.strip().lower() == "default":
            normalized[field] = None
    return normalized


# -----------------------------------------------------------------------------
# Type Aliases for Exports
# -----------------------------------------------------------------------------

ExportFormat = t.Literal["csv", "json", "jsonl", "parquet"]
"""Available export formats for traces and runs"""

StatusFilter = t.Literal["all", "completed", "failed"]
"""Filter for trace and run statuses"""

TimeAxisType = t.Literal["wall", "relative", "step"]
"""Type of time axis for traces and runs"""

TimeAggregationType = t.Literal["max", "min", "sum", "count"]
"""How to aggregate time in traces and runs"""

MetricAggregationType = t.Literal[
    "avg",
    "median",
    "min",
    "max",
    "sum",
    "first",
    "last",
    "count",
    "std",
    "var",
]
"""How to aggregate metrics in traces and runs"""

# -----------------------------------------------------------------------------
# Health & Config
# -----------------------------------------------------------------------------


class AppConfig(BaseModel):
    """Application configuration returned by /api/config."""

    version: str
    """API version."""
    features: dict[str, bool] = Field(default_factory=dict)
    """Feature flags."""


class HealthCheck(BaseModel):
    """Health check response."""

    status: str = "ok"
    """Health status."""


# -----------------------------------------------------------------------------
# User
# -----------------------------------------------------------------------------


class UserAPIKey(BaseModel):
    """User API key."""

    id: str
    """API key ID."""
    key: str | None = None
    """The API key value (only returned on creation)."""
    masked_key: str | None = None
    """Masked API key (returned by GET /user)."""
    active: bool = True
    """Whether the key is active."""
    name: str | None = None
    """Optional name for the key."""
    allowed_scopes: list[str] | None = None
    """Scopes allowed for this key."""
    created_at: datetime | None = None
    """When the key was created."""
    last_used_at: datetime | None = None
    """When the key was last used."""


class UserGroup(BaseModel):
    """Group membership exposed on the current-user payload."""

    id: str
    name: str


class UserTeam(BaseModel):
    """Team membership exposed on the current-user payload."""

    team_id: str
    team_name: str
    org_id: str | None = None
    org_name: str | None = None
    role: t.Literal["owner", "member"]
    member_id: str | None = None
    is_admin: bool | None = None
    is_owner: bool | None = None


class UserIdentity(BaseModel):
    """Compact user identity embedded in cross-domain responses."""

    id: str
    email: str
    username: str
    full_name: str | None = None


class User(BaseModel):
    """Current user information."""

    id: str
    """User ID."""
    email_address: str
    """User's email address."""
    username: str
    """User's username."""
    first_name: str | None = None
    """User's first name."""
    last_name: str | None = None
    """User's last name."""
    full_name: str | None = None
    """User's full display name."""
    onboarding_complete: bool = False
    """Whether the user has completed onboarding."""
    email_opt_in: bool = False
    """Whether the user has opted in to product/marketing email."""
    is_platform_admin: bool = False
    """Whether the user has platform admin privileges."""
    features: list[str] | None = Field(default_factory=list)
    """Feature flags enabled for the user."""
    groups: list[UserGroup] | None = Field(default_factory=list)
    """Group memberships."""
    teams: list[UserTeam] | None = Field(default_factory=list)
    """Team memberships."""
    limits: dict[str, t.Any] | None = None
    """Per-user usage limits payload (server-side ``UsageSummaryResponse``)."""


# -----------------------------------------------------------------------------
# Secrets
# -----------------------------------------------------------------------------


class UserSecret(BaseModel):
    """User secret details."""

    id: str
    """Secret ID."""
    name: str
    """Secret name."""
    provider: str | None = None
    """Provider associated with the secret, if any."""
    masked_value: str
    """Masked secret value."""
    created_at: str
    """Creation timestamp."""
    updated_at: str
    """Last update timestamp."""


class UserSecretsList(BaseModel):
    """Response wrapper for list of user secrets."""

    secrets: list[UserSecret]
    """List of user secrets."""
    total: int
    """Total number of secrets."""


class ProviderPreset(BaseModel):
    """Provider preset details."""

    provider: str
    """Provider name."""
    env_var_name: str
    """Environment variable name for the provider."""
    configured: bool
    """Whether the preset is configured for the user."""


class ProviderPresetsList(BaseModel):
    """Response wrapper for provider presets."""

    presets: list[ProviderPreset]
    """List of provider presets."""


# -----------------------------------------------------------------------------
# Organization
# -----------------------------------------------------------------------------


class OrgOwner(BaseModel):
    """Lightweight organization owner info attached to organization responses."""

    user_id: str
    email: str
    name: str | None = None


class Organization(BaseModel):
    """Organization details."""

    id: str
    """Unique identifier for the organization."""
    name: str
    """Name of the organization."""
    key: str
    """URL-friendly identifier for the organization."""
    description: str | None = None
    """Description of the organization."""
    is_active: bool = True
    """Is the organization active?"""
    allow_external_invites: bool = False
    """Allow external invites to the organization?"""
    max_sandbox_runtime_seconds: int | None = None
    """Organization runtime hard ceiling in seconds."""
    effective_max_sandbox_runtime_seconds: int
    """Effective organization runtime ceiling after platform fallback."""
    max_sandbox_runtime_source_level: str
    """Source level for the effective organization runtime ceiling."""
    default_sandbox_runtime_seconds: int | None = None
    """Organization default sandbox runtime in seconds."""
    effective_default_sandbox_runtime_seconds: int
    """Effective default sandbox runtime after fallback hierarchy."""
    default_sandbox_runtime_source_level: str
    """Source level for the effective default sandbox runtime."""
    platform_max_sandbox_runtime_seconds: int
    """Platform runtime hard ceiling in seconds."""
    platform_default_sandbox_runtime_seconds: int
    """Platform default runtime for orgs without an override."""
    max_members: int = 0
    """Maximum number of members allowed in the organization."""
    member_count: int = 0
    """Current member count for the organization."""
    can_manage_members: bool = False
    """Whether the calling user can add/remove members."""
    plan_type: str | None = None
    """Plan type for the organization (e.g. ``pro``, ``enterprise``)."""
    owners: list[OrgOwner] | None = None
    """Organization owners, if exposed by the response."""
    created_at: datetime
    """Creation timestamp."""
    updated_at: datetime
    """Last update timestamp."""


class OrgMember(BaseModel):
    """Member of an organization."""

    id: str
    """User ID."""
    email_address: str
    """User's email address."""
    username: str | None = None
    """User's username."""
    role: str
    """Role in the organization (owner, contributor, reader)."""
    joined_at: datetime
    """When the user joined the organization."""


class Team(BaseModel):
    """Team within an organization."""

    id: str
    """Team ID."""
    name: str
    """Team name."""
    description: str | None = None
    """Team description."""
    member_count: int = 0
    """Number of members in the team."""
    created_at: datetime
    """When the team was created."""


# -----------------------------------------------------------------------------
# Workspace
# -----------------------------------------------------------------------------


class Workspace(BaseModel):
    """Workspace details."""

    id: str
    """Unique identifier for the workspace."""
    name: str
    """Name of the workspace."""
    key: str
    """Unique key for the workspace."""
    description: str | None = None
    """Description of the workspace."""
    created_by: str | None = None
    """Unique identifier for the user who created the workspace."""
    org_id: str
    """Unique identifier for the organization the workspace belongs to."""
    org_name: str | None = None
    """Name of the organization the workspace belongs to."""
    is_active: bool = True
    """Is the workspace active?"""
    is_default: bool = False
    """Is the workspace the default one?"""
    project_count: int | None = None
    """Number of projects in the workspace."""
    created_at: datetime
    """Creation timestamp."""
    updated_at: datetime
    """Last update timestamp."""


# -----------------------------------------------------------------------------
# Project
# -----------------------------------------------------------------------------


class ProjectResourceCounts(BaseModel):
    """Per-project resource counts attached to ``Project`` responses."""

    sessions: int = 0
    sandboxes: int = 0
    evaluations: int = 0
    airt_assessments: int = 0


class Project(BaseModel):
    """Project metadata."""

    id: str = Field(repr=False)
    """Unique identifier for the project."""
    key: str
    """Key for the project."""
    name: str
    """Name of the project."""
    description: str | None = Field(default=None, repr=False)
    """Description of the project."""
    workspace_id: str | None = None
    """Unique identifier for the workspace the project belongs to."""
    is_default: bool = False
    """Whether this is the workspace default grouping bucket."""
    created_at: datetime
    """Timestamp when the project was created."""
    updated_at: datetime
    """Timestamp when the project was last updated."""
    runtime_count: int = 0
    """Number of runtimes associated with the project."""
    resource_counts: ProjectResourceCounts = Field(default_factory=ProjectResourceCounts)
    """Per-resource counts (sessions, sandboxes, evaluations, AIRT assessments)."""


# -----------------------------------------------------------------------------
# Runs & Traces
# -----------------------------------------------------------------------------

SpanStatus = t.Literal["pending", "completed", "failed"]


class SpanException(BaseModel):
    """Exception details for a span."""

    type: str
    message: str
    stacktrace: str


class Metric(BaseModel):
    """Metric data point."""

    value: float | None
    step: int
    timestamp: datetime
    attributes: AnyDict = {}


class RunSummary(BaseModel):
    """Summary of a run."""

    id: str
    """Unique identifier for the run."""
    name: str
    """Name of the run."""
    span_id: str = Field(repr=False)
    trace_id: str = Field(repr=False)
    timestamp: datetime
    """Timestamp when the run started."""
    duration: int
    """Duration of the run in milliseconds."""
    status: SpanStatus
    """Status of the run."""
    exception: SpanException | None = None
    """Exception details if the run failed."""
    tags: set[str] = set()
    """Tags associated with the run."""
    params: AnyDict = Field(default_factory=dict, repr=False)
    """Parameters logged for the run."""
    metrics: dict[str, list[Metric]] = Field(default_factory=dict, repr=False)
    """Metrics logged for the run."""


# -----------------------------------------------------------------------------
# Run Sharing
# -----------------------------------------------------------------------------


class ShareInfo(BaseModel):
    """Information about a shared run."""

    token: str
    """Share token."""
    run_id: str
    """Run ID."""
    created_at: datetime
    """When the share was created."""
    created_by: str
    """User who created the share."""
    expires_at: datetime | None = None
    """When the share expires, if set."""


class SharedRun(BaseModel):
    """Publicly shared run data (from GET /api/s/{token})."""

    id: str
    """Run ID."""
    name: str
    """Run name."""
    timestamp: datetime
    """Run timestamp."""
    duration: int
    """Duration in milliseconds."""
    status: SpanStatus
    """Run status."""
    params: AnyDict = {}
    """Run parameters."""
    metrics: dict[str, list[Metric]] = {}
    """Run metrics."""


# -----------------------------------------------------------------------------
# Packages
# -----------------------------------------------------------------------------


class PackageVersion(BaseModel):
    """Package version information."""

    version: str
    """Version string."""
    created_at: datetime
    """When this version was created."""
    size_bytes: int = 0
    """Size of this version in bytes."""
    download_count: int = 0
    """Number of downloads for this version."""


class Package(BaseModel):
    """Package metadata."""

    id: str | None = None
    """Package ID."""
    name: str
    """Package name."""
    full_name: str
    """Full package name (org/type/name)."""
    package_type: str | None = None
    """Package type (datasets, models, agents, toolsets, environments)."""
    type: str | None = None
    """Package type (alias for package_type)."""
    summary: str | None = None
    """Package summary/description."""
    visibility: t.Literal["private", "org", "public"] = "private"
    """Package visibility."""
    org_id: str | None = None
    """Organization ID."""
    created_at: datetime | None = None
    """Creation timestamp."""
    updated_at: datetime | None = None
    """Last update timestamp."""
    versions: list[PackageVersion] | list[str] = []
    """Available versions."""
    latest_version: str | None = None
    """Latest version string."""
    download_count: int = 0
    """Total download count."""
    requires_python: str | None = None
    """Python version requirement."""
    requires_dist: list[str] = []
    """Distribution requirements."""
    upload_time: datetime | None = None
    """When the package was uploaded."""
    uploader: str | None = None
    """Username of uploader."""


class PackageAccessGrant(BaseModel):
    """Access grant for a package."""

    id: str
    """Grant ID."""
    user_id: str
    """User ID with access."""
    username: str | None = None
    """Username."""
    email_address: str | None = None
    """Email address."""
    permission: str
    """Permission level (read, write, admin)."""
    granted_at: datetime
    """When access was granted."""
    granted_by: str | None = None
    """User who granted access."""


class PackageAuditEntry(BaseModel):
    """Audit log entry for a package."""

    id: str
    """Entry ID."""
    action: str
    """Action performed (created, updated, downloaded, etc.)."""
    user_id: str
    """User who performed the action."""
    username: str | None = None
    """Username."""
    timestamp: datetime
    """When the action occurred."""
    details: AnyDict = {}
    """Additional details about the action."""


# -----------------------------------------------------------------------------
# Storage
# -----------------------------------------------------------------------------


class StorageCredentials(BaseModel):
    """S3 credentials for storage access."""

    access_key_id: str
    secret_access_key: str
    session_token: str
    expiration: datetime
    region: str
    bucket: str
    prefix: str
    endpoint: str | None = None


class StorageResource(BaseModel):
    """Storage resource in an organization."""

    id: str
    """Storage resource ID."""
    key: str
    """Storage key."""
    name: str
    """Display name."""
    description: str | None = None
    """Description."""
    org_id: str
    """Organization ID."""
    created_by: str | None = None
    """User who created the storage."""
    created_at: datetime
    """Creation timestamp."""
    updated_at: datetime
    """Last update timestamp."""
    size_bytes: int = 0
    """Total size in bytes."""
    version_count: int = 0
    """Number of versions."""


class StoragePermission(BaseModel):
    """Permission for a storage resource."""

    user_id: str
    """User ID."""
    username: str | None = None
    """Username."""
    permission: str
    """Permission level (read, write, admin)."""


# -----------------------------------------------------------------------------
# Explore
# -----------------------------------------------------------------------------


class ExplorePackage(BaseModel):
    """Package in the explore/browse view."""

    name: str
    """Package name."""
    full_name: str
    """Full package name (org/name)."""
    type: str
    """Package type (datasets, models, agents, etc.)."""
    summary: str | None = None
    """Package summary."""
    org_name: str
    """Organization name."""
    download_count: int = 0
    """Number of downloads."""
    latest_version: str | None = None
    """Latest version."""


class ExploreResponse(BaseModel):
    """Response from GET /api/explore."""

    packages: list[ExplorePackage]
    """List of packages."""
    total: int
    """Total number of results."""
    limit: int
    """Page size."""
    offset: int
    """Current offset."""


# -----------------------------------------------------------------------------
# Limits
# -----------------------------------------------------------------------------


LimitStatusValue = t.Literal["ok", "warning", "exceeded"]


class LimitStatus(BaseModel):
    """One usage limit's current status (server-side ``LimitStatusResponse``)."""

    limit_type: str
    status: LimitStatusValue
    current_usage: float
    limit_value: int | None = None
    remaining: int | None = None
    usage_percentage: float | None = None
    warning_message: str | None = None


class UsageLimits(BaseModel):
    """Usage limits and current usage for the calling user.

    Mirrors the server's ``UsageSummaryResponse`` returned from
    ``GET /api/v1/user/limits``.
    """

    user_id: str
    storage: LimitStatus | None = None
    tracked_hours: LimitStatus | None = None
    has_warnings: bool
    has_exceeded: bool
    checked_at: datetime


# -----------------------------------------------------------------------------
# Credits & Plans
# -----------------------------------------------------------------------------


class CreditBalance(BaseModel):
    """Credit balance response."""

    balance: int
    is_low_balance: bool
    auto_refill_enabled: bool = False


class AutoRefillConfig(BaseModel):
    """Auto-refill configuration response."""

    enabled: bool
    threshold: int | None
    quantity: int | None
    monthly_cap: int | None
    month_count: int
    has_payment_method: bool


class PaymentMethod(BaseModel):
    """Saved payment method details."""

    brand: str | None
    last4: str | None
    exp_month: int | None
    exp_year: int | None


class CheckoutSession(BaseModel):
    """Stripe checkout session details."""

    checkout_url: str
    session_id: str


class CreditsPricing(BaseModel):
    """Credits pricing details."""

    price_cents: int
    currency: str
    credits: int
    product_name: str | None = None
    product_description: str | None = None


# -----------------------------------------------------------------------------
# Platform Admin
# -----------------------------------------------------------------------------


class PlatformRelease(BaseModel):
    """Platform release information."""

    version: str
    """Release version."""
    release_date: datetime
    """Release date."""
    notes: str | None = None
    """Release notes."""
    images: list[dict[str, t.Any]] = []
    """Container images for this release."""


class RegistryToken(BaseModel):
    """Container registry token."""

    token: str
    """Registry token."""
    registry: str
    """Registry URL."""
    expires_at: datetime
    """Token expiration."""


class Template(BaseModel):
    """Project template."""

    id: str
    """Template ID."""
    name: str
    """Template name."""
    description: str | None = None
    """Template description."""
    type: str
    """Template type."""


# -----------------------------------------------------------------------------
# OTEL Ingestion
# -----------------------------------------------------------------------------


class OTELTraceResponse(BaseModel):
    """Response from trace ingestion."""

    accepted: int = 0
    """Number of spans accepted."""
    rejected: int = 0
    """Number of spans rejected."""


# -----------------------------------------------------------------------------
# User Data
# -----------------------------------------------------------------------------


class UserDataStore(BaseModel):
    """User data store information."""

    id: str
    """Store ID."""
    user_id: str
    """User ID."""
    created_at: datetime
    """Creation timestamp."""


class PermissionResponse(BaseModel):
    """Response to a permission request from the agent."""

    request_id: str
    decision: t.Literal["allow", "allow_session", "deny"]


class HumanPromptOption(BaseModel):
    """Structured option for a human prompt."""

    label: str
    description: str | None = None


class HumanQuestion(BaseModel):
    """A single question inside a ``HumanPrompt`` bundle."""

    kind: t.Literal["choice", "input"]
    prompt: str
    header: str | None = None
    options: list[HumanPromptOption] = Field(default_factory=list)
    multiple: bool = False
    custom: bool = True

    @model_validator(mode="after")
    def _validate_choice_options(self) -> HumanQuestion:
        if self.kind == "choice" and not self.options:
            raise ValueError("choice questions require at least one option")
        return self


class HumanPrompt(BaseModel):
    """Bundle of one or more questions sent to a human via ``ask_user``."""

    request_id: str
    questions: list[HumanQuestion]

    @model_validator(mode="after")
    def _validate_questions(self) -> HumanPrompt:
        if not self.questions:
            raise ValueError("HumanPrompt requires at least one question")
        return self


class QuestionAnswer(BaseModel):
    """Answer to a single ``HumanQuestion``."""

    selected_labels: list[str] = Field(default_factory=list)
    custom_text: str | None = None
    text: str | None = None
    was_custom: bool = False


class HumanInputResponse(BaseModel):
    """Structured response from a ``HumanPrompt``."""

    request_id: str
    action: t.Literal["submit", "cancel"]
    answers: list[QuestionAnswer] | None = None

    @model_validator(mode="after")
    def _validate_action_answers(self) -> HumanInputResponse:
        if self.action == "submit" and self.answers is None:
            raise ValueError("submit responses require answers")
        if self.action == "cancel" and self.answers:
            raise ValueError("cancel responses must not carry answers")
        return self


class ChatRequest(BaseModel):
    """Request body for chat endpoint."""

    message: str
    session_id: str = Field(min_length=1, validation_alias="sessionId")
    model: str | None = None
    agent: str | None = None
    reset: bool = False
    request_id: str | None = Field(default=None, validation_alias="requestId")
    permission_response: PermissionResponse | None = Field(
        default=None,
        validation_alias="permissionResponse",
    )
    human_input_response: HumanInputResponse | None = Field(
        default=None,
        validation_alias="humanInputResponse",
    )
    generate_params_extra: dict[str, t.Any] | None = Field(
        default=None,
        validation_alias="generateParamsExtra",
    )

    model_config = ConfigDict(populate_by_name=True)

    @model_validator(mode="before")
    @classmethod
    def _normalize_default_agent(cls, data: t.Any) -> t.Any:
        return _normalize_default_agent_fields(data)


class ChatResponse(BaseModel):
    """Response body for chat completion."""

    status: str
    session_id: str | None = None
    events: int = 0
    final_content: str | None = None
    error: str | None = None


class SessionInfo(BaseModel):
    """Information about an agent session."""

    session_id: str
    group_id: str | None = None
    project: str | None
    created_at: datetime
    updated_at: datetime | None = None
    message_count: int = 0
    session_dir: str | None = None
    capability: str | None = None
    agent: str | None = None
    model: str | None = None
    title: str | None = None
    preview: str | None = None
    policy_name: str = "interactive"
    policy_is_autonomous: bool = False
    policy_display_label: str = ""
    # Cumulative usage roll-ups computed at the source (runtime trajectory or
    # platform aggregation). ``total_cost_usd`` is ``None`` when any generation
    # in scope had no cost rate — partial sums sold as totals would diverge
    # from the platform's null-propagating ``SessionUsageResponse`` contract.
    total_tokens: int = 0
    total_tool_call_count: int = 0
    total_cost_usd: float | None = None
    # ``input_tokens`` from the most recent ``GenerationStep`` — represents
    # "context the model last saw", the right denominator for a context-window
    # gauge. ``None`` when no generation has run yet. Mirrors the platform's
    # ``SessionUsageResponse.last_generation_input_tokens``.
    last_generation_input_tokens: int | None = None


class SessionMessage(BaseModel):
    """Simple message payload used to seed a server-side session."""

    role: t.Literal["user", "assistant", "system", "tool"]
    content: str


class SessionCreateRequest(BaseModel):
    """Request body for creating a new session."""

    session_id: str | None = Field(default=None, validation_alias="sessionId")
    group_id: str | None = Field(default=None, validation_alias="groupId")
    model: str | None = None
    project: str | None = None
    capability: str | None = None
    agent: str | None = None
    messages: list[SessionMessage] = Field(default_factory=list)
    generate_params_extra: dict[str, t.Any] | None = Field(
        default=None,
        validation_alias="generateParamsExtra",
    )
    policy: str | dict[str, t.Any] | None = None
    labels: dict[str, list[str]] | None = None
    origin: str | None = None
    engine: str | None = None
    """Loop owner override (e.g. ``claude-code``). ``None``/``inherit`` falls
    through to the agent's declared engine, then native. Sticky per session."""
    project_memory_scope_kind: str = Field(
        default="project",
        validation_alias="projectMemoryScopeKind",
    )
    enable_project_memory_preload: bool = Field(
        default=True,
        validation_alias="enableProjectMemoryPreload",
    )
    project_memory_preload_limit: int = Field(
        default=20,
        ge=1,
        le=200,
        validation_alias="projectMemoryPreloadLimit",
    )

    model_config = ConfigDict(populate_by_name=True)

    @model_validator(mode="before")
    @classmethod
    def _normalize_default_agent(cls, data: t.Any) -> t.Any:
        return _normalize_default_agent_fields(data)


class SessionGroupCreateRequest(BaseModel):
    """Request body for creating a platform-backed session group."""

    kind: t.Literal["worker_run", "evaluation_item", "workflow"] = "workflow"
    title: str | None = None
    status: t.Literal["running", "completed", "failed", "cancelled"] | None = "running"
    project: str | None = None
    runtime_id: str | None = Field(default=None, validation_alias="runtimeId")
    capability: str | None = None
    capability_version: str | None = Field(default=None, validation_alias="capabilityVersion")
    worker: str | None = None
    evaluation_id: str | None = Field(default=None, validation_alias="evaluationId")
    evaluation_item_id: str | None = Field(default=None, validation_alias="evaluationItemId")
    evaluation_item_attempt_id: str | None = Field(
        default=None,
        validation_alias="evaluationItemAttemptId",
    )
    metadata: dict[str, t.Any] = Field(default_factory=dict)

    model_config = ConfigDict(populate_by_name=True)


class SessionGroupUpdateRequest(BaseModel):
    """Request body for updating a session group's lifecycle fields."""

    title: str | None = None
    status: t.Literal["running", "completed", "failed", "cancelled"] | None = None


class SessionGroupInfo(BaseModel):
    """Minimal session group response returned by the local runtime."""

    id: str
    kind: str
    title: str | None = None
    status: str | None = None


class SessionEventPublishRequest(BaseModel):
    """Request body for publishing an event into a session's event bus."""

    kind: str
    payload: dict[str, t.Any] = Field(default_factory=dict)


class SessionRestoreRequest(BaseModel):
    """Request body for restoring a server-side session runtime."""

    model: str | None = None
    project: str | None = None
    capability: str | None = None
    agent: str | None = None
    messages: list[SessionMessage] = Field(default_factory=list)
    trajectory: dict[str, t.Any] | None = None

    @model_validator(mode="before")
    @classmethod
    def _normalize_default_agent(cls, data: t.Any) -> t.Any:
        return _normalize_default_agent_fields(data)


class SessionRestoreResponse(BaseModel):
    """Response returned after restoring a server-side session runtime."""

    status: str = "restored"
    session_id: str = Field(serialization_alias="sessionId")
    message_count: int = Field(serialization_alias="messageCount")
    step_count: int = Field(serialization_alias="stepCount")
    capability: str | None = None
    agent: str | None = None
    project: str | None = None

    model_config = ConfigDict(populate_by_name=True)


class SavedSessionInfo(BaseModel):
    """Persisted session snapshot available in server storage."""

    session_id: str
    created_at: datetime | None = None
    project: str | None = None
    capability: str | None = None
    agent: str | None = None


class SavedSessionRestoreResponse(BaseModel):
    """Response returned after restoring a saved session snapshot."""

    session: SessionInfo
    messages: list[SessionMessage] = []


class CapabilityAgentInfo(BaseModel):
    """Agent metadata exposed by the local runtime."""

    name: str
    description: str
    model: str = "inherit"
    capability: str


ComponentKind = t.Literal[
    "agent",
    "tool",
    "hook",
    "skill",
    "mcp_server",
    "capability",
    "check",
    "worker",
    "policy",
]
"""Kinds emitted in loader health dicts. Keep in sync with the discovery sites
in ``dreadnode/capabilities/loader.py`` — a kind missing here used to take down
health reporting for the whole runtime (ENG-7606)."""


class ComponentStatusInfo(BaseModel):
    """Component-level load/runtime status."""

    kind: ComponentKind
    name: str
    # ``connecting`` and ``needs_auth`` are MCP-only statuses introduced by
    # the non-blocking startup work (ENG-6989 / CAP-MCP-009).
    status: t.Literal[
        "ok",
        "error",
        "degraded",
        "stopped",
        "gated_off",
        "enabled_failed",
        "connecting",
        "needs_auth",
    ]
    error: str | None = None
    detail: str | None = None
    # MCP-specific optional fields
    qualified_name: str | None = None
    capability: str | None = None
    transport: str | None = None
    tool_count: int | None = None
    # Gate-eligible components (MCP server / worker): flag names that would
    # satisfy the when: predicate. Present when status is gated_off so the
    # TUI can tell operators which flag to flip (CAP-FLAG-014).
    when: list[str] | None = None


class FlagInfo(BaseModel):
    """Resolved flag state exposed by the local runtime."""

    name: str
    description: str
    default: bool
    effective: bool
    source: t.Literal["default", "binding", "env", "cli"]


class CapabilityInfo(BaseModel):
    """Capability metadata exposed by the local runtime."""

    name: str
    display_name: str
    canonical_name: str | None = None
    local_path: str | None = None
    source: t.Literal["runtime", "local", "package"] | None = None
    provenance: t.Literal["local", "org", "public"] | None = None
    version: str | None = None
    description: str | None = None
    author: dict[str, t.Any] | None = None
    license: str | None = None
    origin: dict[str, t.Any] | None = None
    enabled: bool = True
    binding_id: str | None = None
    update_available: str | None = None
    flags: list[FlagInfo] = []
    components: list[ComponentStatusInfo] = []
    dependencies: dict[str, t.Any] | None = None
    checks: list[dict[str, t.Any]] | None = None
    # Existing fields retained for backward compat
    entry_agent: str | None = None
    skills_paths: list[str] = []
    agents: list[CapabilityAgentInfo] = []


class RuntimeInfoResponse(BaseModel):
    """Summary of the local runtime state."""

    status: str = "ok"
    version: str = "1.0.0"
    runtime_id: str | None = None
    host_type: str = "local"
    working_dir: str
    default_capability: str | None = None
    capabilities: list[CapabilityInfo] = []


class WsTicketResponse(BaseModel):
    """Short-lived ticket for authenticating a browser websocket handshake."""

    ticket: str
    expires_at: str


class HealthResponse(BaseModel):
    """Response body for health check."""

    status: str
    version: str = "1.0.0"


class ToolInfo(BaseModel):
    """Info about a single tool."""

    name: str
    """Canonical bare name. Preserved for backward compat with existing clients."""
    wire_name: str | None = None
    """LLM-facing projection of the tool's identity (CAP-IDENT-001..-007).

    For capability Python tools: ``{cap}__{name}``. For MCP tools:
    ``{cap}__{server}__{name}``. For built-ins and the bundled capability:
    equals ``name``. ``None`` for synthetic entries without a stamped Tool.
    """
    source: str | None = None
    """Tool origin: ``builtin``, ``python``, ``mcp``, ``synthetic``, or
    ``bundled``. ``None`` for synthetic session-scoped entries."""
    server: str | None = None
    """MCP server name for tools with ``source=mcp``; otherwise ``None``."""
    description: str = ""
    capability: str = ""
    parameters_schema: dict[str, t.Any] | None = None
    """JSON Schema for the tool's parameters, if available.

    Populated for first-class :class:`dreadnode.agents.tools.Tool`
    instances and MCP tools; ``None`` for synthetic session-scoped
    entries (``load_skill``, ``spawn_agent``) where no schema applies.
    The TUI uses this to register per-tool display hints — without it,
    unknown tools fall back to the generic first-string-arg heuristic.
    """


class ToolsResponse(BaseModel):
    """List of all available tools."""

    tools: list[ToolInfo] = []


class SkillInfo(BaseModel):
    """Skill metadata for API responses.

    `name` is the canonical bare name. `qualified_id` is the user-facing
    projection (`{cap}:{name}` for python-sourced skills, bare for bundled).
    See CAP-IDENT-019.
    """

    name: str
    description: str
    qualified_id: str | None = None
    """Qualified identifier projected through the skill `:` separator."""
    source: str | None = None
    """Skill origin — one of `builtin`, `python`, `bundled`."""
    capability: str | None = None
    """Owning capability (None for bundled or builtin skills)."""


class SkillsResponse(BaseModel):
    """Response for /api/skills listing."""

    skills: list[SkillInfo] = []


class SkillContentResponse(BaseModel):
    """Response for /api/skills/{name} content."""

    name: str
    description: str
    instructions: str
    allowed_tools: list[str] = []
    rendered: str = ""
    qualified_id: str | None = None
    source: str | None = None
    capability: str | None = None


# -----------------------------------------------------------------------------
# Platform Sessions
# -----------------------------------------------------------------------------


class PlatformSessionCreate(BaseModel):
    """Request body for creating a platform session (maps to API SessionCreateRequest)."""

    id: str
    """Client-generated session UUID."""
    model: str
    """Model used for the session."""
    agent: str | None = None
    """Accepted agent snapshot for the session."""
    title: str | None = None
    """Optional session title."""
    message_count: int = 0
    """Number of messages so far."""
    project_id: str | None = None
    """Optional project UUID to associate."""
    group_id: str | None = None
    """Optional session group UUID to attach."""


class PlatformSessionResponse(BaseModel):
    """Response from platform session endpoints (maps to API SessionResponse)."""

    id: str
    """Session UUID."""
    title: str | None = None
    """Session title."""
    model: str | None = None
    """Model used."""
    agent: str | None = None
    """Accepted agent snapshot."""
    message_count: int = 0
    """Message count."""
    token_count: int = 0
    """Token count."""
    last_message_at: datetime | None = None
    """Last message timestamp."""
    workspace_id: str | None = None
    """Workspace UUID."""
    project_id: str | None = None
    """Project UUID."""
    group_id: str | None = None
    """Session group UUID."""
    project_name: str | None = None
    """Project name."""
    created_at: datetime | None = None
    """Creation timestamp."""
    updated_at: datetime | None = None
    """Update timestamp."""


# -----------------------------------------------------------------------------
# Training
# -----------------------------------------------------------------------------

TrainingBackend = t.Literal["tinker", "ray"]
TrainingTrainerType = t.Literal["sft", "rl"]
TrainingAlgorithm = t.Literal["grpo", "importance_sampling", "ppo"]
TrainingJobStatus = t.Literal[
    "queued",
    "running",
    "completed",
    "failed",
    "cancelled",
]
TrainingLogLevel = t.Literal["debug", "info", "warning", "error"]


class CapabilityRef(BaseModel):
    """Versioned capability reference for hosted training jobs."""

    name: str
    version: str


class DatasetRef(BaseModel):
    """Versioned dataset reference for hosted training jobs."""

    name: str
    version: str


class RewardRecipe(BaseModel):
    """Server-side reward recipe reference."""

    name: str
    params: dict[str, t.Any] = Field(default_factory=dict)


class WorldRewardPolicy(BaseModel):
    """SDK-side reward policy for live Worlds RL rollouts."""

    name: str
    params: dict[str, t.Any] = Field(default_factory=dict)


class TinkerSFTJobConfig(BaseModel):
    """Hosted Tinker SFT configuration."""

    dataset_ref: DatasetRef | None = None
    trajectory_dataset_refs: list[DatasetRef] = Field(default_factory=list)
    eval_dataset_ref: DatasetRef | None = None
    max_sequence_length: int | None = None
    batch_size: int | None = None
    gradient_accumulation_steps: int | None = None
    learning_rate: float | None = None
    steps: int | None = None
    epochs: int | None = None
    lora_rank: int | None = None
    lora_alpha: int | None = None
    checkpoint_interval: int | None = None

    @model_validator(mode="after")
    def validate_training_inputs(self) -> TinkerSFTJobConfig:
        if self.dataset_ref is None and not self.trajectory_dataset_refs:
            raise ValueError(
                "Tinker SFT jobs require dataset_ref or at least one trajectory_dataset_ref"
            )
        return self


class TinkerRLJobConfig(BaseModel):
    """Hosted Tinker RL configuration."""

    algorithm: t.Literal["importance_sampling", "ppo"]
    task_ref: str | None = None
    world_manifest_id: str | None = None
    world_runtime_id: str | None = None
    world_agent_name: str | None = None
    world_goal: str | None = None
    prompt_dataset_ref: DatasetRef | None = None
    trajectory_dataset_refs: list[DatasetRef] = Field(default_factory=list)
    reward_recipe: RewardRecipe | None = None
    world_reward: WorldRewardPolicy | None = None
    execution_mode: t.Literal["sync", "one_step_off_async", "fully_async"] = "sync"
    prompt_split: str | None = None
    steps: int | None = None
    lora_rank: int | None = None
    max_turns: int | None = None
    max_episode_steps: int | None = None
    num_rollouts: int | None = None
    batch_size: int | None = None
    learning_rate: float | None = None
    weight_sync_interval: int | None = None
    max_steps_off_policy: int | None = None
    max_new_tokens: int | None = None
    temperature: float | None = None
    stop: list[str] | None = None
    checkpoint_interval: int | None = None
    eval_dataset_ref: DatasetRef | None = None
    eval_interval: int | None = None
    eval_max_rollouts: int | None = None

    @model_validator(mode="after")
    def validate_training_inputs(self) -> TinkerRLJobConfig:
        if self.world_runtime_id is not None and self.world_manifest_id is None:
            raise ValueError("world_manifest_id is required when world_runtime_id is provided")
        if self.world_agent_name is not None and self.world_runtime_id is None:
            raise ValueError("world_runtime_id is required when world_agent_name is provided")
        if (
            self.prompt_dataset_ref is None
            and not self.trajectory_dataset_refs
            and self.world_manifest_id is None
        ):
            raise ValueError(
                "Tinker RL jobs require prompt_dataset_ref, world_manifest_id, or at least one trajectory_dataset_ref"
            )
        if self.execution_mode != "sync" and self.max_steps_off_policy is None:
            raise ValueError("max_steps_off_policy is required for async execution modes")
        if self.execution_mode == "one_step_off_async" and self.max_steps_off_policy != 1:
            raise ValueError("max_steps_off_policy must be 1 for one_step_off_async execution mode")
        if self.eval_dataset_ref is None and (
            self.eval_interval is not None or self.eval_max_rollouts is not None
        ):
            raise ValueError("eval_interval / eval_max_rollouts require eval_dataset_ref")
        return self


class RayGRPOJobConfig(BaseModel):
    """Hosted Ray GRPO configuration."""

    algorithm: t.Literal["grpo"] = "grpo"
    task_ref: str
    prompt_dataset_ref: DatasetRef
    reward_recipe: RewardRecipe | None = None
    execution_mode: t.Literal["async", "colocated", "distributed"] = "async"
    max_turns: int | None = None
    max_episode_steps: int | None = None
    num_rollouts: int | None = None
    batch_size: int | None = None
    learning_rate: float | None = None
    num_rollout_workers: int | None = None
    buffer_size: int | None = None
    checkpoint_interval: int | None = None


class CreateTrainingJobBase(BaseModel):
    """Shared fields for hosted training job submission."""

    name: str | None = None
    model: str
    project_ref: str | None = None
    run_ref: str | None = None
    capability_ref: CapabilityRef
    tags: list[str] = Field(default_factory=list)


class CreateTinkerSFTJobRequest(CreateTrainingJobBase):
    """Request to create a hosted Tinker SFT job."""

    backend: t.Literal["tinker"] = "tinker"
    trainer_type: t.Literal["sft"] = "sft"
    config: TinkerSFTJobConfig


class CreateTinkerRLJobRequest(CreateTrainingJobBase):
    """Request to create a hosted Tinker RL job."""

    backend: t.Literal["tinker"] = "tinker"
    trainer_type: t.Literal["rl"] = "rl"
    config: TinkerRLJobConfig


class CreateRayGRPOJobRequest(CreateTrainingJobBase):
    """Request to create a hosted Ray GRPO job."""

    backend: t.Literal["ray"] = "ray"
    trainer_type: t.Literal["rl"] = "rl"
    config: RayGRPOJobConfig


TrainingJobCreateRequest = (
    CreateTinkerSFTJobRequest | CreateTinkerRLJobRequest | CreateRayGRPOJobRequest
)


class TrainingCapabilitySnapshot(BaseModel):
    """Resolved capability metadata attached to a training job."""

    artifact_id: str | None = None
    name: str
    version: str
    runtime_digest: str | None = None


class TrainingJob(BaseModel):
    """Hosted training job detail."""

    id: str
    organization_id: str
    workspace_id: str
    status: TrainingJobStatus
    name: str | None = None
    backend: TrainingBackend
    trainer_type: TrainingTrainerType
    algorithm: TrainingAlgorithm | None = None
    model: str
    project_ref: str | None = None
    run_ref: str | None = None
    dataset_ref: DatasetRef | None = None
    trajectory_dataset_refs: list[DatasetRef] = Field(default_factory=list)
    task_ref: str | None = None
    world_manifest_id: str | None = None
    world_runtime_id: str | None = None
    world_agent_name: str | None = None
    world_goal: str | None = None
    prompt_dataset_ref: DatasetRef | None = None
    capability: TrainingCapabilitySnapshot
    config: dict[str, t.Any] = Field(default_factory=dict)
    metrics: dict[str, t.Any] = Field(default_factory=dict)
    artifacts: dict[str, t.Any] = Field(default_factory=dict)
    tags: list[str] = Field(default_factory=list)
    error: str | None = None
    created_at: datetime
    created_by: str | None = None
    created_by_email: str | None = None
    created_by_user: UserIdentity | None = None
    started_at: datetime | None = None
    completed_at: datetime | None = None
    cancel_requested_at: datetime | None = None


class TrainingJobList(BaseModel):
    """Paginated training job list."""

    items: list[TrainingJob] = Field(default_factory=list)
    total: int = 0
    page: int = 1
    page_size: int = 20


class TrainingJobLogEntry(BaseModel):
    """Structured training log line."""

    timestamp: datetime
    level: TrainingLogLevel
    message: str
    data: dict[str, t.Any] = Field(default_factory=dict)


class TrainingJobLogList(BaseModel):
    """Training log response."""

    items: list[TrainingJobLogEntry] = Field(default_factory=list)


class TrainingJobArtifacts(BaseModel):
    """Training artifact response."""

    artifacts: dict[str, t.Any] = Field(default_factory=dict)


TrainingProgressEventType = t.Literal[
    "training_start",
    "step_complete",
    "eval_complete",
    "checkpoint_saved",
    "training_error",
    "training_end",
]

TERMINAL_TRAINING_PROGRESS_EVENTS: frozenset[TrainingProgressEventType] = frozenset(
    ("training_end", "training_error")
)


class TrainingTaskContext(BaseModel):
    """Mirror of ``app.training.schemas.TrainingTaskContext``."""

    model_config = ConfigDict(extra="forbid")

    id: str
    reference: str
    name: str
    version: str
    instruction: str | None = None
    ports: dict[str, t.Any] | None = None
    verification: dict[str, t.Any] | None = None
    solution: dict[str, t.Any] | None = None
    sandbox_provider: str
    s3_key: str


class TrainingWorldContext(BaseModel):
    """Mirror of ``app.training.schemas.TrainingWorldContext``."""

    model_config = ConfigDict(extra="forbid")

    id: str
    name: str | None = None
    manifest_backend_id: str | None = None
    server_url: str
    artifact_refs: dict[str, t.Any] = Field(default_factory=dict)
    stats: dict[str, t.Any] = Field(default_factory=dict)


class TrainingRLContext(BaseModel):
    """Mirror of ``app.training.schemas.TrainingRLContextResponse``."""

    model_config = ConfigDict(extra="forbid")

    capability_entry_prompt: str | None = None
    task: TrainingTaskContext | None = None
    world: TrainingWorldContext | None = None
    sampled_trajectory_dataset_ref: str | None = None
    reward_recipe: dict[str, t.Any] | None = None


class TrainingJobProgressUpdateRequest(BaseModel):
    """Structured progress update emitted by the hosted training runtime.

    Mirrors ``app.training.schemas.TrainingJobProgressUpdateRequest`` on the
    API side. Terminal events (``training_end`` / ``training_error``) may
    carry ``artifacts`` and ``error`` so the sandbox can ship its final
    result through the same channel.
    """

    model_config = ConfigDict(extra="forbid")

    event_type: TrainingProgressEventType
    message: str | None = None
    level: TrainingLogLevel = "info"
    metrics: dict[str, t.Any] = Field(default_factory=dict)
    data: dict[str, t.Any] = Field(default_factory=dict)
    artifacts: dict[str, t.Any] | None = None
    error: str | None = None


# -----------------------------------------------------------------------------
# Training model catalog
# -----------------------------------------------------------------------------


TrainingModelType = t.Literal["dense", "moe"]
TrainingModelFamily = t.Literal["llama", "qwen"]
TrainingModelAlgorithm = t.Literal["sft", "importance_sampling", "ppo"]


class TrainingModelPricing(BaseModel):
    prefill: float | None = Field(default=None, ge=0)
    sample: float | None = Field(default=None, ge=0)
    train: float | None = Field(default=None, ge=0)


class TrainingModel(BaseModel):
    """One base model available for hosted training jobs."""

    tinker_id: str
    display_name: str
    family: TrainingModelFamily
    type: TrainingModelType
    size_b: float
    context_length: int
    extended_context: bool = False
    supported_algorithms: list[TrainingModelAlgorithm]
    pricing: TrainingModelPricing | None = None


class TrainingCatalogResponse(BaseModel):
    """Paginated response for GET /training/catalog."""

    models: list[TrainingModel] = Field(default_factory=list)
    total: int
    limit: int


# -----------------------------------------------------------------------------
# Optimization
# -----------------------------------------------------------------------------

OptimizationBackend = t.Literal["gepa"]
OptimizationTargetKind = t.Literal["capability_agent", "capability_env"]
OptimizationJobStatus = t.Literal[
    "pending",
    "queued",
    "running",
    "completed",
    "failed",
    "cancelled",
]
OptimizationLogLevel = t.Literal["debug", "info", "warning", "error"]
OptimizationComponent = t.Literal[
    "instructions",
    "agent_prompt",
    "capability_prompt",
    "skill_descriptions",
    "skill_bodies",
]
_AGENT_COMPONENTS: frozenset[OptimizationComponent] = frozenset({"instructions"})
_ENV_COMPONENTS: frozenset[OptimizationComponent] = frozenset(
    {"agent_prompt", "capability_prompt", "skill_descriptions", "skill_bodies"}
)
OptimizationProgressEventType = t.Literal[
    "runtime_checkpoint",
    "optimization_start",
    "iteration_start",
    "candidate_accepted",
    "candidate_rejected",
    "valset_evaluated",
    "budget_updated",
    "pareto_front_updated",
    "optimization_error",
    "optimization_end",
]


class OptimizationJobConfig(BaseModel):
    """Hosted GEPA adapter settings supported by the current optimization API."""

    concurrency: int = 1
    parallel_rows: int = 1
    task_ref: str | None = None
    task_refs: list[str] | None = None
    val_task_refs: list[str] | None = None
    timeout_sec: int | None = None
    seed: int = 0
    max_metric_calls: int | None = 100
    max_trials: int | None = None
    max_trials_without_improvement: int | None = None
    max_runtime_sec: int | None = None
    display_progress_bar: bool = False
    track_best_outputs: bool = False
    val_evaluation_policy: str | None = None
    candidate_selection_strategy: str | None = None
    cache_evaluation: bool = False
    frontier_type: t.Literal["instance", "objective", "hybrid", "cartesian"] | None = None
    skip_perfect_score: bool | None = None
    perfect_score: float | None = None
    batch_sampler: str | None = None
    reflection_minibatch_size: int | None = None
    module_selector: str | None = None
    reflection_lm: str | None = None
    reflection_prompt_template: str | dict[str, str] | None = None
    max_merge_invocations: int | None = None
    merge_val_overlap_floor: int | None = None
    capture_traces: bool = True
    include_outputs: bool = True
    include_errors: bool = True
    max_reflection_examples: int = 10
    max_side_info_chars: int = 4000
    dataset_input_mapping: list[str] | dict[str, str] | None = None


class CreateOptimizationJobBase(BaseModel):
    """Shared fields for hosted optimization job submission."""

    name: str | None = None
    target_kind: OptimizationTargetKind = "capability_agent"
    model: str
    project: str | None = None
    run_ref: str | None = None
    capability_ref: CapabilityRef
    agent_name: str | None = None
    dataset_ref: DatasetRef | None = None
    val_dataset_ref: DatasetRef | None = None
    reward_recipe: RewardRecipe
    components: list[OptimizationComponent] | None = None
    task_ref: str | None = None
    task_refs: list[str] | None = None
    val_task_refs: list[str] | None = None
    timeout_sec: int | None = None
    objective: str | None = None
    config: OptimizationJobConfig = Field(default_factory=OptimizationJobConfig)
    tags: list[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def validate_components(self) -> CreateOptimizationJobBase:
        if self.components is None:
            self.components = (
                ["agent_prompt", "capability_prompt", "skill_descriptions", "skill_bodies"]
                if self.target_kind == "capability_env"
                else ["instructions"]
            )
        if not self.components:
            raise ValueError("Hosted optimization jobs require at least one optimizable component")
        component_set = set(self.components)
        if self.target_kind == "capability_agent":
            invalid = component_set - _AGENT_COMPONENTS
            if invalid:
                raise ValueError(
                    "capability_agent supports only ['instructions'] components"
                    f" (got {sorted(invalid)})"
                )
        else:  # capability_env
            invalid = component_set - _ENV_COMPONENTS
            if invalid:
                raise ValueError(
                    "capability_env supports component surfaces"
                    f" {sorted(_ENV_COMPONENTS)} (got {sorted(invalid)})"
                )
        return self

    @model_validator(mode="after")
    def validate_env_requirements(self) -> CreateOptimizationJobBase:
        if self.target_kind == "capability_env":
            train_sources = [
                ("task_refs", bool(self.task_refs)),
                ("dataset_ref", self.dataset_ref is not None),
                ("task_ref", self.task_ref is not None),
            ]
            active = [name for name, present in train_sources if present]
            if len(active) == 0:
                raise ValueError(
                    "capability_env requires a training surface: provide "
                    "task_refs, task_ref, or dataset_ref"
                )
            if len(active) > 1:
                raise ValueError(
                    "capability_env training surface is ambiguous — provide only "
                    f"one of task_refs / task_ref / dataset_ref (got {active})"
                )
            if self.val_task_refs is not None and self.val_dataset_ref is not None:
                raise ValueError(
                    "capability_env val surface is ambiguous — provide only one "
                    "of val_task_refs or val_dataset_ref"
                )
        else:
            if self.task_ref is not None:
                raise ValueError("task_ref is only valid with target_kind='capability_env'")
            if self.timeout_sec is not None:
                raise ValueError("timeout_sec is only valid with target_kind='capability_env'")
            if self.task_refs is not None:
                raise ValueError("task_refs is only valid with target_kind='capability_env'")
            if self.val_task_refs is not None:
                raise ValueError("val_task_refs is only valid with target_kind='capability_env'")
            if self.dataset_ref is None:
                raise ValueError(
                    "capability_agent requires dataset_ref (dataset rows drive the "
                    "agent's user message and scoring)"
                )
        return self


class CreateGEPAOptimizationJobRequest(CreateOptimizationJobBase):
    """Request to create a hosted GEPA optimization job."""

    backend: t.Literal["gepa"] = "gepa"


OptimizationJobCreateRequest = CreateGEPAOptimizationJobRequest


class OptimizationCapabilitySnapshot(BaseModel):
    """Resolved capability metadata attached to an optimization job."""

    artifact_id: str | None = None
    name: str
    version: str
    runtime_digest: str | None = None


class OptimizationSummary(BaseModel):
    """Normalized optimization outcome summary."""

    best_candidate: dict[str, str] | None = None
    best_score: float | None = None
    best_scores: dict[str, float] = Field(default_factory=dict)
    objective: str | None = None
    train_size: int = 0
    val_size: int = 0
    frontier_size: int = 0
    metadata: dict[str, t.Any] = Field(default_factory=dict)


class OptimizationSummaryPatch(BaseModel):
    """Partial optimization summary update used for live progress reporting."""

    best_candidate: dict[str, str] | None = None
    best_score: float | None = None
    best_scores: dict[str, float] | None = None
    objective: str | None = None
    train_size: int | None = None
    val_size: int | None = None
    frontier_size: int | None = None
    metadata: dict[str, t.Any] | None = None


class OptimizationMetricPoint(BaseModel):
    """One hosted optimization metric sample."""

    value: float
    step: int | None = None
    timestamp: datetime | None = None


OptimizationMetrics = dict[str, list[OptimizationMetricPoint]]


class OptimizationJobProgressUpdateRequest(BaseModel):
    """Structured hosted optimization progress update.

    Terminal events (``optimization_end`` / ``optimization_error``) may carry
    ``artifacts`` (merged into the job's artifact refs) and ``error`` (written
    to the job's error field) so the sandbox can push its final
    ``OptimizationJobResult`` through this one endpoint rather than staging a
    result file for the API to poll.
    """

    event_type: OptimizationProgressEventType
    message: str | None = None
    level: OptimizationLogLevel = "info"
    iteration: int | None = None
    summary: OptimizationSummaryPatch | None = None
    metrics: OptimizationMetrics = Field(default_factory=dict)
    data: dict[str, t.Any] = Field(default_factory=dict)
    artifacts: dict[str, t.Any] | None = None
    error: str | None = None


class OptimizationJob(BaseModel):
    """Hosted optimization job detail."""

    id: str
    organization_id: str
    workspace_id: str
    status: OptimizationJobStatus
    name: str | None = None
    backend: OptimizationBackend
    target_kind: OptimizationTargetKind
    model: str
    project: str | None = None
    run_ref: str | None = None
    dataset_ref: DatasetRef | None = None
    val_dataset_ref: DatasetRef | None = None
    task_refs: list[str] | None = None
    val_task_refs: list[str] | None = None
    objective: str | None = None
    capability: OptimizationCapabilitySnapshot
    agent_name: str | None = None
    reward_recipe: RewardRecipe
    components: list[OptimizationComponent] = Field(default_factory=list)
    config: OptimizationJobConfig = Field(default_factory=OptimizationJobConfig)
    metrics: OptimizationMetrics = Field(default_factory=dict)
    summary: OptimizationSummary = Field(default_factory=OptimizationSummary)
    artifacts: dict[str, t.Any] = Field(default_factory=dict)
    tags: list[str] = Field(default_factory=list)
    error: str | None = None
    created_at: datetime
    created_by: str | None = None
    created_by_email: str | None = None
    created_by_user: UserIdentity | None = None
    started_at: datetime | None = None
    completed_at: datetime | None = None
    cancel_requested_at: datetime | None = None


class OptimizationJobList(BaseModel):
    """Paginated optimization job list."""

    items: list[OptimizationJob] = Field(default_factory=list)
    total: int = 0
    page: int = 1
    page_size: int = 20


class OptimizationJobLogEntry(BaseModel):
    """Structured optimization log line."""

    timestamp: datetime
    level: OptimizationLogLevel
    message: str
    data: dict[str, t.Any] = Field(default_factory=dict)


class OptimizationJobLogList(BaseModel):
    """Optimization log response."""

    items: list[OptimizationJobLogEntry] = Field(default_factory=list)


class OptimizationJobArtifacts(BaseModel):
    """Optimization artifact response."""

    artifacts: dict[str, t.Any] = Field(default_factory=dict)


class OptimizationJobStreamEvent(BaseModel):
    """SSE payload for hosted optimization job updates."""

    type: t.Literal["snapshot", "job", "log", "heartbeat"]
    timestamp: datetime
    job: OptimizationJob | None = None
    log: OptimizationJobLogEntry | None = None


for _model in (
    RewardRecipe,
    WorldRewardPolicy,
    TinkerSFTJobConfig,
    TinkerRLJobConfig,
    RayGRPOJobConfig,
    CreateTinkerSFTJobRequest,
    CreateTinkerRLJobRequest,
    CreateRayGRPOJobRequest,
    TrainingCapabilitySnapshot,
    TrainingJob,
    OptimizationJobConfig,
    CreateGEPAOptimizationJobRequest,
    OptimizationCapabilitySnapshot,
    OptimizationSummary,
    OptimizationSummaryPatch,
    OptimizationMetricPoint,
    OptimizationJobProgressUpdateRequest,
    OptimizationJob,
    OptimizationJobLogEntry,
    OptimizationJobStreamEvent,
):
    _model.model_rebuild(
        _types_namespace={"datetime": __import__("datetime").datetime},
    )

del _model


def _rebuild_models_with_runtime_types() -> None:
    from datetime import datetime

    for value in globals().values():
        if isinstance(value, type) and value is not BaseModel and issubclass(value, BaseModel):
            value.model_rebuild(
                force=True,
                _types_namespace={"datetime": datetime},
            )


_rebuild_models_with_runtime_types()
