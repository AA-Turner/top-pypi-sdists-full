"""
Board Synchronization Service

Handles background synchronization of tickets from external boards (Trello/Jira)
to the InnoDay platform. This service implements the core sync logic for
GitHub Issue #13: Board-Based Ticket Synchronization.
"""

import logging
from datetime import datetime, timezone
from typing import Dict, List, Optional, Tuple

from sqlalchemy import func
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, select

from src.adapters import (
    BaseBoardAdapter,
    BoardAdapterError,
)
from src.adapters.board_assignee import BoardAssignee, read_board_assignee
from src.api.jira_api import JiraAPI
from src.api.trello_api import TrelloAPI
from src.database import engine
from src.domain import (
    BoardRegistration,
    BoardSyncHistory,
    BoardType,
    SyncStatus,
    Ticket,
    TicketStatus,
    TimelineEventType,
)
from src.domain.user_identity import IdentityPlatform
from src.services.board_adapter_factory import build_board_adapter, is_oauth_jira
from src.services.identity_resolution import IdentityResolutionService
from src.services.project_timeline_writer import add_timeline_entry
from src.services.ticket_status_service import (
    GENERIC_SYNC_ERROR,
    classify_push_failure,
)
from src.utils.time_windows import parse_iso_naive, parse_iso_utc

logger = logging.getLogger(__name__)

# Attempts to claim a project_ref_number before giving up on a ticket. Each
# retry costs one MAX() read; collisions only happen when two syncs of the same
# project overlap, so a small number is plenty.
_PROJECT_REF_RETRIES = 4

_PROJECT_REF_CONSTRAINT = "uq_ticket_project_ref_number"


def _same_field(current, incoming) -> bool:
    """Whether a persisted value and an incoming one are the same board fact.

    Empty string and NULL are the same absence here: adapters that omit a field
    hand back ``""`` while the column holds ``None``, and treating that as a
    change would restamp every ticket on every sync -- precisely the bug the
    comparison exists to prevent.
    """
    if current is None and incoming == "":
        return True
    if incoming is None and current == "":
        return True
    return current == incoming


def _is_project_ref_conflict(exc: IntegrityError) -> bool:
    """Whether this IntegrityError is the project_ref_number race, not another one.

    Narrow on purpose: a genuinely different violation (a duplicate
    ``external_ticket_id``, a null FK) must propagate rather than be retried
    pointlessly.

    The two backends word it differently, so both forms are matched --
    Postgres names the constraint (``violates unique constraint
    "uq_ticket_project_ref_number"``), SQLite names the columns instead
    (``UNIQUE constraint failed: ticket.project_id, ticket.project_ref_number``).
    ``project_ref_number`` appears in no other unique constraint, so the column
    form is unambiguous.
    """
    message = str(getattr(exc, "orig", exc))
    if _PROJECT_REF_CONSTRAINT in message:
        return True
    return "project_ref_number" in message and "unique" in message.lower()


def _parse_since(value) -> Optional[datetime]:
    """An ISO timestamp (or a datetime) → an aware UTC datetime, or None.

    Naive input is read as UTC. A naive value compared against an aware one
    raises TypeError, and inside the sync loop that would surface as a
    per-ticket "failed to process" warning on every single ticket -- a
    filtering bug wearing a board-error costume.

    Unparseable means "no watermark", never an error: a malformed option must
    degrade to the full pull the caller would have got anyway, not fail a sync.
    It is logged, though -- a silently ignored watermark looks identical to a
    board that genuinely had no movement.
    """
    if value is None or value == "":
        return None
    parsed = parse_iso_utc(value)
    if parsed is None:
        # Logged, not silent -- an ignored watermark is indistinguishable from
        # a board that genuinely had no movement. The coercion itself is shared
        # (`src/utils/time_windows.py`); only this policy is local.
        logger.warning("Ignoring unparseable sync `since` option %r", value)
    return parsed


class BoardSyncService:
    """
    Service for synchronizing tickets from external boards to InnoDay.

    This service handles the actual synchronization logic called by background tasks.
    It manages API connections, data transformation, and database updates.

    Now uses adapter pattern internally to abstract platform differences.
    """

    def __init__(self):
        self.trello_api = None
        self.jira_api = None
        # Cache adapters by (board_id, token) -- see _get_adapter
        self.adapters: Dict[Tuple[str, str], BaseBoardAdapter] = {}

    async def _get_adapter(
        self, registration: BoardRegistration, token: str, session: Session
    ) -> BaseBoardAdapter:
        """
        Get or create appropriate adapter for the board.

        This method returns a cached adapter if available, or creates a new one.
        The adapter pattern abstracts the differences between Trello and Jira.

        Args:
            registration: BoardRegistration domain object
            token: Authentication token/credentials, or OAUTH_TOKEN_SENTINEL
                for a Jira board whose stored credential is OAuth (see
                payload_to_legacy_token)
            session: DB session, used only to resolve an initial OAuth
                access_token/cloud_id pair for Jira boards -- every
                subsequent call on the resulting adapter refreshes its own
                token via JiraBoardAdapter._jira_request_context, opening
                its own session as needed; this method's session is not
                retained anywhere.

        Returns:
            Appropriate adapter instance (TrelloBoardAdapter or JiraBoardAdapter)

        Raises:
            ValueError: If board type is not supported
        """
        # Cache key includes the token, not just the board ID -- otherwise a
        # rotated credential (innoday board set-credential) is silently
        # ignored for the lifetime of this process, since the first adapter
        # ever built for a board keeps being reused with its original,
        # now-stale token baked into it.
        #
        # OAuth-mode Jira adapters are deliberately NEVER cached (see the
        # `is_oauth_jira` guard around the cache read/write below): every
        # OAuth board would otherwise share one cache entry keyed on the
        # same OAUTH_TOKEN_SENTINEL, and JiraBoardAdapter._refresh_api_auth_if_oauth
        # mutates its JiraAPI's base_url/headers in place on every call --
        # safe only because the adapter's own docstring guarantees it's
        # never shared concurrently across requests. This service is a
        # module-level singleton (see `board_sync_service` below), so a
        # cached OAuth adapter WOULD be shared across concurrent background
        # syncs/requests, racing on that in-place mutation. Skipping the
        # cache for OAuth mode costs one extra ensure_fresh_jira_token call
        # per _get_adapter invocation -- cheap compared to the ticket-sync
        # HTTP calls that follow, and correctness-critical here.
        oauth_jira = is_oauth_jira(registration, token)
        cache_key = (registration.id, token)
        if not oauth_jira and cache_key in self.adapters:
            cached = self.adapters[cache_key]
            # Rebind the ORM row to this request's live instance. Every adapter
            # keeps the BoardRegistration it was constructed with
            # (BaseBoardAdapter.__init__), and this cache outlives the session
            # that produced it -- the service is a module-level singleton. After
            # that session commits (which expires attributes) and closes, the
            # retained instance is detached *and* expired, so the next
            # `self.board_registration.<attr>` raises DetachedInstanceError.
            #
            # It surfaces far from here and misleadingly: LinearBoardAdapter reads
            # `self.board_registration.organization_id` in `_issue_to_ticket`,
            # inside `get_tickets`' except, so a local session-lifecycle bug is
            # reported as "Failed to fetch Linear issues: Instance
            # <BoardRegistration ...> is not bound" -- i.e. as an upstream API
            # failure. Observed on dev with the same object address recurring
            # across requests, which is what identified the cache as the owner.
            cached.board_registration = registration
            return cached

        adapter = await build_board_adapter(
            registration,
            token,
            session,
        )

        # Cache -- except OAuth-mode Jira, see oauth_jira above.
        if not oauth_jira:
            self.adapters[cache_key] = adapter
        return adapter

    def _map_external_status_to_internal(
        self, external_status: str, board_type: BoardType
    ) -> TicketStatus:
        """Delegate to the canonical mapping in BaseBoardAdapter."""
        status = BaseBoardAdapter.map_external_status(external_status)
        if status == TicketStatus.TODO and external_status.lower().strip().replace(
            "_", " "
        ).replace("-", " ") not in [
            "to do",
            "todo",
            "open",
            "new",
            "ready",
            "selected for development",
            "next up",
        ]:
            logger.warning(f"Unknown status '{external_status}' mapped to TODO")
        return status

    def _get_project_id_for_board(
        self, registration: BoardRegistration, session: Session
    ) -> str:
        """Return the project this board registration belongs to.

        BoardRegistration.project_id is a required (NOT NULL) column at the
        database level -- a board cannot be registered without a project. This
        should never return None in practice; the explicit check below is
        defense in depth (e.g. against a raw-SQL row that bypassed the
        constraint) rather than an expected code path, which is why it raises
        instead of falling back to a silent None the way this method used to.
        """
        if not registration.project_id:
            raise ValueError(
                f"Board registration {registration.id} has no project_id -- "
                "boards must belong to a project. Attach it via "
                "ProjectService.attach_board before syncing."
            )
        return registration.project_id

    @staticmethod
    def _next_project_ref_number(session: Session, project_id: str) -> int:
        """Next project-scoped display number (the 42 in "BPAI-42").

        Read-max-then-insert, so inherently racy across sessions — the caller
        must be prepared for ``uq_ticket_project_ref_number`` to reject the
        result. Autoflush makes this see pending inserts in the same session, so
        a single batch is already consistent.
        """
        return (
            session.exec(
                select(func.max(Ticket.project_ref_number)).where(
                    Ticket.project_id == project_id
                )
            ).first()
            or 0
        ) + 1

    def _persist_ticket(
        self,
        external_ticket: Dict,
        registration: BoardRegistration,
        session: Session,
        project_id: str,
        ref_retries: int = _PROJECT_REF_RETRIES,
    ) -> Tuple[bool, Ticket]:
        """Write one ticket inside its own SAVEPOINT.

        Two problems, one mechanism:

        1. **Isolation.** A per-ticket failure used to be swallowed by the
           caller with no rollback. On Postgres that leaves the transaction
           aborted, so every later ticket is rejected *and* the batch
           ``commit()`` silently becomes a ROLLBACK (Postgres treats COMMIT on
           an aborted transaction as ROLLBACK and reports success), discarding
           the whole sync while the counters still claimed rows were created.
           Verified against dev Postgres — SQLite never enters that state,
           which is why no test caught it.
        2. **The ref race.** A concurrent sync can take the display number
           between our read and our insert. The savepoint lets us roll back
           just this ticket and retry with a fresh number.
        """
        last = ref_retries - 1
        for attempt in range(ref_retries):
            try:
                with session.begin_nested():
                    was_created, ticket = self._create_or_update_ticket(
                        external_ticket, registration, session, project_id
                    )
                    # Surface constraint violations inside the savepoint, where
                    # they can still be contained.
                    session.flush()
                return was_created, ticket
            except IntegrityError as exc:
                if attempt == last or not _is_project_ref_conflict(exc):
                    raise
                logger.info(
                    "project_ref_number collision for ticket %s (attempt %d/%d); "
                    "another sync took the number -- retrying",
                    external_ticket.get("id", "unknown"),
                    attempt + 1,
                    ref_retries,
                )
        # Unreachable: the final attempt either returns or re-raises.
        raise AssertionError("ref retry loop exited without a result")

    @staticmethod
    def _resolve_assigned_user_id(
        external_ticket: Dict,
        registration: BoardRegistration,
        session: Session,
        project_id: str,
    ) -> Optional[str]:
        """Board assignee -> users.id, or None.

        Deliberately total: an assignee nobody has mapped is the normal case on
        most boards, and a resolver fault must never cost a ticket. Both answer
        None rather than raising, so neither can fail a sync.

        `Ticket.assignee` -- the board's display-name string -- is written by
        the caller from the board's own value; this method only resolves the FK.

        The registration's `organization_id` is what scopes the match: the
        resolver answers only with an active member of that org, so a board in
        one org can never assign a ticket to a user who only exists in another.

        **The resolver's reads run inside a SAVEPOINT**, for the same reason
        `_persist_ticket` does (see its docstring): swallowing an exception is
        only safe for a *Python* fault. A failed SELECT -- `relation
        "user_identity" does not exist` while an image is live ahead of
        `alembic upgrade head` is the realistic one -- aborts the whole Postgres
        transaction, so returning None without rolling back would leave the
        session in PendingRollbackError and turn the caller's COMMIT into a
        silent ROLLBACK. `sync_single_ticket` has no savepoint of its own, so
        this is the only thing standing between a resolver fault and losing the
        write it was called from.
        """
        try:
            assignee = BoardAssignee(
                display_name=external_ticket.get("assignee"),
                email=external_ticket.get("assignee_email"),
                board_user_id=external_ticket.get("assignee_board_user_id"),
            )
            if assignee.is_empty():
                return None
            platform = IdentityPlatform(registration.board_type.value)
            with session.begin_nested():
                match = IdentityResolutionService.resolve(
                    session,
                    organization_id=registration.organization_id,
                    project_id=project_id,
                    platform=platform,
                    assignee=assignee,
                )
                return match.user.id if match else None
        except Exception as exc:  # pragma: no cover - defensive
            logger.warning(
                "Could not resolve assignee %r for ticket %s: %s",
                external_ticket.get("assignee"),
                external_ticket.get("id", "unknown"),
                exc,
            )
            return None

    @staticmethod
    def _completed_at_from(
        external_ticket: Dict, internal_status: TicketStatus
    ) -> Optional[datetime]:
        """The board's completion timestamp for a DONE ticket, if it gave one.

        Naive UTC, matching the column. Returns None for anything not DONE and
        for a DONE ticket the board dated nothing -- the caller distinguishes
        "no answer" from "not finished".
        """
        if internal_status != TicketStatus.DONE:
            return None
        fields = external_ticket.get("fields") or {}
        # resolutiondate is the real completion time; `updated` is the closest
        # stand-in when the board does not track one separately.
        stamp = fields.get("resolutiondate") or fields.get("updated")
        if not stamp:
            return None
        # `parse_iso_naive`, not a local parse: this used to strip `tzinfo`
        # without converting, so a Jira instance in a non-UTC timezone -- which
        # returns `resolutiondate` with a real offset, not `Z` -- had its
        # completion times stored hours wrong, silently and in the direction of
        # the offset.
        parsed = parse_iso_naive(stamp)
        if parsed is None:
            logger.warning("Unparseable completion date %r; ignored", stamp)
        return parsed

    def _create_or_update_ticket(
        self,
        external_ticket: Dict,
        registration: BoardRegistration,
        session: Session,
        project_id: str,
    ) -> Tuple[bool, Ticket]:
        """
        Create or update a ticket based on external data.

        Returns:
            Tuple of (was_created, ticket_object)
        """
        external_id = str(external_ticket.get("id", ""))

        # Check if ticket already exists
        existing_ticket = session.exec(
            select(Ticket).where(
                Ticket.board_registration_id == registration.id,
                Ticket.external_ticket_id == external_id,
            )
        ).first()

        # Extract common ticket data
        summary = external_ticket.get("name") or external_ticket.get(
            "summary", "Untitled"
        )
        description = external_ticket.get("desc") or external_ticket.get(
            "description", ""
        )
        url = external_ticket.get("url", "")
        source_platform = (
            external_ticket.get("source_platform") or registration.board_type.value
        )
        priority = external_ticket.get("priority")
        parent_external_id = external_ticket.get("parent_external_id")

        # Extract release/fix version from Jira fields
        release = None
        if "fields" in external_ticket:
            fix_versions = external_ticket["fields"].get("fixVersions", [])
            if fix_versions:
                release = fix_versions[0].get("name")
        # Also check top-level release field (set by adapters like Jira)
        if not release:
            release = external_ticket.get("release")

        # The version string lands on the ticket and stops there. Sync used to
        # open a PLANNED Release row for it, and that is how BPAI accumulated
        # forty-odd rows on versioning lines it had long left -- the very mess the
        # high-water-mark rule in `release_planning` had to be written to survive.
        # A project's releases are now a managed two-slot pipeline with a single
        # writer, so a label on somebody's ticket no longer invents a version.

        # Two independent columns, both mirroring the board:
        #   `assignee`    -- the board's raw display-name string, whatever it
        #                    says, unresolved.
        #   `assigned_to` -- the FK, populated only when that person resolves
        #                    to a known user.
        # Both follow the board on every sync, including back to NULL when the
        # board unassigns the work. Leaving a stale name or a stale user
        # attached after a reassignment would be worse than an honest NULL.
        assignee = external_ticket.get("assignee")
        assigned_to = self._resolve_assigned_user_id(
            external_ticket, registration, session, project_id
        )

        # Use pre-resolved status if the adapter already mapped it; otherwise map now.
        if "_resolved_status" in external_ticket:
            internal_status = external_ticket["_resolved_status"]
        else:
            external_status = external_ticket.get("list", {}).get(
                "name", ""
            ) or external_ticket.get("status", "")
            internal_status = self._map_external_status_to_internal(
                external_status, registration.board_type
            )

        completed_at = self._completed_at_from(external_ticket, internal_status)

        if existing_ticket:
            # Everything the board owns, in one place, so "did anything change?"
            # is a comparison rather than a list of assignments to keep in step.
            incoming = {
                "summary": summary,
                "description": description,
                "assignee": assignee,
                "assigned_to": assigned_to,
                "status": internal_status,
                "url": url,
                "source_platform": source_platform,
                "priority": priority,
                "parent_external_id": parent_external_id,
                "project_id": project_id,
                # Revive if this ticket was previously soft-deleted (e.g. board
                # was cleared) but is still present at source. See board-clear
                # design.
                "deleted_at": None,
            }
            # Only overwrite when the board actually supplied one: `None` here
            # means "the board said nothing", not "belongs to no release". Same
            # rule as `completed_at` below -- and without it a release set in
            # InnoDay is erased by the next sync of a board with no semver label,
            # which is every Linear board in practice
            # (`_release_from_labels` returns None unless the issue carries a
            # semver-shaped label). `POST /tickets` pushes to the board by
            # default, so an InnoDay-set release on a board-linked ticket is the
            # common case, not an edge one.
            #
            # The tradeoff, accepted: clearing a `fixVersion` in Jira no longer
            # clears it here -- it has to be cleared in InnoDay too. That is the
            # price of the field being settable here at all, and it is exactly how
            # `completed_at` already behaves.
            if release is not None:
                incoming["release"] = release
            if internal_status == TicketStatus.DONE:
                # Only overwrite when the board actually supplied one: `None`
                # here means "the board said nothing", not "not finished".
                if completed_at is not None:
                    incoming["completed_at"] = completed_at
            else:
                # **A ticket that is not DONE has no completion time.** This
                # used to write only when `completed_at` was non-None, and
                # `_completed_at_from` returns None for every non-DONE status --
                # so reopening a ticket (DONE -> IN_PROGRESS) left the old
                # timestamp behind. `SummaryService._activity_at` reads
                # `completed_at` as evidence of a real terminal transition, so
                # a stale one made a reopened ticket look like in-window work
                # for as long as the window covered the date it was *closed*.
                incoming["completed_at"] = None

            changed = [
                name
                for name, value in incoming.items()
                if not _same_field(getattr(existing_ticket, name), value)
            ]
            for name, value in incoming.items():
                setattr(existing_ticket, name, value)

            # **Only restamp when something moved.** An unconditional
            # `updated_at = now()` on every ticket the adapter returns makes the
            # column mean "last time a sync ran", not "last time this ticket
            # changed" -- which silently marks a whole stale board as freshly
            # active for every consumer that reads it as an activity signal (the
            # summary engine's `_newest`, and any future incremental-sync
            # watermark). Measured: 20 tickets 90 days idle all reported as
            # active work. See tests/test_board_sync_robustness.py.
            if changed:
                existing_ticket.updated_at = datetime.now(timezone.utc)
                session.add(existing_ticket)
            return False, existing_ticket
        else:
            # Assign project-scoped sequential reference number. Racy on its own
            # -- uq_ticket_project_ref_number is what guarantees uniqueness, and
            # _persist_ticket retries this read when the constraint fires.
            next_ref = self._next_project_ref_number(session, project_id)

            new_ticket = Ticket(
                summary=summary,
                description=description,
                assignee=assignee,
                assigned_to=assigned_to,
                status=internal_status,
                release=release,
                url=url,
                source_platform=source_platform,
                priority=priority,
                parent_external_id=parent_external_id,
                organization_id=registration.organization_id,
                project_id=project_id,
                board_registration_id=registration.id,
                external_ticket_id=external_id,
                project_ref_number=next_ref,
                created_at=datetime.now(timezone.utc),
                updated_at=datetime.now(timezone.utc),
                completed_at=completed_at,
            )

            session.add(new_ticket)
            return True, new_ticket

    @staticmethod
    def _ticket_to_external_dict(
        ticket: Ticket, registration: BoardRegistration
    ) -> Dict:
        """
        Convert a Ticket domain object (as returned by an adapter) into the
        external_ticket dict shape expected by _create_or_update_ticket.
        """
        board_assignee = read_board_assignee(ticket) or BoardAssignee()
        return {
            "id": ticket.external_ticket_id or str(ticket.id),
            "summary": ticket.summary,
            "description": ticket.description,
            # Pass the already-resolved TicketStatus directly to avoid
            # re-mapping the enum value string back through the status mapper.
            "_resolved_status": ticket.status,
            "url": ticket.url,
            "assignee": ticket.assignee,
            # The board's own email / user id for that assignee, where the board
            # exposes them (Linear always, Jira sometimes, Trello never). Used
            # only to resolve Ticket.assigned_to -- `assignee` above stays the
            # board's display name.
            "assignee_email": board_assignee.email,
            "assignee_board_user_id": board_assignee.board_user_id,
            "source_platform": ticket.source_platform or registration.board_type.value,
            "priority": ticket.priority,
            "parent_external_id": ticket.parent_external_id,
            "fields": {
                "resolutiondate": (
                    ticket.completed_at.isoformat() if ticket.completed_at else None
                ),
                "updated": (
                    ticket.updated_at.isoformat() if ticket.updated_at else None
                ),
                "fixVersions": ([{"name": ticket.release}] if ticket.release else []),
            },
        }

    @staticmethod
    def _unchanged_since(
        external_ticket: Dict,
        registration: BoardRegistration,
        session: Session,
        since: datetime,
    ) -> bool:
        """Has the board seen no movement on a ticket we already hold?

        Two conditions, both required, and the second is what makes `since` safe
        to honour at all:

        * the board's own `updated` timestamp predates the window, **and**
        * InnoDay already has the row.

        A ticket we have never seen is imported however old it is. Without that
        second condition a windowed sync would be a windowed *import*, and the
        summary engine -- which passes `since` on every gate-1 sync -- would
        leave a fresh project permanently missing every ticket older than the
        first summary anyone happened to ask for.

        A **soft-deleted** row does not count as "already have it", for the same
        reason. The revive path (`_create_or_update_ticket` writes
        `deleted_at=None` for anything still present at source) is only reached
        by a ticket that is actually processed, so without `deleted_at IS NULL`
        here a ticket cleared from InnoDay but still on the board and idle
        beyond the window was skipped and never came back -- and the summary
        engine passes `since` on *every* gate-1 sync, which made that the
        normal case rather than an edge one.

        An unparseable or absent board timestamp answers False: "I cannot tell"
        must mean "sync it", never "skip it".
        """
        updated = _parse_since((external_ticket.get("fields") or {}).get("updated"))
        if updated is None or updated >= since:
            return False
        external_id = str(external_ticket.get("id", ""))
        if not external_id:
            return False
        return (
            session.exec(
                select(Ticket).where(
                    Ticket.board_registration_id == registration.id,
                    Ticket.external_ticket_id == external_id,
                    Ticket.deleted_at.is_(None),
                )
            ).first()
            is not None
        )

    async def sync_single_ticket(
        self,
        registration_id: str,
        external_key: str,
        token: str,
        session: Session,
    ) -> Tuple[bool, Ticket]:
        """
        Fetch one ticket from the board adapter and upsert it immediately.

        Unlike sync_board_tickets, this runs synchronously in the request/response
        cycle and does not write a BoardSyncHistory record.

        Returns:
            Tuple of (was_created, ticket)

        Raises:
            ValueError: If the board registration is not found, or has no
                project_id (should be unreachable given the NOT NULL
                constraint -- see _get_project_id_for_board)
            BoardAdapterError: If the ticket is not found on the external board,
                or the adapter fails to fetch it
        """
        registration = session.exec(
            select(BoardRegistration).where(BoardRegistration.id == registration_id)
        ).first()

        if not registration:
            raise ValueError(f"Board registration not found: {registration_id}")

        project_id = self._get_project_id_for_board(registration, session)

        adapter = await self._get_adapter(registration, token, session)
        await adapter.initialize(token)

        ticket_from_board = await adapter.get_ticket(external_key)
        if ticket_from_board is None:
            raise BoardAdapterError(
                f"Ticket '{external_key}' not found on board {registration.board_name}"
            )

        external_ticket = self._ticket_to_external_dict(ticket_from_board, registration)

        was_created, ticket = self._create_or_update_ticket(
            external_ticket, registration, session, project_id=project_id
        )
        session.commit()

        return was_created, ticket

    async def sync_board_tickets(
        self,
        registration_id: str,
        sync_history_id: str,
        token: str,
        options: Dict = None,
    ) -> Dict:
        """
        Perform the actual board synchronization.

        This is the main sync method called by background tasks.

        Args:
            registration_id: Board registration ID
            sync_history_id: Sync history record ID for tracking
            token: Integration token for API access
            options: Sync options. Exactly two keys are read:

                * ``dry_run`` -- count what would change, write nothing.
                * ``since`` -- an ISO-8601 timestamp. **Only when present** is
                  the pull narrowed to tickets updated after it; omitted (every
                  existing caller) the board is pulled in full, exactly as
                  before. The summary engine passes it so a read-triggered sync
                  is not a whole-board pull.

                ``full_sync`` and ``force`` arrive from the CLI, MCP and router
                request models but have never been read here -- the pull was
                always full. They are listed so nobody re-reads this signature
                and assumes otherwise.

        Returns:
            Dict with sync results
        """
        options = options or {}
        dry_run = options.get("dry_run", False)
        since = _parse_since(options.get("since"))

        results = {
            "success": False,
            "tickets_found": 0,
            "tickets_created": 0,
            "tickets_updated": 0,
            "tickets_skipped": 0,
            # Distinct from `tickets_skipped`, which means "tried and failed".
            # This is "the board says it has not moved since `since`, and we
            # already have it" -- a deliberate no-op, not an error.
            "tickets_unchanged": 0,
            "error_message": None,
        }

        session = None
        sync_history = None
        try:
            # Get database session
            session = Session(engine)

            # Get board registration
            registration = session.exec(
                select(BoardRegistration).where(BoardRegistration.id == registration_id)
            ).first()

            if not registration:
                raise ValueError(f"Board registration not found: {registration_id}")

            # Resolve project once per sync run (board:project is 1:1)
            project_id = self._get_project_id_for_board(registration, session)

            # Get sync history record
            sync_history = session.exec(
                select(BoardSyncHistory).where(BoardSyncHistory.id == sync_history_id)
            ).first()

            if not sync_history:
                raise ValueError(f"Sync history not found: {sync_history_id}")

            # Update sync status to in progress
            sync_history.sync_status = SyncStatus.IN_PROGRESS
            session.add(sync_history)
            session.commit()

            logger.info(
                f"Starting sync for board {registration.board_name} ({registration.board_type})"
            )

            # Get or create adapter for this board
            adapter = await self._get_adapter(registration, token, session)

            # Initialize adapter if needed
            await adapter.initialize(token)

            # Fetch tickets using adapter - it returns Ticket domain objects.
            # `since` is passed only when the caller supplied one AND this board
            # has completed a full sync before, so the default full pull is
            # byte-for-byte the call it always was.
            #
            # The `last_sync_at` guard closes a windowed-*import* hole. Adapters
            # that honour `since` (Linear does; Jira/Trello/Notion treat it as
            # advisory) filter at the source, so an old ticket InnoDay has never
            # seen simply never arrives -- and `_unchanged_since` below, which
            # exists precisely to protect unseen tickets, never gets to see it.
            # On a board's first sync that would leave the project permanently
            # missing everything older than whatever window happened to be asked
            # for first, and the summary engine passes a window on every gate-1
            # sync. First sync is therefore always a full pull; the latency win
            # applies from the second onwards, when there is a baseline to trust.
            windowed = since is not None and registration.last_sync_at is not None
            if not windowed:
                tickets_from_board = await adapter.get_tickets(
                    registration.board_external_id
                )
            else:
                tickets_from_board = await adapter.get_tickets(
                    registration.board_external_id, since=since
                )

            # Convert Ticket objects to the format expected by existing code
            # This maintains backward compatibility with the rest of the sync logic
            external_tickets = [
                self._ticket_to_external_dict(ticket, registration)
                for ticket in tickets_from_board
            ]

            results["tickets_found"] = len(external_tickets)
            logger.info(f"Found {len(external_tickets)} tickets in external board")

            # Process each ticket
            for external_ticket in external_tickets:
                try:
                    if since is not None and self._unchanged_since(
                        external_ticket, registration, session, since
                    ):
                        results["tickets_unchanged"] += 1
                        continue

                    if dry_run:
                        # In dry run mode, just count what would be done
                        external_id = str(external_ticket.get("id", ""))
                        existing = session.exec(
                            select(Ticket).where(
                                Ticket.board_registration_id == registration.id,
                                Ticket.external_ticket_id == external_id,
                            )
                        ).first()

                        if existing:
                            results["tickets_updated"] += 1
                        else:
                            results["tickets_created"] += 1
                    else:
                        # Each ticket writes inside its own SAVEPOINT, so one
                        # failure cannot abort the transaction the remaining
                        # tickets (and the batch commit) depend on.
                        was_created, ticket = self._persist_ticket(
                            external_ticket,
                            registration,
                            session,
                            project_id=project_id,
                        )

                        if was_created:
                            results["tickets_created"] += 1
                        else:
                            results["tickets_updated"] += 1

                except Exception as e:
                    logger.warning(
                        f"Failed to process ticket {external_ticket.get('id', 'unknown')}: {e}"
                    )
                    results["tickets_skipped"] += 1

            # A sync in which every ticket failed is a failed sync. `success`
            # used to be set unconditionally further down, and last_sync_at was
            # stamped regardless, so a board whose every ticket errored looked
            # healthy and freshly synced.
            # `tickets_unchanged` is deliberately excluded from the denominator:
            # a windowed sync in which nothing moved is the *expected* outcome,
            # not a failure, and counting those rows as failures would mark
            # every quiet `--since` sync FAILED and stop stamping last_sync_at.
            considered = results["tickets_found"] - results["tickets_unchanged"]
            everything_failed = (
                considered > 0 and results["tickets_skipped"] == considered
            )
            if everything_failed:
                results["error_message"] = (
                    f"All {results['tickets_found']} ticket(s) failed to sync; "
                    "see the warnings above for the per-ticket errors."
                )

            if not dry_run:
                # Commit all ticket changes
                session.commit()

                # Update registration last sync time -- but not when nothing
                # synced, or a broken board would keep reporting itself current.
                if not everything_failed:
                    registration.last_sync_at = datetime.now(timezone.utc)
                    # Clearing is the half that makes the flag trustworthy. A
                    # mark that only ever gets set becomes a permanent red for
                    # one bad afternoon, and people learn to ignore it (#499).
                    registration.errored_at = None
                    registration.error_message = None
                    session.add(registration)
                    session.commit()
                else:
                    # `last_sync_at` is deliberately NOT advanced above, but that
                    # alone only makes the board look stale -- it cannot say the
                    # credential is broken. This is the difference between "no
                    # one has synced lately" and "syncing does not work".
                    registration.errored_at = datetime.now(timezone.utc)
                    registration.error_message = "Every ticket failed to sync"
                    session.add(registration)
                    session.commit()

            # Update sync history with results
            sync_history.sync_status = (
                SyncStatus.FAILED if everything_failed else SyncStatus.COMPLETED
            )
            sync_history.completed_at = datetime.now(timezone.utc)
            sync_history.tickets_found = results["tickets_found"]
            sync_history.tickets_created = results["tickets_created"]
            sync_history.tickets_updated = results["tickets_updated"]
            sync_history.tickets_skipped = results["tickets_skipped"]

            session.add(sync_history)

            # One timeline entry per sync run (not per ticket -- a 254-ticket
            # sync would otherwise flood the timeline). Skip dry runs and
            # no-op syncs (nothing created/updated).
            if not dry_run and (
                results["tickets_created"] or results["tickets_updated"]
            ):
                add_timeline_entry(
                    session,
                    organization_id=registration.organization_id,
                    project_id=project_id,
                    event_type=TimelineEventType.TICKET_SYNC,
                    title=f"{registration.board_name} synced",
                    summary=(
                        f"Synced {results['tickets_found']} ticket(s) from "
                        f"{registration.board_name}: {results['tickets_created']} "
                        f"created, {results['tickets_updated']} updated"
                        + (
                            f", {results['tickets_skipped']} skipped"
                            if results["tickets_skipped"]
                            else ""
                        )
                        + "."
                    ),
                    created_by="system",
                    metadata={
                        "board_registration_id": registration.id,
                        "tickets_found": results["tickets_found"],
                        "tickets_created": results["tickets_created"],
                        "tickets_updated": results["tickets_updated"],
                        "tickets_skipped": results["tickets_skipped"],
                    },
                )

            session.commit()

            results["success"] = not everything_failed
            logger.info(f"Sync completed successfully: {results}")

        except Exception as e:
            # `classify_push_failure`, not `str(e)`. Everything written below is
            # read by every member of the org -- `BoardSyncHistory.error_message`
            # through `GET .../boards/{id}/sync-history`,
            # `BoardRegistration.error_message` through the dashboard's board
            # icon, and `results["error_message"]` through the summary payload's
            # `sync_error`. `str(e)` on an `IntegrityError` is the failing SQL plus
            # its bound parameters, and on an `OperationalError` psycopg2's
            # connection detail (host, port, user). The full exception goes to the
            # log line below, which is where that detail is safe.
            logger.exception("Sync failed for registration %s", registration_id)
            error_msg = classify_push_failure(
                e, doing="syncing tickets from a board", generic=GENERIC_SYNC_ERROR
            )
            results["error_message"] = error_msg

            if session and sync_history_id:
                self._record_sync_failure(
                    session,
                    sync_history_id=sync_history_id,
                    registration_id=registration_id,
                    error_msg=error_msg,
                    results=results,
                )

        finally:
            if session:
                session.close()

        return results

    def _record_sync_failure(
        self,
        session: Session,
        *,
        sync_history_id: str,
        registration_id: str,
        error_msg: str,
        results: Dict,
    ) -> None:
        """Write the FAILED outcome of a sync that just died.

        **The rollback comes first, and that ordering is the whole point.** This
        handler runs after an arbitrary failure, and the common case is a failed
        *statement*. On Postgres that leaves the transaction aborted: every later
        statement is refused **and** `COMMIT` is silently downgraded to `ROLLBACK`
        while reporting success. Without the rollback, this method believed it had
        persisted FAILED and had persisted nothing -- so the row stayed
        IN_PROGRESS with no error and no `completed_at`, indistinguishable from a
        sync still running.

        That is not a cosmetic loss. `sync_board` refuses to start while an
        IN_PROGRESS row exists, and the 30-minute scheduler POSTs with
        `force=False`, so the board **429s every 30 minutes** until an API restart
        lets `reap_orphaned_syncs` clear it -- while its dashboard icon stays
        green, because `BoardRegistration.errored_at` was lost in the same
        downgraded commit. SQLite has no aborted-transaction state, which is why
        the default fixtures cannot see any of this; the Postgres coverage is in
        `tests/test_postgres_only.py`.

        **Deliberately the same shape as
        `github_connect_service._record_project_sync_error`**, down to the
        re-fetch: `rollback()` expires identity-map state, so re-reading is what
        guarantees the UPDATE is issued in the fresh transaction rather than
        skipped as unchanged. Both rows are fetched by id for that reason -- the
        objects the caller was holding belong to the transaction just discarded.
        Rolling back is safe *because* everything pending belongs to a sync that
        has already failed.

        Either row can come back `None`: the registration or the history row can
        be deleted while a sync runs, and after a rollback there is nothing
        keeping them alive. Reading `.errored_at` off `None` used to be an
        `AttributeError` raised from inside the failure handler, which replaced
        the real error with a bogus one.

        `error_msg` arrives already classified by the caller -- see the comment at
        the call site for why the raw exception must not be stored.
        """
        try:
            session.rollback()

            sync_history = session.get(BoardSyncHistory, sync_history_id)
            if sync_history is not None:
                sync_history.sync_status = SyncStatus.FAILED
                sync_history.completed_at = datetime.now(timezone.utc)
                sync_history.error_message = error_msg[:500]
                sync_history.tickets_found = results["tickets_found"]
                sync_history.tickets_created = results["tickets_created"]
                sync_history.tickets_updated = results["tickets_updated"]
                sync_history.tickets_skipped = results["tickets_skipped"]
                session.add(sync_history)

            # History records the attempt; the registration records the current
            # state a status icon can read without walking it.
            registration = session.get(BoardRegistration, registration_id)
            if registration is not None:
                registration.errored_at = datetime.now(timezone.utc)
                registration.error_message = error_msg[:500]
                session.add(registration)

            session.commit()
        except Exception:
            # A broken recorder must never become the failure the caller reports:
            # `results["error_message"]` already holds the real one, and the
            # traceback for this one belongs in the log.
            logger.exception(
                "Could not record the failed sync for registration %s; the "
                "original failure is the one reported to the caller",
                registration_id,
            )

    async def _fetch_trello_cards(
        self, api_client: TrelloAPI, board_id: str, token: str
    ) -> List[Dict]:
        """
        Fetch cards from a Trello board.

        This is a placeholder implementation. In production, this would:
        1. Use the TrelloAPI client to fetch board cards
        2. Handle pagination and rate limiting
        3. Include card details, lists, and metadata
        """
        logger.info(f"Fetching Trello cards from board {board_id}")

        # TODO: Implement actual Trello API call
        # For now, return mock data for testing
        return [
            {
                "id": "trello_card_1",
                "name": "Sample Trello Card 1",
                "desc": "This is a sample card from Trello",
                "url": "https://trello.com/c/card1/sample-card-1",
                "list": {"name": "To Do"},
            },
            {
                "id": "trello_card_2",
                "name": "Sample Trello Card 2",
                "desc": "Another sample card from Trello",
                "url": "https://trello.com/c/card2/sample-card-2",
                "list": {"name": "In Progress"},
            },
        ]

    async def _fetch_jira_issues(
        self, api_client: JiraAPI, board_id: str, token: str
    ) -> List[Dict]:
        """
        Fetch issues from a Jira board.

        Directly fetches raw Jira data to preserve all fields including dates.
        """
        logger.info(f"Fetching Jira issues from board {board_id}")

        try:
            # Fetch raw Jira data directly to preserve all fields
            import httpx

            all_issues = []
            start_at = 0
            max_results = 100

            async with httpx.AsyncClient() as client:
                while True:
                    response = await client.get(
                        f"{api_client.base_url}/rest/agile/1.0/board/{board_id}/issue",
                        params={"startAt": start_at, "maxResults": max_results},
                        auth=api_client.auth,
                        headers=api_client.headers,
                        timeout=30.0,
                    )

                    if response.status_code != 200:
                        break

                    data = response.json()
                    issues_batch = data.get("issues", [])

                    if not issues_batch:
                        break

                    # Process each issue to match expected format
                    for issue in issues_batch:
                        fields = issue.get("fields", {})
                        status = fields.get("status", {})

                        all_issues.append(
                            {
                                "id": issue.get("key", issue.get("id")),
                                "summary": fields.get("summary", "Untitled"),
                                "description": fields.get("description") or "",
                                "status": status.get("name", "Unknown"),
                                "url": f"{api_client.base_url}/browse/{issue.get('key', '')}",
                                "assignee": (
                                    fields.get("assignee", {}).get("displayName")
                                    if fields.get("assignee")
                                    else None
                                ),
                                # Often absent (Atlassian privacy settings);
                                # absent just means "resolve by handle or not
                                # at all".
                                "assignee_email": (
                                    fields.get("assignee", {}).get("emailAddress")
                                    if fields.get("assignee")
                                    else None
                                ),
                                # Always present when there is an assignee, and
                                # the only stable id Jira gives us. Carried for
                                # the same reason the adapter path carries it.
                                "assignee_board_user_id": (
                                    fields.get("assignee", {}).get("accountId")
                                    if fields.get("assignee")
                                    else None
                                ),
                                "fields": fields,  # Include all fields for date extraction
                            }
                        )

                    start_at += max_results

                    # Stop if we've fetched all issues
                    if len(issues_batch) < max_results:
                        break

            logger.info(f"Retrieved {len(all_issues)} issues from Jira board")
            return all_issues

        except Exception as e:
            logger.error(f"Failed to fetch Jira issues: {e}")
            # Return empty list on error to continue sync process
            return []


# Global service instance
board_sync_service = BoardSyncService()


#: What an orphaned row says about itself once it has been reaped -- written for
#: whoever reads `board sync-status` next, so it names the cause rather than
#: leaving a bare FAILED.
#:
#: It deliberately does **not** say the run is dead, and does not say "just sync
#: again". A reap can only observe that this process found the row already
#: PENDING/IN_PROGRESS at its own boot; during a Railway rolling deploy the new
#: container is started and healthchecked *before* the old one is stopped, so
#: for the length of that window the run this row describes may still be alive
#: in the container being replaced. Asserting otherwise sends the operator to
#: start a second concurrent sync against a board that is still syncing -- and
#: unlike `--force`, which is a deliberate human override, that would be the
#: system instructing them to do it.
ORPHANED_SYNC_ERROR = (
    "Interrupted: the API restarted with this run still unreported, so it was "
    "marked failed at startup to stop it blocking later syncs. That is all "
    "that is known — if a deploy was rolling over, the run may still be alive "
    "in the container being replaced and will overwrite this when it finishes. "
    "Syncing again is safe, but may duplicate work already in flight."
)


def reap_orphaned_syncs(session: Session) -> int:
    """Fail every sync row still PENDING/IN_PROGRESS, and return how many.

    Called once at startup. A board sync is a FastAPI ``BackgroundTasks`` task
    running inside this process (`sync_board` queues `sync_board_tickets_task`),
    so it cannot outlive the process that owned it -- and a row still
    PENDING/IN_PROGRESS at boot therefore belongs to *some other* process. In
    the ordinary case (one container, restarted) that process is gone and the
    row is wreckage. In the **overlapping** case it is not: a Railway rolling
    deploy starts and healthchecks the new container before stopping the old
    one, so during that window two processes exist and the old one's sync is
    still running. This query is unscoped -- no board, org or process filter --
    so it reaps that live run's row too.

    That is accepted, and the claim is narrowed to match rather than the
    mechanism changed: see `ORPHANED_SYNC_ERROR`, which says the row was marked
    failed and what is *not* known, instead of pronouncing the sync dead.
    Age-based expiry is deliberately not the fix -- see below.

    Nothing reaped these before, and `sync_board` refuses to start while one
    exists -- so a deploy landing mid-sync left a row indistinguishable from a
    slow sync (no error, no `completed_at`) and silently disabled sync for that
    board until someone passed `--force` or edited the row by hand. That
    happened twice on the same board in four days (#613).

    Deliberately not age-based: "older than N minutes" needs an N nobody can
    name, and would either reap a live sync or leave a dead one standing. Boot
    is the moment the answer is knowable without guessing.

    Dry-run rows are reaped too. They do not block a later sync (`sync_board`
    excludes them), but a preview that never finished is just as dead, and
    leaving it PENDING misreports the board's history.

    Self-healing when a sibling process really is still finishing that sync: it
    writes its own terminal status over this one at the end, so status
    converges. In the window before it does, the reaped row no longer blocks, so
    a sync started then runs alongside the live one -- the same outcome as
    `--force`, which is why the row's own text must not *recommend* it.
    """
    orphans = session.exec(
        select(BoardSyncHistory).where(
            BoardSyncHistory.sync_status.in_(  # type: ignore[union-attr]
                [SyncStatus.PENDING, SyncStatus.IN_PROGRESS]
            )
        )
    ).all()

    if not orphans:
        return 0

    now = datetime.now(timezone.utc)
    for row in orphans:
        row.sync_status = SyncStatus.FAILED
        row.completed_at = now
        row.error_message = ORPHANED_SYNC_ERROR
        session.add(row)
    session.commit()

    logger.warning(
        "Reaped %d board sync run(s) left in progress by a previous process",
        len(orphans),
    )
    return len(orphans)


# Background task function
async def sync_board_tickets_task(
    registration_id: str, sync_history_id: str, token: str, options: Dict = None
) -> Dict:
    """
    Background task wrapper for board synchronization.

    This function is called by FastAPI BackgroundTasks to perform
    asynchronous board synchronization.
    """
    logger.info(f"Starting background sync task for registration {registration_id}")

    try:
        result = await board_sync_service.sync_board_tickets(
            registration_id=registration_id,
            sync_history_id=sync_history_id,
            token=token,
            options=options,
        )

        if result["success"]:
            logger.info(
                f"Background sync completed successfully for registration {registration_id}"
            )
        else:
            logger.error(
                f"Background sync failed for registration {registration_id}: {result.get('error_message')}"
            )

        return result

    except Exception as e:
        logger.error(
            f"Background sync task failed for registration {registration_id}: {e}"
        )
        return {
            "success": False,
            "error_message": str(e),
            "tickets_found": 0,
            "tickets_created": 0,
            "tickets_updated": 0,
            "tickets_skipped": 0,
        }
