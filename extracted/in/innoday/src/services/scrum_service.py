"""The writes behind a scrum run, shared by the API router and the ``/ui`` page.

**Why this is a service and not just the router.** A scrum is recorded by two
callers that cannot share a route: `src/routers/scrums.py` serves the CLI and
MCP over ``/api/v1`` with a Bearer token, while the workflow page at
``/ui/{org}/workflow`` posts with a session cookie -- and the pages may never
call ``/api/v1`` (a browser cannot send ``X-Team-Secret``, and injecting the
shared secret into page JavaScript would leak it; see CLAUDE.md). Two routes,
one set of writes. Duplicating them is how the two surfaces end up disagreeing
about who may close a scrum.

**Every rule that decides whether a write is allowed lives here**, not in either
router. The routers translate the exceptions below into their own vocabulary --
HTTP status codes for the API, JSON for the page -- and do nothing else.

**That includes the shape of each value, not only who may write it.** The
``/api/v1`` router has a pydantic model in front of it and the ``/ui`` routes
have a JSON body and no model at all, so a rule stated only in `ScrumFinish`
holds on one surface and not the other: ``total_seconds="abc"`` reached the
driver as ``invalid input syntax for type integer`` and a 1,220-character
``transcript_url`` as ``value too long``, both surfacing as an unhandled 500 on
the page while the API answered a clean 422. Field validation lives in
`_checked_int`/`_checked_text` below and runs for both callers -- the exact
drift this module was created to close.

Errors are raised rather than returned because every one of them is a refusal:
there is no partial write, and a caller that ignored a returned error would
carry on believing the scrum was recorded. That belief is the exact failure this
module exists to prevent.
"""

import logging
from datetime import date, datetime, timedelta
from typing import Any, Dict, List, Optional
from uuid import uuid4

from sqlalchemy import func
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, select

from src.domain.scrum import Scrum, ScrumKind, ScrumTicketVisit
from src.domain.summary import Summary, SummaryType
from src.domain.ticket import Ticket, TicketStatus
from src.domain.user import User
from src.utils.time_windows import parse_iso_naive
from src.utils.urls import normalised_link

logger = logging.getLogger(__name__)


class ScrumError(Exception):
    """Base for every refusal in this module."""


class ScrumNotFound(ScrumError):
    """The scrum, ticket or summary named does not exist *for this caller*.

    Deliberately the same error whether the row is absent or belongs to another
    org: telling a caller that an id exists but is not theirs is itself a
    disclosure, and it is the choice the rest of this API already makes.
    """

    def __init__(self, kind: str, ref: str) -> None:
        super().__init__(f"{kind} not found: {ref}")
        self.kind = kind
        self.ref = ref


class ScrumInvalid(ScrumError):
    """A value in the request body is malformed. The caller must fix it.

    Distinct from "not found" because the remedy is different, and distinct from
    silently storing ``None`` because that is what this class was written to
    stop -- see `apply_wrap_up`.

    ``field`` names the input that was refused, when one input is to blame. It
    exists so a page can put the message *beside the box*: the wrap-up form's
    only hint is a placeholder, and a rejection shown as a banner at the top
    leaves the offending field looking perfectly fine while every retry fails
    identically.
    """

    def __init__(self, message: str, field: Optional[str] = None) -> None:
        super().__init__(message)
        self.field = field


class ScrumNotYours(ScrumError):
    """Someone other than the runner tried to write this scrum."""


class ScrumAlreadyClosed(ScrumError):
    """The scrum has an ``ended_at``; the walk it recorded is over."""


#: Each refusal above, and the HTTP status that says the same thing. **One
#: table, in the module that raises them**, because two surfaces answer these:
#: `src/routers/scrums.py` over ``/api/v1`` and the ``/ui`` page's write routes.
#: They kept a copy each, byte-identical, and a copy each is exactly how the two
#: come to disagree about whether a stale tab closing somebody else's scrum is a
#: 403 or a 409 -- the drift this module exists to prevent. A status code is
#: transport vocabulary and a service is not supposed to know one; carrying it
#: here is the smaller price, and both routers still decide what a response
#: *body* looks like.
HTTP_STATUS_FOR = {
    ScrumNotFound: 404,
    ScrumInvalid: 422,
    ScrumNotYours: 403,
    ScrumAlreadyClosed: 409,
}


def http_status(error: ScrumError) -> int:
    """The status code for one refusal. 400 for a refusal nothing has claimed."""
    return HTTP_STATUS_FOR.get(type(error), 400)


#: How long ``scrums.transcript_url`` and the two 50-character status columns
#: actually are. Named here rather than repeated as literals because the check
#: and the column have to agree: the number's whole job is to refuse a value the
#: database would refuse less politely.
TRANSCRIPT_URL_MAX = 1000
STATUS_TEXT_MAX = 50

#: Every kind a scrum may be, by its stored value. Derived from the enum rather
#: than written out, so adding a third kind cannot leave a value the database
#: accepts and this module refuses.
KINDS = {kind.value for kind in ScrumKind}


def _checked_kind(value: Any) -> str:
    """One of `ScrumKind`'s values, or `ScrumInvalid`.

    Checked here for the reason every other value is: the ``/ui`` route forwards
    whatever was in the JSON body and has no model in front of it. An unrecognised
    kind that reached the column would create a partition of the table nothing
    reads, nothing ticks and nothing resumes -- a record that exists and cannot be
    found, which is worse than a refusal.
    """
    if not isinstance(value, str) or value not in KINDS:
        raise ScrumInvalid(
            f"kind must be one of {', '.join(sorted(KINDS))}",
            "kind",
        )
    return value


def _checked_int(value: Any, field: str, *, minimum: int = 0) -> int:
    """An integer at or above ``minimum``, or `ScrumInvalid` naming the field.

    ``bool`` is refused despite being an ``int`` in Python: ``seconds: true`` is
    a client bug, and storing it as 1 records a stop that took one second.
    """
    if isinstance(value, bool) or not isinstance(value, int):
        raise ScrumInvalid(f"{field} must be a whole number", field)
    if value < minimum:
        raise ScrumInvalid(f"{field} cannot be less than {minimum}", field)
    return value


def _checked_text(value: Any, field: str, *, max_length: Optional[int] = None) -> str:
    """A string within ``max_length``, or `ScrumInvalid` naming the field.

    The length check is the point on the columns that have one. A ``Text``
    column has no limit and still needs the type check: a JSON object reaches
    the driver as an object, not as its own repr.
    """
    if not isinstance(value, str):
        raise ScrumInvalid(f"{field} must be text", field)
    if max_length is not None and len(value) > max_length:
        raise ScrumInvalid(
            f"{field} cannot be longer than {max_length} characters", field
        )
    return value


def resolve_scrum(session: Session, scrum_id: str, org_id: str) -> Scrum:
    """The scrum, or `ScrumNotFound` -- including when it is another org's."""
    scrum = session.get(Scrum, scrum_id)
    if not scrum or scrum.organization_id != org_id:
        raise ScrumNotFound("Scrum", scrum_id)
    return scrum


def require_runner(scrum: Scrum, user_id: str) -> None:
    """Only the person who opened the walk may write to it.

    Membership is not enough, and that is the whole point. `record_visit` and
    `apply_wrap_up` overwrite fields -- ``notes_markdown``, ``transcript_url``,
    the clock -- so a second person running their own stand-up against the same
    scrum id, or a stale tab left open from this morning, would blank somebody
    else's minutes with no trace that it happened. The MEMBER gate on the routes
    is about *what* may be written; this is about *whose row*.

    There is no admin override. An org admin who needs the record corrected can
    read it and write their own; silently editing the minutes of a meeting
    somebody else ran is not an administrative act.
    """
    if scrum.run_by_user_id != user_id:
        raise ScrumNotYours("This scrum was opened by someone else")


def writable_scrum(session: Session, scrum_id: str, org_id: str, user_id: str) -> Scrum:
    """The scrum, if this caller may write to it: `resolve_scrum` then `require_runner`.

    The pair was written out at all four call sites that write to a scrum -- two
    on each router -- and the pair is the rule. Splitting it leaves a fifth call
    site free to resolve without checking the runner and look exactly like the
    other four while doing something else entirely.
    """
    scrum = resolve_scrum(session, scrum_id, org_id)
    require_runner(scrum, user_id)
    return scrum


def todays_scrum_summary(session: Session, project_id: str) -> Optional[Summary]:
    """The live scrum summary written today for this project, if there is one.

    "Today" is UTC midnight to now, on naive values, because
    `summaries.created_at` is a naive UTC column like everything else here --
    comparing it against an aware `now()` raises rather than returning the wrong
    rows, which is the one mercy of that failure mode.

    A summary is not required to start a scrum. Nobody may have run one yet, and
    the walk is still worth recording, so this returns None rather than raising.
    """
    day_start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
    return session.exec(
        select(Summary)
        .where(
            Summary.project_id == project_id,
            Summary.summary_type == SummaryType.SCRUM,
            Summary.superseded_by_id.is_(None),  # type: ignore[union-attr]
            Summary.created_at >= day_start,
        )
        .order_by(Summary.created_at.desc())  # type: ignore[attr-defined]
    ).first()


def _existing_scrum(
    session: Session,
    *,
    organization_id: str,
    project_id: str,
    run_by_user_id: str,
    kind: str,
    day: date,
    replaying: bool,
) -> Optional[Scrum]:
    """The record this caller already has for this ask, or None to start a new one.

    **Two rules, because the two kinds are two different things.** They are written
    out separately rather than as one query with a conditional clause, because the
    difference is not a detail of the filter -- it is what an update is versus what a
    scrum is, and a reader who cannot see that here will "simplify" one into the
    other.

    ``ScrumKind.UPDATE`` -- **the day's row, closed or not.** An update is a form:
    one per person per project per day, and re-entering it means correcting the one
    that exists. This is the same key as the partial unique index on the table, so
    the read and the constraint cannot disagree.

    An explicit ``started_at`` is deliberately **not** exempt here. It cannot be:
    the index makes a second update for the same day impossible, so the choice is
    not "fold or insert" but "fold or `IntegrityError`". A replay asserting a
    *different* day still gets its own row, which is the part of the exemption that
    was ever load-bearing.

    ``ScrumKind.SCRUM`` -- **your own un-ended row, and nothing else.** Unchanged
    behaviour, and unchanged for a reason: a closed scrum is a meeting that is over,
    and the next walk is a *new meeting* that gets its own row. Two stand-ups in one
    day is a real thing (a call that dropped and was restarted, a session split
    across a break, two halves of a team in different timezones) and nothing here
    may make the second one unrecordable. The index is partial precisely so it does
    not.

    ``replaying`` (an explicit ``started_at``) exempts a scrum from the lookup, also
    unchanged: the caller is asserting *which* run this is, and silently attaching
    that assertion to a row that happens to be open would be the same quiet
    substitution `open_scrum`'s parse check refuses. Nothing constrains scrums by
    day, so the insert is safe.

    The two cases the scrum branch exists for, both from #643's predecessor:
    a cancelled walk that re-opens must not leave a row behind whose NULL
    ``ended_at`` reads as "somebody walked out of this"; and an open whose response
    was dropped in transit must not split one meeting across two rows when the page
    retries.
    """
    if kind == ScrumKind.UPDATE.value:
        return session.exec(
            select(Scrum)
            .where(
                Scrum.organization_id == organization_id,
                Scrum.project_id == project_id,
                Scrum.run_by_user_id == run_by_user_id,
                Scrum.kind == kind,
                Scrum.day == day,
            )
            .order_by(Scrum.started_at.desc())  # type: ignore[attr-defined]
        ).first()

    if replaying:
        return None
    return session.exec(
        select(Scrum)
        .where(
            Scrum.organization_id == organization_id,
            Scrum.project_id == project_id,
            Scrum.run_by_user_id == run_by_user_id,
            # `kind` is the one addition to the pre-#643 filter, and it is what stops
            # an un-ended *update* being handed to somebody starting the team walk.
            Scrum.kind == kind,
            Scrum.ended_at.is_(None),  # type: ignore[union-attr]
        )
        .order_by(Scrum.started_at.desc())  # type: ignore[attr-defined]
    ).first()


def open_scrum(
    session: Session,
    *,
    organization_id: str,
    project_id: str,
    run_by_user_id: str,
    kind: Any = ScrumKind.SCRUM.value,
    started_at: Optional[str] = None,
) -> Scrum:
    """Open or resume a record: stamp who, what kind, which day, and today's summary.

    ``started_at`` is normally omitted and stamped server-side; it exists for a
    client replaying a run it recorded offline. A value that will not parse is
    refused rather than quietly replaced with "now" -- a replayed run whose start
    time silently became the moment of upload is a record that says the wrong
    thing while looking correct.

    ``day`` is stamped on every row and is derived from ``began``, never from
    ``created_at``: `TimestampMixin` stamps that one *aware* while ``started_at`` is
    naive, and a caller replaying an offline run supplies the latter. The boundary
    is UTC midnight, the same one `todays_scrum_summary` already uses.

    **What counts as "the record you already have" depends on the kind, and the two
    answers are different questions rather than one question with a flag.** See
    `_existing_scrum`; do not fold them together.

    A **team scrum** resumes its own **un-ended** row, and a closed one is not
    resumed at all -- the next walk is a new meeting, with a row of its own. That is
    the behaviour this function has always had and it is deliberately unchanged: a
    team can legitimately hold two stand-ups in a day (a dropped call restarted, a
    split session, two timezones), and "scrums stay final" is enforced by
    `apply_wrap_up` refusing a second *close*, not by refusing a second meeting.

    A **personal update** resumes **the day's row, closed or not** -- requirement 6
    of #643. It is one person's form for one day, so there is exactly one, and
    re-entering it means correcting the one that exists. `apply_wrap_up` lets it be
    re-closed for the same reason. `Scrum.__table_args__` carries the matching
    partial unique index, so this is the database's rule and not merely this
    function's.

    Both branches now filter on ``kind``, which the old ``ended_at IS NULL`` lookup
    could not: without it, somebody holding a half-walked team scrum who opened
    their own daily update **got the meeting's row back**, and every pick landed on
    its minutes with nothing on screen to notice.
    """
    kind = _checked_kind(kind)
    began = datetime.utcnow()
    if started_at is not None:
        parsed = parse_iso_naive(started_at)
        if parsed is None:
            raise ScrumInvalid(
                f"started_at is not an ISO timestamp: {started_at!r}", "started_at"
            )
        began = parsed
    day = began.date()

    existing = _existing_scrum(
        session,
        organization_id=organization_id,
        project_id=project_id,
        run_by_user_id=run_by_user_id,
        kind=kind,
        day=day,
        replaying=started_at is not None,
    )
    if existing is not None:
        return existing

    initial = todays_scrum_summary(session, project_id)
    scrum = Scrum(
        id=str(uuid4()),
        organization_id=organization_id,
        project_id=project_id,
        run_by_user_id=run_by_user_id,
        kind=kind,
        started_at=began,
        day=day,
        initial_summary_id=initial.id if initial else None,
    )
    session.add(scrum)
    try:
        session.commit()
    except IntegrityError:
        # **The race the partial index exists for, resolved rather than raised.**
        # The lookup above is a read and this is a write; two requests that arrive
        # together both find nothing and both insert. That is not hypothetical --
        # the page retries the open after any rejection and re-opens on cancel, so
        # a dropped response followed by a retry is the ordinary case here.
        #
        # Without this the loser gets an `IntegrityError`, which is not a
        # `ScrumError`, so neither router's `except` sees it and the browser is
        # handed a bare 500 about a record that exists and is theirs. Re-reading
        # turns the index from "converts a duplicate into a 500" into what it was
        # added to be: "converts a duplicate into the row that won".
        #
        # Only the update branch can get here -- nothing constrains scrums by day
        # -- so a re-read that finds nothing means the violation was something
        # else entirely and re-raising is the honest answer rather than looping.
        session.rollback()
        winner = _existing_scrum(
            session,
            organization_id=organization_id,
            project_id=project_id,
            run_by_user_id=run_by_user_id,
            kind=kind,
            day=day,
            replaying=False,
        )
        if winner is None:
            raise
        return winner
    session.refresh(scrum)
    return scrum


def record_visit(
    session: Session,
    *,
    scrum: Scrum,
    ticket_id: Any,
    position: Any,
    seconds: Any,
    status_at_visit: Any,
    comment: Any = None,
    moved_to: Any = None,
) -> ScrumTicketVisit:
    """Record one stop on the walk. One call per ticket, as the stop ends.

    Deliberately not a bulk write. A walk interrupted half way through is the
    ordinary case -- a call drops, a conversation runs long, a tab closes -- and
    batching at the finish would mean exactly those runs left no trace.

    The arguments are typed ``Any`` and checked here rather than trusted, because
    one of the two callers has no model in front of it: the ``/ui`` route hands
    over whatever was in the JSON body. ``status_at_visit`` and ``moved_to`` are
    *refused* when they are too long rather than truncated -- the API answers 422
    for the same value, and a page that silently stores half of what it was given
    is the more surprising of the two behaviours.
    """
    ticket_id = _checked_int(ticket_id, "ticket_id", minimum=1)
    position = _checked_int(position, "position")
    seconds = _checked_int(seconds, "seconds")
    status_at_visit = _checked_text(
        status_at_visit, "status_at_visit", max_length=STATUS_TEXT_MAX
    )
    if not status_at_visit.strip():
        raise ScrumInvalid("status_at_visit is required", "status_at_visit")
    comment = (
        None
        if comment in (None, "")
        else _checked_text(comment, "comment")  # Text column: no length, still text
    )
    moved_to = (
        None
        if moved_to in (None, "")
        else _checked_text(moved_to, "moved_to", max_length=STATUS_TEXT_MAX)
    )

    ticket = session.get(Ticket, ticket_id)
    if not ticket or ticket.project_id != scrum.project_id:
        # Checked against the scrum's *project*, not merely its org: a visit to a
        # ticket from a different project would be a row nothing could ever
        # correctly render beside the others.
        raise ScrumNotFound("Ticket", str(ticket_id))

    visit = ScrumTicketVisit(
        id=str(uuid4()),
        scrum_id=scrum.id,
        ticket_id=ticket_id,
        position=position,
        seconds=seconds,
        status_at_visit=status_at_visit,
        comment=comment,
        moved_to=moved_to,
    )
    session.add(visit)
    session.commit()
    session.refresh(visit)
    return visit


def replace_picks(
    session: Session, *, scrum: Scrum, sent: Any, offered: Any = None
) -> List[ScrumTicketVisit]:
    """Make this update's visits **be** ``sent`` -- not the union of it and history.

    **The invariant, stated here because it is the one that gets simplified back
    into an append:** after this returns, the record holds a visit for exactly the
    tickets in ``sent``, in that order, and for no others. Un-ticking a box removes
    the pick. Submitting the same selection twice changes nothing. Neither is true
    of a per-ticket `record_visit` loop, and both are what the page's own copy
    promises -- step 2 says "yours to correct until the day is over", and the
    completion panel says the record holds what you asked for. A write that only
    ever adds makes both of those sentences false, on the ordinary path, since
    re-entering to correct a pick is requirement 6's whole purpose.

    It also matters beyond the copy: `moved_to` is what a later change reads to
    decide which ticket to actually move. A withdrawn pick that survives in the
    record is a status change nobody asked for, applied to somebody's ticket.

    **A whole set, not a diff.** The caller sends its complete selection every time
    and this replaces the lot, which makes the write **idempotent**: a retry after a
    partial failure re-sends the same set and converges instead of doubling it. A
    per-ticket endpoint cannot express "and nothing else", so it cannot express a
    removal at all.

    **Reconciled, not deleted-and-reinserted.** A ticket that is still selected
    keeps *its own row* -- same primary key -- and only its position and status are
    rewritten. Churning the id would be simpler and is the wrong trade: a visit
    carries a comment, a delivery marker and two push errors, and re-creating the
    row every time somebody re-submits would throw those away for tickets the user
    never touched.

    **A withdrawn ticket keeps its row too, flagged rather than deleted** -- and
    that is this function following its own reasoning into the one branch where it
    used not to. `comment_id` and `comment_error` are the only record that a
    comment reached the client's board, or that it did not, and a withdrawal
    cannot un-say a sentence the board has already been given. Deleting the row
    made a board that was down at the time, followed by a withdrawal and a
    re-tick, end with the board never having the comment and the page reporting no
    error: silent non-delivery, reachable by changing your mind twice.

    A withdrawn visit is **not part of the update** -- it moves nothing, is not
    returned here, is not counted by `visit_count`, and is not resumed by
    `data.scrum_activity_today`. Those exclusions are precisely why deletion was
    chosen originally, so each is written explicitly. Re-ticking **revives the
    same row**, which is what keeps the memory continuous.

    **Updates only.** A team scrum's visits are stops on a walk, written one at a
    time as the meeting happens precisely so an interrupted run leaves a trace;
    replacing that set wholesale would delete the first half of a meeting because
    somebody retried the second. `record_visit` remains the only way to write one.

    **A whole set, of the part the caller could see.** ``offered`` is every
    ticket whose box was *on screen* when this was posted; a visit outside it is
    left alone. Omit it and the scope is every visit the record holds, which is
    the original whole-set behaviour.

    That parameter exists because the page posts as each picker step is left, and
    the steps render one at a time: on a resumed record the first post carries
    only step 0's boxes. Scoped to the posted picks alone, that post deleted the
    take-picks recorded earlier -- restored a moment later when step 1 was left,
    but *not* if the tab was abandoned in between. A crash between two steps
    would take the day's record and every visit's `push_error` with it while the
    tickets stayed moved and assigned. Withdrawal is still expressible because a
    withdrawn box is offered-and-unticked, not absent.

    ``position`` is the order the picks arrive in, renumbered from zero on every
    call -- it is the shape of the current answer, not a history of edits.
    ``seconds`` is 0: a form has no clock. Both columns are NOT NULL.
    """
    if scrum.kind != ScrumKind.UPDATE.value:
        raise ScrumInvalid(
            "Only a personal update's picks may be replaced as a set; a scrum's "
            "visits are recorded one stop at a time",
            "kind",
        )
    if not isinstance(sent, list):
        raise ScrumInvalid("picks must be a list", "picks")

    # Validated in full *before* anything is written, so a malformed fifth pick
    # cannot leave the record holding the first four and missing the rest -- which
    # would be a silently partial answer to a call whose whole contract is "this
    # is the answer".
    wanted: List[Dict[str, Any]] = []
    seen: set = set()
    for index, raw in enumerate(sent):
        if not isinstance(raw, dict):
            raise ScrumInvalid(f"pick {index} must be an object", "picks")
        ticket_id = _checked_int(raw.get("ticket_id"), "ticket_id", minimum=1)
        if ticket_id in seen:
            # Two boxes cannot be the same box. Silently collapsing them would
            # make the returned count disagree with what the page counted.
            raise ScrumInvalid(f"ticket {ticket_id} was picked twice", "picks")
        seen.add(ticket_id)
        status_at_visit = _checked_text(
            raw.get("status_at_visit"), "status_at_visit", max_length=STATUS_TEXT_MAX
        )
        if not status_at_visit.strip():
            raise ScrumInvalid("status_at_visit is required", "status_at_visit")
        moved_to = raw.get("moved_to")
        moved_to = (
            None
            if moved_to in (None, "")
            else _checked_text(moved_to, "moved_to", max_length=STATUS_TEXT_MAX)
        )
        # **Absent and empty are different answers, and the difference is a
        # deletion.** The pickers now carry a comment box, so an emptied box has
        # to blank the stored comment -- but a caller that never mentions the key
        # must not blank one another surface put there. Keyed on presence, not on
        # truthiness, because `""` is what "I deleted what I wrote" looks like on
        # the wire.
        comment_sent = "comment" in raw
        comment = raw.get("comment")
        comment = None if comment in (None, "") else _checked_text(comment, "comment")

        ticket = session.get(Ticket, ticket_id)
        if not ticket or ticket.project_id != scrum.project_id:
            # Against the scrum's *project*, exactly as `record_visit` checks it.
            raise ScrumNotFound("Ticket", str(ticket_id))
        wanted.append(
            {
                "ticket_id": ticket_id,
                "status_at_visit": status_at_visit,
                "moved_to": moved_to,
                "comment": comment,
                "comment_sent": comment_sent,
            }
        )

    if offered is None:
        in_scope = None
    else:
        if not isinstance(offered, list):
            raise ScrumInvalid("offered must be a list of ticket ids", "offered")
        in_scope = {
            _checked_int(value, "offered", minimum=1) for value in offered
        } | set(seen)

    existing = {
        visit.ticket_id: visit
        for visit in session.exec(
            select(ScrumTicketVisit).where(ScrumTicketVisit.scrum_id == scrum.id)
        ).all()
    }

    kept: List[ScrumTicketVisit] = []
    for position, pick in enumerate(wanted):
        visit = existing.pop(pick["ticket_id"], None)
        if visit is None:
            visit = ScrumTicketVisit(
                id=str(uuid4()),
                scrum_id=scrum.id,
                ticket_id=pick["ticket_id"],
                position=position,
                seconds=0,
                status_at_visit=pick["status_at_visit"],
                moved_to=pick["moved_to"],
                comment=pick["comment"],
            )
        else:
            visit.position = position
            # **`status_at_visit` is not overwritten.** It records where the
            # ticket was when it was picked, and its own description says
            # re-labelling later "must not rewrite what was true then". A
            # resubmit is exactly such a later event -- and by then the move has
            # been applied, so the page is posting the *new* status. Keeping the
            # first observation is what lets a resumed pick be rendered back
            # under the picker the person actually used, on the second re-entry
            # as well as the first. Same rule, and the same reason, as `comment`
            # below.
            visit.moved_to = pick["moved_to"]
            # A comment is overwritten only when the key was actually **sent** --
            # including when it was sent empty, which is a deletion. An absent key
            # is a caller not mentioning comments at all (the `/api/v1` shape, and
            # every test written before the box existed), and must leave alone
            # what another surface put there.
            if pick["comment_sent"]:
                visit.comment = pick["comment"]
            # **Revived, not re-inserted.** This is the row that remembers whether
            # the board ever got this ticket's comment; taking the pick back and
            # putting it down again must not start that memory over.
            visit.withdrawn_at = None
            visit.touch()
        session.add(visit)
        kept.append(visit)

    # Whatever is left in `existing` is a ticket the user has withdrawn -- but
    # only among the ones they could see. A visit for a box that was never on
    # screen was not withdrawn; it was simply not asked about.
    retained: List[ScrumTicketVisit] = []
    # **One counter for both branches below, not one each.** They interleave in a
    # single pass over `existing`, so two counters hand out the same number the
    # moment a retained row and a withdrawn row both appear -- which is the exact
    # collision this renumbering exists to prevent, reintroduced by fixing it
    # carelessly.
    after = len(wanted)
    for ticket_id, visit in existing.items():
        if in_scope is not None and ticket_id not in in_scope:
            # Renumbered to follow the posted picks rather than left holding a
            # position inside their range: `position` is an ordering, and two
            # rows claiming the same one is a record that cannot be read back in
            # a stable order.
            visit.position = after
            after += 1
            session.add(visit)
            retained.append(visit)
            continue
        # Withdrawn, not deleted -- see the docstring. `moved_to` is cleared as
        # well as the flag being set, so the ask really is gone and only the
        # delivery record remains.
        #
        # **Renumbered past the live rows, for the reason the retained branch
        # above states.** It used to keep the position it held inside the live
        # range, so a withdrawn row and a live one both claimed `position = 0` --
        # and `/api/v1`'s `ORDER BY position, created_at` then resolved that tie
        # by age, which makes the ordering reliably wrong rather than
        # intermittently wrong. Deletion hid this; keeping the row does not.
        visit.moved_to = None
        visit.withdrawn_at = datetime.utcnow()
        visit.position = after
        after += 1
        visit.touch()
        session.add(visit)

    session.commit()
    held = kept + retained
    for visit in held:
        session.refresh(visit)
    # Everything the record now holds, not only what this call posted -- the page
    # paints this count as "recorded so far", and a step that answered with its
    # own picks alone would make the number shrink as somebody walked forward
    # through the workflow.
    return held


#: The wrap-up fields that are written straight through once checked, and the
#: check each one gets -- the shape its column can actually hold. ``ended_at``,
#: ``transcript_url`` and ``updated_summary_id`` are absent because each has a
#: rule of its own below.
_PLAIN_WRAP_UP_CHECKS = {
    "total_seconds": lambda value: _checked_int(value, "total_seconds"),
    "lingering_count": lambda value: _checked_int(value, "lingering_count"),
    "notes_markdown": lambda value: _checked_text(value, "notes_markdown"),
}


def apply_wrap_up(session: Session, *, scrum: Scrum, sent: Dict[str, Any]) -> Scrum:
    """Close a scrum: end time, clock, transcript, regenerated summary, notes.

    ``sent`` holds **only the keys the caller actually supplied**, so a wrap-up
    that fills in the notes cannot blank a transcript URL it never mentioned.

    Three fields are validated rather than assigned:

    ``ended_at`` -- a value that will not parse is a refusal, not ``None``.
    `parse_iso_naive` never raises (by design: it reads third-party sync
    payloads, where one junk field must not take down a sync), so a body of
    ``{"ended_at": "15/08/2026 10:30"}`` used to answer 200 with the column left
    NULL. NULL is not a neutral outcome on this column -- it is precisely how an
    *abandoned* run is told from a finished one, so a client date-format bug
    would have silently marked every completed scrum abandoned.

    ``transcript_url`` -- validated on write, not merely on render. There is no
    CSP on this app, so a stored ``javascript:`` URL is a live payload for every
    later reader of the row, including ones that are not this codebase. A value
    with no scheme at all is *completed* rather than refused (`normalised_link`):
    the field is typed by hand from a meeting invite, so ``meet.google.com/x`` is
    the ordinary input, and rejecting it strands the whole wrap-up on a value
    only the typist can see is wrong. Anything that already carries a scheme
    keeps it and is judged on it.

    ``updated_summary_id`` -- checked against the scrum's own org, the way
    `record_visit` checks the ticket. Without it a scrum in one org accepted a
    `Summary.id` belonging to another and linked the two.

    **Closing a team scrum is once, so everything the caller wants recorded goes
    in this call** -- including ``updated_summary_id``. A scrum that already has an
    ``ended_at`` refuses further writes: the second caller is either a stale tab
    or a different person, and both would overwrite minutes that are already
    final. A caller regenerating a summary therefore does so *before* closing and
    sends the two together; there is no later PATCH to add it in. The ``/ui``
    walk regenerates nothing, so its scrums leave that column NULL, which is the
    honest record of what happened.

    **A personal update may be re-closed. A team scrum may not.** This asymmetry
    is a rule, not an oversight, and it reads like something to simplify away, so:

    A `ScrumKind.UPDATE` row is *one person's form for one day*. It is theirs, it
    describes only their own intentions, and correcting it before the day is over
    is the reason re-entry exists at all -- requirement 6 of #643. Refusing the
    second close would be worse than useless here: the workflow page treats 409 as
    the done state (deliberately, since that is what a retry gets when a finish
    that committed had its response dropped), so a corrected update would be shown
    as saved while the record still held the first answer. A save reported that
    never happened is the one thing that surface may not do.

    A `ScrumKind.SCRUM` row is *minutes of a meeting other people attended*. Its
    second closer is a stale tab or somebody else's tab, and there is no version
    of "correct it" that does not mean overwriting what the room agreed. That
    refusal is unchanged and pre-dates this rule.

    Note what is **not** asymmetric: `require_runner`. An update being re-closable
    does not make it re-closable by anybody -- only by the person whose day it is.
    """
    if scrum.ended_at is not None and scrum.kind != ScrumKind.UPDATE.value:
        raise ScrumAlreadyClosed("This scrum was already closed")

    if "ended_at" in sent:
        raw = sent["ended_at"]
        if raw is None:
            scrum.ended_at = None
        else:
            # `parse_iso_naive`, never `fromisoformat().replace(tzinfo=None)`:
            # the latter *strips* an offset rather than converting it, so a
            # client an hour off UTC would record an end time an hour wrong.
            parsed = parse_iso_naive(raw)
            if parsed is None:
                raise ScrumInvalid(
                    f"ended_at is not an ISO timestamp: {raw!r}", "ended_at"
                )
            scrum.ended_at = parsed

    if "transcript_url" in sent:
        raw = sent["transcript_url"]
        if raw in (None, ""):
            scrum.transcript_url = None
        else:
            # Normalised *before* the length check, because completing the
            # scheme lengthens the value -- checking first would accept a
            # 997-character link and then hand the column 1,005.
            checked = normalised_link(_checked_text(raw, "transcript_url"))
            if checked is None:
                raise ScrumInvalid(
                    "transcript_url must be an http or https URL", "transcript_url"
                )
            _checked_text(checked, "transcript_url", max_length=TRANSCRIPT_URL_MAX)
            scrum.transcript_url = checked

    if "updated_summary_id" in sent:
        raw = sent["updated_summary_id"]
        if raw is None:
            scrum.updated_summary_id = None
        else:
            summary = session.get(Summary, raw)
            if not summary or summary.organization_id != scrum.organization_id:
                raise ScrumNotFound("Summary", str(raw))
            scrum.updated_summary_id = summary.id

    for attr, check in _PLAIN_WRAP_UP_CHECKS.items():
        if attr in sent:
            raw = sent[attr]
            setattr(scrum, attr, None if raw is None else check(raw))

    scrum.touch()
    session.add(scrum)
    session.commit()
    session.refresh(scrum)
    return scrum


#: The most a push error is allowed to be, matching `ScrumTicketVisit.push_error`
#: and `BoardRegistration.error_message`. Trimmed on write rather than trusted:
#: an adapter's message is third-party text, and a `value too long` from the
#: column would turn a *reported* failure into an unhandled 500 -- the module's
#: one rule, broken by the code that exists to keep it.
PUSH_ERROR_MAX = 500

#: The status a personal update applies. **One status, named once**, and the only
#: one an update's recorded pick may ask for: `moved_to` is free text on the
#: column (a team scrum records observations there), so without this a
#: hand-rolled post could name any status at all and have it written and pushed.
#:
#: Here rather than in `routers/webui/workflow.py` -- which owns the picker copy
#: and used to own this constant -- because a router may import a service and not
#: the other way round, and the enforcement has to live where the write is.
APPLIED_UPDATE_STATUS = TicketStatus.IN_PROGRESS

#: How far back a finished ticket may be brought back from. Mirrors the window the
#: "bring anything back" picker is built with; stated here because this is where a
#: submitted pick is *checked* rather than merely offered.
REOPEN_WINDOW_DAYS = 7


#: The visit columns `_record_visit_outcome` may write, and the ceiling each one
#: has. A name absent from here is refused rather than set, because the whole
#: value of a generic writer is lost the moment a typo can silently write nothing.
_OUTCOME_FIELDS = {
    "push_error": PUSH_ERROR_MAX,
    "comment_error": PUSH_ERROR_MAX,
    "comment_id": None,
}


def _record_visit_outcome(
    session: Session, *, visit: ScrumTicketVisit, **fields: Any
) -> None:
    """Write the outcome columns named in ``fields``. Best-effort, by construction.

    **Generic over the column because there are now two independent outcomes on
    one row.** The status push writes `push_error`; the comment push writes
    `comment_error` and `comment_id`. They fail separately, so one shared column
    would let a clean status push clear a still-true comment failure -- which is
    the exact erasure review found on `push_error` itself.

    Cleared only on a push that actually returned -- see `apply_recorded_moves`
    and `deliver_recorded_comments`, neither of which calls this when no push was
    attempted. A no-op that never contacted the board is not a success to clear
    on, and treating it as one is what deleted a still-true error on every
    re-submit.

    Writes nothing when every value is already right, so a re-submit does not
    restamp `updated_at` on a visit nothing happened to -- the same objection this
    change raises against restamping `Ticket.updated_at`.

    Its caller wraps it -- see `_safely_record`. A recorder that raises must never
    replace the failure it was reporting.
    """
    changed = False
    for name, value in fields.items():
        if name not in _OUTCOME_FIELDS:
            raise KeyError(f"{name} is not a scrum visit outcome column")
        ceiling = _OUTCOME_FIELDS[name]
        wanted = value[:ceiling] if (ceiling and isinstance(value, str)) else value
        if getattr(visit, name) == wanted:
            continue
        setattr(visit, name, wanted)
        changed = True
    if not changed:
        return
    visit.touch()
    session.add(visit)
    session.commit()


def _safely_record(session: Session, *, visit: ScrumTicketVisit, **fields: Any) -> None:
    """`_record_visit_outcome`, wrapped so it can never win.

    **From #641.** The recorder is best-effort reporting: if writing the error
    itself raises, the last exception would otherwise propagate and the user
    would be told about a database problem they can do nothing about, while the
    board quietly stays out of step with InnoDay. The thing that actually went
    wrong has to be the thing that gets reported.

    **Retried once, after a rollback.** The likeliest way this fails is not a bug
    in the write but a transaction Postgres has already deactivated -- every
    later statement refused, ``COMMIT`` silently becoming ``ROLLBACK``. The reads
    that can cause that are wrapped in savepoints in `ticket_status_service`, so
    it should not arrive here; this is the second line, because losing the record
    is exactly the outcome the column exists to prevent and a rollback makes the
    session usable again.

    Indirect through a module-level name on purpose, so a test can replace the
    recorder and watch this hold.

    **The allowlist is checked here, before the `try`, and not inside it.** A name
    that is not an outcome column is a *programming* error, not a board being
    down -- and the blanket `except` below would have logged it, rolled back,
    retried it, logged it again and returned, so a typo wrote nothing at all,
    silently. That is precisely the outcome the allowlist exists to prevent, so
    the guard has to fire somewhere the swallowing does not reach.
    """
    unknown = sorted(set(fields) - set(_OUTCOME_FIELDS))
    if unknown:
        raise KeyError(
            f"{', '.join(unknown)} is not a scrum visit outcome column; "
            f"known columns are {', '.join(sorted(_OUTCOME_FIELDS))}"
        )
    try:
        _record_visit_outcome(session, visit=visit, **fields)
        return
    except Exception:  # noqa: BLE001 -- the original failure must survive this
        logger.exception(
            "Could not record the push outcome for scrum visit %s; retrying once",
            visit.id,
        )
        session.rollback()
    try:
        _record_visit_outcome(session, visit=visit, **fields)
    except Exception:  # noqa: BLE001
        logger.exception(
            "Could not record the push outcome for scrum visit %s", visit.id
        )
        session.rollback()


#: The two states a picker offers work *from*: "bring anything back" reads DONE,
#: "take anything on" reads TODO. Nothing else was ever on either list.
_PICKABLE_FROM = (TicketStatus.DONE.value, TicketStatus.TODO.value)


def _pick_is_eligible(
    ticket: Ticket, *, actor: User, target: TicketStatus, was: str
) -> bool:
    """Whether this ticket is one the pickers would actually have offered.

    **The payload must never be the authority on what may move.** The rules below
    are what the two picker queries are built from, and they lived *only* there:
    `replace_picks` checked that a ticket belonged to the scrum's project and
    nothing else, so a hand-rolled post could name any ticket in the project -- a
    colleague's in-review work, say -- and have InnoDay write its status and push
    it to the client's board. A docstring saying "so the two cannot drift" is not
    enforcement.

    ``was`` is the visit's `status_at_visit`, and gating on it is what closes the
    hole a status-only check leaves. "Already at the target and unowned" has to be
    allowed -- it is a take being re-submitted after a sync nulled `assigned_to` --
    but on its own it also admits an **IN_PROGRESS, unowned** ticket that neither
    picker has ever shown. Requiring the recorded observation to be one of the two
    states a picker reads *from* ties eligibility to the list the pick claims to
    have come off.

    Eligible means the recorded state was DONE or TODO, and one of:

    * **bring it back** -- DONE, *theirs*, finished inside the window the picker
      offers. `completed_at` with no fallback to `updated_at`, the same rule the
      list uses.
    * **take it on** -- TODO and genuinely unowned, on both the FK and the board's
      display mirror. Exactly what "unowned work only" means.
    * **already applied** -- at the target already, and theirs or still unowned.
      This is the re-submit case, and it must pass or a correction would report
      every previously-applied pick as refused.

    A soft-deleted ticket is never eligible: `deleted_at` is how a cleared board
    keeps its rows for audit, and moving one pushes to a board that no longer
    tracks it.

    **What this does not close**, stated rather than glossed: `was` comes off the
    payload the first time a visit is created (`replace_picks` preserves it only
    on rows that already exist), so a crafted first post can still claim
    ``status_at_visit: "todo"`` for an IN_PROGRESS unowned ticket and take it.
    The actor must hold DEVELOPER, the ticket is by definition unowned, and the
    only effect is that it becomes theirs -- nobody else's work moves. Closing it
    completely needs a column recording that *we* applied a visit, which is a
    migration for a residual this narrow.
    """
    if ticket.deleted_at is not None:
        return False
    if (was or "").strip().lower() not in _PICKABLE_FROM:
        return False

    mine = ticket.assigned_to == actor.id
    unowned = ticket.assigned_to is None and not (ticket.assignee or "").strip()

    if ticket.status == target and (mine or unowned):
        return True

    if ticket.status == TicketStatus.DONE and mine and ticket.completed_at is not None:
        # **Measured back from today's UTC midnight, not from `now()`** -- the
        # same boundary `workflow_launcher` builds the offer list with. From
        # `now()` the enforcement window would be up to a day narrower than the
        # offer window, so a ticket the picker showed could be refused for having
        # finished seven days and five hours ago. A check that disagrees with the
        # list it is checking is worse than no check, because it fails only for
        # the people at the edge of it.
        midnight = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
        return ticket.completed_at >= midnight - timedelta(days=REOPEN_WINDOW_DAYS)

    if ticket.status == TicketStatus.TODO and unowned:
        return True

    return False


async def apply_recorded_moves(
    session: Session, *, scrum: Scrum, actor: User
) -> Dict[str, Any]:
    """Make this update's recorded picks real: move each ticket, push each move.

    **This is the step that turns the record into an action, and it runs at
    submit rather than at each pick.** A pick is an answer somebody is still
    editing -- `replace_picks` exists precisely so a box can be un-ticked -- and
    moving on every keystroke of that would apply changes the person then
    withdrew. Submitting is the moment they stop editing.

    Runs over the visits the record *currently* holds, which is what makes the
    withdrawal real: a pick that was removed has no row, so it has no move.

    **Only an update.** A team scrum's visits are minutes of what was discussed,
    and `moved_to` on one records an observation rather than an instruction.

    **Every pick is re-checked against the rules its picker was built from**
    (`_pick_is_eligible`) and against the one status an update may apply. An
    ineligible pick is recorded as refused on its own visit and the rest of the
    submit proceeds -- rejecting the whole post would lose the picks that are
    valid, and this is a person's daily form, not a transaction.

    **A push that failed last time is retried.** `visit.push_error` is the record
    of that, and it is why the retry decision lives here rather than in
    `ticket_status_service`: the durable evidence is on the visit.

    Returns the shape the route answers with -- ``applied``/``pushed``/``error``/
    ``notice``. ``pushed`` is False if *any* ticket has something outstanding;
    ``error`` is the first one, because a banner listing five is a banner nobody
    reads, and every visit keeps its own in `push_error` regardless.
    """
    # Imported here, not at module scope. This module is imported by both
    # routers; `ticket_status_service` pulls in Vault credentials and the board
    # HTTP clients, and only this one function needs them.
    from src.services.ticket_status_service import move_ticket_status

    if scrum.kind != ScrumKind.UPDATE.value:
        raise ScrumInvalid(
            "Only a personal update applies the moves it recorded", "kind"
        )

    visits = session.exec(
        select(ScrumTicketVisit)
        .where(ScrumTicketVisit.scrum_id == scrum.id)
        .order_by(ScrumTicketVisit.position)  # type: ignore[arg-type]
    ).all()

    moved = 0
    pushed = True
    # **Every failure, not the first.** These were single strings kept with
    # `x = x or result.x`, so a second ticket's refusal was discarded before the
    # answer left the building -- the page could only ever show one thing gone
    # wrong out of however many did.
    errors: List[str] = []
    notices: List[str] = []

    def _refuse(visit: ScrumTicketVisit, message: str) -> None:
        nonlocal pushed
        pushed = False
        errors.append(message)
        _safely_record(session, visit=visit, push_error=message)

    for visit in visits:
        # A withdrawn pick moves nothing. Checked on the flag rather than on
        # `moved_to` being NULL, even though the withdrawal clears both: reading
        # the fact from the column that states it is what stops this quietly
        # depending on the other one still being cleared.
        if visit.withdrawn_at is not None or not visit.moved_to:
            continue

        try:
            target = TicketStatus(visit.moved_to)
        except ValueError:
            # A status the enum does not have cannot be applied to a column that
            # only holds the enum. Recorded as this visit's own refusal rather
            # than raised: the rest of the update is still worth applying, and a
            # 500 here would lose the wrap-up that already committed.
            _refuse(visit, f"Unknown status: {visit.moved_to}")
            continue

        if target != APPLIED_UPDATE_STATUS:
            _refuse(
                visit,
                f"A daily update only moves work to "
                f"{APPLIED_UPDATE_STATUS.value}, not {target.value}",
            )
            continue

        ticket = session.get(Ticket, visit.ticket_id)
        if ticket is None:
            continue

        if not _pick_is_eligible(
            ticket, actor=actor, target=target, was=visit.status_at_visit
        ):
            _refuse(
                visit,
                "This ticket is not one your update offered — it is not your "
                "recently finished work, and it is not unowned queued work. "
                "Nothing was changed.",
            )
            continue

        result = await move_ticket_status(
            session,
            ticket=ticket,
            new_status=target,
            actor=actor,
            assign_to_actor=ticket.assigned_to is None,
            # The only durable evidence that the board disagrees lives on this
            # visit, so this is the only place that can ask for a retry.
            retry_push=bool(visit.push_error),
        )
        if result.written:
            moved += 1
        if result.error:
            pushed = False
            errors.append(result.error)
        if result.notice:
            notices.append(result.notice)
        if result.pushed is not None:
            # Only when a push was actually attempted. `None` means nothing was
            # sent -- a no-op with nothing outstanding, or a ticket with no board
            # -- and clearing on that is what erased a still-true failure.
            _safely_record(session, visit=visit, push_error=result.error)

    return {
        "applied": True,
        "moved": moved,
        "pushed": pushed,
        "errors": errors,
        "notices": notices,
    }


async def deliver_recorded_comments(
    session: Session, *, scrum: Scrum, actor: User
) -> Dict[str, Any]:
    """Send what was said about each ticket to the ticket -- here, and on the board.

    **Requirement 8, and it is two writes rather than one.** InnoDay keeps its own
    record (`TicketComment`) and the client's board gets the comment too, because
    a comment that only exists in InnoDay is invisible to everyone reading the
    board -- which is most of the people it is addressed to.

    **At submit, not at each keystroke**, for the same reason the moves are: a
    pick and its comment are an answer somebody is still editing, and `replace_picks`
    exists precisely so a box can be un-ticked. Delivering as they typed would post
    sentences they then withdrew, to a client's board, permanently.

    **Only an update.** A team scrum's per-stop comments are minutes of a meeting
    that the room was in; pushing every one of them out to the board would be a
    different feature with a different audience, and nobody asked for it. Stated
    rather than assumed, because the column is shared.

    **Idempotent through `visit.comment_id`.** A daily update is re-enterable and
    re-closable all day, so this runs repeatedly over the same visits. Delivery is
    keyed on the row that was actually sent, so an unchanged comment is a no-op
    and an *edited* one is a genuinely new comment -- `add_comment` cannot edit a
    board comment, and leaving the old text standing on the board while showing
    the new one here is exactly the misunderstanding this is for. **That marker
    survives a withdrawal** because the visit now does
    (`ScrumTicketVisit.withdrawn_at`); it used to be deleted with the row, which
    is how untick-and-re-tick posted the same sentence to a client's board twice.

    **A withdrawn pick delivers nothing new, and still retries.** Those are not in
    tension: the comment is already InnoDay's and the board is recorded as not
    having it, and taking the pick back cannot make an out-of-step board in step.
    Skipping the retry is how a board that was down at the time ends up never
    getting the comment while the page reports no error -- silent non-delivery,
    which this module ranks as its worst outcome.

    **A push that failed last time is retried**, driven from `visit.comment_error`
    -- the durable evidence, which is why the retry decision lives here rather
    than in `ticket_comment_service`.

    Returns ``commented``/``comments_pushed``/``comment_error``/
    ``comment_notice``. Separate keys from the moves' rather than merged: "the
    board would not take your comment" and "the board would not take your move"
    are different things to be told, and one shared `error` would show whichever
    happened to run second.
    """
    # Imported here, not at module scope, for the reason `apply_recorded_moves`
    # gives: this module is imported by both routers, and the board HTTP clients
    # and Vault credentials are wanted by these two functions alone.
    from src.services.ticket_comment_service import post_ticket_comment
    from src.services.ticket_status_service import classify_push_failure

    if scrum.kind != ScrumKind.UPDATE.value:
        raise ScrumInvalid(
            "Only a personal update delivers the comments it recorded", "kind"
        )

    visits = session.exec(
        select(ScrumTicketVisit)
        .where(ScrumTicketVisit.scrum_id == scrum.id)
        .order_by(ScrumTicketVisit.position)  # type: ignore[arg-type]
    ).all()

    commented = 0
    pushed: Optional[bool] = None
    # Every failure, for the reason the moves collect every failure: a comment
    # the board refused is the one thing here most likely to cause a real
    # misunderstanding between two people, and keeping only the first meant a
    # second one was dropped before anybody could be told.
    errors: List[str] = []
    notices: List[str] = []

    for visit in visits:
        if not (visit.comment or "").strip():
            continue

        outstanding = bool(visit.comment_error)
        if visit.withdrawn_at is not None and not (
            outstanding and visit.comment_id is not None
        ):
            # **A withdrawn pick delivers nothing new** -- it is not part of the
            # update any more. The one thing that still happens to it is a
            # **retry**: its comment is already on InnoDay and the board is
            # recorded as not having it, and taking a pick back cannot make a
            # board that is out of step be in step. This is the whole reason the
            # row is kept rather than deleted.
            continue

        # **Per visit, and it wraps the local write as well as the push.**
        # `deliver_recorded_comments` runs *after* `apply_recorded_moves` in the
        # same request, and `answer.update(...)` is the last thing before the
        # response -- so an exception escaping here is a 500 with no body while
        # the statuses have already been written, pushed to the board, and had
        # their `push_error` persisted. Everywhere else this feature holds the
        # line that no path reports a save it did not get; this is the same rule
        # failing in the other direction, a save that happened reported as
        # nothing at all. One visit's failure costs that visit, not the answer.
        try:
            ticket = session.get(Ticket, visit.ticket_id)
            if ticket is None:
                continue

            result = await post_ticket_comment(
                session,
                ticket=ticket,
                comment=visit.comment,
                actor=actor,
                delivered_comment_id=visit.comment_id,
                retry_push=outstanding,
            )
        except Exception as exc:  # noqa: BLE001 -- classified, then reported
            # Classified for the same reason a board failure is: this string is
            # read by every member of the org, and `str(exc)` on a DBAPI error is
            # the SQL plus its bound parameters. `_safely_record` rolls back
            # first if the transaction is already deactivated.
            message = classify_push_failure(exc, doing="recording a ticket comment")
            errors.append(message)
            pushed = False
            _safely_record(session, visit=visit, comment_error=message)
            continue

        if result.written:
            commented += 1
        if result.error:
            errors.append(result.error)
        if result.notice:
            notices.append(result.notice)
        if result.pushed is not None:
            # Only when a push was actually attempted. `None` means nothing was
            # sent -- nothing outstanding, or a ticket with no board -- and
            # clearing on that is what erases a still-true failure.
            # Three-valued to the end: None until something was actually sent,
            # and False wins over True because one undelivered comment is the
            # thing the reader has to be told about.
            if result.pushed is False:
                pushed = False
            elif pushed is not False:
                pushed = True
            _safely_record(
                session,
                visit=visit,
                comment_id=result.comment_id,
                comment_error=result.error,
            )
        elif result.comment_id is not None and visit.comment_id != result.comment_id:
            # No push attempted, but the local record moved -- either it was just
            # written, or an orphaned `TicketComment` was **adopted** after its
            # visit had been withdrawn. Either way the marker has to land, or the
            # next submit writes and posts the same sentence again.
            _safely_record(session, visit=visit, comment_id=result.comment_id)

    return {
        "commented": commented,
        "comments_pushed": pushed,
        "comment_errors": errors,
        "comment_notices": notices,
    }


def visit_count(session: Session, scrum_id: str) -> int:
    """How many stops this scrum recorded.

    ``COUNT`` in SQL, not ``len()`` of every id. `list_scrums` calls this once
    per row it returns, so at the route's 200-scrum limit the old form issued
    201 statements and dragged 3,000 ids across the wire to print 200 integers.
    """
    return int(
        session.exec(
            select(func.count())
            .select_from(ScrumTicketVisit)
            .where(
                ScrumTicketVisit.scrum_id == scrum_id,
                # A withdrawn pick is not part of the record. Its row survives
                # only to remember whether the board ever got its comment, and
                # counting it would make the page's "recorded so far" number
                # include picks somebody explicitly took back.
                ScrumTicketVisit.withdrawn_at.is_(None),  # type: ignore[union-attr]
            )
        ).one()
    )
