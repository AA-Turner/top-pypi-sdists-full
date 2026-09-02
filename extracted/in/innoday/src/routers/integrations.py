"""
Unified Integrations Router for External Services

This module consolidates all external service integration endpoints including:
- GitHub/GitLab connections
- Jira/Trello board connections
- Slack integration
- Webhook management
- Integration status monitoring

All endpoints follow the pattern: /api/v1/organizations/{org_id}/integrations/...
"""

import logging
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from uuid import uuid4

from fastapi import (
    APIRouter,
    BackgroundTasks,
    Depends,
    HTTPException,
    status,
)
from pydantic import BaseModel, Field, HttpUrl
from sqlalchemy import func
from sqlmodel import Session, select

from src.database import get_session
from src.domain.board import BoardRegistration, BoardType
from src.domain.organization import Organization, OrganizationRole
from src.domain.project import Project
from src.domain.repository import GitHubOrgRegistration, Repository
from src.domain.user import User
from src.middleware.rbac import (
    get_current_user,
    require_org_role,
    resolve_organization,
)
from src.services.org_credential_service import get_github_credentials

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/api/v1/organizations/{organization_id}/integrations",
    tags=["integrations"],
)


# =============================================================================
# Request/Response Models
# =============================================================================


class IntegrationStatus(BaseModel):
    """Status of a single integration"""

    service: str = Field(..., description="Service name (github, jira, trello, slack)")
    connected: bool = Field(..., description="Whether the integration is connected")
    last_sync: Optional[datetime] = Field(None, description="Last successful sync time")
    error: Optional[str] = Field(None, description="Last error message if any")
    metadata: Dict[str, Any] = Field(
        default_factory=dict, description="Service-specific metadata"
    )


class IntegrationsOverview(BaseModel):
    """Overview of all integrations for an organization"""

    github: IntegrationStatus
    jira: IntegrationStatus
    trello: IntegrationStatus
    slack: IntegrationStatus
    summary: Dict[str, int] = Field(..., description="Summary statistics")


class ServiceConnection(BaseModel):
    """Request model for connecting a service"""

    service: str = Field(..., pattern="^(github|jira|trello|slack)$")
    config: Dict[str, Any] = Field(..., description="Service-specific configuration")
    test_connection: bool = Field(True, description="Test connection before saving")


class CredentialValidation(BaseModel):
    """Result of re-checking a credential the organization already has stored.

    Carries no part of the credential. `github_login` is the GitHub *account*
    the stored token belongs to -- the thing that makes a failure actionable
    ("that token is Alex's personal one") -- not the token.
    """

    service: str = Field(..., description="Service the credential belongs to")
    valid: Optional[bool] = Field(
        ...,
        description=(
            "True if the stored credential still works, False if GitHub "
            "answered no, null if GitHub did not answer (unreachable, "
            "throttled, 5xx) and the check is therefore undetermined"
        ),
    )
    github_org: Optional[str] = Field(
        None, description="GitHub org the credential was checked against"
    )
    github_login: Optional[str] = Field(
        None, description="GitHub account the stored token authenticates as"
    )
    org_access: Optional[bool] = Field(
        None,
        description=(
            "Whether the token can reach github_org; null when none is "
            "configured or the check did not complete (see error)"
        ),
    )
    last_validated_at: Optional[datetime] = Field(
        None, description="Timestamp stamped on this check; null unless valid"
    )
    error: Optional[str] = Field(
        None, description="Why validation failed, if it did (never the credential)"
    )


class WebhookConfig(BaseModel):
    """Webhook configuration for a service"""

    service: str = Field(..., pattern="^(github|jira|trello|slack)$")
    webhook_url: HttpUrl = Field(..., description="Webhook endpoint URL")
    events: List[str] = Field(..., description="Events to subscribe to")
    secret: Optional[str] = Field(None, description="Webhook secret for verification")
    active: bool = Field(True, description="Whether webhook is active")


# =============================================================================
# Helper Functions
# =============================================================================


async def verify_organization_access(
    organization_id: str,
    session: Session,
    user_id: Optional[str] = None,
) -> Organization:
    """Verify organization exists and user has access"""
    org = resolve_organization(organization_id, session)

    # TODO: Add user membership verification when user_id is provided

    return org


# =============================================================================
# Integration Overview Endpoints
# =============================================================================


@router.get("", response_model=IntegrationsOverview)
async def get_integrations_overview(
    organization_id: str,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
    _org: Organization = Depends(require_org_role()),
):
    """
    Get overview of all integrations for an organization.

    Returns the connection status, last sync time, and any errors
    for each supported integration service.
    """
    org = await verify_organization_access(organization_id, session)

    # Check GitHub integration
    github_registration = session.exec(
        select(GitHubOrgRegistration)
        .where(GitHubOrgRegistration.organization_id == organization_id)
        .where(GitHubOrgRegistration.status == "active")
    ).first()

    # `connected` answers from the **credential**, not from the registration row.
    # A registration is created only by `connect_github_organization`, and only when
    # a user is attributable -- discovery and every project sync work perfectly well
    # without one -- so the row's existence answers "did somebody once use the
    # connect endpoint?", not "can this org reach GitHub?". Orgs that reach GitHub
    # daily through a Vault credential and no registration reported
    # `connected: false`. The credential is the thing whose presence or absence
    # actually decides whether a sync can run.
    github_credential = get_github_credentials(session, org.id)

    # `last_sync` answers from `Repository.last_synced_at`, which the discovery pass
    # stamps on every repo it creates or updates (`GitHubConnectService`), i.e. on
    # every real sync. It replaces `registration.last_sync_at`, whose only writer was
    # `RepositorySyncService` -- the org-wide registration sync, whose sole remote
    # caller spent months posting to a path no route served (#652), and which #658
    # deleted outright. So an org syncing daily reported "connected, never synced":
    # the column was accurate, it was simply never written, and now never will be.
    last_repo_sync = session.exec(
        select(func.max(Repository.last_synced_at)).where(
            Repository.organization_id == organization_id
        )
    ).one()

    # `error` is the third field with the same defect, and fixing only the first two
    # would leave the most consequential one lying: `registration.last_error` was
    # also written solely by that deleted path, so an org whose every project sync
    # was failing reported `error: null` beside a `last_sync` that now correctly
    # shows the failure's own age. `Project.github_error_message` is what #641 added and what the
    # dashboard's GitHub icon already reads, and it arrives pre-narrowed through
    # `_reportable_sync_error` -- so it is a string this response may carry, which
    # `str(exc)` would not have been. Newest first, and the registration's copy is
    # still the fallback for an org whose failure predates that column.
    project_error = session.exec(
        select(Project.github_error_message)
        .where(Project.organization_id == organization_id)
        .where(Project.github_errored_at.is_not(None))  # type: ignore[union-attr]
        .order_by(Project.github_errored_at.desc())  # type: ignore[union-attr]
    ).first()

    github_status = IntegrationStatus(
        service="github",
        connected=bool(github_credential),
        last_sync=last_repo_sync,
        error=project_error
        or (github_registration.last_error if github_registration else None),
        metadata={
            # Prefer the credential's own `github_org` -- it is what a sync
            # authenticates against -- and fall back to the registration's copy.
            "organization": (
                (github_credential or {}).get("github_org")
                or (github_registration.organization if github_registration else None)
            ),
            # Counted from the repositories that exist, not from
            # `registration.total_repos_count`: that column is written only by the
            # same never-called registration sync, so it read 0 for every org.
            "total_repos": session.exec(
                select(func.count(Repository.id)).where(
                    Repository.organization_id == organization_id
                )
            ).one(),
            # Whether a registration exists is still worth reporting -- it is what
            # the org-wide bulk-import endpoints key on -- but it is no longer
            # allowed to stand in for "connected".
            "has_org_registration": bool(github_registration),
        },
    )

    # Check Trello integration
    trello_boards = session.exec(
        select(BoardRegistration)
        .where(BoardRegistration.organization_id == organization_id)
        .where(BoardRegistration.board_type == BoardType.TRELLO)
        .where(BoardRegistration.is_active == True)
    ).all()

    trello_status = IntegrationStatus(
        service="trello",
        connected=len(trello_boards) > 0,
        last_sync=max(
            [b.last_sync_at for b in trello_boards if b.last_sync_at], default=None
        ),
        error=None,
        metadata={
            "boards_count": len(trello_boards),
            "board_names": [b.board_name for b in trello_boards],
        },
    )

    # Check Jira integration
    jira_boards = session.exec(
        select(BoardRegistration)
        .where(BoardRegistration.organization_id == organization_id)
        .where(BoardRegistration.board_type == BoardType.JIRA)
        .where(BoardRegistration.is_active == True)
    ).all()

    jira_status = IntegrationStatus(
        service="jira",
        connected=len(jira_boards) > 0,
        last_sync=max(
            [b.last_sync_at for b in jira_boards if b.last_sync_at], default=None
        ),
        error=None,
        metadata={
            "projects_count": len(jira_boards),
            "project_names": [b.board_name for b in jira_boards],
        },
    )

    # Slack integration (check organization settings)
    slack_config = org.settings.get("slack", {}) if org.settings else {}
    slack_status = IntegrationStatus(
        service="slack",
        connected=bool(slack_config.get("webhook_url")),
        last_sync=None,  # Slack doesn't sync, it's event-driven
        error=None,
        metadata={
            "channel": slack_config.get("default_channel"),
            "notifications_enabled": slack_config.get("notifications_enabled", False),
        },
    )

    # Calculate summary statistics
    total_integrations = 4
    connected_count = sum(
        [
            github_status.connected,
            jira_status.connected,
            trello_status.connected,
            slack_status.connected,
        ]
    )

    return IntegrationsOverview(
        github=github_status,
        jira=jira_status,
        trello=trello_status,
        slack=slack_status,
        summary={
            "total": total_integrations,
            "connected": connected_count,
            "disconnected": total_integrations - connected_count,
        },
    )


# =============================================================================
# Service Connection Endpoints
# =============================================================================


@router.post("/{service}/connect", status_code=status.HTTP_201_CREATED)
async def connect_service(
    organization_id: str,
    service: str,
    connection: ServiceConnection,
    background_tasks: BackgroundTasks,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
    _org: Organization = Depends(require_org_role()),
):
    """
    Connect an external service to the organization.

    This endpoint handles the initial connection and configuration
    of external services like GitHub, Jira, Trello, etc.
    """
    org = await verify_organization_access(organization_id, session)

    if service != connection.service:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Service in URL must match service in request body",
        )

    # Handle service-specific connection logic
    if service == "github":
        github_org_name = connection.config.get(
            "organization"
        ) or connection.config.get("github_org")
        if not github_org_name:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="config.organization (GitHub org name) is required",
            )

        github_token = connection.config.get("token") or connection.config.get(
            "github_token"
        )

        if github_token:
            # BUG 1 fix: this is the only path that both validates the token
            # against the real GitHub API and stores the token (in Vault
            # `org_credentials`; it was CredentialProvider when this was written)
            # (previously this endpoint created a GitHubOrgRegistration row
            # without ever storing a usable token -- the org showed as
            # "connected" but discovery/sync had nothing to authenticate
            # with). See GitHubConnectService.connect_github_organization.
            from src.services.github_connect_service import GitHubConnectService

            try:
                result = await GitHubConnectService(
                    session
                ).connect_github_organization(
                    organization_id=organization_id,
                    github_org=github_org_name,
                    github_token=github_token,
                    user_id=current_user.id if current_user else None,
                    force=bool(connection.config.get("force")),
                )
            except ValueError as e:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
                )

            return {
                "status": "connected",
                "service": "github",
                "organization": {
                    "id": org.id,
                    "alias": org.alias,
                    "github_org": result["github_org"],
                },
                "total_repos_discovered": result["total_repos_discovered"],
                "message": "GitHub organization connected successfully",
            }

        # No token provided: fall back to the lighter-weight registration-only
        # path (no live GitHub validation, no credential storage). Callers
        # relying on this should pass config.token to get a fully working
        # connection -- this path exists for backward compatibility only.
        registration = session.exec(
            select(GitHubOrgRegistration).where(
                GitHubOrgRegistration.organization_id == organization_id
            )
        ).first()
        if registration:
            registration.organization = github_org_name
        else:
            registration = GitHubOrgRegistration(
                id=str(uuid4()),
                user_id=current_user.id if current_user else None,
                organization_id=organization_id,
                organization=github_org_name,
                sync_enabled=True,
                sync_readme=connection.config.get("sync_readme", True),
                sync_interval_minutes=connection.config.get("sync_interval", 60),
            )
            session.add(registration)
        session.commit()

        return {
            "status": "connected",
            "service": "github",
            "registration_id": registration.id,
            "organization": {
                "id": org.id,
                "alias": org.alias,
                "github_org": registration.organization,
            },
            "message": (
                "GitHub organization registered (no token provided -- pass "
                "config.token to fully connect and enable repo discovery)"
            ),
        }

    elif service == "trello":
        # Create Trello board registration
        board_url = connection.config.get("board_url")
        board_name = connection.config.get("board_name", "Trello Board")
        project_id = connection.config.get("project_id")

        if not project_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="config.project_id is required -- a board cannot be "
                "registered without a project",
            )
        project = session.exec(
            select(Project).where(
                Project.id == project_id,
                Project.organization_id == organization_id,
            )
        ).first()
        if not project:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Project {project_id} not found in this organization",
            )

        # Extract board ID from URL
        import re

        match = re.search(r"/b/([a-zA-Z0-9]+)", board_url)
        if not match:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid Trello board URL",
            )

        board_registration = BoardRegistration(
            user_id=current_user.id if current_user else None,
            organization_id=organization_id,
            project_id=project_id,
            board_name=board_name,
            board_url=board_url,
            board_type=BoardType.TRELLO,
            board_external_id=match.group(1),
            is_active=True,
        )

        session.add(board_registration)
        session.commit()

        return {
            "status": "connected",
            "service": "trello",
            "registration_id": board_registration.id,
            "message": "Trello board connected successfully",
        }

    elif service == "slack":
        # Update organization settings with Slack configuration
        if not org.settings:
            org.settings = {}

        org.settings["slack"] = {
            "webhook_url": connection.config.get("webhook_url"),
            "default_channel": connection.config.get("channel", "#general"),
            "notifications_enabled": connection.config.get(
                "notifications_enabled", True
            ),
            "connected_at": datetime.now(timezone.utc).isoformat(),
            "connected_by": current_user.id if current_user else None,
        }

        session.add(org)
        session.commit()

        return {
            "status": "connected",
            "service": "slack",
            "message": "Slack workspace connected successfully",
        }

    else:
        raise HTTPException(
            status_code=status.HTTP_501_NOT_IMPLEMENTED,
            detail=f"Service {service} connection not yet implemented",
        )


@router.post("/{service}/validate", response_model=CredentialValidation)
async def validate_service_credential(
    organization_id: str,
    service: str,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
    _org: Organization = Depends(require_org_role(OrganizationRole.ADMIN)),
):
    """
    Re-check the credential this organization has **already stored**, without
    the caller re-supplying it.

    Before this existed, the only way to revalidate was to POST the token again
    to `/{service}/connect`, which requires whoever is asking to still hold it.
    An expired token is not visibly an expired token anywhere else in the
    system: it made onboarding/resolve answer 500 and repository discovery
    answer `[]`.

    Runs the same checks `connect` runs and stamps `last_validated_at` on
    success. The credential is never returned or logged.

    **ADMIN, unlike the sibling routes' bare `require_org_role()`.** This is a
    credential-lifecycle operation, not a read of project data: it exercises
    the organization's stored secret against a third party, writes an audit
    column, and its response names the GitHub account that secret belongs to.
    Any member being able to ask "whose token is the org using?" is a
    disclosure a DEVELOPER or MEMBER has no need for, and rate-limit-wise it
    lets any member drive outbound calls as the org's identity.

    That guard is deliberately *stricter* than `connect`/`disconnect`, which
    write and destroy the same credential behind a bare `require_org_role()`.
    The asymmetry runs the wrong way and this route is not the place to fix it:
    tightening a deployed write route is a behaviour change for its existing
    callers (the `/ui` connect flow, `innoday` onboarding), needs its own
    migration note, and would be invisible in a PR about validation. Left
    deliberately alone, flagged in review of #572 -- do not read this route's
    ADMIN as evidence the sibling routes were considered adequate.

    **A rejected credential is 200 with `valid: false`, not a 4xx.** The
    request was well-formed and the question was answered; that answer is the
    payload. A 400 would say the caller did something wrong, and would give a
    diagnostic endpoint the same shape as a broken one. `404` is reserved for
    "there is no stored credential to check", and `503` for "Vault itself could
    not be read" -- the one failure this endpoint exists to name, so it must not
    arrive as an opaque 500 with the cause only in the server log.

    `valid` is three-valued: true/false are verdicts, **null means GitHub did
    not answer** and nothing was proved. See
    `GitHubConnectService.validate_stored_github_credential`.
    """
    if service != "github":
        # Scoped to what exists. org_credentials holds exactly one integration
        # type; a generic multi-integration validator would be built for a
        # caller that does not exist. Same 501 shape as connect/disconnect.
        raise HTTPException(
            status_code=status.HTTP_501_NOT_IMPLEMENTED,
            detail=f"Service {service} credential validation not yet implemented",
        )

    from src.services.github_connect_service import GitHubConnectService
    from src.services.org_credential_service import VaultUnavailableError

    try:
        result = await GitHubConnectService(session).validate_stored_github_credential(
            organization_id
        )
    except VaultUnavailableError as e:
        # The route whose caller is literally asking "can you read my
        # credential?" must answer that question, not 500. The message names the
        # extension, the function and the grant, and holds no secret.
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=str(e)
        )
    except ValueError as e:
        # Nothing stored, or no such organization -- neither is a failed
        # validation, so it must not come back as valid: false.
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

    logger.info(
        "credential validation for org=%s service=%s by user=%s: valid=%s",
        organization_id,
        service,
        current_user.id if current_user else None,
        result["valid"],
    )
    return CredentialValidation(**result)


@router.delete("/{service}/disconnect", status_code=status.HTTP_204_NO_CONTENT)
async def disconnect_service(
    organization_id: str,
    service: str,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
    _org: Organization = Depends(require_org_role()),
):
    """
    Disconnect an external service from the organization.

    This will deactivate all registrations for the specified service
    but preserve the data for audit purposes.
    """
    org = await verify_organization_access(organization_id, session)

    if service == "github":
        # Deactivate all GitHub registrations
        registrations = session.exec(
            select(GitHubOrgRegistration)
            .where(GitHubOrgRegistration.organization_id == organization_id)
            .where(GitHubOrgRegistration.status == "active")
        ).all()

        for reg in registrations:
            reg.status = "paused"
            reg.sync_enabled = False
            session.add(reg)

    elif service in ["trello", "jira"]:
        # Deactivate all board registrations of this type
        board_type = BoardType.TRELLO if service == "trello" else BoardType.JIRA
        boards = session.exec(
            select(BoardRegistration)
            .where(BoardRegistration.organization_id == organization_id)
            .where(BoardRegistration.board_type == board_type)
            .where(BoardRegistration.is_active == True)
        ).all()

        for board in boards:
            board.is_active = False
            session.add(board)

    elif service == "slack":
        # Remove Slack configuration from organization settings
        if org.settings and "slack" in org.settings:
            org.settings["slack"]["notifications_enabled"] = False
            org.settings["slack"]["disconnected_at"] = datetime.now(
                timezone.utc
            ).isoformat()
            session.add(org)

    else:
        raise HTTPException(
            status_code=status.HTTP_501_NOT_IMPLEMENTED,
            detail=f"Service {service} disconnection not yet implemented",
        )

    session.commit()


# =============================================================================
# Webhook Management Endpoints
# =============================================================================


@router.get("/{service}/webhooks", response_model=List[WebhookConfig])
async def get_service_webhooks(
    organization_id: str,
    service: str,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
    _org: Organization = Depends(require_org_role()),
):
    """
    Get webhook configurations for a service.

    Returns all configured webhooks for the specified service,
    including their URLs, subscribed events, and status.
    """
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Webhook configuration is not stored yet. Not implemented -- this previously returned a fabricated success. See GitHub issue #374.",
    )


@router.post("/{service}/webhooks", status_code=status.HTTP_201_CREATED)
async def create_service_webhook(
    organization_id: str,
    service: str,
    webhook: WebhookConfig,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
    _org: Organization = Depends(require_org_role()),
):
    """
    Create a new webhook for a service.

    This will register a webhook with the external service
    to receive real-time updates for the specified events.
    """
    await verify_organization_access(organization_id, session)

    if service != webhook.service:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Service in URL must match service in webhook config",
        )

    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Webhook creation is not implemented. Not implemented -- this previously returned a fabricated success. See GitHub issue #374.",
    )


@router.delete(
    "/{service}/webhooks/{webhook_id}", status_code=status.HTTP_204_NO_CONTENT
)
async def delete_service_webhook(
    organization_id: str,
    service: str,
    webhook_id: str,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
    _org: Organization = Depends(require_org_role()),
):
    """
    Delete a webhook configuration.

    This will unregister the webhook with the external service
    and remove it from our database.
    """
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Webhook deletion is not implemented. Not implemented -- this previously returned a fabricated success. See GitHub issue #374.",
    )


# =============================================================================
# Synchronization Endpoints
# =============================================================================


@router.get("/{service}/sync/status")
async def get_sync_status(
    organization_id: str,
    service: str,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
    _org: Organization = Depends(require_org_role()),
):
    """
    Get the current synchronization status for a service.

    Returns information about ongoing syncs, last sync time,
    and any errors from recent sync attempts.
    """
    # Of all the fabricated responses in this router this was the worst: it
    # reported `last_sync_status: "success"` with `last_sync` stamped to the
    # moment of the call, so a service that had never synced once was
    # indistinguishable from one that had just succeeded -- and the more recently
    # you asked, the healthier it looked.
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail=(
            "Sync status tracking is not implemented -- this previously "
            "reported a successful sync that never ran. See GitHub issue #374. "
            "For real sync history use GET /boards/{board_id}/sync-history or "
            "GET /projects/{project_id}/repositories/sync-history."
        ),
    )


# =============================================================================
# Service-Specific Configuration Endpoints
# =============================================================================


@router.get("/{service}/config")
async def get_service_config(
    organization_id: str,
    service: str,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
    _org: Organization = Depends(require_org_role()),
):
    """
    Get configuration for a specific service.

    Returns the current configuration settings for the service,
    excluding sensitive information like tokens.
    """
    org = await verify_organization_access(organization_id, session)

    if service == "github":
        registration = session.exec(
            select(GitHubOrgRegistration)
            .where(GitHubOrgRegistration.organization_id == organization_id)
            .where(GitHubOrgRegistration.status == "active")
        ).first()

        if not registration:
            return {"configured": False}

        return {
            "configured": True,
            "organization": registration.organization,
            "sync_readme": registration.sync_readme,
            "sync_interval_minutes": registration.sync_interval_minutes,
            "total_repos": registration.total_repos_count,
        }

    elif service == "slack":
        slack_config = org.settings.get("slack", {}) if org.settings else {}

        if not slack_config:
            return {"configured": False}

        return {
            "configured": True,
            "default_channel": slack_config.get("default_channel"),
            "notifications_enabled": slack_config.get("notifications_enabled"),
            "connected_at": slack_config.get("connected_at"),
        }

    else:
        return {
            "configured": False,
            "message": f"Service {service} not yet implemented",
        }


@router.put("/{service}/config")
async def update_service_config(
    organization_id: str,
    service: str,
    config: Dict[str, Any],
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
    _org: Organization = Depends(require_org_role()),
):
    """
    Update configuration for a specific service.

    Allows updating service-specific settings without
    reconnecting the entire integration.
    """
    await verify_organization_access(organization_id, session)

    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Service configuration updates are not implemented. Not implemented -- this previously returned a fabricated success. See GitHub issue #374.",
    )
