"""Models for CLI command data flow (model/loader/view pattern).

TypedDicts here are returned by loaders (helpers) and consumed by views.
They carry no display logic — views decide how to render them.
"""

from datetime import datetime
from typing import Any, Literal, Optional

from dlt.common.typing import NotRequired, TypedDict


class SyncResult(TypedDict):
    """Result of a deployment or configuration sync operation."""

    status: Literal["no_changes", "not_found", "created"]
    data: NotRequired[dict[str, Any]]


class RuntimeInfo(TypedDict):
    """Workspace overview info for `dlt runtime info`."""

    workspace_id: str
    workspace_name: Optional[str]
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


class ConnectInfo(TypedDict):
    """Result of workspace connection resolution."""

    workspace_id: str
    workspace_name: Optional[str]
    local_dir: str
    needs_selection: NotRequired[Literal["no_local", "mismatch"]]


class LoginResult(TypedDict):
    """Result of login logic, before display."""

    email: str
    web_ui_url: str
    is_new_login: bool
    connect_info: NotRequired[ConnectInfo]


class SwitchedWorkspaceInfo(TypedDict):
    """Result of a workspace switch — passed to the success view."""

    workspace_id: str
    workspace_name: NotRequired[str]
