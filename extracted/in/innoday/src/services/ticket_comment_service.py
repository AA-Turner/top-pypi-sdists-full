"""Saying something about a ticket: the local record, the board push, and what to
say when only one of them happened.

**The same shape as `ticket_status_service`, on purpose.** A comment is two
writes to two systems with different owners, and the rules that reconcile them
are the rules that were already settled for a status move:

**1. Local-first, push-second, and the local write is never rolled back because a
third party was down.** InnoDay keeps its own record whatever the board does.

**2. A push failure is reported, never swallowed.** `CommentResult` carries it,
the caller persists it (`ScrumTicketVisit.comment_error`), and the page paints
it. *Reporting a comment as delivered when the board never got it is the failure
mode most likely to cause a real misunderstanding between teammates* -- somebody
writes "I'm blocked on this, don't start it" and everyone reading the board sees
nothing at all.

**3. Classified before anything is stored or shown**, through the *same*
`classify_push_failure` the status push uses rather than a second copy of the
whitelist. What lands in `comment_error` is read by every member of the org, and
`str(exc)` on a DBAPI error is SQL with its bound parameters.

**4. A board that cannot comment is a fact, not a failure** -- a
`BoardCapabilityError` becomes a notice, is not persisted, and therefore does not
ask to be retried on every later submit. That distinction was a review finding on
the status push; it holds identically here.

**5. `BoardRegistration.errored_at` is not touched.** It means "the last *sync*
of this board failed" and the dashboard reads it.

Two things are specific to comments rather than inherited:

**The author has to be in the text.** The board has no idea which InnoDay user
wrote this -- the push authenticates as the board *integration*, so an
un-attributed comment appears to come from a robot. There is nowhere else to put
it: `add_comment` takes a body and nothing else on all four adapters.

**A falsy return is a failure.** `BaseBoardAdapter.add_comment` returns `bool`,
and `LinearBoardAdapter` hands back exactly what `commentCreate.success` said --
so a board that *declines* the comment raises nothing and returns `False`. A
caller that only watches for exceptions reports that comment as delivered. This
is the single most likely way this path half-works against a real board while
every mock-based test passes.

Trello and Notion used to `return True` unconditionally, discarding what their
API had said, so the contract could not bite on the two boards where it failed
*silently*. Both now answer with the API's own result.

---

**Delivery is at-least-once. It is not exactly-once, and the difference is
disclosed rather than defended.** `post_ticket_comment` reads its memory, pushes,
and writes the memory back, with no lock and no unique constraint. Four routes
by which one sentence reaches a board twice:

1. **Two tabs, or two clicks.** Both submits read the marker as absent and both
   push. Closing this needs a unique constraint or a lock.
2. **A lost response.** A push the board *accepted* whose reply never arrived is
   stored as a failure and retried verbatim on the next submit. Retrying is the
   right choice -- the alternative is silently losing a comment -- but it is a
   choice for at-least-once.
3. **A recorder that fails both attempts** after a successful push loses
   `comment_id`, and the next submit writes and posts again.

The route that was reachable by ordinary use -- withdrawing a pick and taking it
back -- used to delete the visit holding the marker; withdrawal flags the row now
instead, so the memory survives. The rest are here so nobody reads this file as
promising more than it does.

**And repeating is the safe direction.** Every route above ends with the board
holding the sentence twice. The alternative failure -- suppressing a push for a
comment the board never got, while reporting success -- is the one this module
ranks worst, and an earlier attempt to close (1) and (3) by matching on text
manufactured exactly that. When the two cannot both be had, this errs towards the
board being told.
"""

import logging
from dataclasses import dataclass
from typing import Optional

from sqlmodel import Session

from src.adapters.base_adapter import BoardCapabilityError
from src.domain.board import BoardRegistration
from src.domain.organization import Organization
from src.domain.ticket import Ticket, TicketComment
from src.domain.user import User
from src.services.board_adapter_factory import build_board_adapter, resolve_board_token
from src.services.ticket_status_service import classify_push_failure

logger = logging.getLogger(__name__)

#: Said when the board type has no comments at all. Deliberately not an error:
#: nothing broke, and nothing will ever succeed, so recording it would make it
#: permanent *and* mark the visit for a retry that can never work -- the same
#: reasoning `_BOARD_CANNOT_ASSIGN` carries in `ticket_status_service`.
_BOARD_CANNOT_COMMENT = (
    "Your comment is saved in InnoDay. This board type does not take comments, "
    "so it stays here only."
)

#: What a reader is told when the board answered without raising and without
#: accepting. `commentCreate.success == false` on Linear is exactly this: no
#: exception, no comment. Written to be *actionable* -- the reader's comment is
#: safe, and the board is the thing that is behind.
_BOARD_DECLINED = (
    "The board would not take the comment. InnoDay has it; the board does not. "
    "Check the board connection, then submit again."
)


def attributed(comment: str, actor: User) -> str:
    """``comment``, signed with who wrote it.

    **The board cannot work this out.** The push authenticates as the board
    *integration*, not as a person, so every comment InnoDay sends arrives from
    the same machine account -- an unattributed one reads as the robot's opinion.

    Plain text with a blank line, not markdown: Linear renders markdown, Jira
    uses its own wiki syntax, Trello renders almost none of it, and a `**bold**`
    that shows up literally on three of the four boards is worse than none.
    """
    who = (actor.full_name or actor.email or "Someone").strip()
    return f"{who} (via InnoDay):\n\n{comment}"


@dataclass
class CommentResult:
    """What happened, in the parts a caller has to be able to tell apart.

    ``comment_id`` -- the local `TicketComment` this comment now lives in. Set
    whether or not this call created it, because the caller stores it as the
    marker for "already delivered" and needs it either way.

    ``written`` -- whether *this call* created the local row. Distinct from
    ``comment_id`` so a re-submit of an unchanged comment can be a genuine no-op.

    ``pushed`` -- **three-valued, exactly as `MoveResult.pushed` is.** ``True``
    the board took it; ``False`` a push was attempted and did not land; ``None``
    no push was attempted -- no board, or nothing outstanding. Collapsing ``None``
    into ``True`` is what would let a caller clear a still-true `comment_error`
    on a no-op that never contacted the board.

    ``error`` / ``notice`` -- an **error** is something out of step that must
    outlive the response; a **notice** is a true statement about a configuration,
    recomputable at any time and therefore never persisted.
    """

    comment_id: Optional[int] = None
    written: bool = False
    pushed: Optional[bool] = None
    error: Optional[str] = None
    notice: Optional[str] = None


async def _push(
    session: Session,
    *,
    ticket: Ticket,
    body: str,
    registration: BoardRegistration,
) -> CommentResult:
    """Everything that talks to the board. Raises nothing the caller must catch.

    **The database reads are wrapped in a SAVEPOINT**, for the reason
    `ticket_status_service._push` records: on Postgres a failure inside the
    blanket ``except`` -- the organization lookup, the Vault credential (a
    ``SECURITY DEFINER`` call), the Jira OAuth refresh -- *deactivates the
    transaction*, so every later statement is refused and ``COMMIT`` silently
    becomes ``ROLLBACK``. The caller would then fail to write `comment_error`,
    which exists precisely so this outlives the response. SQLite has no such
    state, which is why this class of bug is invisible without the Postgres run.
    """
    try:
        with session.begin_nested():
            org = session.get(Organization, ticket.organization_id)
            token = resolve_board_token(session, registration, org)
            adapter = await build_board_adapter(registration, token, session)
    except Exception as exc:  # noqa: BLE001 -- classified, then reported
        return CommentResult(
            pushed=False,
            error=classify_push_failure(exc, doing="posting a ticket comment"),
        )

    try:
        # **Mandatory, and separate.** `build_board_adapter` does not call it.
        # Linear's `add_comment` happens not to read anything `initialize` fills
        # today, but the Jira and Trello adapters resolve their own client state
        # there and an uninitialised adapter is not a thing any board method is
        # documented to accept -- getting this right only for the board that
        # currently tolerates it is how the next board type breaks in production.
        await adapter.initialize(token)
        accepted = await adapter.add_comment(ticket, body)
    except BoardCapabilityError:
        # A fact about the board type. Not persisted, so it cannot become a
        # permanent error asking for a retry that can never succeed.
        return CommentResult(pushed=False, notice=_BOARD_CANNOT_COMMENT)
    except Exception as exc:  # noqa: BLE001 -- classified, then reported
        return CommentResult(
            pushed=False,
            error=classify_push_failure(exc, doing="posting a ticket comment"),
        )

    if not accepted:
        # **Answered without raising and without accepting.** `add_comment`
        # returns `bool`, and Linear returns `commentCreate.success` verbatim, so
        # this is a real outcome rather than a defensive branch -- and the one
        # that silently reports an undelivered comment as delivered.
        return CommentResult(pushed=False, error=_BOARD_DECLINED)

    return CommentResult(pushed=True)


async def post_ticket_comment(
    session: Session,
    *,
    ticket: Ticket,
    comment: str,
    actor: User,
    delivered_comment_id: Optional[int] = None,
    retry_push: bool = False,
) -> CommentResult:
    """Record ``comment`` against ``ticket`` locally, then send it to the board.

    ``delivered_comment_id`` is the caller's durable memory of what it has already
    delivered (`ScrumTicketVisit.comment_id`). Its two jobs:

    * **Idempotence.** A daily update is re-enterable and re-closable until the
      day ends, so submitting happens repeatedly. Without this, every re-submit
      would post the day's comments to the client's board again.
    * **Telling an edit from a repeat.** The text is compared against the row
      this points at. Unchanged is a no-op; changed is a genuinely new comment,
      because `add_comment` cannot edit a board comment and leaving the old one
      standing while showing the new one here is the disagreement this path
      exists to prevent.

    **The marker is the only memory, and it has to be one.** An earlier version
    added a fallback that searched the already-written `TicketComment` rows by
    text when the marker was missing. That answered *"has this person written this
    sentence today?"* while this function needs *"does the board have it"* -- two
    different questions, and every place they came apart the caller reported a
    delivery that had not happened: a comment written before a failed push was
    adopted as delivered, a comment written by `/api/v1` suppressed the push
    entirely, and a reverted edit left the board's last word contradicting
    InnoDay. Silent non-delivery is the worst outcome this module has, and the
    fallback manufactured it.

    The real defect was the marker's *home*, not the marker: it lived on a visit
    that was deleted when a pick was withdrawn. Withdrawal now flags the row
    instead (`ScrumTicketVisit.withdrawn_at`), so `comment_id` and `comment_error`
    both survive a withdrawal and the search is unnecessary. **The only evidence
    that the board has something is evidence that we sent it.**

    ``retry_push`` is how a caller says "the last push failed" -- the local write
    is still skipped when nothing changed, and the push happens anyway. The caller
    owns that knowledge because the caller owns the durable record of it
    (`ScrumTicketVisit.comment_error`).

    **Delivery is at-least-once, not exactly-once**, and the module docstring lists
    the routes by which it can repeat. This closes the one that was reachable by
    ordinary use; the rest need a lock or a unique constraint to close and are
    disclosed instead.

    Never raises for a board problem. The board is a third party; its failures are
    data, not control flow.
    """
    text = (comment or "").strip()
    if not text:
        # Nothing to say is not a failure and is not a comment. Callers reach here
        # with an empty box more often than with a full one.
        return CommentResult()

    delivered = (
        session.get(TicketComment, delivered_comment_id)
        if delivered_comment_id is not None
        else None
    )
    # **The one text comparison, and it is about editing rather than delivery.**
    # The marker says what was sent; if what is in the box no longer matches it,
    # this is a new thing to say. `add_comment` cannot edit a board comment, so a
    # changed sentence has to be posted as another one -- leaving the old wording
    # standing on the board while InnoDay shows the new one is exactly the
    # disagreement between teammates this path exists to prevent.
    settled = delivered is not None and (delivered.comment or "") == text

    written = False
    if not settled:
        row = TicketComment(
            ticket_id=ticket.id,
            # **A UUID string, and the column has to be one.** `users.id` is a
            # UUID string while this column was originally created as an integer,
            # which 500'd every write that ever reached it. This path is the first
            # thing to write it in anger, so it is verified on Postgres rather
            # than only on SQLite, whose loose typing accepts either.
            commenter_id=actor.id,
            comment=text,
        )
        session.add(row)
        session.commit()
        session.refresh(row)
        delivered = row
        written = True

    result = CommentResult(comment_id=delivered.id if delivered else None)

    if not written and not retry_push:
        return result

    registration = (
        session.get(BoardRegistration, ticket.board_registration_id)
        if ticket.board_registration_id
        else None
    )
    if registration is None or not ticket.external_ticket_id:
        # No board, or a ticket that exists only here. Nothing to push to is not a
        # push failure, and reporting one would train people to ignore the banner
        # that matters. `pushed` stays None for the same reason.
        result.written = written
        return result

    pushed = await _push(
        session, ticket=ticket, body=attributed(text, actor), registration=registration
    )
    pushed.comment_id = result.comment_id
    pushed.written = written
    return pushed
