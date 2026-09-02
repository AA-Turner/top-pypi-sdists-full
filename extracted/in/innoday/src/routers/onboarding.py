"""Workspace onboarding resolution endpoint (auth P4, PF-350, §5.2/§5.5).

The server half of ``innoday init``/``join``/``refresh`` and the MCP tool
``setup_project_workspace``: it resolves an org (+ optional project) by alias
and discovers the repos to clone, using its DB + GitHub token. The CLIENT then
performs the local git clone/pull and writes ``.innoday/project.yml`` (the CLI
has no DB access — it is a pure API client — so the split is deliberate).

    GET /api/v1/onboarding/resolve?org=<alias>[&project=<alias>]   [authed]
        → { org:{id,alias,name,github_org}, project:{...}|null,
            github_topic, repos:[{name, clone_url, ssh_url, default_branch}] }

Authorization: any authenticated user may resolve (the sensitive action —
membership — is `join`, handled by the invites router). A non-platform user can
only resolve orgs they belong to; platform users resolve any (the standard
bypass).
"""

from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlmodel import Session, select

from src.database import get_session
from src.domain.organization import OrganizationMembership
from src.domain.user import User
from src.middleware.rbac import get_current_user
from src.services.workspace_onboard import (
    WorkspaceCredentialMissingError,
    WorkspaceOnboardError,
    WorkspaceOnboardService,
)

router = APIRouter(prefix="/api/v1/onboarding", tags=["onboarding"])


class RepoRef(BaseModel):
    name: str
    clone_url: Optional[str] = None
    ssh_url: Optional[str] = None
    default_branch: Optional[str] = None


class OrgRef(BaseModel):
    id: str
    alias: str
    name: str
    github_org: str


class ProjectRef(BaseModel):
    id: str
    alias: str
    name: str


class RemovedRepoRef(BaseModel):
    name: str
    removed_at: Optional[str] = None


class TimelineEntryRef(BaseModel):
    event_type: str
    title: str
    summary: str
    occurred_at: Optional[str] = None
    created_by: Optional[str] = None


class ResolveResponse(BaseModel):
    org: OrgRef
    project: Optional[ProjectRef] = None
    github_topic: Optional[str] = None
    repos: List[RepoRef] = []

    # Everything below is additive and optional: an older CLI ignores unknown
    # keys, so extending this response does not require a project.yml schema
    # bump (readers reject on schema_version INEQUALITY, so a bump would make
    # every older CLI refuse the file outright).
    removed_repos: List[RemovedRepoRef] = []
    additional_context: Optional[str] = None
    project_context_version: Optional[int] = None
    timeline: List[TimelineEntryRef] = []


class ContextPushRequest(BaseModel):
    """What a refresh sends back after rendering the workspace files."""

    org: str
    project: str
    # Omitting either field means "leave it alone". For additional_context
    # that distinction matters: "" is a deliberate clear, None is silence.
    project_context: Optional[str] = None
    template_version: Optional[int] = None
    additional_context: Optional[str] = None


class ContextPushResponse(BaseModel):
    project_context_written: bool
    project_context_version: Optional[int] = None
    additional_context_stored: bool


@router.get("/resolve", response_model=ResolveResponse)
async def resolve_workspace(
    org: str,
    project: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    """Resolve an org/project by alias and list its repos (for the CLI to clone)."""
    svc = WorkspaceOnboardService(session)
    try:
        organization = svc.resolve_org(org)
    except WorkspaceOnboardError as exc:
        raise HTTPException(status_code=404, detail=str(exc))

    # Non-platform users may only resolve orgs they belong to.
    if not current_user.is_platform_member:
        member = session.exec(
            select(OrganizationMembership).where(
                OrganizationMembership.user_id == current_user.id,
                OrganizationMembership.organization_id == organization.id,
                OrganizationMembership.is_active == True,  # noqa: E712
            )
        ).first()
        if not member:
            raise HTTPException(
                status_code=403,
                detail="You are not a member of this organization. "
                "Use `innoday join` (if self-registration is enabled) or accept an invite.",
            )

    try:
        proj = svc.resolve_project(organization.id, project)
    except WorkspaceOnboardError as exc:
        raise HTTPException(status_code=404, detail=str(exc))

    github_org = svc.github_org(organization, proj)
    github_topics = svc.github_topics(organization, proj)
    # Reported back as the comma-separated list the settings map holds, so the
    # response shows every topic the selection covered, not just the first.
    github_topic = ",".join(github_topics) if github_topics else None

    repos: List[RepoRef] = []
    if github_topics:
        try:
            raw = await svc.discover_repos(organization, github_org, github_topics)
        except WorkspaceCredentialMissingError as exc:
            # 400, not 502: this org has no GitHub credential stored, which the
            # caller can fix. A 502 would read as "GitHub is down" and send them
            # looking at the wrong system. Checked before the parent class below.
            raise HTTPException(status_code=400, detail=str(exc))
        except WorkspaceOnboardError as exc:
            raise HTTPException(status_code=502, detail=str(exc))
        repos = [
            RepoRef(
                name=r["name"],
                clone_url=r.get("clone_url"),
                ssh_url=r.get("ssh_url"),
                default_branch=r.get("default_branch"),
            )
            for r in raw
        ]

    return ResolveResponse(
        org=OrgRef(
            id=organization.id,
            alias=organization.alias,
            name=organization.name,
            github_org=github_org,
        ),
        project=(
            ProjectRef(id=proj.id, alias=proj.alias, name=proj.name) if proj else None
        ),
        github_topic=github_topic,
        repos=repos,
        removed_repos=[RemovedRepoRef(**r) for r in svc.removed_repos(proj)],
        # The generated half is never sent back: a client writes the template
        # it ships with, so handing it a newer generation would leave a file
        # it cannot itself reproduce on the next refresh. Only the version is
        # returned, which is all a client needs to know whether its push will
        # be accepted.
        additional_context=(proj.additional_context if proj else None),
        project_context_version=(proj.project_context_version if proj else None),
        timeline=[TimelineEntryRef(**e) for e in svc.recent_timeline(proj)],
    )


@router.post("/context", response_model=ContextPushResponse)
async def push_workspace_context(
    payload: ContextPushRequest,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    """Store the context a refresh just rendered.

    Split from `resolve` rather than folded into it because resolve is a GET
    that `init` also uses, and because the client can only send the generated
    context *after* it has rendered it from the resolve response. Two calls,
    each doing one thing.

    Authorization matches resolve: any member of the org may push, platform
    users may push anywhere. That is deliberate -- this stores a workspace's
    own context, which every member of the project already reads and writes
    locally; gating it more tightly than resolve would mean a developer could
    read the project but silently fail to contribute notes back to it.
    """
    svc = WorkspaceOnboardService(session)
    try:
        organization = svc.resolve_org(payload.org)
    except WorkspaceOnboardError as exc:
        raise HTTPException(status_code=404, detail=str(exc))

    if not current_user.is_platform_member:
        member = session.exec(
            select(OrganizationMembership).where(
                OrganizationMembership.user_id == current_user.id,
                OrganizationMembership.organization_id == organization.id,
                OrganizationMembership.is_active == True,  # noqa: E712
            )
        ).first()
        if not member:
            raise HTTPException(
                status_code=403,
                detail="You are not a member of this organization.",
            )

    try:
        proj = svc.resolve_project(organization.id, payload.project)
    except WorkspaceOnboardError as exc:
        raise HTTPException(status_code=404, detail=str(exc))

    if not proj:
        raise HTTPException(
            status_code=404,
            detail=(
                f"No project '{payload.project}' in organization "
                f"'{payload.org}'. Context is stored per project, so an "
                f"org-only workspace has nowhere to put it."
            ),
        )

    result = svc.store_context(
        proj,
        project_context=payload.project_context,
        template_version=payload.template_version,
        additional_context=payload.additional_context,
    )
    return ContextPushResponse(**result)
