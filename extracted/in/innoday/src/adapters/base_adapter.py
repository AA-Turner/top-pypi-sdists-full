"""
Base adapter interface for board platforms

This adapter works with existing domain objects (Ticket, BoardRegistration)
rather than creating new unified models.
"""

from abc import ABC, abstractmethod
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from src.domain import BoardRegistration, Ticket
from src.domain.ticket import TicketStatus


class BoardAdapterError(Exception):
    """Base exception for board adapter errors.

    **Raising this is a statement that the message is fit for a person to read.**
    Callers that surface a board failure to a user (see
    `services/ticket_status_service.py`) key on `user_message`, which this
    populates, rather than on the exception's *type* — because a type cannot
    express "written to be read". The previous whitelist used `ValueError`, and
    `json.JSONDecodeError`, `pydantic.ValidationError` and `UnicodeDecodeError`
    are all `ValueError` subclasses, so it admitted three classes of internal
    detail while excluding `LinearAPIError`, which is a `RuntimeError`.

    So: wrap what a board told you in this, and let everything else stay
    unexpected. Anything unexpected gets a generic message and a server-side log
    with its traceback, which is where host names, SQL and bound parameters are
    safe to appear and a rendered string is not.
    """

    def __init__(self, message: str = "", *args: object) -> None:
        super().__init__(message, *args)
        #: The explanation to show. Set here rather than derived by the reader, so
        #: a subclass can narrow it and a caller never has to guess.
        self.user_message = message


class BoardCapabilityError(BoardAdapterError):
    """This board type cannot do that at all — a fact, not a failure.

    **The distinction decides whether the outcome gets recorded and retried.** A
    board that refused a push is out of step and must be remembered until it is
    not; a board that structurally has no assignee field will refuse identically
    forever. Storing that as a `push_error` makes it permanent and un-clearable,
    and marks the visit for retry on every later submit — so the same status gets
    re-pushed indefinitely for a thing that can never succeed.

    Raised only by a default implementation standing in for a capability the
    adapter does not have. Anything an adapter actually attempted and lost is a
    plain `BoardAdapterError`.
    """


class BoardCredentialError(BoardAdapterError, ValueError):
    """No usable credential for this board, or the one stored is unusable.

    **A `BoardAdapterError` so it is displayable**, which it must be: the message
    names the board and the single store that fixes it, and replacing it with the
    generic "check the board connection" leaves an operator a shrug.

    **Still a `ValueError` too**, because that is what this refusal has always
    been and callers outside the display path — `BoardTicketCreationService` and
    its tests — catch it as one. Inheriting both keeps every existing `except
    ValueError` working while giving the display path a class it can name
    exactly, rather than admitting the whole `ValueError` hierarchy to say
    "credential".
    """


class BaseBoardAdapter(ABC):
    """
    Abstract base class for board adapters.

    This adapter provides a common interface for different board platforms
    (Trello, Jira) while working with existing InnoDay domain objects.
    All methods return existing domain objects rather than new unified models.
    """

    def __init__(self, board_registration: BoardRegistration):
        """
        Initialize the adapter with a board registration.

        Args:
            board_registration: The BoardRegistration domain object
        """
        self.board_registration = board_registration
        self.board_id = board_registration.board_external_id
        self.metadata_cache: Optional[Dict[str, Any]] = None
        self.last_metadata_sync: Optional[datetime] = None

    @abstractmethod
    async def initialize(self, token: str) -> None:
        """
        Initialize the adapter with authentication.

        Args:
            token: Authentication token/credentials

        Raises:
            BoardAdapterError: If initialization fails
        """

    @abstractmethod
    async def get_tickets(
        self, board_id: str, since: Optional[datetime] = None
    ) -> List[Ticket]:
        """
        Get all tickets from the board.

        Args:
            board_id: External board ID
            since: Optional watermark — return only tickets updated after this
                instant. **Advisory.** A board whose API cannot express the
                filter may ignore it and answer in full; a caller must never
                treat the absence of a ticket as proof it did not change. It
                exists so a summary read does not force a whole-board pull.
                Omitted, every adapter returns everything, as they always have.

        Returns:
            List of Ticket domain objects

        Raises:
            BoardAdapterError: If fetching tickets fails
        """

    @abstractmethod
    async def get_ticket(self, ticket_id: str) -> Optional[Ticket]:
        """
        Get a specific ticket by ID.

        Args:
            ticket_id: External ticket ID (card ID for Trello, issue key for Jira)

        Returns:
            Ticket domain object or None if not found

        Raises:
            BoardAdapterError: If fetch fails
        """

    @abstractmethod
    async def create_ticket(self, board_id: str, ticket_data: Dict[str, Any]) -> Ticket:
        """
        Create a new ticket on the board.

        Args:
            board_id: External board ID
            ticket_data: Ticket data dictionary with fields:
                - summary: str (required)
                - description: str (optional)
                - assignee: str (optional)
                - labels: List[str] (optional)
                - status: str (optional, will map to appropriate list/status)
                - priority: str (optional)
                - due_date: datetime (optional)
                - list_id: str (optional, Trello-specific)
                - project_key: str (optional, Jira-specific)
                - issue_type: str (optional, Jira-specific)

        Returns:
            Created Ticket domain object

        Raises:
            BoardAdapterError: If creation fails
        """

    @abstractmethod
    async def update_ticket(self, ticket: Ticket, updates: Dict[str, Any]) -> Ticket:
        """
        Update an existing ticket.

        Args:
            ticket: Ticket domain object to update
            updates: Dictionary of fields to update

        Returns:
            Updated Ticket domain object

        Raises:
            BoardAdapterError: If update fails
        """

    @abstractmethod
    async def update_ticket_status(self, ticket: Ticket, new_status: str) -> Ticket:
        """
        Update ticket status (handles platform-specific transitions).

        For Trello: Moves card to appropriate list
        For Jira: Executes workflow transition

        Args:
            ticket: Ticket domain object
            new_status: Target status name

        Returns:
            Updated Ticket domain object

        Raises:
            BoardAdapterError: If status update fails or transition invalid
        """

    async def set_board_assignee(self, ticket: Ticket, board_user_id: str) -> Ticket:
        """Set who the *board* thinks owns this ticket.

        **Not abstract, and it raises rather than passing.** Only Linear
        implements it today. The refusal is a `BoardCapabilityError` -- a *fact*
        about this board type, distinct from a push that was attempted and lost,
        because the caller records and retries the second and must not record the
        first. A default that quietly did nothing would report an
        assignment the board never received -- and because `BoardSyncService`
        rewrites `assignee`/`assigned_to` from the board on every sync, the local
        half would then vanish, after the page had already said it worked. A
        refusal the caller can catch degrades honestly instead: the status still
        pushes, and the user is told the assignment is InnoDay-only.

        **Separate from `update_ticket_status`, deliberately.** Linear can carry
        `stateId` and `assigneeId` in one `issueUpdate` mutation, which is one
        fewer round trip -- but folding the assignee into the status call means a
        board that cannot assign loses the status push with it, which is a strictly
        worse failure than an extra request.

        Args:
            ticket: the ticket, which must already exist on the board.
            board_user_id: the board's own id for the person -- never a display
                name. Resolve it from `get_board_metadata()["members"]`.

        Raises:
            BoardAdapterError: this board type cannot set an assignee, or the
                board refused.
        """
        raise BoardCapabilityError(
            f"{self.__class__.__name__} cannot set a board assignee"
        )

    async def add_comment(self, ticket: Ticket, comment: str) -> bool:
        """Add a comment to a ticket.

        **Not abstract, and the default raises rather than passing** -- the same
        shape, and the same argument, as `set_board_assignee`. All four adapters
        shipped today override it, so this changes nothing for them; what it
        changes is what a board type that *cannot* take a comment has to do.
        While this was abstract, such an adapter had two choices, and both were
        wrong: return `True` for a comment it never posted, or raise a plain
        `BoardAdapterError` that the caller records and retries forever for
        something that can never succeed.

        A `BoardCapabilityError` is neither. It says "this board type has nowhere
        to put a comment", which is a fact rather than a failure, so the caller
        shows a notice, persists nothing, and does not come back.

        **Returns the board's own answer, and a falsy one means it did not land.**
        `LinearAPI.add_comment` hands back `commentCreate.success` verbatim and
        `JiraAPI.add_comment` a status-code check, so an implementation that
        returns a hardcoded `True` is discarding the only evidence the caller has.

        Args:
            ticket: Ticket domain object
            comment: Comment text

        Returns:
            True if the board accepted the comment.

        Raises:
            BoardCapabilityError: this board type has no comments at all.
            BoardAdapterError: the board was asked and the attempt failed.
        """
        raise BoardCapabilityError(f"{self.__class__.__name__} cannot add a comment")

    @abstractmethod
    async def get_board_metadata(self) -> Dict[str, Any]:
        """
        Get board-specific metadata.

        For Trello: Lists, members, labels
        For Jira: Statuses, issue types, fields

        Returns:
            Dictionary with platform-specific metadata:
            - lists/statuses: List of available statuses
            - members: List of board members
            - labels: List of available labels
            - custom_fields: List of custom fields (Jira)
            - issue_types: List of issue types (Jira)

        Raises:
            BoardAdapterError: If fetch fails
        """

    @abstractmethod
    async def validate_connection(self) -> bool:
        """
        Validate that the adapter can connect to the board.

        Returns:
            True if connection is valid and authenticated
        """

    # Helper methods that can be shared

    @staticmethod
    def map_external_status(external_status: str) -> TicketStatus:
        """
        Map any external status string to a TicketStatus enum value.

        Handles all common Jira, Linear, Trello, GitHub, and Notion status names,
        including enum value representations (e.g. "in_review", "in-review", "In Review"
        all resolve to IN_REVIEW). This is the single source of truth for status
        mapping — both adapters and the sync service use this method.
        """
        # Normalize: lowercase, collapse separators so variants all match
        s = external_status.lower().strip().replace("_", " ").replace("-", " ")
        s = " ".join(s.split())

        if s in ["backlog"]:
            return TicketStatus.BACKLOG
        elif s in [
            "to do",
            "todo",
            "open",
            "new",
            "ready",
            "selected for development",
            "next up",
        ]:
            return TicketStatus.TODO
        elif s in [
            "in progress",
            "doing",
            "active",
            "assigned",
            "in development",
            "development",
        ]:
            return TicketStatus.IN_PROGRESS
        elif s in [
            "in test",
            "testing",
            "qa",
            "code review",
            "review",
            "internal review",
            "in review",
            "peer review",
            "awaiting review",
            "ready for review",
            "ready for qa",
            "in qa",
        ]:
            return TicketStatus.IN_REVIEW
        elif s in [
            "done",
            "completed",
            "closed",
            "resolved",
            "finished",
            "released",
            "deployed",
            "canceled",
            "cancelled",
            "wont fix",
            "won t fix",
            "duplicate",
            "invalid",
        ]:
            return TicketStatus.DONE
        else:
            return TicketStatus.TODO

    def map_external_status_to_internal(self, external_status: str) -> str:
        """Thin wrapper for backwards compatibility. Prefer map_external_status()."""
        return self.map_external_status(external_status).name  # e.g. "IN_REVIEW"

    def should_refresh_metadata(self, max_age_seconds: int = 300) -> bool:
        """
        Check if metadata should be refreshed based on age.

        Args:
            max_age_seconds: Maximum age in seconds before refresh

        Returns:
            True if metadata should be refreshed
        """
        if not self.metadata_cache or not self.last_metadata_sync:
            return True

        age = (datetime.now(timezone.utc) - self.last_metadata_sync).total_seconds()
        return age > max_age_seconds
