"""Models for CLI command data flow (model/loader/view pattern).

TypedDicts here are returned by loaders (helpers) and consumed by views.
They carry no display logic — views decide how to render them.
"""

# Python internals
from datetime import datetime
from typing import Any, Literal, Optional

# Other libraries
from dlt._workspace.deployment._run_typing import TRunBannerInfo as _OSSRunBannerInfo
from dlt.common.typing import NotRequired, TypedDict


class FileDelta(TypedDict):
    """Per-file diff between two TFilesManifests."""

    # added/updated/deleted are sorted lists of relative_path strings
    added: list[str]
    updated: list[str]
    deleted: list[str]
    unchanged_count: int


# MINIMAL → one line per sync stage
# FULL    → full tabulate row + no_changes notice
SyncLoggingLevel = Literal["silent", "minimal", "full"]


class SyncResult(TypedDict):
    """Result of a deployment or configuration sync operation."""

    # would_create is the dry-run analogue of created: local package differs
    # from latest remote, so a real run would have uploaded.
    status: Literal["no_changes", "not_found", "created", "would_create"]
    data: NotRequired[dict[str, Any]]


class RuntimeInfo(TypedDict):
    """Workspace overview info for `dlthub workspace info`."""

    workspace_id: str
    workspace_name: Optional[str]
    organization_name: Optional[str]
    workspace_url: str
    local_dir: str
    job_count: int
    # Only present when fetch_user_info() returned a UserInfo (not on stale-token paths).
    email: NotRequired[str]
    latest_run_name: NotRequired[str]
    latest_run_status: NotRequired[str]
    latest_run_started: NotRequired[datetime]
    latest_run_ended: NotRequired[datetime]
    deployment_version: NotRequired[int]
    deployment_date: NotRequired[datetime]
    configuration_version: NotRequired[int]
    configuration_date: NotRequired[datetime]
    # Profiles predefined on the server, keyed by access level name
    # (e.g. {"DATA_WRITE": "prod", "DATA_READ": "access"}).
    predefined_profiles: NotRequired[dict[str, str]]


class WorkspaceInfo(TypedDict):
    """Server-side workspace as parsed from `/me`."""

    id: str
    name: str
    # `description` accepts None because the server returns `null` for
    # workspaces created without one; tests routinely pass `description=None`.
    description: NotRequired[Optional[str]]
    role: NotRequired[str]
    predefined_profiles: NotRequired[dict[str, str]]
    organization_id: NotRequired[str]
    organization_name: NotRequired[str]


class OrganizationInfo(TypedDict):
    """Organization the user belongs to (from `/me`)."""

    id: str
    name: str
    role: str
    active: bool


class WorkspaceChoice(TypedDict):
    """A picker row for an existing workspace — `id` is the `[N]` shown."""

    id: int
    workspace: WorkspaceInfo


class OrganizationGroup(TypedDict):
    """One org section in the workspace picker — bold header + owned workspaces."""

    organization_id: str
    organization_name: str
    create_id: int
    workspaces: list[WorkspaceChoice]


class CreateInOrgChoice(TypedDict):
    """Picker result when the user picks `[N] Create new workspace`."""

    organization_id: str
    organization_name: str


class UserInfo(TypedDict):
    """Authenticated user's identity + accessible workspaces / orgs (from `/me`)."""

    email: str
    user_id: str
    identity_id: str
    default_organization_id: str
    default_workspace: NotRequired[
        WorkspaceInfo
    ]  # absent when the user has no workspace
    workspaces: list[WorkspaceInfo]
    organizations: list[OrganizationInfo]


class LoginResult(TypedDict):
    """Result of login logic, before display."""

    email: str
    web_ui_url: str
    is_new_login: bool


class DeviceFlowStartResult(TypedDict):
    """Phase 1 result: device flow started, awaiting user action."""

    verification_uri: str
    verification_uri_complete: str
    user_code: str
    device_code: str
    interval: int


class ConnectedWorkspaceInfo(TypedDict):
    """Result of a workspace connect — passed to the success view."""

    workspace_id: str
    workspace_name: NotRequired[str]
    organization_name: NotRequired[str]
    # true if workspace was automatically connected without explicit args
    auto: NotRequired[bool]
    # true if this connect call also created the workspace just now
    created: NotRequired[bool]


# Mirror of `dlt_runtime_common.schemas.TriggerStatus` — kept local so the CLI
# does not depend on the common package, only on its generated client.
TriggerStatus = Literal[
    "triggered",
    "skipped_fresh",
    "skipped_upstream_pending",
    "skipped_out_of_interval",
    "skipped_concurrency_limit",
    "skipped_already_covered",
    "skipped_trial_expired",
    "skipped_minutes_limit",
    "skipped_org_concurrency_limit",
]


class RuntimeRunBannerInfo(_OSSRunBannerInfo):
    """OSS run banner extended with the remote run's web UI URL."""

    run_url: NotRequired[str]


class TriggerSkipInfo(TypedDict):
    """Skipped TriggerJob — minimal data for `_print_trigger_skip`."""

    job_ref: str
    status: TriggerStatus
    trigger: str
    # Local script concurrency setting (from manifest `execute.concurrency`).
    # Only known on the launch/serve path; absent on the bulk `trigger` path.
    concurrency: NotRequired[int]
    # Web UI URL for interactive jobs — shown alongside the concurrency hint
    # so the user can jump to the already-running notebook/app.
    web_url: NotRequired[str]
    # Server-supplied per-upstream reasons for the skip (e.g. which upstreams
    # failed the freshness check). Populated for `skipped_fresh`.
    reasons: NotRequired[list[str]]
