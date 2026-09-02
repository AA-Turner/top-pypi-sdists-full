"""Moving a ticket: the local write, the board push, and what to say when they
disagree.

**One service rather than a method on whoever asked first.** A status move is two
writes to two systems with different owners, and the rules that reconcile them --
which one is authoritative, what happens to `completed_at`, what a third party
being down may and may not cost -- are the same whoever asks. The personal scrum
update asks today (`scrum_service.apply_recorded_moves`); the two ticket `PUT`
routes (`routers/tickets.py`) want the same thing and currently write `status`
and commit with **no board push at all**.

Not in `scrum_service`, which is imported by both `/api/v1` and `/ui`: pulling
Vault credentials and board HTTP clients in there widens both import graphs for a
concern neither router asked for. `scrum_service` *calls* this; it does not
become it.

The rules, in the order they matter:

**1. Local-first, push-second, and the local write is never rolled back because
a third party was down.** Push-first would leave a board write with no local row,
which the next inbound sync would present as a change nobody made from InnoDay --
a phantom edit, attributable to no one. The failure this ordering does allow is
the honest one: InnoDay is ahead of the board, and it says so.

**2. A push failure is reported, never swallowed.** `MoveResult` carries it, the
caller persists it (`ScrumTicketVisit.push_error`), and the page paints it. The
surfaces this feeds have one hard rule -- never report a save you did not get,
and never report a failure you did not get either.

**3. Classify before anything is stored or shown.** This exact finding landed on
PR #641: `str(exc)` on a DBAPI error stringifies to the SQL plus its bound
parameters, and on a connection failure to host, port and user. That string is
rendered to every member of the org.

So only exceptions raised *to be read* pass through, and **the signal is an
explicit `user_message`, not the exception's type**. A type cannot carry that
meaning: the first version of this whitelisted `(BoardAdapterError, ValueError)`
and was wrong in both directions on Linear, the only board that can be verified
live -- `LinearAPIError` is a `RuntimeError` and so lost its message to the
generic one, while `json.JSONDecodeError`, `pydantic.ValidationError`,
`UnicodeDecodeError` and a bare `ValueError` carrying Linear's raw GraphQL error
array all passed straight through to every org member. `BoardAdapterError` sets
`user_message`; adapters wrap what a board told them in it. Everything else
becomes `GENERIC_PUSH_ERROR` and is logged server-side with its traceback.

**4. Never guess an assignee.** `identity_resolution.py` refuses fuzzy
display-name matching inbound -- "two people called 'Alex' on a client's board is
normal; guessing between them silently reassigns someone's work" -- and reversing
the direction does not make the guess safe. Email, then a *claimed* handle, then
nothing, and say so.

**5. `BoardRegistration.errored_at` is not touched.** It means "the last *sync* of
this board failed" and the dashboard's status icon reads it. One ticket's push
failure reddening the whole board is the misreport #641 exists to remove.
"""

import logging
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from sqlmodel import Session, select

from src.adapters.base_adapter import BoardCapabilityError
from src.domain.board import BoardRegistration
from src.domain.organization import Organization
from src.domain.ticket import Ticket, TicketStatus
from src.domain.user import User
from src.domain.user_identity import IdentityPlatform, UserIdentity
from src.services.board_adapter_factory import build_board_adapter, resolve_board_token

logger = logging.getLogger(__name__)

#: What a reader is told when the push failed for a reason that was not written
#: to be read. Deliberately says *what to do* rather than *what happened*: the
#: real cause is in the server log, where it can safely include the detail this
#: string must not.
GENERIC_PUSH_ERROR = (
    "The board could not be updated. InnoDay has the change; the board does not. "
    "Check the board connection, then try again."
)

#: The same thing for the *pull* direction, which `board_sync_service` records on a
#: failed sync. Kept beside `GENERIC_PUSH_ERROR` rather than in that module so that
#: every string a reader may be told about a board failure is decided in one place,
#: which is the property `classify_push_failure`'s docstring argues for. The wording
#: differs because what the reader can conclude does: a failed push means InnoDay is
#: ahead of the board, a failed pull means InnoDay may be behind it.
GENERIC_SYNC_ERROR = (
    "The board could not be read. The tickets InnoDay holds may be out of date. "
    "Check the board connection, then sync again."
)

#: Returned by `_completed_at_for` to mean "do not touch this column", which
#: ``None`` cannot say -- ``None`` is a value the column legitimately holds.
_UNCHANGED = object()


def _assignee_error(message: str) -> str:
    """A push that reached the board for the status and not for the assignee.

    Named separately because the two halves land differently: the move is on the
    board, the ownership is not, and the next inbound sync will overwrite the
    local assignment from a board that still thinks the ticket is unowned. A
    reader needs to know it is the *assignment* that is outstanding.
    """
    return f"The move reached the board; the assignment did not: {message}"


#: How the "your assignment did not reach the board" case is worded. It names all
#: three things the reader needs: that the move itself worked, that the
#: assignment is local-only, and that it will not survive -- plus where to fix
#: it, because a warning with no remedy is just noise.
_ASSIGNEE_UNRESOLVED = (
    "{summary} is yours in InnoDay, but the board does not know who you are, so "
    "the next sync will overwrite it. Claim your board handle on your profile to "
    "make it stick."
)

#: Said when the board type has no assignee at all (Jira/Trello/Notion today).
#: Deliberately *not* `_ASSIGNEE_UNRESOLVED`: that one tells somebody to claim a
#: handle, which cannot help when the board has nowhere to put one.
_BOARD_CANNOT_ASSIGN = (
    "{summary} is yours in InnoDay. This board type does not record an assignee, "
    "so the ownership stays here only."
)

#: Board platforms whose members can be matched to an InnoDay `UserIdentity`.
#: Keyed on the board type's value so a new board type simply has no handle path
#: rather than a wrong one.
_HANDLE_PLATFORMS = {
    "linear": IdentityPlatform.LINEAR,
    "jira": IdentityPlatform.JIRA,
    "trello": IdentityPlatform.TRELLO,
    "github": IdentityPlatform.GITHUB,
}


@dataclass
class MoveResult:
    """What happened, in parts a caller has to be able to tell apart.

    ``applied`` -- the local state is now what was asked for. True even when it
    already was; it is never False alongside a push error, because a third party
    being down does not undo a committed local write.

    ``written`` -- whether *this call* changed the local row. Distinct from
    ``applied`` so a caller can count real moves rather than visits, and so a
    no-op cannot restamp anything.

    ``pushed`` -- **three-valued, and the distinction is load-bearing.** ``True``
    the board was updated; ``False`` a push was attempted and failed; ``None``
    no push was attempted at all -- no board, or nothing outstanding to send.
    Collapsing ``None`` into ``False`` is what let a caller "clear the error on
    success" and thereby delete a still-true `push_error` on a no-op that never
    contacted the board.

    ``assignee_pushed`` -- ``None`` the move was not a take, so nothing was
    attempted; ``False`` attempted and not completed.

    ``error`` / ``notice`` -- different severities, kept apart. An **error** is
    something out of step that InnoDay could not fix and that must outlive the
    response: the board refused, or the assignee push failed. A **notice** is a
    true statement about a configuration the reader can act on -- the board does
    not know who they are -- which is recomputable at any time and therefore
    needs no durable record. Sending a 429 down the notice path is how somebody
    gets told to go and edit their profile about a rate limit.
    """

    applied: bool
    written: bool = False
    pushed: Optional[bool] = None
    error: Optional[str] = None
    assignee_pushed: Optional[bool] = None
    notice: Optional[str] = None


def _completed_at_for(
    new_status: TicketStatus, *, was: Optional[TicketStatus]
) -> Optional[datetime]:
    """The completion timestamp after moving from ``was`` to ``new_status``.

    **Cleared when leaving DONE, not merely set when entering it.** That
    asymmetry is the whole bug: `SummaryService._activity_at` reads
    `completed_at` as evidence of a real terminal transition, so a reopened
    ticket that keeps its old date reads as in-window finished work for as long
    as the window covers the day it was closed. Board sync learned this
    (`board_sync_service.py:511-524`); neither ticket `PUT` route has.

    **Only those two transitions touch the column.** An earlier version returned
    NULL for every non-DONE status, so TODO → IN_PROGRESS actively blanked it.
    Harmless while nothing sets `completed_at` on a non-DONE ticket -- but that
    is an assumption about every other writer, present and future, and the rule
    this implements says "cleared when leaving DONE". Anything else is left
    alone, which is also what makes the sentinel ``None`` unambiguous below.
    """
    if new_status == TicketStatus.DONE:
        return datetime.utcnow()
    if was == TicketStatus.DONE:
        return None
    return _UNCHANGED


def classify_push_failure(
    exc: Exception,
    *,
    doing: str = "pushing a ticket status to its board",
    generic: str = GENERIC_PUSH_ERROR,
) -> str:
    """The message a reader may see for ``exc``.

    **Public, and shared.** `ticket_comment_service` pushes to the same boards
    through the same adapters and hands the result to the same readers, so it
    classifies with this rather than with a second copy. Two copies of "which
    exceptions are fit to read" is how one of them comes to admit a stack trace.
    ``doing`` only names the operation in the server-side log line; the message
    handed back to a reader is deliberately identical either way, because what
    they can do about it is.

    ``generic`` is the one exception to that last sentence, and it exists for the
    one caller whose direction differs: `board_sync_service` *pulls*, so
    `GENERIC_PUSH_ERROR`'s "InnoDay has the change; the board does not" would be
    the opposite of true. It passes `GENERIC_SYNC_ERROR`. **Only the fallback is
    parameterised** — the classification, which is the part that decides whether
    an internal string reaches a reader, stays here and is not overridable.

    **Keyed on an explicit signal, not on the exception's type.** The signal is
    `user_message`, which `BoardAdapterError` sets: raising one is an author
    stating that the text is fit for a person to read.

    The previous version whitelisted `(BoardAdapterError, ValueError)` and was
    wrong in both directions on the only board that can be verified live:

    * `LinearAPIError` is a `RuntimeError`, so every real 401/403/429/502 was
      classified as unexpected and lost the actionable message. (`LinearAPIError`
      no longer reaches here at all -- the adapter wraps it -- but a type-based
      whitelist would have kept saying yes to the wrong set.)
    * `json.JSONDecodeError`, `pydantic.ValidationError` and `UnicodeDecodeError`
      are `ValueError` subclasses, and `linear_api` raised a bare `ValueError`
      carrying Linear's whole raw error array. All four went to every org member
      verbatim.

    Everything unsignalled is replaced and logged with its traceback, which is
    where a host name, SQL or a bound parameter is safe and a rendered string is
    not.
    """
    message = getattr(exc, "user_message", None)
    if isinstance(message, str) and message.strip():
        return message
    logger.exception("Unexpected failure %s", doing)
    return generic


def _member_names(member: Dict[str, Any]) -> List[str]:
    """Every name this board member could reasonably be *claimed* as.

    ``displayName`` first because on Linear that is the unique ``@``-handle --
    the thing somebody means by "my Linear handle". ``name`` is their full name
    and is not unique; it is accepted only because a person may have claimed
    that spelling, and never as a tie-break (see the ambiguity rule below).
    """
    return [
        str(value).strip().lower()
        for key in ("displayName", "display_name", "name")
        for value in [member.get(key)]
        if value
    ]


def _resolve_board_member(
    session: Session,
    *,
    members: List[Dict[str, Any]],
    actor: User,
    registration: BoardRegistration,
) -> Optional[str]:
    """The board's id for ``actor``, or None -- **and None is a normal answer.**

    Matched on the same kinds of evidence the inbound resolver uses
    (`identity_resolution.py`), in the same order:

    1. **Email**, case-insensitively. Boards often withhold it -- Atlassian
       privacy settings, Trello never exposes it at all -- so it is a strong
       match when present and absent more often than not.
    2. **A claimed handle** for this platform, project row before global. A
       `UserIdentity` row only ever exists because a person said "this handle is
       me", which is what makes it identity rather than a guess.
    3. **Nothing.** There is no display-name tail and there must never be one.

    **A handle that matches more than one member resolves to nobody.** That is
    the reachable half of the two-Alexes hazard: not an unconditional name
    fallback (there is none), but a genuine claim colliding with a board where
    two people answer to it. Returning the first hit would silently assign
    somebody else's work, and which one it is depends on the order the board
    happened to list them in.

    Not an exact mirror of the inbound resolver, and the differences are real:
    inbound also reads `users.jira_email`, requires an active
    `OrganizationMembership`, and matches against `BoardAssignee.handle` -- which
    the Linear adapter never populates. The membership requirement is redundant
    here because the actor is the signed-in viewer of this org's own page.
    """
    email = (actor.email or "").strip().lower()
    if email:
        for member in members:
            if (member.get("email") or "").strip().lower() == email:
                return member.get("id")

    platform = _HANDLE_PLATFORMS.get(
        getattr(registration.board_type, "value", registration.board_type)
    )
    if platform is None:
        return None

    rows = session.exec(
        select(UserIdentity).where(
            UserIdentity.user_id == actor.id,
            UserIdentity.platform == platform,
            (UserIdentity.project_id == registration.project_id)
            | (UserIdentity.project_id.is_(None)),  # type: ignore[union-attr]
        )
    ).all()
    # The project's own row wins over the global one: it exists precisely because
    # the generic answer was wrong on this board.
    claimed = [row.handle for row in rows if row.project_id] + [
        row.handle for row in rows if not row.project_id
    ]
    for handle in claimed:
        wanted = (handle or "").strip().lower()
        if not wanted:
            continue
        matched = [m.get("id") for m in members if wanted in _member_names(m)]
        if len(matched) == 1:
            return matched[0]
        if matched:
            logger.info(
                "Board handle %r matches %d members of board %s -- refusing to "
                "choose between them",
                handle,
                len(matched),
                registration.id,
            )
            return None
    return None


async def _push(
    session: Session,
    *,
    ticket: Ticket,
    new_status: TicketStatus,
    actor: User,
    assign_to_actor: bool,
    registration: BoardRegistration,
) -> MoveResult:
    """Everything that talks to the board. Raises nothing the caller must catch.

    Split out so the local write above it is a straight line: the whole of the
    "and now a third party is involved" problem is inside this function, and the
    caller's only job is to decide what to do with the answer.

    **The database reads in here are wrapped in a SAVEPOINT.** Three of them
    happen inside the blanket ``except`` -- the organization, the Vault
    credential (a `SECURITY DEFINER` function call), and the claimed handle. On
    Postgres a failure in any of them *deactivates the transaction*: every later
    statement is refused and ``COMMIT`` silently becomes ``ROLLBACK``. The caller
    would then fail to write `push_error` -- the record that exists precisely so
    a push failure outlives the response reporting it -- and, because that write
    is deliberately wrapped so it can never replace the failure it reports, would
    lose it to a log line. `session.begin_nested()` contains the damage so the
    outer transaction is still usable. SQLite has no such state, which is why
    this class of bug is invisible to all but the Postgres tests.
    """
    try:
        with session.begin_nested():
            org = session.get(Organization, ticket.organization_id)
            token = resolve_board_token(session, registration, org)
            # **Inside the savepoint too.** It reads no database for Linear or
            # Trello, but the Jira OAuth branch calls `ensure_fresh_jira_token`,
            # which does -- and that read is as able to abort the transaction as
            # the credential lookup above it. Leaving it outside protected the
            # cheaper half of the same hazard. The adapter it returns refreshes
            # its own token later on a session of its own, so nothing after this
            # point can poison ours.
            adapter = await build_board_adapter(registration, token, session)
    except Exception as exc:  # noqa: BLE001 -- classified, then reported
        return MoveResult(applied=True, pushed=False, error=classify_push_failure(exc))

    try:
        # **Mandatory, and separate.** `build_board_adapter` does not call it,
        # and `LinearBoardAdapter.update_ticket_status` reads
        # `state_name_to_id`, which nothing but `initialize` fills. Omitting it
        # raises "Unknown Linear workflow state" against a real board and
        # nothing at all against a mock -- which is why it has a test with a
        # stub that reads the map at the moment of the call.
        await adapter.initialize(token)
        await adapter.update_ticket_status(ticket, new_status.value)
    except Exception as exc:  # noqa: BLE001 -- classified, then reported
        return MoveResult(applied=True, pushed=False, error=classify_push_failure(exc))

    if not assign_to_actor:
        return MoveResult(applied=True, pushed=True)

    # **The status is on the board now and stays there.** Everything below can
    # only downgrade the *assignment*, never the move -- a board that cannot
    # assign at all (three of the four adapters) must not take the status push
    # down with it.
    try:
        metadata = await adapter.get_board_metadata()
        members = list(metadata.get("members") or [])
        with session.begin_nested():
            board_user_id = _resolve_board_member(
                session, members=members, actor=actor, registration=registration
            )
    except Exception as exc:  # noqa: BLE001
        return MoveResult(
            applied=True,
            pushed=True,
            assignee_pushed=False,
            error=_assignee_error(classify_push_failure(exc)),
        )

    if not board_user_id:
        # **Not a failure -- a configuration the reader can fix.** Nothing broke:
        # the board simply has no way to tell which of its members this person
        # is. It is a *notice* rather than an error precisely so it is not
        # persisted: it is recomputable from the same data at any time, and it
        # points at a remedy, which the branch below must not.
        return MoveResult(
            applied=True,
            pushed=True,
            assignee_pushed=False,
            # Truncated: a board-supplied summary can be 500 characters and this
            # is a one-line banner. Board-controlled text either way, which is
            # why the page writes it with `textContent` and not into markup.
            notice=_ASSIGNEE_UNRESOLVED.format(summary=(ticket.summary or "")[:60]),
        )

    try:
        await adapter.set_board_assignee(ticket, board_user_id)
    except BoardCapabilityError:
        # **A fact about the board type, not a failure.** Three of the four
        # adapters have no assignee to set, and they will refuse identically
        # forever. Recording that as a `push_error` would make it permanent and
        # un-clearable -- and because a stored error is what asks for a retry, it
        # would re-push the status on every later submit for something that can
        # never succeed. This is the clean degradation the separate call was
        # added for: the move landed, the ownership is InnoDay's alone, and the
        # page says so once.
        return MoveResult(
            applied=True,
            pushed=True,
            assignee_pushed=False,
            notice=_BOARD_CANNOT_ASSIGN.format(summary=(ticket.summary or "")[:60]),
        )
    except Exception as exc:  # noqa: BLE001
        # **A failure, and persisted as one.** The member resolved and the board
        # can assign; this particular push did not land. Sending it down the
        # notice path would tell somebody to go and claim a board handle they
        # already have -- a false diagnosis, after a 429, pointing at a remedy
        # that cannot help -- and would leave nothing recording that the board
        # thinks the ticket is unowned while InnoDay says it is theirs, which the
        # next sync then silently confirms.
        return MoveResult(
            applied=True,
            pushed=True,
            assignee_pushed=False,
            error=_assignee_error(classify_push_failure(exc)),
        )

    return MoveResult(applied=True, pushed=True, assignee_pushed=True)


async def move_ticket_status(
    session: Session,
    *,
    ticket: Ticket,
    new_status: TicketStatus,
    actor: User,
    assign_to_actor: bool = False,
    retry_push: bool = False,
) -> MoveResult:
    """Move ``ticket`` to ``new_status``, locally and then on its board.

    ``assign_to_actor`` is the "I am taking this on" half. It writes **both**
    columns: `assigned_to`, the FK every InnoDay reader uses (`my_tickets`,
    `viewer_has_identity`, contributor avatars, summary attribution), and
    `assignee`, the board's display mirror that `ProjectTicketRow.owner` reads.
    Writing one without the other leaves the ticket assigned on exactly one of
    the two surfaces that show it.

    **"The local state is correct" and "the board has been told" are different
    questions, and this used to answer the second with the first.** A ticket
    already in the target status short-circuited to "pushed", without pushing --
    so after a failed push no later submit could ever re-attempt it (the status
    matches, so there is nothing to re-apply), and the caller, handed no error,
    cleared the record that the board disagreed. The board stayed out of step,
    permanently and silently, while the page said it had been updated.

    ``retry_push`` is how a caller says "the last push failed": the local write
    is still skipped when nothing changed, and the push happens anyway. The
    caller owns that knowledge because the caller owns the durable record of it
    (`ScrumTicketVisit.push_error`).

    **Idempotent.** With nothing outstanding, a repeat is a no-op: nothing is
    written, nothing is pushed, and ``pushed`` is ``None`` rather than ``True``
    so nobody mistakes it for a push that happened. Asserted as "`updated_at` did
    not change" rather than "no error", because a re-stamped `updated_at`
    republishes an idle ticket as freshly active to every consumer reading that
    column as an activity signal.

    Note the asymmetry: the status being settled does not settle the assignment.
    A ticket already IN_PROGRESS but unowned is exactly what "take this on"
    means.

    Never raises for a board problem. The board is a third party; its failures
    are data (`MoveResult.error`), not control flow.
    """
    take_outstanding = assign_to_actor and ticket.assigned_to != actor.id
    settled = ticket.status == new_status and not take_outstanding

    written = False
    if not settled:
        # Read the old status *before* overwriting it: the `completed_at` rule is
        # about the transition, not about the destination.
        completed_at = _completed_at_for(new_status, was=ticket.status)
        ticket.status = new_status
        if completed_at is not _UNCHANGED:
            ticket.completed_at = completed_at
        if assign_to_actor:
            ticket.assigned_to = actor.id
            ticket.assignee = actor.full_name or actor.email
        # Matching `board_sync_service`'s rule: restamped because something moved,
        # which is what every activity reader takes this column to mean.
        ticket.updated_at = datetime.now(timezone.utc)
        session.add(ticket)
        session.commit()
        session.refresh(ticket)
        written = True

    if settled and not retry_push:
        return MoveResult(applied=True, written=False)

    registration = (
        session.get(BoardRegistration, ticket.board_registration_id)
        if ticket.board_registration_id
        else None
    )
    if registration is None or not ticket.external_ticket_id:
        # No board, or a ticket that exists only here. Nothing to push to is not
        # a push failure, and reporting one would train people to ignore the
        # banner that matters. `pushed` stays None for the same reason.
        return MoveResult(applied=True, written=written)

    result = await _push(
        session,
        ticket=ticket,
        new_status=new_status,
        actor=actor,
        assign_to_actor=assign_to_actor,
        registration=registration,
    )
    result.written = written
    return result
