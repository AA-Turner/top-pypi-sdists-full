"""
Authentication API endpoints for InnoDay.

CLI access tokens are durable, revocable rows in ``cli_tokens`` (see
src/domain/cli_token.py) — this replaced the former process-local in-memory
``api_keys_store``. Only the SHA-256 hash is stored; the raw ``idt_...`` value
(PAT) is returned exactly once at mint time.
"""

from datetime import datetime, timedelta, timezone
from typing import Dict, List, Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlmodel import Session, select

from src.database import get_session
from src.domain.cli_token import CLIToken, generate_cli_token, hash_cli_token
from src.domain.organization import Organization, OrganizationMembership
from src.domain.project import Project
from src.domain.user import User
from src.domain.user_identity import IdentityPlatform, MatchSource, UserIdentity
from src.middleware.rbac import get_current_user
from src.services.identity_resolution import (
    HandleAlreadyClaimedError,
    IdentityResolutionService,
)
from src.services.sign_in_link import request_sign_in_link

router = APIRouter(prefix="/api/v1/auth", tags=["authentication"])


def _enum_value(value) -> str:
    """The enum's *value*, whichever half of the divide it arrived from.

    Postgres stores an enum's NAME while the Python member's value is
    lowercase, so the same column reaches here as either -- see CLAUDE.md,
    "Enum casing". Clients compare against the value, so normalise to it.
    """
    return getattr(value, "value", str(value))


class TokenCreate(BaseModel):
    """Request to mint a CLI token (non-device path)."""

    name: str = "cli"
    expires_days: Optional[int] = None


class TokenResponse(BaseModel):
    """Response when a CLI token is minted — the raw token is shown once."""

    id: str
    name: str
    token: str  # only returned here, never again
    expires_at: Optional[datetime]
    created_at: datetime


class TokenInfo(BaseModel):
    """A CLI token's metadata (no secret) for listing."""

    id: str
    name: str
    scopes: List[str]
    last_used_at: Optional[datetime]
    expires_at: Optional[datetime]
    created_at: datetime


class UserProfile(BaseModel):
    """User profile response"""

    id: str
    full_name: str
    email: str
    is_platform_member: bool = False
    organizations: List[Dict[str, str]]
    current_organization: Optional[Dict[str, str]] = None
    identities: List[Dict[str, Optional[str]]] = []
    """The caller's board handles (`user_identity` rows), read-only.

    Added here rather than as a route of its own (PF-398): "which board handles
    are me?" is part of who you are, it is only ever asked about yourself, and
    `/auth/me` is already the one call every client makes to find that out.

    It is also what lets `innoday summary` tell two identical-looking failures
    apart -- a genuinely quiet window, and a caller InnoDay cannot recognise on
    the board -- because only the second has a fix to offer.
    """


class IdentityClaim(BaseModel):
    """Request to map one of the caller's own board handles to a project.

    There is deliberately **no `user_id`**: the route claims for the bearer of
    the token and nobody else, so the ability to claim someone else's handle
    does not exist to be got wrong.
    """

    project_id: str
    platform: str
    handle: str


def _project_for_caller(
    session: Session, user: User, project_ref: str
) -> Optional[Project]:
    """A project the caller may act on, addressed by **id or alias**.

    Accepting only a UUID was a real dead end rather than a strictness: the
    CLI's `--project` takes the same alias every other command takes, so
    `innoday auth identity --set x --project BPAI` answered "Project not
    found" for a project the caller is an admin of, while the identical
    command from inside that project's directory worked — because the cwd
    resolves to an id. The failure named the wrong cause, which is the part
    that wastes someone's afternoon.

    Alias resolution is deliberately **scoped to orgs the caller belongs to**
    (all orgs for a platform member) rather than done globally and then
    authorized. Project aliases are only unique *within* an org, so a global
    alias lookup would resolve `BPAI` to whichever org's row came back first
    and then 404 on the authorization check — telling a member of the right
    org that their own project does not exist. Searching only what they may
    see removes the ambiguity instead of ruling on it afterwards.

    Returns None rather than raising: the caller turns every miss into the
    same 404, so an unauthorized project and an absent one are indistinguish-
    able from outside. That is the point — a distinguishable 403 would confirm
    the existence of another tenant's project.
    """
    from sqlalchemy import func as sa_func

    def _visible(project: Project) -> bool:
        if user.is_platform_member:
            return True
        return (
            session.exec(
                select(OrganizationMembership).where(
                    OrganizationMembership.user_id == user.id,
                    OrganizationMembership.organization_id == project.organization_id,
                    OrganizationMembership.is_active.is_(True),
                )
            ).first()
            is not None
        )

    direct = session.get(Project, project_ref)
    if direct is not None:
        return direct if _visible(direct) else None

    if user.is_platform_member:
        org_ids = None
    else:
        org_ids = [
            row.organization_id
            for row in session.exec(
                select(OrganizationMembership).where(
                    OrganizationMembership.user_id == user.id,
                    OrganizationMembership.is_active.is_(True),
                )
            ).all()
        ]
        if not org_ids:
            return None

    for column, value, unique in (
        (sa_func.upper(Project.alias), project_ref.upper(), True),
        (sa_func.lower(Project.name), project_ref.lower(), False),
    ):
        statement = select(Project).where(column == value)
        if org_ids is not None:
            statement = statement.where(Project.organization_id.in_(org_ids))
        if unique:
            match = session.exec(statement).first()
            if match is not None:
                return match
            continue

        # **Names are not unique**, and this search may span several orgs, so
        # ambiguity is likelier here than in `routers/projects.resolve_project`.
        # Refuse rather than pick: quietly claiming a board handle against
        # whichever project the database happened to return first would map an
        # identity to the wrong project, and the caller would have no way to
        # tell it had happened.
        matches = session.exec(statement.order_by(Project.alias)).all()
        if len(matches) > 1:
            raise HTTPException(
                status_code=409,
                detail=(
                    f"{len(matches)} projects you can see are named "
                    f"{project_ref!r}. Use the alias instead: "
                    + ", ".join(p.alias for p in matches if p.alias)
                ),
            )
        if matches:
            return matches[0]
    return None


def default_org_alias(session: Session, user: User) -> Optional[str]:
    """The alias of a user's default org, or None (→ ``plat0`` in the token).

    Used only to stamp the token's informational org segment; it is never an
    authorization input.
    """
    if not user.default_organization_id:
        return None
    org = session.get(Organization, user.default_organization_id)
    return org.alias if org else None


def mint_cli_token(
    session: Session,
    user_id: str,
    name: str = "cli",
    expires_days: Optional[int] = None,
    kind: str = "pat",
    org_alias: Optional[str] = None,
) -> tuple[CLIToken, str]:
    """Create and persist a CLI token row; return (row, raw_token).

    Shared by the non-device mint endpoint and the device-flow approval path.
    ``kind`` selects the prefix ("pat" | "oauth"); ``org_alias`` is hashed into
    the token's org segment (``plat0`` when None). The raw token is returned to
    the caller once and never stored.
    """
    raw_token = generate_cli_token(kind=kind, org_alias=org_alias)
    expires_at = None
    if expires_days:
        expires_at = datetime.now(timezone.utc) + timedelta(days=expires_days)
    row = CLIToken(
        user_id=user_id,
        token_hash=hash_cli_token(raw_token),
        name=name,
        scopes=["cli"],
        expires_at=expires_at,
    )
    session.add(row)
    session.commit()
    session.refresh(row)
    return row, raw_token


class SignInLinkRequest(BaseModel):
    """Ask for a sign-in link to be emailed.

    ``redirect_to`` is where Supabase returns the browser afterwards. It is not
    validated here on purpose: Supabase matches it against
    ``additional_redirect_urls`` and silently substitutes ``site_url`` when it is
    not listed, so the allowlist in ``supabase/config.toml`` is the guard. A second
    check here would be a second place to forget to update.
    """

    email: str
    redirect_to: str


@router.post("/sign-in-link", status_code=202)
async def request_sign_in_link_route(
    request: SignInLinkRequest,
    session: Session = Depends(get_session),
):
    """Email an existing user a sign-in link.

    Answers ``202 {"status": "sent"}`` whatever happens -- unknown address,
    throttled, upstream failure. Any difference between those responses is an
    oracle for which addresses have accounts, so there is deliberately only one.

    The single exception is a deployment with no identity provider configured,
    which is true for every caller equally and so reveals nothing about anyone.

    Unauthenticated, because the person calling it cannot sign in yet. It is still
    behind the team secret, which the browser never sees -- the Next.js UI calls
    this from its server, so it can send that header where a page script could not.
    """
    reason = request_sign_in_link(
        session, email=request.email, redirect_to=request.redirect_to
    )
    if reason == "not_configured":
        raise HTTPException(
            status_code=503,
            detail="This deployment has no identity provider configured.",
        )
    if reason == "missing_email":
        raise HTTPException(status_code=422, detail="An email address is required.")
    return {"status": "sent"}


@router.get("/tokens", response_model=List[TokenInfo])
async def list_tokens(
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    """List the caller's active (non-revoked) CLI tokens."""
    rows = session.exec(
        select(CLIToken).where(
            CLIToken.user_id == current_user.id,
            CLIToken.revoked_at == None,  # noqa: E711
        )
    ).all()
    return [
        TokenInfo(
            id=r.id,
            name=r.name,
            scopes=r.scopes,
            last_used_at=r.last_used_at,
            expires_at=r.expires_at,
            created_at=r.created_at,
        )
        for r in rows
    ]


@router.post("/tokens", response_model=TokenResponse)
async def create_token(
    request: TokenCreate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    """Mint a new CLI token for the caller (non-device path)."""
    row, raw_token = mint_cli_token(
        session,
        user_id=current_user.id,
        name=request.name,
        expires_days=request.expires_days,
        kind="pat",
        org_alias=default_org_alias(session, current_user),
    )
    return TokenResponse(
        id=row.id,
        name=row.name,
        token=raw_token,
        expires_at=row.expires_at,
        created_at=row.created_at,
    )


@router.delete("/tokens/{token_id}")
async def revoke_token(
    token_id: str,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    """Revoke one of the caller's CLI tokens by id.

    Platform users may revoke any token (cross-org authority, §4); ordinary
    users may revoke only their own.
    """
    row = session.get(CLIToken, token_id)
    if not row:
        raise HTTPException(status_code=404, detail="Token not found")
    if row.user_id != current_user.id and not current_user.is_platform_member:
        raise HTTPException(
            status_code=403, detail="Cannot revoke another user's token"
        )
    row.revoke()
    session.add(row)
    session.commit()
    return {"message": "Token revoked", "id": token_id}


@router.delete("/tokens")
async def revoke_all_tokens(
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    """Revoke all of the caller's CLI tokens.

    `innoday logout` takes no `--all`; this route is reached by the CLI, not by
    a flag somebody types.
    """
    rows = session.exec(
        select(CLIToken).where(
            CLIToken.user_id == current_user.id,
            CLIToken.revoked_at == None,  # noqa: E711
        )
    ).all()
    for row in rows:
        row.revoke()
        session.add(row)
    session.commit()
    return {"message": f"Revoked {len(rows)} tokens"}


@router.get("/me", response_model=UserProfile)
async def get_current_user_profile(
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    """Get current authenticated user's profile"""
    memberships = session.exec(
        select(OrganizationMembership, Organization)
        .join(Organization)
        .where(OrganizationMembership.user_id == current_user.id)
    ).all()

    organizations = []
    current_org = None
    for membership, org in memberships:
        org_info = {"id": org.id, "name": org.name, "alias": org.alias}
        organizations.append(org_info)
        if not current_org:
            current_org = org_info

    # A project row shadows a global one for the same platform, so order by
    # scope: the reader sees the specific mapping above the fallback it beats.
    identity_rows = session.exec(
        select(UserIdentity, Project)
        .outerjoin(Project, Project.id == UserIdentity.project_id)
        .where(UserIdentity.user_id == current_user.id)
        .order_by(UserIdentity.platform, UserIdentity.handle)
    ).all()

    return UserProfile(
        id=current_user.id,
        full_name=current_user.full_name,
        email=current_user.email,
        is_platform_member=current_user.is_platform_member,
        organizations=organizations,
        current_organization=current_org,
        identities=[
            {
                "platform": _enum_value(identity.platform),
                "handle": identity.handle,
                # NULL project_id is not missing data -- it is the *global*
                # handle, the one auto-matching draws from. Name it, so a
                # reader is never left guessing what an empty column meant.
                "project": project.alias if project else None,
                "scope": "project" if identity.project_id else "global",
                "match_source": _enum_value(identity.match_source),
            }
            for identity, project in identity_rows
        ],
    )


@router.put("/me/identities", response_model=UserProfile)
async def claim_my_identity(
    body: IdentityClaim,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    """Register one of *your own* board handles, scoped to one project.

    The counterpart write to `/auth/me`'s read, and deliberately self-only:
    there is no `user_id` in the body, so this can never claim a handle on
    someone else's behalf.

    **Why it exists at all.** Until this route, the only way to map an identity
    was the `/ui/{org}/profile` form. So a personal summary run from a terminal
    dead-ended on "map it at /ui/…/profile" — an instruction the CLI could
    print and could not carry out, on the one platform surface whose whole
    premise is that agents and skills drive it through the CLI. That made
    `innoday summary` (personal) unreachable to every non-browser caller.

    Mirrors the profile page's semantics exactly, because two write paths that
    disagree about identity are worse than one: at most one handle per person
    per platform per project (the previous one is removed), a conflicting claim
    is refused rather than stolen, and the source is recorded as MANUAL.
    """
    project = _project_for_caller(session, current_user, body.project_id)
    if project is None:
        raise HTTPException(status_code=404, detail="Project not found")

    try:
        platform = IdentityPlatform(body.platform.lower())
    except ValueError:
        raise HTTPException(
            status_code=422,
            detail=(
                "Unknown platform. One of: "
                + ", ".join(p.value for p in IdentityPlatform)
            ),
        )

    handle = body.handle.strip()
    if not handle:
        raise HTTPException(status_code=422, detail="handle must not be empty")

    conflict = IdentityResolutionService.find_conflicting_claim(
        session,
        user_id=current_user.id,
        platform=platform,
        handle=handle,
        organization_id=project.organization_id,
        project_id=project.id,
    )
    if conflict is not None:
        raise HTTPException(
            status_code=409,
            detail="That handle is already linked to another user",
        )

    # Only once the claim is known to be accepted: one handle per person per
    # platform per project, so the previous one goes. Ordered exactly as the
    # profile page does it — deleting first and then failing the claim would
    # leave the person with no mapping at all.
    for stale in session.exec(
        select(UserIdentity).where(
            UserIdentity.user_id == current_user.id,
            UserIdentity.project_id == project.id,
            UserIdentity.platform == platform,
            UserIdentity.handle != handle,
        )
    ).all():
        session.delete(stale)
    session.flush()

    try:
        IdentityResolutionService.claim_identity(
            session,
            user_id=current_user.id,
            platform=platform,
            handle=handle,
            organization_id=project.organization_id,
            project_id=project.id,
            match_source=MatchSource.MANUAL,
        )
    except HandleAlreadyClaimedError:
        # Raced between the check above and here. Roll back so the delete does
        # not survive a claim that did not.
        session.rollback()
        raise HTTPException(
            status_code=409,
            detail="That handle is already linked to another user",
        )

    session.commit()
    return await get_current_user_profile(current_user=current_user, session=session)


@router.post("/confirm-email")
async def confirm_email(
    current_user: User = Depends(get_current_user),
):
    """Mirror IdP email confirmation into InnoDay. Called by /ui/auth/callback.

    A Supabase invite/magic link is verified at Supabase's own
    ``/auth/v1/verify`` endpoint, which sets ``auth.users.email_confirmed_at``
    and *then* redirects the browser here. InnoDay's own
    ``users.email_verified_at`` is a separate column, and it is only written
    when a Supabase JWT reaches the API — so without this call the person is
    confirmed at the IdP but still unverified here, and would be locked out the
    moment ``REQUIRE_VERIFIED_EMAIL`` is switched on.

    The work happens in the dependency: resolving the caller from a Supabase
    JWT (``_user_from_supabase_jwt``) links ``supabase_user_id`` and mirrors
    ``email_confirmed_at`` as a side effect. This endpoint just reports the
    result, so it stays correct if that logic changes.

    **Exempt from the team secret** (see ``EXEMPT_PATHS``): the browser arrives
    from an email and cannot send that header — the same reasoning as
    ``/ui/invite/accept`` and the device-flow routes. It is not unauthenticated:
    it requires a JWKS-verified Supabase JWT, and a caller can only ever
    confirm themselves.
    """
    return {
        "email": current_user.email,
        "verified": current_user.email_verified,
        "verified_at": current_user.email_verified_at,
    }


@router.get("/users/{user_id}/organizations")
async def get_user_organizations(
    user_id: str,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    """Get organizations for a specific user (must be same user or platform)."""
    if user_id != current_user.id and not current_user.is_platform_member:
        raise HTTPException(status_code=403, detail="Access denied")

    memberships = session.exec(
        select(OrganizationMembership, Organization)
        .join(Organization)
        .where(OrganizationMembership.user_id == user_id)
    ).all()

    return [
        {"id": org.id, "name": org.name, "alias": org.alias, "role": membership.role}
        for membership, org in memberships
    ]
