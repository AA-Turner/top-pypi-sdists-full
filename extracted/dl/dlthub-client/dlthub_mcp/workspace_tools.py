"""Tools that answer where the agent is and, on the platform, what it is.

Orientation reads, meant to be called once rather than per question.
"""

from __future__ import annotations

# Python internals
from dataclasses import dataclass
from datetime import datetime
from typing import Mapping, Optional

# Other libraries
from dlt.common.typing import Annotated

# Current package
from dlthub_mcp._access import CONTEXT_READ
from dlthub_mcp._client import runtime, setting, tool, tool_error, workspace
from dlthub_sdk import JobRun, Sync, WorkspaceMember
from dlthub_sdk.errors import DlthubError

#: Members returned when the caller does not say, and the ceiling it may ask for.
MEMBERS = 50
MAX_MEMBERS = 200


@dataclass(frozen=True)
class WorkspaceInfo:
    """Everything the platform knows about the workspace the agent is reading.

    Attributes:
        id: The workspace's uuid, which every other tool addresses it by.
        name: Its name, which need not be unique.
        description: Free-text description, or ``None``.
        organization_id: The owning organization's uuid.
        organization_name: The organization's name, or ``None`` when the caller
            may not read the organization. An API key is usually workspace
            scoped, so absence says nothing about the organization existing.
        dataplane_id: The data plane this workspace's data and runs live on.
        playground: Whether this is the caller's auto-created personal
            workspace. A playground is single-member and cannot be renamed.
        profiles: Profile names the platform offers, keyed by access level.
            What a job's ``profile`` is drawn from.
        dashboard_url: Where a human can see this workspace in the web UI.
            Worth quoting when reporting something a person should look at.
        caller_email: Who this tool's credential belongs to.
        caller_role: What the caller may do in this workspace.
        caller_organization_role: What the caller may do in the organization.
        members: Who else has access, and in what role. Empty when the caller
            may not list them.
        members_listed: Whether ``members`` was readable. False separates "not
            allowed to look" from "nobody else here".
        created_at: When the workspace was created.
    """

    id: str
    name: str
    description: str | None
    organization_id: str
    organization_name: str | None
    dataplane_id: str
    playground: bool
    profiles: Mapping[str, str]
    dashboard_url: str
    caller_email: str
    caller_role: str
    caller_organization_role: str
    members: tuple[WorkspaceMember, ...]
    members_listed: bool
    created_at: datetime


@tool
def dlthub_workspace_info(
    members: int = MEMBERS,
) -> Annotated[WorkspaceInfo, CONTEXT_READ]:
    """Where the agent is: the workspace, its organization, and who is in it.

    Reach for this once, before anything else, to learn which workspace the
    credential reaches and what it is called — every other tool addresses this
    workspace implicitly, so this is the only thing that names it. It also
    carries the dashboard URL, which is what to quote when a person should go
    look at something.

    Costs several platform calls, so it is an orientation read rather than
    something to repeat. The organization name and the member list each need
    their own permission; either may be absent without the rest failing.

    Args:
        members: How many members to list, at most 200. Pass 0 to skip the
            member read entirely.

    Returns:
        The workspace's identity, its organization, the caller's own roles, and
        its members.

    Raises:
        Exception: A ``ToolError`` when the credential reaches no workspace.
    """
    held = workspace()
    caller = held.me()

    organization_name = None
    try:
        organization_name = runtime().organizations.get(id=held.organization_id).name
    except DlthubError:
        # Workspace-scoped credentials are the norm, so this is expected.
        pass

    listed: tuple[WorkspaceMember, ...] = ()
    members_listed = False
    if members > 0:
        try:
            listed = tuple(held.members(limit=min(members, MAX_MEMBERS)))
            members_listed = True
        except DlthubError:
            pass

    return WorkspaceInfo(
        id=held.id,
        name=held.name,
        description=held.description,
        organization_id=held.organization_id,
        organization_name=organization_name,
        dataplane_id=held.dataplane_id,
        playground=held.playground,
        profiles=held.predefined_profiles,
        dashboard_url=held.dashboard_url,
        caller_email=caller.email,
        caller_role=caller.role,
        caller_organization_role=caller.organization_role,
        members=listed,
        members_listed=members_listed,
        created_at=held.created_at,
    )


@tool
def dlthub_this_run(
    run_id: Optional[str] = None,
) -> Annotated[JobRun[Sync], CONTEXT_READ]:
    """The run the agent is itself executing inside, when it runs on the platform.

    Reach for this first when running as a job: it answers which run this is
    without being told, so the agent can report against its own number, read its
    own trigger, and follow ``prev_run_id`` back to the run that triggered it —
    which is what a job chained on ``job.success:`` needs to know what it is
    reacting to.

    Only answers on the platform. A developer machine runs inside no run, so
    there is nothing to resolve and this says so.

    Args:
        run_id: Read this run instead of the agent's own. Rarely needed —
            ``dlthub_get_run`` is the tool for an arbitrary run.

    Returns:
        The run, with its number, status, trigger, timings, executed pipelines
        and the run that triggered it.

    Raises:
        Exception: A ``ToolError`` when no run is in scope, or the run is gone.
    """
    wanted = run_id or setting("run_id", "RUNTIME__RUN_ID")
    if not wanted:
        raise tool_error(
            "This process is not a platform run, so there is no run to report. "
            "A run's environment carries RUNTIME__RUN_ID; use dlthub_list_runs "
            "to pick a run instead."
        )
    return workspace().job_runs.get(id=wanted)


__tools__ = (dlthub_workspace_info, dlthub_this_run)
