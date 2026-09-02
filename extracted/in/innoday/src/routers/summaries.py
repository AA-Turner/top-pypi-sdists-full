"""Project summaries: the assembly engine's HTTP surface (PF-398).

Two halves, deliberately separate, mirroring what
``GET .../boards/{id}/summary-data`` + ``POST .../boards/{id}/summaries``
already do for boards:

* ``GET  .../projects/{p}/summary-data`` runs the three gates and hands back
  **structured, assembled data** -- plus cached prose when a gate short-circuits.
  It writes no prose and calls no LLM.
* ``POST .../projects/{p}/summaries`` takes the prose the calling Claude session
  wrote and persists it, superseding the previous live summary.

The remaining routes are reads around that pair: the summary history, the latest
one, a ticket's appearances across summaries, the sync state gate 1 consults,
and the unmapped-assignee list behind the footer count.
"""

import logging
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel, Field
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, select

from src.database import get_session
from src.domain.board import SyncStatus
from src.domain.organization import Organization, OrganizationMembership
from src.domain.release import Recommendation, ReleaseVerdict
from src.domain.summary import (
    Attribution,
    GeneratedBy,
    Summary,
    SummaryItem,
    SummaryType,
)
from src.domain.ticket import Ticket
from src.domain.user import User
from src.middleware.rbac import (
    get_current_user,
    not_found,
    require_org_role,
    resolve_organization,
)
from src.routers.projects import resolve_project
from src.services.summary_service import (
    SYNC_FRESHNESS,
    Block,
    InvalidWindowSpec,
    SummaryService,
    as_utc,
    canonical_window_spec,
    mirror_release_notes,
)

# The `current` sentinel and the one function that resolves it. From the service
# that owns the sentinel, NOT from `src.routers.tickets` -- this used to import
# that router's private `_resolve_release_filter`, which is a router reaching into
# another router's internals for a question neither router owns. A third
# hand-rolled copy of the answer is how the CLI once computed its own and got a
# different one; `current_release_version` is the single place it is computed, and
# each caller supplies its own error (404 here, 422 on the write path).
from src.services.ticket_release import (
    CURRENT_RELEASE,
    NO_CURRENT_RELEASE_DETAIL,
    current_release_version,
)
from src.utils.time_windows import parse_iso_utc

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1", tags=["summaries"])


# --------------------------------------------------------------------- models


class SummaryItemPayload(BaseModel):
    """One line of a narrated summary, as the caller writes it back.

    **The field set is exactly what `SummaryLine.to_dict()` emits**, because
    posting an assembled line back unchanged is the intended use -- see
    `test_every_assembled_key_survives_the_write_path`, which compares the two
    sets rather than trusting this comment.

    Pydantic's default is `extra="ignore"`, and that default is what let `block`
    go missing on the real write path while every test -- each constructing
    `SummaryItem` rows directly -- stayed green. It had also quietly dropped
    six more keys. The specific keys matter less than that dropping was
    *silent*, so the model now forbids extras: the next field added to
    `SummaryLine` is a 422 naming itself, not a value that disappears.

    Six of the fields below have no column on `SummaryItem` and are
    deliberately not stored. They are declared anyway, because a caller
    echoing an assembled line back verbatim must not be rejected for doing the
    documented thing -- and each is re-derivable, which is why the column does
    not exist. Where they are re-derived is stated per field.
    """

    model_config = {"extra": "forbid"}

    #: Which assembled block the line came from. `SummaryItem` stores no block
    #: column -- the panel re-derives the other blocks from the columns it does
    #: store -- but `no_work_detected` is not re-derivable from anything, so
    #: this is the one that has to survive the round trip. Mapped in
    #: `SummaryService._summary_item`; see `_no_work` there.
    block: Optional[Block] = None
    ticket_id: Optional[int] = None
    assignee_user_id: Optional[str] = None
    assignee_display: Optional[str] = None
    attribution: Attribution = Attribution.NONE
    repo: Optional[str] = None
    branch: Optional[str] = None
    pr_url: Optional[str] = None
    pr_state: Optional[str] = None
    body_markdown: Optional[str] = None
    occurred_at: Optional[datetime] = None
    rank: Optional[int] = None
    no_work_detected: bool = False

    # ------------------------------------------------ the release line's fields
    #: How the ticket was judged. `releases content` spells it `state`; both
    #: names are accepted and land in one column, because a release line has to
    #: keep its verdict and recomputing one later is not equivalent -- the hour
    #: BPAI v1.11.0 was cut, recomputation turned seven shipped tickets into
    #: `no_code`.
    verdict: Optional[ReleaseVerdict] = None
    state: Optional[ReleaseVerdict] = None
    #: The single move the verdict implies, where it implies one. Typed, so a
    #: recommendation this platform has no name for is a 422 rather than a string
    #: somebody downstream has to interpret. `None` is a real value: where an
    #: unticketed pull request belongs is a judgement, not a derivation.
    recommendation: Optional[Recommendation] = None
    #: Everyone credited, not just the one the board named. A ticket delivered
    #: by two people stored the first and lost the second.
    people: Optional[List[str]] = None
    #: Every pull request that delivered the ticket. `pr_url` holds one; a
    #: release line names them all, and a ticket delivered across the API and
    #: the UI showed half of itself.
    prs: Optional[List[Dict[str, Any]]] = None

    # ------------------------------------------ accepted, deliberately unstored
    #: The ticket's own board key or org display ref. Re-derived per read by
    #: `SummaryService._display_ref` from the ticket, which is authoritative --
    #: storing it would freeze a name the board can rename.
    ticket_ref: Optional[str] = None
    #: The ticket's title. Lives on `ticket`; `summary_items.body_markdown` is
    #: the narrator's line *about* it, which is the part with no other home.
    summary: Optional[str] = None
    #: The ticket's status at assembly time. Read from the ticket on display;
    #: the only place a *previous* status is kept is the summary's
    #: `source_fingerprint` (see `_previous_statuses`), on purpose.
    status: Optional[str] = None
    #: Whether the board named someone unmappable. Re-derived exactly by
    #: `assignee_user_id IS NULL AND assignee_display IS NOT NULL`, which is
    #: the definition `_attribute` applies.
    assignee_unmapped: bool = False
    #: Pure presentation -- `SummaryLine.owner_label` decorates
    #: `assignee_display`. A view concern, never a stored one.
    owner_label: Optional[str] = None
    #: How many commits the fetcher linked. A property of the window, not of
    #: the line: it is not recomputable from a stored row and is not meant to
    #: be, since a later read covers a different window.
    commit_count: int = 0

    # ------------------------- accepted from a release line, deliberately unstored
    #
    # **`extra="forbid"` and an assembled release item were incompatible, and
    # the skill instructed callers to combine them.** Posting an
    # `innoday releases content` item back -- the documented way to save a
    # release summary -- failed with ten `extra_forbidden` errors at once, so a
    # release summary could only be stored by stripping it down to a stand-up
    # line, which is where its verdict and its second contributor went.
    #
    # Declared rather than un-forbidden: a field that arrives is either stored
    # or accounted for here, and the next one added to the release payload is
    # still a 422 naming itself.
    #: The ticket's display ref. Same re-derivation as `ticket_ref`.
    ref: Optional[str] = None
    #: The board's own key and InnoDay's own number. Both live on the ticket.
    board_ref: Optional[str] = None
    innoday_ref: Optional[str] = None
    #: The ticket's URL, re-derived from the ticket, which can be renamed.
    url: Optional[str] = None
    #: The engine's own one-line reading of the item, and the `off_release` pair
    #: that says which release a stray ticket is on and the command that moves it.
    #:
    #: **All three are emitted by `releases content` and were not declared here**,
    #: so echoing an item back -- the thing the skill instructs -- was still a 422
    #: after #715 reduced it from ten `extra_forbidden` errors to one. A key is
    #: refused on *presence*, so even the common `narrative: null` failed.
    narrative: Optional[str] = None
    #: Which release a stray ticket is actually on. Not `Summary.window_spec` --
    #: that is the scope asked for; this is the row's own answer.
    release: Optional[str] = None
    remedy: Optional[str] = None
    #: A conflict row's plain sentence, where `remedy` would be a lie. A ticket
    #: stranded on a version that shipped without it can be moved forward or
    #: split apart, and which the work wants is a judgement this engine cannot
    #: make -- so the row says what happened and offers no command. Declared for
    #: the same reason as everything above it: the row is echoed back verbatim.
    detail: Optional[str] = None
    #: The ticket's title. `body_markdown` is the line *about* it.
    title: Optional[str] = None
    #: Gaps are a property of the window the release was assembled over, and are
    #: re-derived from the verdict and the pull requests on read.
    gaps: Optional[List[Dict[str, Any]]] = None
    #: Whether every pull request landed in a design repository. Re-derived on
    #: read from the repositories the project marks as design.
    is_design: bool = False


class CreateSummaryRequest(BaseModel):
    """The narrated write path. Prose comes from the caller, never from here."""

    summary_type: SummaryType = Field(
        default=SummaryType.SCRUM, description="scrum (team) or personal"
    )
    window_spec: str = Field(
        ...,
        description=(
            "The window asked for -- a duration like '3d', '12h' or '2w', or "
            "'day'/'week', normalised before storage. Required and never "
            "defaulted -- it is the cache key, and '' is a sentinel meaning "
            "'outside the windowed regime'."
        ),
    )
    body_markdown: str = Field(..., description="The summary prose, already written")
    notes_markdown: Optional[str] = Field(
        default=None,
        description=(
            "A person's own words to keep beside the generated prose. **Omit "
            "to leave any existing note untouched** -- a re-run must not "
            "silently delete what someone typed earlier. Pass an empty string "
            "to clear it deliberately."
        ),
    )
    generated_by: GeneratedBy = Field(
        default=GeneratedBy.AGENT,
        description=(
            "Who wrote the prose: 'agent' unattended, 'hybrid' if a person "
            "edited the agent's draft, 'human' if they wrote it themselves. "
            "The skill has always instructed callers to record this; until now "
            "the request had no field for it and every row was AGENT."
        ),
    )
    items: List[SummaryItemPayload] = Field(default_factory=list)
    source_fingerprint: Dict[str, Any] = Field(default_factory=dict)
    user_id: Optional[str] = Field(
        default=None, description="Whose summary this is. Omit for the team roll-up."
    )
    period_start: Optional[datetime] = None
    period_end: Optional[datetime] = None
    highlights: List[str] = Field(default_factory=list)
    concerns: List[str] = Field(default_factory=list)
    ticket_stats: Dict[str, Any] = Field(default_factory=dict)
    motivational_message: str = Field(default="")


def _assert_scope_is_coherent(
    summary_type: SummaryType, user_id: Optional[str]
) -> None:
    """A personal summary has to say whose it is.

    ``summary_type=personal`` with ``user_id IS NULL`` is not a personal
    summary at all -- it lands in the *team* slot, because `user_id IS NULL`
    is precisely what the team roll-up means (see `src/domain/summary.py`).
    Everything downstream then reads it as one: the live-uniqueness index that
    applies is `uq_summaries_live_team`, `live_summary` looks it up with
    `user_id IS NULL`, so gates 2 and 3 never match the personal read that
    wrote it, and ``GET .../summaries/latest?user_id=me`` cannot find the row
    it just created. `innoday summary` re-assembles from scratch, for ever.

    Nothing caught this because the two halves each looked reasonable alone:
    the MCP tool forwarded a `user_id` that defaulted to None, and the route
    accepted it. 422 rather than a silent coercion to `scrum`: the caller
    asked for something specific and got it wrong, and guessing which of the
    two fields they meant is how the bug got here.
    """
    if summary_type == SummaryType.PERSONAL and not user_id:
        raise HTTPException(
            status_code=422,
            detail=(
                "summary_type='personal' requires a user_id -- a summary with "
                "no user_id is the team roll-up. Pass the user's id (or 'me'), "
                "or use summary_type='scrum'."
            ),
        )


def _assert_org_member(
    session: Session, user_ref: Optional[str], organization_id: str, field: str
) -> None:
    """Refuse a user id that is not an active member of the path's organisation.

    Nothing else checked this. `POST .../projects/{p}/summaries` took
    `user_id` and each `items[].assignee_user_id` straight to an INSERT, so a
    member of org A could file a summary against a user who exists only in
    org B -- and a *nonexistent* id reached `session.commit()` as a raw FK
    violation, which `src/api/app.py` has no handler for and so answered 500.
    SQLite fixtures do not enforce foreign keys, which is why the suite was
    green; the tests for this are Postgres-only for that reason.
    """
    if not user_ref:
        return
    member = session.exec(
        select(User.id)
        .join(OrganizationMembership, OrganizationMembership.user_id == User.id)
        .where(
            User.id == user_ref,
            OrganizationMembership.organization_id == organization_id,
            OrganizationMembership.is_active.is_(True),
        )
    ).first()
    if member is None:
        # 422, not 404: the path resolved fine, the *body* is wrong. And the
        # same answer whether the user is absent or merely in another org --
        # distinguishing them is the oracle this is closing.
        raise HTTPException(
            status_code=422,
            detail=f"{field} is not an active member of this organization",
        )


def _assert_project_tickets(
    session: Session,
    ticket_ids: List[int],
    organization_id: str,
    project_id: str,
) -> None:
    """Refuse ticket ids belonging to another organisation or project.

    `SummaryItem.ticket_id` is an FK to an **integer** primary key, so the id
    space is trivially enumerable. Unvalidated, any authenticated org member
    could write arbitrary markdown into any other org's per-ticket history --
    read back by `GET .../tickets/{id}/summary-items`, a route that *does* check
    tenancy and therefore makes the injected line look vouched for.
    """
    wanted = {t for t in ticket_ids if t is not None}
    if not wanted:
        return
    found = set(
        session.exec(
            select(Ticket.id).where(
                Ticket.id.in_(wanted),
                Ticket.organization_id == organization_id,
                Ticket.project_id == project_id,
            )
        ).all()
    )
    missing = sorted(wanted - found)
    if missing:
        raise HTTPException(
            status_code=422,
            detail=(
                "items reference tickets that are not in this project: "
                + ", ".join(str(t) for t in missing)
            ),
        )


def _summary_line(item: SummaryItem) -> Dict[str, Any]:
    """One stored line, as the five fields anything rendering it needs.

    **The stored verdict, never a recomputed one.** A reader that re-derived it
    from today's pull requests would answer differently from the summary it is
    part of -- the failure that made every ticket on a freshly cut release read
    as `no_code`.
    """
    return {
        "ticket_id": item.ticket_id,
        "body_markdown": item.body_markdown,
        "people": list(item.people or [])
        or ([item.assignee_display] if item.assignee_display else []),
        "prs": list(item.prs or []),
        "verdict": item.verdict,
        "no_work_detected": item.no_work_detected,
        "rank": item.rank,
    }


def _summary_payload(
    summary: Summary, *, session: Optional[Session] = None
) -> Dict[str, Any]:
    """The summary, and -- when a session is to hand -- its lines.

    Lines are the point of the thing: prose alone tells a reader what happened
    and not which tickets, who, or how it was judged. They were absent from this
    shape, so every client that wanted the five-field line had to call the
    assembling endpoint instead -- which syncs, and is not what a page should do
    to render what is already stored.
    """
    data = summary.to_dict()
    if session is not None:
        rows = session.exec(
            select(SummaryItem)
            .where(SummaryItem.summary_id == summary.id)
            .order_by(SummaryItem.rank)
        ).all()
        data["items"] = [_summary_line(row) for row in rows]
    data.update(
        {
            "period_start": (
                summary.period_start.isoformat() if summary.period_start else None
            ),
            "period_end": (
                summary.period_end.isoformat() if summary.period_end else None
            ),
            "source_fingerprint": summary.source_fingerprint,
            "superseded_by_id": summary.superseded_by_id,
        }
    )
    return data


# ---------------------------------------------------------------- the engine


@router.get(
    "/organizations/{organization_id}/projects/{project_ref}/summary-data",
    summary="Assemble the structured data behind a project summary",
)
async def get_project_summary_data(
    organization_id: str,
    project_ref: str,
    summary_type: SummaryType = Query(
        default=SummaryType.SCRUM, description="scrum (team) or personal"
    ),
    window_spec: str = Query(
        default="3d",
        description=(
            "Window to cover: a duration like '3d', '12h' or '2w', or "
            "'day'/'week'. Normalised before it is used as the cache key."
        ),
    ),
    user_id: Optional[str] = Query(
        default=None,
        description=(
            "Whose work to summarise. Omit for the team roll-up. Pass 'me' for "
            "the authenticated caller."
        ),
    ),
    release: Optional[str] = Query(
        default=None,
        description=(
            "Scope the summary to one release: a version string, or 'current' "
            "for the one this project is cutting. Tickets on any other release "
            "-- and tickets on none -- are not assembled at all, so this "
            "**replaces** window_spec rather than narrowing it, and the payload "
            "reports how many of the project's tickets it left out."
        ),
    ),
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
    _org: Organization = Depends(require_org_role()),
):
    """Run the freshness, cache and fingerprint gates, then assemble.

    Returns structured data and any cached prose. **No LLM call happens here** --
    the caller writes the narrative and posts it back to
    `POST .../projects/{p}/summaries`.
    """
    org = resolve_organization(organization_id, session)
    project = resolve_project(project_ref, org.id, session)

    # Mapped here, not in the service: `current` has an *HTTP* answer when it
    # cannot be satisfied (404 -- the project has no current release), and only a
    # route can give one. What version it names is the service's answer, shared
    # with the `?release=` ticket filter. Any other value passes through verbatim
    # -- `Ticket.release` is free text, so a version nothing carries is a
    # legitimate query. The engine only ever sees a concrete version.
    if release == CURRENT_RELEASE:
        version = current_release_version(
            session, organization_id=org.id, project_id=project.id
        )
        if version is None:
            raise HTTPException(
                status_code=404,
                detail=NO_CURRENT_RELEASE_DETAIL.format(project=project.id),
            )
        release = version

    _assert_scope_is_coherent(summary_type, user_id)

    scope_user_id = current_user.id if user_id == "me" else user_id
    service = SummaryService(session)

    if scope_user_id:
        target = service.resolve_user(scope_user_id, org.id)
        if target is None:
            raise not_found("User", scope_user_id)
        scope_user_id = target.id

    try:
        assembly = await service.assemble(
            project=project,
            summary_type=summary_type,
            window_spec=window_spec,
            release=release,
            user_id=scope_user_id,
            requested_by=current_user.id,
        )
    except InvalidWindowSpec as exc:
        raise HTTPException(status_code=422, detail=str(exc))

    # The fingerprint gate restamps the live row's window in place; nothing
    # else here writes, so this is the only commit the read path needs.
    session.commit()

    payload = assembly.to_dict()
    payload["unmapped_assignees"] = service.unmapped_assignees(project.id)
    payload["project_id"] = project.id
    return payload


# ---------------------------------------------------------------- write path


@router.post(
    "/organizations/{organization_id}/projects/{project_ref}/summaries",
    summary="Persist a narrated project summary",
    status_code=201,
)
async def create_project_summary(
    organization_id: str,
    project_ref: str,
    request: CreateSummaryRequest,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
    _org: Organization = Depends(require_org_role()),
):
    """Store prose written elsewhere, superseding the previous live summary.

    The old row is never overwritten -- it gets `superseded_by_id` pointing at
    the replacement, so history survives and "the current summary" stays
    expressible as `superseded_by_id IS NULL`.
    """
    org = resolve_organization(organization_id, session)
    project = resolve_project(project_ref, org.id, session)

    # Validation only. Canonicalising the spec is `SummaryService`'s job, not
    # this route's -- the spec is a cache key, so the layer that reads and
    # writes the key is the one place that can guarantee both use one spelling.
    try:
        # `canonical_window_spec`, not `parse_window_spec`: a release scope has no
        # duration to parse, and refusing it here would 422 the save of a summary
        # this same router had just assembled. The value is discarded --
        # canonicalising the stored spec is `SummaryService`'s job, as below.
        canonical_window_spec(request.window_spec)
    except InvalidWindowSpec as exc:
        raise HTTPException(status_code=422, detail=str(exc))

    _assert_scope_is_coherent(request.summary_type, request.user_id)

    # `me` is accepted here for the same reason the read path accepts it: the
    # caller knows the scope it asked for, not necessarily its own user id.
    if request.user_id == "me":
        request.user_id = current_user.id

    service = SummaryService(session)

    # Recover the `ticket_id`/`assignee_user_id` a narrator dropped, *before* the
    # tenancy checks below rather than after: resolution only ever looks inside
    # this project, so the ids it fills in are project-owned by construction --
    # but they are then checked by the same gate as a caller's own, so there is
    # one place that decides whether an id may be written and it does not care
    # where the id came from.
    filled_tickets, filled_owners = service.resolve_narrated_items(
        project, request.items
    )
    if filled_tickets or filled_owners:
        logger.info(
            "Narrated summary for project %s: filled %d ticket ids and %d owners "
            "the caller omitted",
            project.id,
            filled_tickets,
            filled_owners,
        )

    # Tenancy, before anything is written. Everything below names a row by id,
    # and an id in a request body is a claim, not a fact.
    _assert_org_member(session, request.user_id, org.id, "user_id")
    for index, item in enumerate(request.items):
        _assert_org_member(
            session,
            item.assignee_user_id,
            org.id,
            f"items[{index}].assignee_user_id",
        )
    _assert_project_tickets(
        session,
        [item.ticket_id for item in request.items if item.ticket_id is not None],
        org.id,
        project.id,
    )

    if not request.source_fingerprint:
        request.source_fingerprint = await _compute_fingerprint(
            service, project, request.window_spec
        )
    try:
        summary = _persist_summary(service, org, project, request, current_user)
        # Inside the `try` as well: the live-uniqueness indexes fire at the
        # flush, but the deferred self-FK on `superseded_by_id` settles at
        # COMMIT, so both statements can lose the race.
        session.commit()
    except IntegrityError:
        # Two agents narrating the same (project, type, window) within the
        # minute both read no live summary, both insert, and one of them races
        # the partial unique indexes. `src/api/app.py` registers no exception
        # handlers at all, so the loser used to get a raw IntegrityError and a
        # 500 -- which reads as "the server is broken" rather than "someone
        # else just wrote this", and would send a retrying client round again.
        #
        # 409 rather than re-reading and returning the winner: the loser holds
        # prose the winner does not, and silently answering 201 with somebody
        # else's summary would look like its own write succeeded.
        session.rollback()
        raise HTTPException(
            status_code=409,
            detail=(
                "another summary for this project, type and window was written "
                "concurrently. Re-read the latest summary before writing again."
            ),
        )

    session.refresh(summary)
    return _summary_payload(summary, session=session)


async def _compute_fingerprint(
    service: SummaryService, project, window_spec: str
) -> Dict[str, Any]:
    """The fingerprint for this project and window, computed here.

    **Why the caller no longer has to echo it.** The fingerprint is every
    ticket id + status + timestamp and every commit sha and PR url in the
    window — 28 KB of JSON for a mid-sized project. The documented flow made
    the narrator carry all of that back out of `summary-data` and into this
    write, unchanged, purely so the *next* run could compare it. For an LLM
    narrator that is tens of thousands of tokens of hex per summary, spent to
    move a value the server just computed back to the server.

    So an omitted fingerprint is no longer "the next run cannot tell nothing
    moved" — it is recomputed here. Callers may still pass one and it wins
    verbatim, which keeps the echo path working for anything that already
    does it.

    The nuance worth stating: this is the fingerprint as of *save* time, not
    of the assemble a moment earlier. If the board moved in between, the next
    run compares against what was true when the prose was stored — which is
    the more defensible reading of "has anything changed since this summary",
    not a compromise.

    Never raises: a fingerprint that could not be computed degrades to `{}`,
    which costs one redundant re-narration. Failing the write over it would
    throw away prose someone is waiting on.

    **The swallow is the only thing this function still owns.** Gathering the
    inputs -- resolving the scope, reading the scoped tickets, fetching the
    activity, counting the release boundary -- is `SummaryService.fingerprint_for`,
    shared with `assemble`. It has to be: this value is what the *next* read
    compares against, so an input the save path gathered differently would differ
    from every assemble by construction, and re-narrate every morning while
    looking like the cache working. Two bugs of exactly that shape (a release spec
    parsed as a duration, then the boundary counts) are recorded there.

    The `except` stays *here* rather than moving into the service with the rest: a
    service that swallowed its own failures would hide them from `assemble` too,
    where there is no prose to protect and a bug should surface.
    """
    try:
        gathered = await service.fingerprint_for(
            project=project,
            window_spec=window_spec,
            now=datetime.now(timezone.utc),
        )
        return gathered.fingerprint
    except Exception as exc:  # noqa: BLE001 - see docstring
        logger.warning(
            "Could not compute a fingerprint for project %s (%s): %s",
            project.id,
            window_spec,
            exc,
        )
        return {}


def _persist_summary(
    service: SummaryService,
    org: Organization,
    project,
    request: CreateSummaryRequest,
    current_user: User,
) -> Summary:
    """The write itself, so the route's `except` covers flush as well as commit.

    The live-uniqueness indexes are checked immediately, so a losing racer
    fails inside `persist`'s flush, not at COMMIT.
    """
    summary = service.persist(
        organization_id=org.id,
        project=project,
        summary_type=request.summary_type,
        window_spec=request.window_spec,
        body_markdown=request.body_markdown,
        notes_markdown=request.notes_markdown,
        generated_by=request.generated_by,
        items=[item.model_dump() for item in request.items],
        source_fingerprint=request.source_fingerprint,
        user_id=request.user_id,
        period_start=request.period_start,
        period_end=request.period_end,
        created_by=current_user.id,
        motivational_quote=request.motivational_message,
        highlights=request.highlights,
        concerns=request.concerns,
        ticket_stats=request.ticket_stats,
    )
    # A release-scoped summary is that release's notes; mirror it onto the row
    # the release card and the release API read, so one artifact cannot look like
    # two depending on which door you came through.
    mirror_release_notes(
        service.session,
        organization_id=org.id,
        project_id=project.id,
        window_spec=request.window_spec,
        body_markdown=request.body_markdown,
    )
    return summary


# --------------------------------------------------------------------- reads


@router.get(
    "/organizations/{organization_id}/projects/{project_ref}/summaries/latest",
    summary="Get the current live summary for a project",
)
async def get_latest_project_summary(
    organization_id: str,
    project_ref: str,
    summary_type: SummaryType = Query(default=SummaryType.SCRUM),
    window_spec: Optional[str] = Query(default=None),
    user_id: Optional[str] = Query(default=None),
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
    _org: Organization = Depends(require_org_role()),
):
    """The newest summary for this scope, live ones first."""
    org = resolve_organization(organization_id, session)
    project = resolve_project(project_ref, org.id, session)

    scope_user_id = current_user.id if user_id == "me" else user_id
    query = select(Summary).where(
        Summary.project_id == project.id,
        Summary.summary_type == summary_type,
        Summary.superseded_by_id.is_(None),
    )
    query = (
        query.where(Summary.user_id.is_(None))
        if scope_user_id is None
        else query.where(Summary.user_id == scope_user_id)
    )
    if window_spec is not None:
        query = query.where(Summary.window_spec == window_spec)

    summary = session.exec(query.order_by(Summary.created_at.desc())).first()
    if summary is None:
        raise not_found("Summary", f"{project.alias}/{summary_type.value}")
    return _summary_payload(summary, session=session)


@router.get(
    "/organizations/{organization_id}/projects/{project_ref}/summaries",
    summary="List a project's summaries",
)
async def list_project_summaries(
    organization_id: str,
    project_ref: str,
    summary_type: Optional[SummaryType] = Query(default=None, alias="type"),
    user_id: Optional[str] = Query(default=None),
    window_spec: Optional[str] = Query(default=None),
    include_superseded: bool = Query(
        default=False,
        description="Include rows a later run replaced. Off by default.",
    ),
    limit: int = Query(default=20, ge=1, le=100),
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
    _org: Organization = Depends(require_org_role()),
):
    """Summaries for a project, newest first, filtered by scope and window."""
    org = resolve_organization(organization_id, session)
    project = resolve_project(project_ref, org.id, session)

    query = select(Summary).where(Summary.project_id == project.id)
    if summary_type is not None:
        query = query.where(Summary.summary_type == summary_type)
    if window_spec is not None:
        query = query.where(Summary.window_spec == window_spec)
    if user_id is not None:
        scope_user_id = current_user.id if user_id == "me" else user_id
        query = query.where(Summary.user_id == scope_user_id)
    if not include_superseded:
        query = query.where(Summary.superseded_by_id.is_(None))

    summaries = session.exec(
        query.order_by(Summary.created_at.desc()).limit(limit)
    ).all()
    return {
        "summaries": [_summary_payload(s, session=session) for s in summaries],
        "count": len(summaries),
    }


@router.get(
    "/organizations/{organization_id}/tickets/{ticket_id}/summary-items",
    summary="Every summary line that mentioned this ticket, newest first",
)
async def list_ticket_summary_items(
    organization_id: str,
    ticket_id: int,
    limit: int = Query(default=20, ge=1, le=100),
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
    _org: Organization = Depends(require_org_role()),
):
    """A ticket's history as told by the summaries it appeared in."""
    org = resolve_organization(organization_id, session)
    ticket = session.get(Ticket, ticket_id)
    if ticket is None or ticket.organization_id != org.id:
        raise not_found("Ticket", str(ticket_id))

    rows = session.exec(
        select(SummaryItem, Summary)
        .join(Summary, Summary.id == SummaryItem.summary_id)
        .where(SummaryItem.ticket_id == ticket_id)
        .order_by(Summary.created_at.desc())
        .limit(limit)
    ).all()

    return {
        "ticket_id": ticket_id,
        "items": [
            {
                "id": item.id,
                "summary_id": item.summary_id,
                "summary_type": summary.summary_type,
                "window_spec": summary.window_spec,
                "summary_created_at": summary.created_at.isoformat(),
                "assignee_user_id": item.assignee_user_id,
                "assignee_display": item.assignee_display,
                "attribution": item.attribution,
                "repo": item.repo,
                "branch": item.branch,
                "pr_url": item.pr_url,
                "pr_state": item.pr_state,
                "body_markdown": item.body_markdown,
                "occurred_at": (
                    item.occurred_at.isoformat() if item.occurred_at else None
                ),
                "no_work_detected": item.no_work_detected,
                "rank": item.rank,
            }
            for item, summary in rows
        ],
        "count": len(rows),
    }


@router.get(
    "/organizations/{organization_id}/projects/{project_ref}/sync/status",
    summary="Whether a sync is running now, and how the last finished one went",
)
async def get_project_sync_status(
    organization_id: str,
    project_ref: str,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
    _org: Organization = Depends(require_org_role()),
):
    """Whether a sync is in flight, when the boards last finished, and if that is fresh.

    Three questions that look like one and are not. `is_fresh` is the exact
    condition gate 1 uses to decide *not* to sync, so a caller can see why a
    summary did or did not trigger one. `last_sync` is the run that decision
    rests on. `running` is none of that -- it is the work in flight, which the
    freshness lookup deliberately ignores.
    """
    from datetime import timezone

    org = resolve_organization(organization_id, session)
    project = resolve_project(project_ref, org.id, session)

    service = SummaryService(session)
    now = datetime.now(timezone.utc)
    last = service.latest_sync(project.id)
    completed = as_utc(last.completed_at) if last else None

    # **`running` is not derivable from `last_sync`.** That field is the last
    # *finished* run by design -- an unfinished one is no evidence of freshness
    # -- so a caller asking "is something happening right now" could never get
    # an answer from this payload, and the only way to find out was to start a
    # sync and be refused. Two sessions doing that at once is exactly the
    # collision this route now exists to prevent.
    running = [
        {
            "id": row.id,
            "board_registration_id": row.board_registration_id,
            "status": row.sync_status,
            "started_at": row.started_at.isoformat() if row.started_at else None,
        }
        for row in service.running_syncs(project.id)
    ]

    return {
        "project_id": project.id,
        "is_fresh": service.sync_is_fresh(project.id, now),
        "running": running,
        "is_running": bool(running),
        "last_sync": (
            {
                "id": last.id,
                "board_registration_id": last.board_registration_id,
                "status": last.sync_status,
                "started_at": last.started_at.isoformat() if last.started_at else None,
                "completed_at": completed.isoformat() if completed else None,
                "tickets_found": last.tickets_found,
                "tickets_created": last.tickets_created,
                "tickets_updated": last.tickets_updated,
                "error_message": last.error_message,
            }
            if last
            else None
        ),
    }


@router.get(
    "/organizations/{organization_id}/projects/{project_ref}/unmapped-assignees",
    summary="Board assignees on this project that map to no InnoDay user",
)
async def list_project_unmapped_assignees(
    organization_id: str,
    project_ref: str,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
    _org: Organization = Depends(require_org_role()),
):
    """The footer's "N assignees unmapped" count, and the handles behind it."""
    org = resolve_organization(organization_id, session)
    project = resolve_project(project_ref, org.id, session)

    assignees = SummaryService(session).unmapped_assignees(project.id)
    return {
        "project_id": project.id,
        "assignees": assignees,
        "count": len(assignees),
    }


@router.get(
    "/organizations/{organization_id}/projects/{project_ref}/release/content",
    summary="What this release contains, assembled with the org's own credential",
)
async def get_release_content(
    organization_id: str,
    project_ref: str,
    since: Optional[str] = Query(
        None,
        description=(
            "ISO timestamp the window opens at — normally the previous "
            "release's date. Omitted means an unbounded window."
        ),
    ),
    window_label: Optional[str] = Query(
        None, description="Human phrase for the window, echoed into the report."
    ),
    version: Optional[str] = Query(
        None,
        description=(
            "The version being cut. Scopes the ticket half of the payload: "
            "without it there are no tickets, which is correct for a hotfix "
            "-- that targets a commit, not a planned set of work."
        ),
    ),
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
    _org: Organization = Depends(require_org_role()),
):
    """The merged and open pull requests, per repository, for a release window.

    **This exists so that cutting a release needs no GitHub credential on the
    client.** The engine used to find all of this itself, wherever it ran, which
    meant whoever ran a release had to supply a token — and the nearest one to
    hand is a personal login, which is the wrong credential for a release and
    hides that the right one was already stored here.

    A missing credential is a **409, not an empty result**: "nothing shipped"
    and "we cannot see GitHub" must never render as the same report.
    """
    from src.services.release_content import (
        NoGitHubCredential,
        ReleaseContentService,
    )

    org = resolve_organization(organization_id, session)
    project = resolve_project(project_ref, org.id, session)

    opened_at = parse_iso_utc(since) if since else None
    if since and opened_at is None:
        raise HTTPException(
            status_code=422,
            detail=f"'{since}' is not a timestamp this can read.",
        )

    service = ReleaseContentService(session)
    try:
        content = await service.assemble(
            project=project,
            organization_id=org.id,
            since=opened_at,
            window_label=window_label,
            version=version,
        )
    except NoGitHubCredential as exc:
        raise HTTPException(status_code=409, detail=str(exc))

    # **When the tickets were last refreshed, reported and never enforced.**
    # A stale board and a quiet release render identically -- both say "nothing
    # moved" -- so this payload has to carry which it is. It does *not* sync and
    # does not refuse: the pull-request half of this report comes from GitHub and
    # is unaffected by a board being stale, so blocking would withhold good data
    # over a defect in unrelated data. The caller decides.
    content["board_sync"] = _board_sync_state(session, project.id)
    return content


def _board_sync_state(session: Session, project_id: str) -> Dict[str, Any]:
    """`{synced_at, age_seconds, stale, status, error}` for the project's board.

    `stale` is computed here against the same `SYNC_FRESHNESS` the summary engine
    gates on, rather than left to each caller's own arithmetic -- two definitions
    of "an hour old" is how one surface reassures you while another warns.

    A board that has never synced is `synced_at: null` with `stale: true`. That
    is not a hedge: never-synced tickets are the stalest there are, and the
    honest reading of "no evidence of a sync" is not "probably fine".
    """
    service = SummaryService(session)
    last = service.latest_sync(project_id)
    if last is None:
        return {
            "synced_at": None,
            "age_seconds": None,
            "stale": True,
            "status": None,
            "error": None,
        }
    completed = as_utc(last.completed_at)
    age = (
        int((datetime.now(timezone.utc) - completed).total_seconds())
        if completed is not None
        else None
    )
    return {
        "synced_at": completed.isoformat() if completed else None,
        "age_seconds": age,
        # A failed run is not freshness, and it carries a `completed_at` -- so the
        # status is read as well as the clock, or an expired credential reports
        # fresh for an hour after every failure.
        "stale": last.sync_status != SyncStatus.COMPLETED
        or age is None
        or age > SYNC_FRESHNESS.total_seconds(),
        "status": getattr(last.sync_status, "value", last.sync_status),
        "error": last.error_message,
    }
