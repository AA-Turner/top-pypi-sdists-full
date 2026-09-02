"""
Trello adapter implementation

Handles Trello-specific operations while working with existing domain objects.
"""

import logging
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from src.adapters.base_adapter import BaseBoardAdapter, BoardAdapterError
from src.api.trello_api import TrelloAPI
from src.domain import BoardRegistration, Ticket, TicketStatus

logger = logging.getLogger(__name__)


class TrelloBoardAdapter(BaseBoardAdapter):
    """
    Trello-specific implementation of board adapter.

    This adapter handles the unique aspects of Trello:
    - Cards exist in lists (status = list position)
    - No workflow constraints (cards can move freely)
    - Simple field structure
    """

    def __init__(self, api: TrelloAPI, board_registration: BoardRegistration):
        """
        Initialize the Trello adapter.

        Args:
            api: TrelloAPI instance
            board_registration: BoardRegistration domain object
        """
        super().__init__(board_registration)
        self.api = api
        self.list_mapping: Dict[str, str] = {}  # list_id -> status
        self.status_to_list: Dict[str, str] = {}  # status -> list_id
        self._initialized = False

    async def initialize(self, token: str) -> None:
        """Initialize the adapter and setup list mappings"""
        try:
            # Validate connection first
            if not await self.validate_connection():
                raise BoardAdapterError("Failed to validate Trello connection")

            # Initialize list mappings
            await self._init_list_mapping()
            self._initialized = True

            logger.info(f"Initialized Trello adapter for board {self.board_id}")

        except Exception as e:
            logger.error(f"Failed to initialize Trello adapter: {e}")
            raise BoardAdapterError(f"Initialization failed: {e}")

    async def get_tickets(
        self, board_id: str, since: Optional[datetime] = None
    ) -> List[Ticket]:
        """
        Get all tickets (cards) from the Trello board.

        Returns existing Ticket domain objects from TrelloAPI.

        `since` is accepted for the interface and not honoured — Trello's cards
        endpoint has no updated-after filter. It is advisory (see
        `BaseBoardAdapter`), so answering in full is correct, not a shortcut.
        """
        try:
            # TrelloAPI already returns Ticket objects
            tickets = await self.api.get_tickets_by_board(board_id)

            # Tickets from TrelloAPI should already have proper status set
            # The API handles the list-to-status mapping internally
            # No additional status mapping needed here

            return tickets

        except Exception as e:
            logger.error(f"Failed to get Trello tickets: {e}")
            raise BoardAdapterError(f"Failed to get tickets: {e}")

    async def get_ticket(self, ticket_id: str) -> Optional[Ticket]:
        """Get a specific ticket (card) by ID"""
        try:
            return await self.api.get_ticket(ticket_id)
        except Exception as e:
            logger.error(f"Failed to get Trello card {ticket_id}: {e}")
            raise BoardAdapterError(f"Failed to get ticket: {e}")

    async def create_ticket(self, board_id: str, ticket_data: Dict[str, Any]) -> Ticket:
        """Create a new ticket (card) on the Trello board"""
        try:
            # Determine target list
            list_id = ticket_data.get("list_id")

            if not list_id:
                # Try to map from status
                status = ticket_data.get("status", "TODO")
                list_id = self._get_list_for_status(status)

            if not list_id:
                # Use first available list
                lists = await self.api.get_lists(board_id)
                if lists:
                    list_id = lists[0]["id"]
                else:
                    raise BoardAdapterError("No lists available on board")

            # Create the card using existing TrelloAPI
            created_ticket = await self.api.create_ticket(
                board_id, list_id, ticket_data
            )

            # Set proper status based on list
            if list_id in self.list_mapping:
                mapped_status = self.list_mapping[list_id]
                status_map = {
                    "TODO": TicketStatus.TODO,
                    "IN_PROGRESS": TicketStatus.IN_PROGRESS,
                    "IN_REVIEW": TicketStatus.IN_REVIEW,
                    "DONE": TicketStatus.DONE,
                    "BACKLOG": TicketStatus.BACKLOG,
                }
                created_ticket.status = status_map.get(
                    mapped_status, TicketStatus.BACKLOG
                )

            return created_ticket

        except Exception as e:
            logger.error(f"Failed to create Trello card: {e}")
            raise BoardAdapterError(f"Failed to create ticket: {e}")

    async def update_ticket(self, ticket: Ticket, updates: Dict[str, Any]) -> Ticket:
        """Update an existing ticket (card)"""
        try:
            if not ticket.external_ticket_id:
                raise BoardAdapterError("Ticket missing external_ticket_id")

            # Prepare update data for Trello API
            card_updates = {}

            if "summary" in updates:
                card_updates["name"] = updates["summary"]
            if "description" in updates:
                card_updates["desc"] = updates["description"]
            if "due_date" in updates:
                due_date = updates["due_date"]
                card_updates["due"] = due_date.isoformat() if due_date else None

            # Update via Trello API
            if card_updates:
                await self.api.update_card(ticket.external_ticket_id, card_updates)

            # Update local ticket object
            for key, value in updates.items():
                if hasattr(ticket, key):
                    setattr(ticket, key, value)

            ticket.updated_at = datetime.now(timezone.utc)
            return ticket

        except Exception as e:
            logger.error(f"Failed to update Trello card: {e}")
            raise BoardAdapterError(f"Failed to update ticket: {e}")

    async def update_ticket_status(self, ticket: Ticket, new_status: str) -> Ticket:
        """Update ticket status by moving card to appropriate list"""
        try:
            if not ticket.external_ticket_id:
                raise BoardAdapterError("Ticket missing external_ticket_id")

            # Get target list for status
            list_id = self._get_list_for_status(new_status)
            if not list_id:
                raise BoardAdapterError(
                    f"Cannot map status '{new_status}' to a Trello list"
                )

            # Move the card
            await self.api.update_card(ticket.external_ticket_id, {"idList": list_id})

            # Update ticket object - map to internal status
            mapped_status = self.map_external_status_to_internal(new_status)
            # Convert to TicketStatus enum value
            status_map = {
                "TODO": TicketStatus.TODO,
                "IN_PROGRESS": TicketStatus.IN_PROGRESS,
                "IN_REVIEW": TicketStatus.IN_REVIEW,
                "DONE": TicketStatus.DONE,
                "BACKLOG": TicketStatus.BACKLOG,
            }
            ticket.status = status_map.get(mapped_status, TicketStatus.BACKLOG)
            ticket.updated_at = datetime.now(timezone.utc)

            return ticket

        except Exception as e:
            logger.error(f"Failed to update Trello card status: {e}")
            raise BoardAdapterError(f"Failed to update ticket status: {e}")

    async def add_comment(self, ticket: Ticket, comment: str) -> bool:
        """Add a comment to a ticket (card).

        **Answers with what Trello said, rather than with `True`.** It used to
        discard the response and return `True` unconditionally, so the caller's
        "a falsy return means the board did not take it" contract could not bite
        here at all -- the one board where it *silently* could not.

        `except BoardAdapterError: raise` so an exception written to be read --
        the missing-id guard above, or a future `BoardCapabilityError` -- reaches
        the caller as itself instead of being re-wrapped as a generic failure.
        """
        try:
            if not ticket.external_ticket_id:
                raise BoardAdapterError("Ticket missing external_ticket_id")

            created = await self.api.add_comment(ticket.external_ticket_id, comment)
            return bool(created)

        except BoardAdapterError:
            raise
        except Exception as e:
            logger.error(f"Failed to add comment to Trello card: {e}")
            raise BoardAdapterError(f"Failed to add comment: {e}")

    async def get_board_metadata(self) -> Dict[str, Any]:
        """Get Trello board metadata"""
        try:
            lists = await self.api.get_lists(self.board_id)
            members = await self.api.get_board_members(self.board_id)
            labels = await self.api.get_labels(self.board_id)

            # Update metadata cache
            self.metadata_cache = {
                "lists": lists,
                "members": members,
                "labels": labels,
                "list_mapping": self.list_mapping,
            }
            self.last_metadata_sync = datetime.now(timezone.utc)

            return self.metadata_cache

        except Exception as e:
            logger.error(f"Failed to get Trello board metadata: {e}")
            raise BoardAdapterError(f"Failed to get board metadata: {e}")

    async def validate_connection(self) -> bool:
        """Validate connection to Trello board"""
        try:
            board = await self.api.get_board(self.board_id)
            return board is not None
        except Exception as e:
            logger.error(f"Failed to validate Trello connection: {e}")
            return False

    # Private helper methods

    async def _init_list_mapping(self) -> None:
        """Initialize list-to-status mapping"""
        try:
            lists = await self.api.get_lists(self.board_id)

            # Auto-detect status mapping from list names
            patterns = {
                "TODO": ["to do", "todo", "backlog", "ideas", "inbox", "icebox"],
                "IN_PROGRESS": [
                    "in progress",
                    "doing",
                    "wip",
                    "development",
                    "working",
                ],
                "IN_REVIEW": ["review", "testing", "qa", "verification", "in review"],
                "DONE": ["done", "completed", "finished", "deployed", "closed"],
            }

            for list_item in lists:
                list_name = list_item["name"].lower()
                list_id = list_item["id"]

                # Try to match against patterns
                matched = False
                for status, keywords in patterns.items():
                    if any(keyword in list_name for keyword in keywords):
                        self.list_mapping[list_id] = status
                        matched = True
                        break

                # If no match, use the internal mapping
                if not matched:
                    # Use the base class mapping method
                    status = self.map_external_status_to_internal(list_item["name"])
                    self.list_mapping[list_id] = status

            # Create reverse mapping
            self.status_to_list = {}
            for list_id, status in self.list_mapping.items():
                # Only map the first list for each status (in case of duplicates)
                if status not in self.status_to_list:
                    self.status_to_list[status] = list_id

            # Store in board registration metadata
            if not self.board_registration.metadata:
                self.board_registration.metadata = {}
            self.board_registration.metadata["list_mapping"] = self.list_mapping

            logger.info(f"Initialized list mapping: {self.list_mapping}")

        except Exception as e:
            logger.error(f"Failed to initialize list mapping: {e}")
            # Continue without mapping - will use defaults

    def _get_list_for_status(self, status: str) -> Optional[str]:
        """Get Trello list ID for a status"""
        # Try exact match
        if status in self.status_to_list:
            return self.status_to_list[status]

        # Try uppercase match (for TicketStatus enum values)
        status_upper = status.upper()
        if status_upper in self.status_to_list:
            return self.status_to_list[status_upper]

        # Try mapped status
        mapped_status = self.map_external_status_to_internal(status)
        if mapped_status in self.status_to_list:
            return self.status_to_list[mapped_status]

        return None
