"""
Linear board adapter implementation.

Maps Linear teams → boards, Linear issues → tickets.
Uses GraphQL API via LinearAPI client.
"""

import logging
from datetime import datetime
from typing import Any, Dict, List, Optional

from src.adapters.base_adapter import BaseBoardAdapter, BoardAdapterError
from src.adapters.board_assignee import BoardAssignee, attach_board_assignee
from src.api.linear_api import LinearAPI, is_uuid
from src.domain import BoardRegistration, Ticket, TicketStatus
from src.utils.time_windows import parse_iso_naive

logger = logging.getLogger(__name__)

_PRIORITY_MAP = {
    0: "no_priority",
    1: "urgent",
    2: "high",
    3: "medium",
    4: "low",
}

# Board-state spellings -> InnoDay status. **Declaration order is meaningful**:
# `_state_id_for` walks this map to pick a board state for an outbound status, so
# the first spelling of a status listed here is the one preferred when a board has
# several. "internal review" precedes "in test" for that reason -- a team using
# both means them as different steps, and the review one is the review one.
_STATUS_MAP = {
    "todo": TicketStatus.TODO,
    "to do": TicketStatus.TODO,
    "backlog": TicketStatus.BACKLOG,
    "in progress": TicketStatus.IN_PROGRESS,
    "in review": TicketStatus.IN_REVIEW,
    "internal review": TicketStatus.IN_REVIEW,
    "code review": TicketStatus.IN_REVIEW,
    "peer review": TicketStatus.IN_REVIEW,
    "in test": TicketStatus.IN_REVIEW,
    "done": TicketStatus.DONE,
    "cancelled": TicketStatus.DONE,
    "canceled": TicketStatus.DONE,
}

# Spellings that may be read INBOUND but must never be chosen as the destination
# of an outbound transition. A cancelled issue arriving as DONE is lossy; marking
# somebody's finished ticket "Canceled" because DONE had no exact match is a wrong
# fact written to a client's board, and `TicketStatus.CANCELLED` exists to say
# that on purpose.
_OUTBOUND_EXCLUDED_SPELLINGS = {"cancelled", "canceled"}

# ...but CANCELLED itself still has to be able to reach them, and cannot get there
# through `_STATUS_MAP`, which points both spellings at DONE. Without this, asking
# for CANCELLED on a board whose state is spelled "Canceled" (one L) matched
# nothing: the normalised comparison sees "canceled" vs "cancelled" as two names,
# and the exclusion above then removed the only route left.
_OUTBOUND_EXTRA_SPELLINGS = {
    TicketStatus.CANCELLED: ("cancelled", "canceled"),
}


def _normalised_state(name: str) -> str:
    """A workflow-state name reduced to what a human would call the same name.

    Case and every non-alphanumeric character removed, so ``"In Progress"``,
    ``"in-progress"`` and ``"inprogress"`` collapse to one key. Used only for
    *comparison*; whatever the board calls the state is what gets shown back in
    an error.
    """
    return "".join(char for char in (name or "").lower() if char.isalnum())


def _release_from_labels(labels: List[str]) -> Optional[str]:
    """Return the first label that parses as a semantic version, else None.

    Linear has no native "fix version" field (unlike Jira), so a release is
    conventionally expressed as a label like ``v1.0.0`` / ``1.2.3-beta``. This
    is the Linear equivalent of the Jira adapter reading ``fixVersions``
    (see jira_adapter.py). We validate against blastoff's ``SemanticVersion``
    grammar rather than a bespoke regex so the accepted version format stays
    identical to the one the release engine and ``InnoDayVersionStore`` use.
    The extracted string flows into ``Ticket.release``; downstream,
    ``BoardSyncService._ensure_release_exists`` creates the PLANNED Release row.
    """
    # Imported lazily so the adapter has no hard import-time dependency on the
    # blastoff package (keeps board sync importable if blastoff is absent).
    try:
        from blastoff.version_manager import SemanticVersion
    except Exception:  # pragma: no cover - blastoff is a declared dependency
        return None

    for name in labels:
        candidate = (name or "").strip()
        if not candidate:
            continue
        try:
            SemanticVersion.from_string(candidate)
        except ValueError:
            continue
        return candidate
    return None


class LinearBoardAdapter(BaseBoardAdapter):
    def __init__(self, api: LinearAPI, board_registration: BoardRegistration):
        super().__init__(board_registration)
        self.api = api
        self.workflow_states: Dict[str, str] = {}
        self.state_name_to_id: Dict[str, str] = {}
        self._initialized = False

    async def initialize(self, token: str) -> None:
        try:
            # Self-heal boards registered before register_board resolved
            # Linear team keys to UUIDs (see src/routers/boards.py): if
            # board_id still looks like a short key ("UI", "PF") rather than
            # a UUID, resolve it once here so create_ticket/etc. use a value
            # Linear's mutations will actually accept. Confirmed live: a
            # board registered from a /team/<key>/... URL had board_id equal
            # to the key, and every mutation using it as teamId 400'd with
            # "Argument Validation Error".
            if not is_uuid(self.board_id):
                resolved = await self.api.resolve_team_id_by_key(self.board_id)
                if resolved:
                    self.board_id = resolved

            if not await self.validate_connection():
                raise BoardAdapterError(
                    f"Failed to connect to Linear team {self.board_id}"
                )
            states = await self.api.get_team_workflow_states(self.board_id)
            for state in states:
                self.workflow_states[state["id"]] = state["name"]
                self.state_name_to_id[state["name"]] = state["id"]
            self._initialized = True
        except BoardAdapterError:
            raise
        except Exception as e:
            raise BoardAdapterError(f"Linear initialization failed: {e}") from e

    async def get_tickets(
        self, board_id: str, since: Optional[datetime] = None
    ) -> List[Ticket]:
        try:
            issues = await self.api.get_team_issues(board_id, updated_after=since)
            return [self._issue_to_ticket(issue) for issue in issues]
        except Exception as e:
            raise BoardAdapterError(f"Failed to fetch Linear issues: {e}") from e

    async def get_ticket(self, ticket_id: str) -> Optional[Ticket]:
        try:
            issue = await self.api.get_issue(ticket_id)
            return self._issue_to_ticket(issue) if issue else None
        except Exception as e:
            raise BoardAdapterError(
                f"Failed to fetch Linear issue {ticket_id}: {e}"
            ) from e

    async def create_ticket(self, board_id: str, ticket_data: Dict[str, Any]) -> Ticket:
        try:
            # Use self.board_id, not the board_id parameter: initialize()
            # may have resolved a legacy team-key registration ("UI") to its
            # real UUID, but callers (board_ticket_creation_service.py) still
            # pass the raw, unresolved board_registration.board_external_id
            # here. Confirmed live: without this, a board registered before
            # register_board started resolving team keys kept sending the
            # stale key as teamId to Linear's API on every create, 400ing
            # with "teamId must be a UUID" even after initialize() had
            # already fixed self.board_id.
            issue = await self.api.create_issue(self.board_id, ticket_data)
            if not issue:
                raise BoardAdapterError("Linear issue creation returned no data")
            return self._issue_to_ticket(issue)
        except BoardAdapterError:
            raise
        except Exception as e:
            raise BoardAdapterError(f"Failed to create Linear issue: {e}") from e

    async def update_ticket(self, ticket: Ticket, updates: Dict[str, Any]) -> Ticket:
        try:
            linear_updates: Dict[str, Any] = {}
            if "summary" in updates or "title" in updates:
                linear_updates["title"] = updates.get("summary") or updates.get("title")
            if "description" in updates:
                linear_updates["description"] = updates["description"]
            issue = await self.api.update_issue(
                ticket.external_ticket_id, linear_updates
            )
            if not issue:
                raise BoardAdapterError("Linear issue update returned no data")
            return self._issue_to_ticket(issue)
        except BoardAdapterError:
            raise
        except Exception as e:
            raise BoardAdapterError(f"Failed to update Linear issue: {e}") from e

    def _state_id_for(self, new_status: str) -> Optional[str]:
        """The board's own id for the state a caller named, or None.

        **The caller names an InnoDay status; the board names a workflow state;
        the two are spelled differently and always were.** ``TicketStatus.TODO``
        is ``"todo"``, and the state a Linear team actually has is commonly
        ``"To Do"``. Neither an exact nor a case-insensitive comparison matches
        those -- and `_STATUS_MAP` above carries *both* spellings on the way in,
        which is the evidence that both occur on real boards rather than a
        hypothetical.

        So the comparison normalises: case, and every non-alphanumeric character.
        ``"To Do"``, ``"to-do"``, ``"todo"`` and ``"TODO"`` are one name to a
        human and are now one name here.

        **There is deliberately no alias tier.** An earlier version read
        `_STATUS_MAP` backwards to find other spellings of the same
        `TicketStatus`, so ``"done"`` could reach a board state named
        "Cancelled". Inbound that conflation is merely lossy -- a cancelled issue
        read as DONE. Outbound it is a *write*: it marks somebody's ticket
        cancelled when they finished it, and `TicketStatus.CANCELLED` exists
        separately, so the substitution runs in both directions. A wrong fact on
        a client's board is worse than a move that failed loudly, and the failure
        below names every state the board has, which is the whole diagnosis.

        Returning None rather than raising keeps that message in one place.
        """
        if new_status in self.state_name_to_id:
            return self.state_name_to_id[new_status]

        by_normalised = {
            _normalised_state(name): sid for name, sid in self.state_name_to_id.items()
        }
        exact = by_normalised.get(_normalised_state(new_status))
        if exact:
            return exact

        # Tier 3: the board names this state something else entirely.
        #
        # Bright Power's Linear team calls its review state "Internal Review". A
        # caller asking for `in review` normalises to "inreview", the board offers
        # "internalreview", and tiers 1-2 cannot bridge that -- so the transition
        # failed, `create_ticket_on_board` swallowed it as best-effort, and the
        # issue silently stayed in Linear's default Backlog while the API answered
        # 200. Inbound already knew better: `_STATUS_MAP` has classified
        # "internal review" as IN_REVIEW all along. This tier just spends that
        # same knowledge in the other direction.
        #
        # Walked in `_STATUS_MAP` declaration order so a board carrying several
        # spellings of one status resolves to the same state every time, and
        # `_OUTBOUND_EXCLUDED_SPELLINGS` keeps "Canceled" from ever being chosen
        # as the destination for DONE.
        try:
            requested = TicketStatus(new_status)
        except ValueError:
            return None

        spellings = [
            *_OUTBOUND_EXTRA_SPELLINGS.get(requested, ()),
            *(
                spelling
                for spelling, mapped in _STATUS_MAP.items()
                if mapped is requested and spelling not in _OUTBOUND_EXCLUDED_SPELLINGS
            ),
        ]
        for spelling in spellings:
            candidate = by_normalised.get(_normalised_state(spelling))
            if candidate:
                return candidate
        return None

    async def update_ticket_status(self, ticket: Ticket, new_status: str) -> Ticket:
        state_id = self._state_id_for(new_status)
        if not state_id:
            raise BoardAdapterError(
                f"Unknown Linear workflow state: '{new_status}'. Available: {list(self.state_name_to_id.keys())}"
            )
        # **Wrapped, like `update_ticket` and `add_comment` already are.** This
        # method alone let `LinearAPI`'s own exceptions escape unconverted, and
        # `LinearAPIError` is a `RuntimeError` -- so callers that tell "the board
        # said something" apart from "something unexpected happened" classified
        # every real 401/403/429/502 as unexpected and replaced Linear's own
        # explanation with a generic one. That only ever happens against a live
        # board, which is why it survived a suite that fabricates its errors.
        try:
            issue = await self.api.update_issue(
                ticket.external_ticket_id, {"stateId": state_id}
            )
        except BoardAdapterError:
            raise
        except Exception as e:
            raise BoardAdapterError(f"Failed to update Linear issue status: {e}") from e
        if not issue:
            raise BoardAdapterError("Status update returned no data")
        return self._issue_to_ticket(issue)

    async def set_board_assignee(self, ticket: Ticket, board_user_id: str) -> Ticket:
        """Assign the issue to a Linear user, by Linear's own id for them.

        **Why the assignee has to reach the board at all.** `BoardSyncService`
        overwrites both `Ticket.assignee` and `Ticket.assigned_to` from the board
        on every sync, *including back to NULL*. So an assignment written only in
        InnoDay silently disappears at the next sync -- and it disappears after
        the page said the take succeeded, which is the worst failure shape
        available here.

        ``board_user_id`` is Linear's id, never a name: `get_board_metadata`
        returns the team's members with their ids, and the caller resolves one
        there. Nothing in this repo persists a board user id (`BoardAssignee`
        carries it inbound and deliberately drops it), so it is resolved per push
        rather than stored.
        """
        if not ticket.external_ticket_id:
            raise BoardAdapterError("Ticket missing external_ticket_id")
        try:
            issue = await self.api.update_issue(
                ticket.external_ticket_id, {"assigneeId": board_user_id}
            )
        except BoardAdapterError:
            raise
        except Exception as e:
            raise BoardAdapterError(f"Failed to set Linear assignee: {e}") from e
        if not issue:
            raise BoardAdapterError("Assignee update returned no data")
        return self._issue_to_ticket(issue)

    async def add_comment(self, ticket: Ticket, comment: str) -> bool:
        """Post a comment on the issue. **The bool is the board's answer.**

        `LinearAPI.add_comment` returns `commentCreate.success` verbatim, so a
        board that *declines* the comment raises nothing and returns ``False``.
        A caller watching only for exceptions would report it as delivered.

        The `except BoardAdapterError: raise` is the same re-raise
        `update_ticket_status` carries, and for the same reason turned round:
        without it, an exception written **to be read** -- a
        `BoardCapabilityError` saying this board has no comments, or an error
        `LinearAPI` had already classified -- is caught by the blanket handler
        below and re-wrapped as a plain `BoardAdapterError`. The caller keys on
        the *type* to tell "this can never work" from "this did not work this
        time", so the downgrade turns a permanent fact into a failure that gets
        recorded and retried forever.
        """
        try:
            return await self.api.add_comment(ticket.external_ticket_id, comment)
        except BoardAdapterError:
            raise
        except Exception as e:
            raise BoardAdapterError(f"Failed to add comment: {e}") from e

    async def get_board_metadata(self) -> Dict[str, Any]:
        try:
            members = await self.api.get_team_members(self.board_id)
            return {
                "workflow_states": [
                    {"id": sid, "name": name}
                    for sid, name in self.workflow_states.items()
                ],
                "status_options": list(self.state_name_to_id.keys()),
                "members": members,
                "team_id": self.board_id,
            }
        except Exception as e:
            raise BoardAdapterError(f"Failed to get board metadata: {e}") from e

    async def validate_connection(self) -> bool:
        try:
            team = await self.api.get_team(self.board_id)
            return team is not None
        except Exception:
            return False

    def _issue_to_ticket(self, issue: Dict[str, Any]) -> Ticket:
        state_name = (issue.get("state") or {}).get("name", "")
        status = _STATUS_MAP.get(state_name.lower(), TicketStatus.TODO)
        assignee_data = issue.get("assignee")
        parent_data = issue.get("parent")
        # Linear expresses a release as a semver-shaped label (no fix-version
        # field). Pull the label names and pick the first that parses as a
        # version -> Ticket.release, so board sync auto-discovers releases the
        # way the Jira adapter does from fixVersions (PF-372).
        label_names = [
            node.get("name", "")
            for node in ((issue.get("labels") or {}).get("nodes") or [])
        ]
        # `updated_at` is non-Optional on TimestampMixin, so an unparseable or
        # absent `updatedAt` must leave the default in place rather than write
        # None -- omitted from the kwargs, not passed as None.
        board_updated_at = parse_iso_naive(issue.get("updatedAt"))
        timestamps = {"updated_at": board_updated_at} if board_updated_at else {}
        ticket = Ticket(
            summary=issue.get("title", ""),
            description=issue.get("description"),
            status=status,
            url=issue.get("url"),
            assignee=assignee_data["name"] if assignee_data else None,
            external_ticket_id=issue.get("identifier"),
            organization_id=self.board_registration.organization_id,
            project_id=self.board_registration.project_id,
            board_registration_id=self.board_registration.id,
            source_platform="linear",
            priority=self._map_priority(issue.get("priority", 0)),
            parent_external_id=parent_data["identifier"] if parent_data else None,
            release=_release_from_labels(label_names),
            # **Linear's own timestamps, not this object's construction time.**
            # `TimestampMixin` defaults `updated_at` to `now()`, and nothing
            # here used to overwrite it -- so every Linear ticket reached
            # `board_sync_service._ticket_to_dict` claiming it was updated at
            # the instant of the sync. Two things read that:
            #
            #   * `_completed_at_from` falls back to it when the board gave no
            #     completion date, so **every DONE Linear ticket was recorded as
            #     completed *now***. The summary engine treats `completed_at`
            #     inside the window as evidence of a real terminal transition,
            #     which made a project's entire closed backlog read as work
            #     finished in the last three days. Measured on BPAI's first
            #     import: 114 of 175 tickets stamped completed at 11:36:36,
            #     all within the same microsecond.
            #   * `_unchanged_since` compares it to the window start, so it was
            #     always "moved just now" and the incremental-skip optimisation
            #     never once fired for Linear.
            #
            # `updatedAt` was already being fetched and thrown away;
            # `completedAt` is newly requested so the real completion time is
            # available rather than inferred.
            completed_at=parse_iso_naive(issue.get("completedAt")),
            **timestamps,
        )
        # Ticket.assignee stays the board's display name. The email and Linear
        # user id ride alongside so board sync can resolve a real user without
        # guessing from the name -- see src/adapters/board_assignee.py.
        attach_board_assignee(
            ticket,
            BoardAssignee(
                display_name=assignee_data.get("name") if assignee_data else None,
                email=assignee_data.get("email") if assignee_data else None,
                board_user_id=assignee_data.get("id") if assignee_data else None,
            ),
        )
        return ticket

    @staticmethod
    def _map_priority(linear_priority: int) -> str:
        return _PRIORITY_MAP.get(linear_priority, "no_priority")
