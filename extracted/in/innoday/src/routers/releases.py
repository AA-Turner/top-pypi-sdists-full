"""
Releases API Router

Tracks versioned releases within an org/project. A Release row is the
authoritative record of when a version shipped. Tickets are joined loosely
via ticket.release == release.version within the same organization.

If the ticketing system (Jira, Linear) creates a version/cycle, store its
external ID in external_release_id — status updates from syncs can then
update the release row too.
"""

import logging
from datetime import date, datetime, timezone
from typing import Dict, List, Optional, Tuple
from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel, Field
from sqlalchemy import case
from sqlmodel import Session, func, select

from src.database import get_session
from src.domain.organization import Organization, OrganizationRole
from src.domain.project import Project
from src.domain.project_timeline import TimelineEventType
from src.domain.release import Release, ReleaseStatus
from src.domain.ticket import Ticket, TicketStatus
from src.domain.user import User
from src.middleware.rbac import (
    conflict,
    get_current_user,
    not_found,
    require_org_role,
    resolve_project_ref,
)
from src.services.project_timeline_writer import add_timeline_entry
from src.services.release_pipeline import promote_backlog_in
from src.services.release_planning import (
    ensure_pipeline,
    is_semver,
    next_release,
    release_being_cut,
    semver_key,
)

logger = logging.getLogger(__name__)

router = APIRouter(tags=["releases"])


# ---------------------------------------------------------------------------
# Request / Response models
# ---------------------------------------------------------------------------


class ReleaseCreate(BaseModel):
    version: str = Field(..., max_length=100, description="Version string, e.g. v1.4.0")
    name: Optional[str] = Field(None, max_length=255)
    description: Optional[str] = None
    notes: Optional[str] = Field(
        None, description="Narrative summary compiled by github-ops at release time"
    )
    summary: Optional[str] = Field(
        None,
        description="Human-readable bulleted narrative for client/executive audience",
    )
    changelog: Optional[dict] = Field(
        None,
        description='Structured per-repo PR inventory, wrapped: {"repos": '
        "[{repo, prs: [{number, title, author}]}]}. The wrapper is not optional "
        "-- this field is a dict, so blastoff's bare list is wrapped by "
        "InnoDayVersionStore._wrap_changelog before it is sent, and the Releases "
        "tab unwraps it to count repos and PRs.",
    )
    project_id: str = Field(
        ...,
        description="Project this release belongs to (required -- version strings "
        "are unique per project, not per organization)",
    )
    status: ReleaseStatus = ReleaseStatus.PLANNED
    target_date: Optional[date] = Field(
        None,
        description="The calendar day this release is aimed at. Never derived -- "
        "it stays unset until somebody sets it, because a guessed date reads as a "
        "commitment. Distinct from released_at, which is when it actually shipped.",
    )
    released_at: Optional[datetime] = None


class ReleaseUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=255)
    description: Optional[str] = None
    notes: Optional[str] = None
    summary: Optional[str] = Field(
        None,
        description="Human-readable bulleted narrative for client/executive audience",
    )
    changelog: Optional[dict] = Field(
        None,
        description='Structured per-repo PR inventory, wrapped: {"repos": '
        "[{repo, prs: [{number, title, author}]}]}. The wrapper is not optional "
        "-- this field is a dict, so blastoff's bare list is wrapped by "
        "InnoDayVersionStore._wrap_changelog before it is sent, and the Releases "
        "tab unwraps it to count repos and PRs.",
    )
    project_id: Optional[str] = None
    status: Optional[ReleaseStatus] = None
    target_date: Optional[date] = Field(
        None, description="The calendar day this release is aimed at."
    )
    released_at: Optional[datetime] = None


class TicketSummary(BaseModel):
    id: int
    external_ticket_id: Optional[str]
    summary: str
    status: str
    assignee: Optional[str]
    priority: Optional[str]
    url: Optional[str]


class ReleaseResponse(BaseModel):
    id: str
    organization_id: str
    project_id: str
    version: str
    name: Optional[str] = None
    description: Optional[str] = None
    notes: Optional[str] = None
    summary: Optional[str] = None
    changelog: Optional[dict] = None
    status: str
    target_date: Optional[date] = None
    released_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
    # Aggregates — populated on list; full tickets on detail endpoint
    ticket_count: int = 0
    open_ticket_count: int = 0


class CurrentRelease(BaseModel):
    """One project, and the version it is cutting. Nothing else.

    **Deliberately not a `ReleaseResponse`.** That model carries ticket counts,
    and populating them for an organization's every project is the cost this
    route exists to avoid: the dashboard's version badge needs a project, a
    version and a word for its state, and asking for the counts as well would
    make the cheap answer as expensive as the list it replaces.
    """

    project_id: str
    project_alias: Optional[str] = None
    id: str
    version: str
    status: str


class ReleaseDetail(ReleaseResponse):
    tickets: List[TicketSummary] = []


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _ticket_counts(org_id: str, version: str, session: Session, project_id: str):
    """Return (total, open) ticket counts for this release's project+version."""
    base = select(func.count(Ticket.id)).where(
        Ticket.organization_id == org_id,
        Ticket.project_id == project_id,
        Ticket.release == version,
        Ticket.deleted_at.is_(None),
    )
    total = session.exec(base).one()
    open_ = session.exec(base.where(Ticket.status != TicketStatus.DONE)).one()
    return total, open_


def _ticket_counts_bulk(
    org_id: str, releases: List[Release], session: Session
) -> Dict[Tuple[str, str], Tuple[int, int]]:
    """(total, open) ticket counts for many releases, in one query.

    **`_ticket_counts` is two COUNTs, and the list endpoint called it per row.**
    BPAI has 88 releases, so listing them issued ~176 queries -- and because
    `tickets update --release` validates the version by fetching that same list,
    setting one field on one ticket took ~28 seconds against ~0.6 for a read.

    Keyed on (project_id, version) because a version string is only unique inside
    a project: two projects in one org can both have a v1.9.0, and they are
    different releases.

    Releases whose version nothing carries are absent from the result; callers
    treat a miss as (0, 0). That is the same answer the per-row COUNTs gave, and
    it keeps the query proportional to tickets that exist rather than versions
    that might.
    """
    if not releases:
        return {}

    rows = session.exec(
        select(
            Ticket.project_id,
            Ticket.release,
            func.count(Ticket.id),
            func.sum(case((Ticket.status != TicketStatus.DONE, 1), else_=0)),
        )
        .where(
            Ticket.organization_id == org_id,
            Ticket.deleted_at.is_(None),
            Ticket.release.in_({r.version for r in releases}),
        )
        .group_by(Ticket.project_id, Ticket.release)
    ).all()

    return {
        (project_id, version): (int(total or 0), int(open_ or 0))
        for project_id, version, total, open_ in rows
    }


def _covered_repo_names(release: Release, session: Session) -> List[str]:
    """The repositories this release covers, by name, sorted.

    Archived and deleted repositories are excluded, matching what the release
    engine actually tags -- a record that named repositories the release did
    not touch would report a shrink every time one was archived.
    """
    from src.services.code_activity import CodeActivityFetcher

    repos = CodeActivityFetcher(session).project_repositories(release.project_id)
    return sorted({repo.name for repo in repos})


def _shipped_stamp(release: Release, session: Session) -> str:
    """What was planned into this release, as a line for its notes.

    **This replaced `_bulk_close_tickets_for_release`, which set every ticket
    carrying this version to DONE.** Membership in a release is a free-text
    string somebody typed or dragged -- not evidence that work happened -- so a
    ticket nobody ever started was closed, with a completion timestamp, exactly
    like one that shipped. That destroyed the only record that it had not been
    done, wrote nothing back to the external board (so InnoDay said done while
    Linear still said todo), and could not be undone.

    Nothing warned about it either: blastoff never queries tickets, so the dry
    run -- the command whose whole job is to say what is about to happen -- was
    silent about the change with the widest reach.

    So shipping now touches no ticket at all. It records what it found, and
    `open_ticket_count` on the release keeps answering "how much of this was
    never finished" instead of being zeroed by the act of shipping.

    Closing finished work stays a person's job, through the board or
    `innoday tickets update`.
    """
    total, open_ = _ticket_counts(
        release.organization_id,
        release.version,
        session,
        project_id=release.project_id,
    )
    if not total:
        return "Shipped with no tickets planned in."
    if not open_:
        return f"Shipped with {total} ticket(s) planned in, all done."
    return f"Shipped with {total} ticket(s) planned in -- {open_} not done."


def _advance_release_pipeline(release: Release, session: Session) -> List[str]:
    """Rotate the project's two-slot pipeline after a version ships.

    A project keeps slot 1 (IN_PROGRESS -- what blastoff cuts) and slot 2
    (PLANNED -- what tickets are planned into). When slot 1 ships, slot 2 must be
    promoted into it and a new slot 2 opened above, or the project is left with
    nothing upcoming until someone notices.

    **This lives on "a release became RELEASED", not on the command that caused
    it.** Every path that ships a version goes through this router -- the
    ``innoday release`` proxy via ``InnoDayVersionStore.record_release``, the
    ``blastoff`` MCP tool, GitHub release discovery, and a person in the UI. A
    rotation implemented in the version store would have covered only the first.

    Does NOT commit; the caller commits the release, its closed tickets and these
    rows together, so a project can never be observed mid-rotation.

    Nothing is caught here. A rotation that cannot be written is a project whose
    next version is now unknown, and 500ing at the caller is how that gets
    noticed -- the next repository sync runs the same invariant and repairs it.
    """
    # Explicitly, not on autoflush: this release's own status is what makes it the
    # new high-water mark, and reading the project's rows before that reaches the
    # database would rotate around the version that shipped *last* time.
    session.flush()

    releases = list(
        session.exec(
            select(Release).where(
                Release.project_id == release.project_id,
                Release.deleted_at.is_(None),
            )
        ).all()
    )
    opened: List[str] = []
    for version, status_ in ensure_pipeline(releases):
        session.add(
            Release(
                id=str(uuid4()),
                organization_id=release.organization_id,
                project_id=release.project_id,
                version=version,
                status=status_,
            )
        )
        opened.append(version)

    # `ensure_pipeline` also reconciles statuses in place -- that is how slot 2 is
    # promoted into slot 1 -- so every row it touched has to be persisted, not
    # just the new ones.
    for row in releases:
        session.add(row)

    # Whatever now occupies slot 1 is the release being cut, so nothing in it may
    # still be sitting in the backlog. This is the same invariant the Releases tab
    # asserts when someone plans a ticket in by hand -- one rule, one
    # implementation, asserted at both moments it can be violated. A rotation is
    # the moment a whole release's worth of backlog arrives in that slot at once,
    # which is the case a per-ticket rule alone would miss.
    session.flush()
    cutting = release_being_cut(releases)
    if cutting is not None:
        promote_backlog_in(session, release.project_id, cutting.version)

    return opened


def _release_to_response(
    r: Release,
    session: Session,
    counts: Optional[Dict[Tuple[str, str], Tuple[int, int]]] = None,
) -> ReleaseResponse:
    # `counts` is the bulk-query result when the caller has many releases to
    # render; a miss there means no ticket carries this version, which is (0, 0).
    # Single-release callers pass nothing and keep the direct COUNTs.
    if counts is not None:
        total, open_ = counts.get((r.project_id, r.version), (0, 0))
    else:
        total, open_ = _ticket_counts(
            r.organization_id, r.version, session, project_id=r.project_id
        )
    return ReleaseResponse(
        id=r.id,
        organization_id=r.organization_id,
        project_id=r.project_id,
        version=r.version,
        name=r.name,
        description=r.description,
        notes=r.notes,
        summary=r.summary,
        changelog=r.changelog,
        status=r.status.value,
        target_date=r.target_date,
        released_at=r.released_at,
        created_at=r.created_at,
        updated_at=r.updated_at,
        ticket_count=total,
        open_ticket_count=open_,
    )


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------


@router.get(
    "/api/v1/organizations/{org_id}/releases",
    response_model=List[ReleaseResponse],
)
async def list_releases(
    org_id: str,
    project_id: Optional[str] = Query(None),
    status_filter: Optional[ReleaseStatus] = Query(None, alias="status"),
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
    _org: Organization = Depends(require_org_role()),
):
    """List all releases for an organization, with optional project/status filters."""

    q = select(Release).where(
        Release.organization_id == org_id,
        Release.deleted_at.is_(None),
    )
    if project_id:
        # A query parameter, so `normalize_path_refs` never saw it. Unresolved,
        # an alias here filtered a UUID column and answered 200 with [].
        q = q.where(
            Release.project_id == resolve_project_ref(project_id, org_id, session)
        )
    if status_filter:
        q = q.where(Release.status == status_filter)

    releases = list(session.exec(q).all())

    # **`ORDER BY version DESC` is a string sort, and versions are not strings.**
    # It put "v1.9.0" above "v1.12.0", "v1.11.0" and "v1.10.0" -- because "1.9"
    # beats "1.1" one character at a time -- so the three newest releases sorted
    # down among the v1.1.x rows. Combined with a client-side default limit of 10,
    # the version being cut and the one planned after it were simply absent from
    # the page, which is how a project cutting v1.11.0 looked like it had last
    # shipped v1.9.0.
    #
    # `semver_key` was written for exactly this ("v1.10.0 must sort after v1.9.0
    # -- a plain string compare puts it before") and was never wired in here.
    # Sorted in Python rather than SQL because no portable SQL expression orders
    # a dotted version correctly across SQLite and Postgres.
    #
    # Non-semver rows (BPAI carries a literal "rancher-FINAL", and some month
    # names) are kept but pushed to the end: they are real records, and mixing
    # them into the numeric ordering is what `is_semver` exists to prevent.
    numbered = [r for r in releases if is_semver(r.version)]
    unnumbered = [r for r in releases if not is_semver(r.version)]
    numbered.sort(key=lambda r: semver_key(r.version), reverse=True)
    unnumbered.sort(key=lambda r: r.version)

    ordered = numbered + unnumbered
    counts = _ticket_counts_bulk(org_id, ordered, session)
    return [_release_to_response(r, session, counts=counts) for r in ordered]


@router.post(
    "/api/v1/organizations/{org_id}/releases",
    response_model=ReleaseResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_release(
    org_id: str,
    body: ReleaseCreate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
    _org: Organization = Depends(require_org_role(OrganizationRole.DEVELOPER)),
):
    """Create a release record. Version must be unique per project."""

    # A body field, so `normalize_path_refs` never saw it either -- and this one
    # is written to `Release.project_id`, so an unresolved alias does not merely
    # read wrong, it persists wrong.
    body.project_id = resolve_project_ref(body.project_id, org_id, session)

    existing = session.exec(
        select(Release).where(
            Release.organization_id == org_id,
            Release.project_id == body.project_id,
            Release.version == body.version,
            # A soft-deleted row must not block the version: freeing it for
            # reuse is the entire reason a delete is a delete and not an
            # archive. The partial unique index enforces the same rule.
            Release.deleted_at.is_(None),
        )
    ).first()
    if existing:
        raise conflict("Release", body.version)

    release = Release(
        id=str(uuid4()),
        organization_id=org_id,
        project_id=body.project_id,
        version=body.version,
        name=body.name,
        description=body.description,
        notes=body.notes,
        summary=body.summary,
        changelog=body.changelog,
        status=body.status,
        # **`ReleaseCreate` has accepted `target_date` all along and this
        # constructor never read it**, so `releases create --target-date` (and the
        # equivalent API POST) answered 201 with the date silently discarded. The
        # only way to set one was a follow-up PATCH, which nothing told you about.
        target_date=body.target_date,
        released_at=body.released_at,
    )
    session.add(release)

    if body.status == ReleaseStatus.RELEASED:
        session.flush()
        opened = _advance_release_pipeline(release, session)
        stamp = _shipped_stamp(release, session)
        release.notes = f"{release.notes}\n{stamp}" if release.notes else stamp
        logger.info(
            "release.pipeline_advanced org_id=%s version=%s project_id=%s opened=%s",
            org_id,
            release.version,
            release.project_id,
            opened,
        )
        logger.info(
            "release.shipped org_id=%s release_id=%s version=%s project_id=%s stamp=%s",
            org_id,
            release.id,
            release.version,
            release.project_id,
            stamp,
        )

    add_timeline_entry(
        session,
        organization_id=org_id,
        project_id=body.project_id,
        event_type=TimelineEventType.RELEASE_CREATED,
        title=f"Release {release.version} created",
        summary=f"Release {release.version}"
        + (f" ({release.name})" if release.name else "")
        + f" was created with status {release.status.value}.",
        created_by=current_user.id,
        metadata={"release_id": release.id, "version": release.version},
    )

    session.commit()
    session.refresh(release)
    return _release_to_response(release, session)


def _ticket_summaries(
    org_id: str, project_id: str, version: str, session: Session
) -> List[TicketSummary]:
    """Every live ticket carrying ``version`` on this project, newest movement first.

    The join is ``ticket.release == release.version`` -- free text, no foreign key
    (see the ``Release`` docstring). Uncapped: a release's ticket list is bounded
    by the release itself, and a truncated one would misreport what shipped.
    """
    tickets = session.exec(
        select(Ticket)
        .where(
            Ticket.organization_id == org_id,
            Ticket.project_id == project_id,
            Ticket.release == version,
            Ticket.deleted_at.is_(None),
        )
        .order_by(Ticket.updated_at.desc())
    ).all()
    return [
        TicketSummary(
            id=t.id,
            external_ticket_id=t.external_ticket_id,
            summary=t.summary,
            status=t.status.value if hasattr(t.status, "value") else str(t.status),
            assignee=t.assignee,
            priority=t.priority,
            url=t.url,
        )
        for t in tickets
    ]


@router.get(
    "/api/v1/organizations/{org_id}/releases/current",
    response_model=List[CurrentRelease],
)
async def list_current_releases(
    org_id: str,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
    _org: Organization = Depends(require_org_role()),
):
    """What every project in this organization is cutting, one row each.

    **The question a dashboard asks, answered where the rule lives.** Without
    this route the only way to badge an organization's projects with their
    versions was to ask for `/releases` -- every row the organization has ever
    had, ticket counts computed for all of them -- and re-derive `next_release`
    in the client. BPAI alone carries ninety rows to produce at most seven short
    strings, and the derivation is subtle enough (a `planned` row below the
    high-water mark is history, not a plan) that a second copy of it in another
    language is a disagreement waiting to happen: the client had already drifted
    once, badging nothing on a project whose own release page showed a version.

    One query, grouped in Python, `next_release` per project -- the same helper
    `/releases/current/tickets` and the Releases tab resolve with, so this route
    can never name a version a project page does not.

    A project with nothing upcoming is **absent from the list** rather than
    present with a null. There is no 404 here for the same reason: an
    organization where no project is cutting anything is an ordinary state, not
    a missing resource.
    """
    releases = list(
        session.exec(
            select(Release).where(
                Release.organization_id == org_id,
                Release.deleted_at.is_(None),
            )
        ).all()
    )

    by_project: Dict[str, List[Release]] = {}
    for release in releases:
        by_project.setdefault(release.project_id, []).append(release)

    # The alias so a caller can link to the project without a second call; it is
    # what the URLs are built from.
    aliases = {
        project_id: alias
        for project_id, alias in session.exec(
            select(Project.id, Project.alias).where(
                Project.organization_id == org_id,
            )
        ).all()
    }

    current: List[CurrentRelease] = []
    for project_id, rows in by_project.items():
        release = next_release(rows)
        if release is None:
            continue
        current.append(
            CurrentRelease(
                project_id=project_id,
                project_alias=aliases.get(project_id),
                id=release.id,
                version=release.version,
                status=release.status.value,
            )
        )
    return current


@router.get(
    "/api/v1/organizations/{org_id}/releases/current/tickets",
    response_model=ReleaseDetail,
)
async def get_current_release_tickets(
    org_id: str,
    project_id: str = Query(
        ...,
        description="The project whose current release to read. Required -- an "
        "organization has many projects and each runs its own pipeline.",
    ),
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
    _org: Organization = Depends(require_org_role()),
):
    """The release this project is cutting, and every ticket in it.

    **One call, one required parameter, no filters to get right.** The caller does
    not have to know the version, ask what "current" means, or assemble anything:
    the point is that a summary can be generated by reading this route and nothing
    else. Adding status or date filters here would push that decision onto every
    caller and let two of them disagree about what the release contains.

    "Current" is the project's **IN_PROGRESS** release -- slot 1 of the two-slot
    pipeline, the version blastoff cuts next. It is resolved by ``next_release``,
    the same helper the dashboard and the Releases tab use, so this route can
    never name a different version than the page does.

    404 when a project has no upcoming release. That is a real state -- a project
    that has never shipped and never synced -- and answering 200 with an empty
    release would read as "the current release is empty" rather than "there
    isn't one".
    """
    # A query parameter, so `normalize_path_refs` never saw it. Unresolved, an
    # alias filtered a UUID column, found nothing, and produced the 404 above --
    # which on this route reads as "nothing shipped", the one answer a summary
    # built from this endpoint must never be given wrongly. The original ref is
    # kept for the message: echoing the UUID would name something the caller
    # never typed.
    project_ref = project_id
    project_id = resolve_project_ref(project_id, org_id, session)

    releases = list(
        session.exec(
            select(Release).where(
                Release.organization_id == org_id,
                Release.project_id == project_id,
                Release.deleted_at.is_(None),
            )
        ).all()
    )

    current = next_release(releases)
    if current is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=(
                f"Project {project_ref} has no current release. One opens when "
                "something ships or on the next repository sync."
            ),
        )

    summaries = _ticket_summaries(org_id, project_id, current.version, session)
    resp = _release_to_response(current, session)
    return ReleaseDetail(**resp.model_dump(), tickets=summaries)


@router.get(
    "/api/v1/organizations/{org_id}/releases/by-version/{version:path}",
    response_model=ReleaseDetail,
)
async def get_release_by_version(
    org_id: str,
    version: str,
    project_id: str = Query(
        ...,
        description="Project to look up this version within -- version strings "
        "are unique per project, not per organization",
    ),
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
    _org: Organization = Depends(require_org_role()),
):
    """
    Look up a release by its version string within a project (e.g. v1.4.0).

    If no Release row exists for this version, returns a synthetic summary
    built from the tickets that carry that version in ticket.release.
    This allows querying versions that came from Jira but haven't been
    explicitly registered in InnoDay yet.

    **The synthetic response is deliberate and depended upon.** `innoday releases
    show` reads `status == "unregistered"` together with `ticket_count == 0` and
    prints "Release not found" for that pair, so the two states this route can be
    in -- a version known only to the board, and a version known to nobody -- are
    told apart by the caller, not here. Changing it to a 404 would take a
    board-sourced release out of the CLI's reach.
    """

    # Resolved *before* the lookup, so an unresolvable ref cannot reach the
    # fabrication below: `?project_id=PF` used to answer 200 with a made-up
    # `{"id": "", "status": "unregistered", "project_id": "PF"}` while the UUID
    # returned the real in-progress release. An invented record where a lookup
    # failed is worse than the empty list this change exists to remove -- the
    # caller cannot tell it from a real answer. Now the ref either names a project
    # or 404s, and "unregistered" only ever describes a project that exists.
    project_id = resolve_project_ref(project_id, org_id, session)

    release = session.exec(
        select(Release).where(
            Release.organization_id == org_id,
            Release.project_id == project_id,
            Release.version == version,
            Release.deleted_at.is_(None),
        )
    ).first()

    ticket_summaries = _ticket_summaries(org_id, project_id, version, session)
    open_count = sum(1 for t in ticket_summaries if t.status != TicketStatus.DONE.value)

    if release:
        resp = _release_to_response(release, session)
        return ReleaseDetail(**resp.model_dump(), tickets=ticket_summaries)

    # Synthetic release — tickets reference this version but no Release row exists.
    # project_id is threaded through from the query param (tickets in this
    # response are already scoped to it above), not left as None.
    return ReleaseDetail(
        id="",
        organization_id=org_id,
        project_id=project_id,
        version=version,
        name=None,
        description=None,
        status="unregistered",
        released_at=None,
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
        ticket_count=len(ticket_summaries),
        open_ticket_count=open_count,
        tickets=ticket_summaries,
    )


@router.get(
    "/api/v1/organizations/{org_id}/releases/{release_id}",
    response_model=ReleaseDetail,
)
async def get_release(
    org_id: str,
    release_id: str,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
    _org: Organization = Depends(require_org_role()),
):
    """Get a release by its ID, including all associated tickets."""

    release = session.exec(
        select(Release).where(
            Release.id == release_id,
            Release.organization_id == org_id,
            Release.deleted_at.is_(None),
        )
    ).first()
    if not release:
        raise not_found("Release", release_id)

    tickets = session.exec(
        select(Ticket)
        .where(
            Ticket.organization_id == org_id,
            Ticket.release == release.version,
            Ticket.deleted_at.is_(None),
        )
        .order_by(Ticket.updated_at.desc())
    ).all()

    ticket_summaries = [
        TicketSummary(
            id=t.id,
            external_ticket_id=t.external_ticket_id,
            summary=t.summary,
            status=t.status.value if hasattr(t.status, "value") else str(t.status),
            assignee=t.assignee,
            priority=t.priority,
            url=t.url,
        )
        for t in tickets
    ]

    resp = _release_to_response(release, session)
    return ReleaseDetail(**resp.model_dump(), tickets=ticket_summaries)


@router.patch(
    "/api/v1/organizations/{org_id}/releases/{release_id}",
    response_model=ReleaseResponse,
)
async def update_release(
    org_id: str,
    release_id: str,
    body: ReleaseUpdate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
    _org: Organization = Depends(require_org_role(OrganizationRole.DEVELOPER)),
):
    """Update a release. Use status=released + released_at to mark it shipped."""

    release = session.exec(
        select(Release).where(
            Release.id == release_id,
            Release.organization_id == org_id,
            Release.deleted_at.is_(None),
        )
    ).first()
    if not release:
        raise not_found("Release", release_id)

    was_released = release.status == ReleaseStatus.RELEASED

    update_fields = body.model_dump(exclude_unset=True)
    if "project_id" in update_fields:
        if update_fields["project_id"] is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="project_id cannot be cleared -- a release must always "
                "belong to a project",
            )
        # A body field, so `normalize_path_refs` never saw it -- and every field
        # in `update_fields` is `setattr`'d onto the row below, so this one lands
        # in `Release.project_id`, a validated non-deferrable FK. `create_release`
        # had this line; here it was missing, 300 lines away in the same file, so
        # `{"project_id": "PF"}` failed the constraint and answered 500 -- and did
        # so *mid-release*, since a PATCH to `released` is also what closes the
        # tickets and advances the pipeline below.
        #
        # Resolved in `update_fields` rather than on `body`: assigning to
        # `body.project_id` adds the field to `model_fields_set`, so an
        # unrelated PATCH would acquire a `project_id: None` and be refused by
        # the check above.
        update_fields["project_id"] = resolve_project_ref(
            update_fields["project_id"], org_id, session
        )

    for field, value in update_fields.items():
        setattr(release, field, value)

    # Auto-set released_at when marking as released
    if body.status == ReleaseStatus.RELEASED and release.released_at is None:
        release.released_at = datetime.now(timezone.utc)

    # **Record what it covered, at the moment it covered it.**
    #
    # The repository set is read live from the project links, so once a release
    # ships nothing remembers what was in it -- and the next one cannot tell a
    # deliberately smaller release from a broken one. Written here rather than
    # derived later for exactly that reason: derived later, it would agree with
    # today's links by construction, which is the comparison it exists to make.
    if body.status == ReleaseStatus.RELEASED and release.repo_names is None:
        release.repo_names = _covered_repo_names(release, session)

    newly_released = body.status == ReleaseStatus.RELEASED and not was_released

    if newly_released:
        opened = _advance_release_pipeline(release, session)
        stamp = _shipped_stamp(release, session)
        release.notes = f"{release.notes}\n{stamp}" if release.notes else stamp
        logger.info(
            "release.pipeline_advanced org_id=%s version=%s project_id=%s opened=%s",
            org_id,
            release.version,
            release.project_id,
            opened,
        )
        logger.info(
            "release.shipped org_id=%s release_id=%s version=%s project_id=%s stamp=%s",
            org_id,
            release.id,
            release.version,
            release.project_id,
            stamp,
        )

    release.touch()
    session.add(release)

    if update_fields:
        summary = (
            f"Release {release.version} marked as released."
            if newly_released
            else f"Release {release.version} updated ({', '.join(update_fields.keys())})."
        )
        add_timeline_entry(
            session,
            organization_id=org_id,
            project_id=release.project_id,
            event_type=TimelineEventType.RELEASE_UPDATED,
            title=f"Release {release.version} updated",
            summary=summary,
            created_by=current_user.id,
            metadata={
                "release_id": release.id,
                "version": release.version,
                "updated_fields": list(update_fields.keys()),
            },
        )

    session.commit()
    session.refresh(release)
    return _release_to_response(release, session)


@router.delete(
    "/api/v1/organizations/{org_id}/releases/{release_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_release(
    org_id: str,
    release_id: str,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
    _org: Organization = Depends(require_org_role(OrganizationRole.ADMIN)),
):
    """Withdraw a release record, freeing its version to be cut again.

    **Soft, and that is the point.** Tickets join a release by *version string*
    (`ticket.release == release.version`), so removing the row would leave those
    tickets pointing at a version nothing can explain. Stamping `deleted_at`
    instead hides it from every reader while the record of what happened
    survives.

    **Deleted is not archived.** The difference is visibility and usage: an
    archived release stays visible as history and keeps its version spent; a
    deleted one disappears from every view and gives the number back, because
    the uniqueness index is partial on `deleted_at IS NULL`. Archiving as a way
    to undo was the trap — it read like putting the release away and quietly
    spent the version forever, with no way to reclaim it.

    Deleting again is a no-op rather than a 404: the caller asked for the
    release to be gone, and it is.

    **This does not touch GitHub.** If the release was really cut, its tags and
    GitHub Releases still exist, and blastoff skips a repo whose release already
    exists — so re-cutting the version silently does nothing until they are
    removed. The response names them so the caller is not left guessing.

    *Possible improvement, deliberately not done here:* delete the tags and
    Releases automatically. It is destructive, irreversible, and partial across
    repos in exactly the way tagging already is — a failure halfway leaves some
    repos untagged and others not — so it wants its own design and an explicit
    confirmation, not a side effect of this call.
    """

    release = session.exec(
        select(Release).where(
            Release.id == release_id,
            Release.organization_id == org_id,
        )
    ).first()
    if not release:
        raise not_found("Release", release_id)

    if release.deleted_at is None:
        release.deleted_at = datetime.now(timezone.utc)
        session.add(release)
        session.commit()
