"""Board and commit handle → user mappings, over the API (#569).

**Why this exists: mapping was UI-only.** `POST /ui/{org}/team/map` was the sole
way to say who a handle belongs to, so it could not be scripted, could not happen
during onboarding, and could not be done by an agent. That gap was hit for real —
`dgillen27` resolved to nobody, so two open pull requests were attributed to no
one on BPAI, and it was fixed by writing to the database by hand because no admin
path existed.

**Two columns, one question, and the API must not repeat the UI's mistake.** A
GitHub login lives in `users.github_username`; a board handle lives in
`user_identity`. Until #569 `IdentityResolutionService.resolve` read only the
second, so the Team page's commit-handle mapping silenced its own unmapped list
without making the author resolvable anywhere. `resolve` now consults both, which
is what makes a single write enough — so these routes write exactly one place per
kind and nothing has to be kept in step.

**One write is enough for the mapping; the board's history is a separate
matter.** Summaries re-resolve a GitHub login on every run, but `board_sync_service`
resolves once and *persists* `ticket.assigned_to`, so a board mapping would leave
every ticket already synced unattributed until somebody re-synced. `POST` therefore
also does what the next sync would do to those rows, and `DELETE` releases them
again — see `_attribute_synced_tickets`. That is a denormalised copy being kept in
step, not a second source of truth: the mapping still lives in exactly one place.

Admin-only for the writes, matching the Team page: a mapping reattributes somebody's
work in every summary that follows, so it is not a thing any member may do. Reading
is open to any member — knowing who a handle belongs to is not a privilege.
Reversible for the same reason — a wrong mapping is worse than a missing one, so
`DELETE` is a first-class operation rather than an afterthought.

**Everything here is scoped to the organization in the path**, on the read side as
much as the write side. `UserIdentity` carries no `organization_id`, so that scope
has to be derived rather than assumed — see `_org_scoped_rows`, which also records
what a global (`project_id IS NULL`) row means here. `?unmapped=true` derives it a
second way, from the org's projects — see `_unmapped_rows`.

**Listing what is *not* mapped is half the feature.** Adding the write without it
left discovery on the Team page, which is exactly the browser dependency #569
existed to remove: an operator onboarding an org has no way to find the handles
that need mapping without one. `?unmapped=true` answers from the same function
that page's panel reads, so a script and the page cannot disagree.
"""

import logging
from typing import List, Optional, Union

from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel, Field
from sqlalchemy import or_
from sqlmodel import Session, select

from src.database import get_session
from src.domain.organization import (
    Organization,
    OrganizationMembership,
    OrganizationRole,
)
from src.domain.project import Project
from src.domain.ticket import Ticket
from src.domain.user import User
from src.domain.user_identity import IdentityPlatform, MatchSource, UserIdentity
from src.middleware.rbac import (
    require_org_role,
    resolve_organization,
    resolve_project_ref,
)
from src.services.identity_resolution import (
    HandleAlreadyClaimedError,
    IdentityResolutionService,
)

# The org's unmapped handles, from the one function that already computes them.
#
# **Reused rather than reimplemented, on purpose.** `unmapped_handles` is what
# the Team page's panel reads, and the whole point of `?unmapped=true` is that a
# scripted caller and that page must never disagree about who still needs
# mapping -- a second query answering "nearly the same" is how the two halves of
# #569 came apart in the first place.
#
# It used to live in `src/routers/webui/data.py`, which made this line the only
# `src.routers.webui.*` import from outside that package: an API router
# depending on the UI that is being retired, so the retirement would have had to
# route around a live endpoint. Moved here rather than left as a follow-up --
# see `tests/test_webui_is_not_imported_outside_webui.py`, which keeps the edge
# from coming back.
from src.services.summary_service import unmapped_handles

logger = logging.getLogger(__name__)

router = APIRouter(tags=["identities"])


class IdentityCreate(BaseModel):
    """Who a handle belongs to."""

    user: str = Field(
        ...,
        description=(
            "The person, by email or user id. Email is accepted because an admin "
            "knows the address and not the uuid."
        ),
    )
    platform: IdentityPlatform = Field(
        ..., description="Which system the handle comes from"
    )
    handle: str = Field(
        ...,
        max_length=255,
        description=(
            "The board's or GitHub's own identifier — usually a display name, or a "
            "login for github"
        ),
    )
    project_id: Optional[str] = Field(
        None,
        description=(
            "Scope a board handle to one project, shadowing any global row. "
            "Ignored for github, which is one login per person platform-wide."
        ),
    )


class IdentityResponse(BaseModel):
    id: Optional[str]
    user_id: str
    user_email: Optional[str]
    platform: str
    handle: str
    project_id: Optional[str]
    match_source: Optional[str]
    #: Where this mapping is stored. `github_username` is a column on the user;
    #: everything else is a `user_identity` row. Surfaced because it decides what
    #: `DELETE` has to touch, and because a caller comparing two mappings should
    #: not have to infer it from the platform.
    stored_as: str
    #: How many already-synced tickets this call re-attributed. Surfaced because
    #: it is the difference between "future syncs will get this right" and "the
    #: board's history now reads correctly", and the caller cannot tell which
    #: happened from a 201 alone. Always 0 on a listing, which writes nothing.
    tickets_reattributed: int = 0


class UnmappedHandleResponse(BaseModel):
    """A handle on this organization's work that currently names nobody.

    **A different shape from `IdentityResponse`, because it is a different
    fact.** There is no user, so `user_id` and `user_email` would be null on
    every row; and an unmapped *board* handle has no platform -- it is a
    `Ticket.assignee` string grouped across whatever boards the project has, and
    the grouping does not carry `source_platform`. Squeezing it into the mapping
    model would mean inventing both, which is how a listing starts lying about
    what it knows. `kind` is the honest discriminator instead.
    """

    #: `board` -- a `Ticket.assignee` string no sync could attribute.
    #: `commit` -- a pull-request author login matching no member's GitHub login.
    kind: str
    handle: str
    #: What is behind the name, for triage: "3 tickets", "2 open pull requests".
    #: Free text on purpose -- the two kinds count different things, and a shared
    #: numeric field would need a unit beside it to be readable anyway.
    detail: str


def _org_scoped_rows(
    session: Session,
    org: Organization,
    *,
    platform: Optional[IdentityPlatform] = None,
    handle: Optional[str] = None,
) -> List[UserIdentity]:
    """The `user_identity` rows that belong to this organization.

    **`UserIdentity` carries no `organization_id`, so the scope has to be
    derived, and "the row's owner is a member of my org" is not it.** A user in
    two organizations is ordinary — a contractor, or any platform member, for
    whom `verify_org_membership` synthesises an ADMIN membership in *every* org
    — so an owner-only filter let an admin of org A list and delete a row that
    belongs entirely to org B's project. Org is the tenancy boundary (CLAUDE.md,
    "Architecture"); `find_conflicting_claim` already took the trouble to scope
    the *claim* rule to one org, and read and delete get the same treatment
    rather than a weaker one.

    A **project-scoped** row reaches its org through `Project.organization_id`,
    which is what the JOIN below asserts.

    A **global** row (`project_id IS NULL`) has no project and therefore no org
    of its own, so it is included here and left to the caller's membership check
    — deliberately, and for the same reason `resolve` honours a global row only
    for a member: an org's members are exactly who that row answers *for* here.
    The consequence is real and is the model's limitation, not an oversight:
    deleting a global row also stops it answering in any other org its owner
    belongs to. The alternative — refusing to delete global rows — would leave
    `--map` (which creates precisely one, whenever `--project` is omitted) with
    no matching `--unmap`, and an irreversible mapping is the thing these routes
    exist to avoid. A per-org global row would need an `organization_id` column
    on the table; until then, one person's handle is one person's handle.
    """
    stmt = (
        select(UserIdentity)
        .join(Project, Project.id == UserIdentity.project_id, isouter=True)
        .where(
            or_(
                UserIdentity.project_id.is_(None),
                Project.organization_id == org.id,
            )
        )
    )
    if platform is not None:
        stmt = stmt.where(UserIdentity.platform == platform)
    if handle is not None:
        stmt = stmt.where(UserIdentity.handle == handle)
    return list(session.exec(stmt).all())


def _tickets_carrying_handle(
    session: Session,
    org: Organization,
    *,
    platform: IdentityPlatform,
    handle: str,
    project_id: Optional[str],
) -> List[Ticket]:
    """Already-synced tickets whose board assignee is this handle.

    `source_platform` is the board type the row came from, so it is what tells a
    Linear "Sam Patel" from a Jira one; `assignee` is the board's raw display
    name, matched exactly, which is the same match `resolve` makes.
    """
    stmt = select(Ticket).where(
        Ticket.organization_id == org.id,
        Ticket.source_platform == platform.value,
        Ticket.assignee == handle,
    )
    if project_id:
        stmt = stmt.where(Ticket.project_id == project_id)
    return list(session.exec(stmt).all())


def _attribute_synced_tickets(
    session: Session,
    org: Organization,
    *,
    user: User,
    platform: IdentityPlatform,
    handle: str,
    project_id: Optional[str],
) -> int:
    """Point already-synced tickets at the person the handle now names.

    **Without this, one write is not enough for a board handle.** Summaries
    re-resolve a GitHub login on every run, which is why mapping one takes
    effect immediately; `board_sync_service` does the opposite — it resolves
    once and *persists* `ticket.assigned_to` (see `_create_or_update_ticket`).
    So a Linear or Jira mapping fixed future syncs and left every ticket already
    in the table unattributed until somebody happened to re-sync — which is not
    something the person who made the mapping can see.

    Does exactly what the next sync would do, and no more: only where
    `assigned_to` is currently NULL, so an attribution the email path already
    made is never overwritten. Email is checked before the handle, so such a
    ticket would resolve to the same person again anyway, and the row keeps no
    record of which path set it.
    """
    changed = 0
    for ticket in _tickets_carrying_handle(
        session, org, platform=platform, handle=handle, project_id=project_id
    ):
        if ticket.assigned_to is not None:
            continue
        ticket.assigned_to = user.id
        session.add(ticket)
        changed += 1
    return changed


def _unattribute_synced_tickets(
    session: Session,
    org: Organization,
    *,
    user_id: str,
    platform: IdentityPlatform,
    handle: str,
    project_id: Optional[str],
) -> int:
    """Undo what `_attribute_synced_tickets` could have done.

    Matched on the handle *and* the user it was mapped to, so it can only
    release attributions this mapping is capable of having produced. Leaving
    them behind would make an unmap look reversible and leave the wrong person
    credited on every ticket already synced — the same half-done state the
    mapping direction exists to avoid.
    """
    changed = 0
    for ticket in _tickets_carrying_handle(
        session, org, platform=platform, handle=handle, project_id=project_id
    ):
        if ticket.assigned_to != user_id:
            continue
        ticket.assigned_to = None
        session.add(ticket)
        changed += 1
    return changed


def _resolve_user(session: Session, org: Organization, who: str) -> User:
    """The person named by an email or an id, if they are in this organisation.

    404 rather than 403 for a non-member, matching the pages: revealing that a
    user exists but is outside the org tells a caller something about the platform
    they have no claim to.
    """
    wanted = (who or "").strip()
    if not wanted:
        raise HTTPException(status_code=422, detail="A user email or id is required.")

    user = session.exec(select(User).where(User.email == wanted)).first()
    if user is None:
        user = session.get(User, wanted)
    if user is None:
        raise HTTPException(status_code=404, detail=f"No such user: {wanted}")

    membership = IdentityResolutionService.active_member(
        session, user_id=user.id, organization_id=org.id
    )
    if membership is None:
        raise HTTPException(
            status_code=404,
            detail=(
                f"{user.email} is not an active member of this organization, so a "
                "handle cannot be mapped to them — resolution would refuse the "
                "match anyway."
            ),
        )
    return user


def _unmapped_rows(session: Session, org: Organization) -> List[UnmappedHandleResponse]:
    """The handles on this org's work that resolve to nobody.

    **The project filter is what scopes the *work* being examined.**
    `unmapped_handles` derives every candidate handle from the project ids it is
    handed -- board assignees through `Ticket.project_id`, commit logins through
    `ProjectRepository` -- so a query that forgot `Project.organization_id ==
    org.id` would answer with every tenant's unmapped handles to any member of
    any org. That is the same hole #593 had to close on the mapping listing,
    reached by a different route: there the rows had to be joined back to an org
    through their project, here the projects are the join.

    It is **not** the whole of the scope, which is why `org.id` is passed too and
    no longer ignored. Deciding which of those handles is already *mapped* means
    reading users and `user_identity` rows, and neither is reachable from a
    project id -- so that half is scoped by `organization_id` inside
    `unmapped_handles`. Passing the projects alone let any tenant's mapping
    suppress a row here.
    """
    project_ids = list(
        session.exec(select(Project.id).where(Project.organization_id == org.id)).all()
    )
    return [
        UnmappedHandleResponse(kind=row.kind, handle=row.handle, detail=row.detail)
        for row in unmapped_handles(session, org.id, project_ids)
    ]


@router.get(
    "/api/v1/organizations/{org_id}/identities",
    response_model=List[Union[IdentityResponse, UnmappedHandleResponse]],
    summary="List handle mappings for this organization",
)
async def list_identities(
    org_id: str,
    session: Session = Depends(get_session),
    _org: Organization = Depends(require_org_role()),
    platform: Optional[IdentityPlatform] = Query(
        None, description="Only this platform"
    ),
    unmapped: bool = Query(
        False,
        description=(
            "Invert the question: instead of the mappings that exist, the "
            "handles on this org's work that resolve to nobody."
        ),
    ),
) -> List[Union[IdentityResponse, UnmappedHandleResponse]]:
    """Every mapping this organisation's resolution can currently use.

    Both stores in one list, because "who is this handle?" is one question and a
    caller should not have to know that GitHub logins live somewhere else.

    Scoped twice, and both are load-bearing. **To this organization** (see
    `_org_scoped_rows`): another tenant's project-scoped row is not this org's
    to read, and listing one leaked its handle and its project id. **To active
    members**: a mapping to somebody outside the org is one `resolve` would
    refuse, so listing it would describe a mapping that does not work.

    **`?unmapped=true` asks the opposite question, and it is the one an operator
    actually starts from.** #569's premise was that mapping was UI-only; adding
    the write without this left the only way to *discover* what needs mapping
    being to read the Team page, which is the dependency #569 set out to remove.
    It answers from `unmapped_handles` -- the same function behind that page's
    panel -- so the two can never disagree, and it is open to any member for the
    same reason the mapping listing is.

    Neither half asks `IdentityResolutionService` per handle, and the two are
    honest about that in different ways.

    The **commit** half consults both stores this organization's resolution
    would, and only this organization's: active members' `users.github_username`
    plus the github `user_identity` rows that belong here. That was not true
    until #598's review. It read the column alone, so a login mapped by a row --
    which since #593 *beats* the column -- came back mapped from this listing and
    unmapped from `?unmapped=true`, in the same request, with `POST` then
    answering 409 about a person it would not name. It also carried no org
    filter, so another tenant's mapping suppressed a row here that `resolve`
    would have called unmapped. See `unmapped_handles`.

    The **board** half reads `ticket.assigned_to` -- a persisted attribution, not
    a live resolution -- which is what "resolves to nobody" means to the surfaces
    that show it. A `user_identity` row written while tickets were already synced
    is reconciled by `POST` here (see `_attribute_synced_tickets`), so the two
    agree in practice; a row written by any other path leaves the board handle
    listed until the next sync re-resolves it. Unlike the commit divergence
    above, that one is temporary by construction.
    """
    org = resolve_organization(org_id, session)

    if unmapped:
        if platform is not None:
            # Refused rather than ignored. An unmapped board handle carries no
            # platform (see `UnmappedHandleResponse`), so `?platform=linear`
            # could only be honoured by guessing one -- and silently dropping
            # the filter would answer a question the caller did not ask while
            # looking like it had.
            raise HTTPException(
                status_code=422,
                detail=(
                    "platform cannot be combined with unmapped: an unmapped "
                    "board handle has no platform recorded. Filter the "
                    "response on `kind` instead (board or commit)."
                ),
            )
        return list(_unmapped_rows(session, org))

    # Active members only, as a JOIN. A mapping to somebody outside the org is one
    # `resolve` would refuse, so listing it would describe a mapping that does not
    # work.
    members = {
        u.id: u
        for u in session.exec(
            select(User)
            .join(OrganizationMembership, OrganizationMembership.user_id == User.id)
            .where(
                OrganizationMembership.organization_id == org.id,
                OrganizationMembership.is_active.is_(True),
            )
        ).all()
    }

    out: List[IdentityResponse] = []
    for row in _org_scoped_rows(session, org, platform=platform):
        if row.user_id not in members:
            continue
        out.append(
            IdentityResponse(
                id=row.id,
                user_id=row.user_id,
                user_email=members[row.user_id].email,
                platform=str(getattr(row.platform, "value", row.platform)),
                handle=row.handle,
                project_id=row.project_id,
                match_source=str(getattr(row.match_source, "value", row.match_source)),
                stored_as="user_identity",
            )
        )

    if platform in (None, IdentityPlatform.GITHUB):
        for user in members.values():
            if not (user.github_username or "").strip():
                continue
            out.append(
                IdentityResponse(
                    id=None,
                    user_id=user.id,
                    user_email=user.email,
                    platform=IdentityPlatform.GITHUB.value,
                    handle=user.github_username,
                    project_id=None,
                    match_source=MatchSource.MANUAL.value,
                    stored_as="github_username",
                )
            )
    out.sort(key=lambda r: (r.platform, r.handle.lower()))
    return out


@router.post(
    "/api/v1/organizations/{org_id}/identities",
    response_model=IdentityResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Map a handle to a user (org admin only)",
)
async def create_identity(
    org_id: str,
    body: IdentityCreate,
    session: Session = Depends(get_session),
    _org: Organization = Depends(require_org_role(OrganizationRole.ADMIN)),
) -> IdentityResponse:
    """Say who a handle belongs to.

    **One write per kind.** A `github` handle sets `users.github_username`, which
    is the column the profile page writes and — since #569 — the one `resolve`
    consults for that platform. Anything else creates a `user_identity` row. There
    is deliberately no path that writes both: two sources for one fact is what
    made the Team page's mapping look like it worked while changing nothing.

    409 when somebody else in this organisation already holds the handle, naming
    the handle but **not** its current owner: echoing that would turn a mapping
    call into a way to enumerate who is on the board by guessing display names —
    the same reasoning the profile page's duplicate message follows.

    **Both stores are consulted for that clash, including on the github path.**
    Checking only `users.github_username` there meant a login already registered
    as somebody's `user_identity` row was taken with a 201, and every commit of
    theirs quietly reattributed — the precise harm this route exists to prevent.
    """
    org = resolve_organization(org_id, session)
    # A body field, so `normalize_path_refs` never saw it -- and it is written to
    # `user_identity.project_id`, a validated non-deferrable FK, so an alias was
    # a 500 rather than a wrong row. `--project PF` is how every other command
    # names a project.
    body.project_id = resolve_project_ref(body.project_id, org.id, session)
    user = _resolve_user(session, org, body.user)
    handle = body.handle.strip()
    if not handle:
        raise HTTPException(status_code=422, detail="handle must not be empty")

    if body.platform == IdentityPlatform.GITHUB:
        github_conflict = (
            f"The GitHub login {handle!r} is already mapped to another "
            "member of this organization."
        )
        clash = session.exec(
            select(User).where(
                User.github_username == handle,
                User.id != user.id,
            )
        ).first()
        if clash is not None and IdentityResolutionService.active_member(
            session, user_id=clash.id, organization_id=org.id
        ):
            raise HTTPException(status_code=409, detail=github_conflict)
        # The other store. A `user_identity` row for this login now beats the
        # column (see `IdentityResolutionService.resolve`), so taking the handle
        # anyway would answer 201 for a mapping that never fires — while the
        # older, deliberate row keeps the commits. Same message either way, so
        # the two paths cannot be told apart by a caller probing for names.
        registered = next(
            (
                row
                for row in _org_scoped_rows(
                    session, org, platform=IdentityPlatform.GITHUB, handle=handle
                )
                if row.user_id != user.id
                and IdentityResolutionService.active_member(
                    session, user_id=row.user_id, organization_id=org.id
                )
            ),
            None,
        )
        if registered is not None:
            logger.info(
                "identity.conflict org=%s github=%s: held by a user_identity row",
                org.id,
                handle,
            )
            raise HTTPException(status_code=409, detail=github_conflict)

        # Both halves of the pair, the way the profile page writes them
        # (`connected=bool(handle)`): `github_connected` means "we know this
        # person's GitHub login", so setting one without the other leaves the
        # profile page and `GET /users/{id}/integrations` disagreeing with the
        # column they both read. `DELETE` clears the pair for the same reason.
        user.github_username = handle
        user.github_connected = True
        session.add(user)
        reattributed = _attribute_synced_tickets(
            session,
            org,
            user=user,
            platform=IdentityPlatform.GITHUB,
            handle=handle,
            project_id=None,
        )
        session.commit()
        logger.info("identity.mapped org=%s github=%s user=%s", org.id, handle, user.id)
        return IdentityResponse(
            id=None,
            user_id=user.id,
            user_email=user.email,
            platform=IdentityPlatform.GITHUB.value,
            handle=handle,
            project_id=None,
            match_source=MatchSource.MANUAL.value,
            stored_as="github_username",
            tickets_reattributed=reattributed,
        )

    try:
        identity = IdentityResolutionService.claim_identity(
            session,
            user_id=user.id,
            platform=body.platform,
            handle=handle,
            organization_id=org.id,
            project_id=body.project_id,
            match_source=MatchSource.MANUAL,
        )
    except HandleAlreadyClaimedError as exc:
        # The exception carries the current owner; the response deliberately does
        # not.
        logger.info("identity.conflict org=%s handle=%s: %s", org.id, handle, exc)
        raise HTTPException(
            status_code=409,
            detail=(
                f"The handle {handle!r} is already mapped to another member of "
                "this organization."
            ),
        )
    reattributed = _attribute_synced_tickets(
        session,
        org,
        user=user,
        platform=body.platform,
        handle=handle,
        project_id=body.project_id,
    )
    session.commit()
    logger.info(
        "identity.mapped org=%s platform=%s handle=%s user=%s tickets=%s",
        org.id,
        body.platform.value,
        handle,
        user.id,
        reattributed,
    )
    return IdentityResponse(
        id=identity.id,
        user_id=identity.user_id,
        user_email=user.email,
        platform=str(getattr(identity.platform, "value", identity.platform)),
        handle=identity.handle,
        project_id=identity.project_id,
        match_source=str(
            getattr(identity.match_source, "value", identity.match_source)
        ),
        stored_as="user_identity",
        tickets_reattributed=reattributed,
    )


@router.delete(
    "/api/v1/organizations/{org_id}/identities",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Unmap a handle (org admin only)",
)
async def delete_identity(
    org_id: str,
    platform: IdentityPlatform = Query(..., description="Which system"),
    handle: str = Query(..., description="The handle to unmap"),
    session: Session = Depends(get_session),
    _org: Organization = Depends(require_org_role(OrganizationRole.ADMIN)),
) -> None:
    """Undo a mapping.

    **By (platform, handle) rather than by id**, because a `github` mapping has no
    id — it is a column on the user — and a caller undoing a mistake knows what
    they typed, not which of the two stores it landed in.

    A wrong mapping reattributes somebody else's work in every summary that
    follows, so this is as easy as making one. Idempotent: unmapping something that
    is not mapped answers 204 rather than 404, since the caller's intent is already
    satisfied and there is nothing for them to do about it.

    **Scoped to this organization**, exactly as the listing is — an admin of one
    tenant deleting another tenant's mapping is worse than reading it, because
    nothing about it is visible afterwards. See `_org_scoped_rows`, including
    what a global row means here.

    **Unmapping a github handle clears `users.github_connected` with it.** That
    column is not an OAuth fact this route is trampling on: the profile page
    writes it as `connected=bool(handle)`, so it means "we know this person's
    GitHub login", and blanking the login while leaving it True leaves the
    profile page and `GET /users/{id}/integrations` reporting "connected,
    username unknown". Refusing to blank an automatically-derived value was the
    alternative and is not implementable — the column carries no provenance, so
    a login written by an account connection is indistinguishable from one an
    admin typed on the Team page, and refusing would make the mistake this route
    exists to undo the one mistake it could not. The cost is real and belongs in
    the CLI's warning rather than in a refusal: their `my_pull_requests` panel
    goes empty until a login is set again, which is honest, since without a
    login nothing can be attributed to them.
    """
    org = resolve_organization(org_id, session)
    wanted = handle.strip()

    if platform == IdentityPlatform.GITHUB:
        for user in session.exec(
            select(User).where(User.github_username == wanted)
        ).all():
            if IdentityResolutionService.active_member(
                session, user_id=user.id, organization_id=org.id
            ):
                user.github_username = None
                user.github_connected = False
                session.add(user)
                _unattribute_synced_tickets(
                    session,
                    org,
                    user_id=user.id,
                    platform=platform,
                    handle=wanted,
                    project_id=None,
                )
        session.commit()
        return None

    for row in _org_scoped_rows(session, org, platform=platform, handle=wanted):
        if IdentityResolutionService.active_member(
            session, user_id=row.user_id, organization_id=org.id
        ):
            _unattribute_synced_tickets(
                session,
                org,
                user_id=row.user_id,
                platform=platform,
                handle=wanted,
                project_id=row.project_id,
            )
            session.delete(row)
    session.commit()
    return None
