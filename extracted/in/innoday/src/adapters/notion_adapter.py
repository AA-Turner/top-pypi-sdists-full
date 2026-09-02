"""
Notion adapter implementation

Handles Notion-specific operations:
- Databases as boards
- Pages as tickets
- Property-based status (not physical position like Trello)
- Rich text formatting
- Flexible property detection
- Block-based content
"""

import logging
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from src.adapters.base_adapter import BaseBoardAdapter, BoardAdapterError
from src.api.notion_api import NotionAPI
from src.domain import BoardRegistration, Ticket, TicketStatus

logger = logging.getLogger(__name__)


class NotionBoardAdapter(BaseBoardAdapter):
    """
    Notion-specific implementation of board adapter.

    This adapter handles the unique aspects of Notion:
    - Databases as boards with flexible property schemas
    - Pages as tickets with rich content blocks
    - Property-based status detection (select/multi_select)
    - No native comment system (uses appended blocks)
    - Pagination for large databases
    """

    def __init__(self, api: NotionAPI, board_registration: BoardRegistration):
        """
        Initialize the Notion adapter.

        Args:
            api: NotionAPI instance
            board_registration: BoardRegistration domain object
        """
        super().__init__(board_registration)
        self.api = api
        self.database_properties: Dict[str, Any] = {}
        self.status_property_name: Optional[str] = None
        self.status_property_type: Optional[str] = None  # 'select' or 'multi_select'
        self.title_property_name: Optional[str] = None
        self.status_options: List[str] = []  # Available status option names
        self._initialized = False

    async def initialize(self, token: str) -> None:
        """
        Initialize the adapter:
        1. Validate database access
        2. Fetch database schema
        3. Auto-detect status property
        4. Auto-detect title property
        5. Build status option list
        """
        try:
            # Validate connection first
            if not await self.validate_connection():
                raise BoardAdapterError("Failed to validate Notion connection")

            # Fetch database schema
            database = await self.api.get_database(self.board_id)
            self.database_properties = database.get("properties", {})

            # Detect title property (type: title)
            for prop_name, prop_data in self.database_properties.items():
                if prop_data.get("type") == "title":
                    self.title_property_name = prop_name
                    break

            if not self.title_property_name:
                raise BoardAdapterError(
                    "No title property found in database. Every database should have a title property."
                )

            # Detect status property
            status_detect = await self.api._detect_status_property(
                self.database_properties
            )

            if status_detect:
                self.status_property_name, self.status_property_type = status_detect

                # Get available status options
                status_prop = self.database_properties[self.status_property_name]
                if self.status_property_type == "select":
                    options = status_prop.get("select", {}).get("options", [])
                    self.status_options = [opt.get("name", "") for opt in options]
                elif self.status_property_type == "multi_select":
                    options = status_prop.get("multi_select", {}).get("options", [])
                    self.status_options = [opt.get("name", "") for opt in options]

                logger.info(
                    f"Detected status property '{self.status_property_name}' "
                    f"with options: {self.status_options}"
                )
            else:
                logger.warning(
                    f"No status property found in database {self.board_id}. "
                    "All tickets will be synced with TODO status. "
                    "Add a 'Status' property (Select type) for status tracking."
                )

            self._initialized = True
            logger.info(f"Initialized Notion adapter for database {self.board_id}")

        except Exception as e:
            logger.error(f"Failed to initialize Notion adapter: {e}")
            raise BoardAdapterError(f"Initialization failed: {e}")

    async def get_tickets(
        self, board_id: str, since: Optional[datetime] = None
    ) -> List[Ticket]:
        """
        Get all tickets (pages) from the Notion database.

        `since` is accepted for the interface and not honoured — narrowing would
        mean a `last_edited_time` filter on the database query, which needs the
        database's own schema. It is advisory (see `BaseBoardAdapter`).

        Returns:
            List of Ticket domain objects
        """
        try:
            if not self._initialized:
                raise BoardAdapterError("Adapter not initialized")

            # Query all pages from database (with pagination)
            pages = await self.api.query_database_pages(board_id)

            tickets = []
            for page in pages:
                ticket = await self._page_to_ticket(page)
                if ticket:
                    tickets.append(ticket)

            logger.info(f"Retrieved {len(tickets)} tickets from Notion database")
            return tickets

        except Exception as e:
            logger.error(f"Failed to get Notion tickets: {e}")
            raise BoardAdapterError(f"Failed to get tickets: {e}")

    async def get_ticket(self, ticket_id: str) -> Optional[Ticket]:
        """
        Get a specific ticket (page) by ID.

        Args:
            ticket_id: Notion page ID

        Returns:
            Ticket domain object or None
        """
        try:
            page = await self.api.get_page(ticket_id)
            if not page:
                return None

            return await self._page_to_ticket(page)

        except Exception as e:
            logger.error(f"Failed to get Notion page {ticket_id}: {e}")
            return None

    async def create_ticket(self, board_id: str, ticket_data: Dict[str, Any]) -> Ticket:
        """
        Create a new ticket (page) in the Notion database.

        Args:
            board_id: Notion database ID
            ticket_data: Ticket data with summary, description, status, etc.

        Returns:
            Created Ticket domain object
        """
        try:
            if not self._initialized:
                raise BoardAdapterError("Adapter not initialized")

            # Build properties
            properties = {}

            # Title property (required)
            summary = ticket_data.get("summary", "Untitled")
            properties[self.title_property_name] = self.api._build_property_object(
                "title", summary
            )

            # Status property (if available)
            if self.status_property_name:
                status = ticket_data.get("status", "TODO")
                notion_status = self._map_internal_status_to_notion(status)

                if notion_status:
                    properties[self.status_property_name] = (
                        self.api._build_property_object(
                            self.status_property_type, notion_status
                        )
                    )

            # Build content blocks from description
            content_blocks = []
            description = ticket_data.get("description", "")
            if description:
                # Split into paragraphs and create blocks
                paragraphs = description.split("\n\n")
                for para in paragraphs[:10]:  # Limit to 10 paragraphs
                    if para.strip():
                        content_blocks.append(self.api._build_text_block(para.strip()))

            # Create page
            created_page = await self.api.create_page(
                board_id, properties, content_blocks
            )

            # Convert to Ticket
            return await self._page_to_ticket(created_page)

        except Exception as e:
            logger.error(f"Failed to create Notion page: {e}")
            raise BoardAdapterError(f"Failed to create ticket: {e}")

    async def update_ticket(self, ticket: Ticket, updates: Dict[str, Any]) -> Ticket:
        """
        Update an existing ticket (page).

        Args:
            ticket: Ticket domain object to update
            updates: Dictionary of fields to update

        Returns:
            Updated Ticket domain object
        """
        try:
            if not ticket.external_ticket_id:
                raise BoardAdapterError("Ticket missing external_ticket_id")

            if not self._initialized:
                raise BoardAdapterError("Adapter not initialized")

            # Build property updates
            properties = {}

            if "summary" in updates:
                properties[self.title_property_name] = self.api._build_property_object(
                    "title", updates["summary"]
                )

            if "status" in updates and self.status_property_name:
                notion_status = self._map_internal_status_to_notion(updates["status"])
                if notion_status:
                    properties[self.status_property_name] = (
                        self.api._build_property_object(
                            self.status_property_type, notion_status
                        )
                    )

            # Update page properties
            if properties:
                await self.api.update_page(ticket.external_ticket_id, properties)

            # Update description (append blocks)
            if "description" in updates:
                description = updates["description"]
                if description:
                    content_blocks = [self.api._build_text_block(description)]
                    await self.api.append_block_children(
                        ticket.external_ticket_id, content_blocks
                    )

            # Fetch updated page and return
            updated_page = await self.api.get_page(ticket.external_ticket_id)
            return await self._page_to_ticket(updated_page)

        except Exception as e:
            logger.error(f"Failed to update Notion page: {e}")
            raise BoardAdapterError(f"Failed to update ticket: {e}")

    async def update_ticket_status(self, ticket: Ticket, new_status: str) -> Ticket:
        """
        Update ticket status property.

        Args:
            ticket: Ticket domain object
            new_status: Target internal status (TODO, IN_PROGRESS, etc.)

        Returns:
            Updated Ticket domain object
        """
        try:
            if not ticket.external_ticket_id:
                raise BoardAdapterError("Ticket missing external_ticket_id")

            if not self.status_property_name:
                logger.warning("Cannot update status: database has no status property")
                return ticket

            # Map internal status to Notion status
            notion_status = self._map_internal_status_to_notion(new_status)

            if not notion_status:
                logger.warning(f"Could not map status '{new_status}' to Notion option")
                return ticket

            # Build property update
            properties = {
                self.status_property_name: self.api._build_property_object(
                    self.status_property_type, notion_status
                )
            }

            # Update page
            await self.api.update_page(ticket.external_ticket_id, properties)

            # Update ticket object
            ticket.status = self._string_to_ticket_status(new_status)
            ticket.updated_at = datetime.now(timezone.utc)

            return ticket

        except Exception as e:
            logger.error(f"Failed to update status: {e}")
            raise BoardAdapterError(f"Failed to update ticket status: {e}")

    async def add_comment(self, ticket: Ticket, comment: str) -> bool:
        """
        Add comment as paragraph block to page.

        Note: Notion pages don't have a separate comment system,
        so we append blocks to the page body with a timestamp.

        Args:
            ticket: Ticket domain object
            comment: Comment text

        Returns:
            True if comment added successfully
        """
        try:
            if not ticket.external_ticket_id:
                raise BoardAdapterError("Ticket missing external_ticket_id")

            # Build comment block with timestamp
            timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
            comment_text = f"Comment ({timestamp}): {comment}"

            content_blocks = [self.api._build_text_block(comment_text)]

            appended = await self.api.append_block_children(
                ticket.external_ticket_id, content_blocks
            )

            return bool(appended)

        except BoardAdapterError:
            # As itself, not as `False`. The caller distinguishes an exception
            # written to be read (a capability this board does not have, the
            # missing-id guard above) from a board that answered "no", and it
            # records and retries only the latter.
            raise
        except Exception as e:
            # **Raised rather than returned as `False`.** Swallowing it here left
            # the caller with "the board declined" and no reason at all -- and it
            # converted the `BoardAdapterError` above, which carries a message
            # written for a person, into a bare falsy answer.
            logger.error(f"Failed to add comment: {e}")
            raise BoardAdapterError(f"Failed to add comment: {e}") from e

    async def get_board_metadata(self) -> Dict[str, Any]:
        """
        Get database metadata.

        Returns:
            Dictionary with Notion-specific metadata
        """
        try:
            if not self._initialized:
                await self.initialize("")

            metadata = {
                "properties": self.database_properties,
                "status_property": self.status_property_name,
                "title_property": self.title_property_name,
                "status_options": self.status_options,
                "property_types": {
                    name: prop.get("type")
                    for name, prop in self.database_properties.items()
                },
            }

            self.metadata_cache = metadata
            self.last_metadata_sync = datetime.now(timezone.utc)

            return metadata

        except Exception as e:
            logger.error(f"Failed to get board metadata: {e}")
            raise BoardAdapterError(f"Failed to get metadata: {e}")

    async def validate_connection(self) -> bool:
        """
        Validate that the adapter can access the database.

        Returns:
            True if connection is valid
        """
        try:
            database = await self.api.get_database(self.board_id)
            return database is not None

        except Exception as e:
            logger.error(f"Failed to validate Notion connection: {e}")
            return False

    # Helper methods

    async def _page_to_ticket(self, page: Dict[str, Any]) -> Optional[Ticket]:
        """
        Convert Notion page object to Ticket domain object.

        Args:
            page: Notion page object from API

        Returns:
            Ticket domain object or None
        """
        try:
            properties = page.get("properties", {})

            # Extract title
            title = ""
            if self.title_property_name:
                title_prop = properties.get(self.title_property_name, {})
                title = self.api._extract_property_value(title_prop, "title")

            # Extract status
            status = TicketStatus.TODO
            if self.status_property_name:
                status_prop = properties.get(self.status_property_name, {})
                notion_status = self.api._extract_property_value(
                    status_prop, self.status_property_type
                )

                if notion_status:
                    # Handle multi_select (list of statuses)
                    if isinstance(notion_status, list) and notion_status:
                        notion_status = notion_status[0]  # Use first status

                    internal_status = self._map_notion_status_to_internal(notion_status)
                    status = self._string_to_ticket_status(internal_status)

            # Extract description from blocks (async call)
            description = ""
            try:
                blocks = await self.api.get_page_content(page["id"])
                description = self.api._extract_text_from_blocks(blocks)
            except Exception as e:
                logger.warning(f"Failed to get page content: {e}")

            # Extract timestamps
            created_at = datetime.fromisoformat(
                page.get(
                    "created_time", datetime.now(timezone.utc).isoformat()
                ).replace("Z", "+00:00")
            )
            updated_at = datetime.fromisoformat(
                page.get(
                    "last_edited_time", datetime.now(timezone.utc).isoformat()
                ).replace("Z", "+00:00")
            )

            # Build ticket
            ticket = Ticket(
                summary=title or "Untitled",
                description=description,
                status=status,
                external_ticket_id=page["id"],
                url=page.get("url", ""),
                created_at=created_at,
                updated_at=updated_at,
                board_registration_id=self.board_registration.id,
                organization_id=self.board_registration.organization_id,
                project_id=self.board_registration.project_id,
            )

            return ticket

        except Exception as e:
            logger.error(f"Failed to convert page to ticket: {e}")
            return None

    def _map_notion_status_to_internal(self, notion_status: str) -> str:
        """
        Map Notion status option to internal status.

        Uses base class mapping with Notion-specific handling.

        Args:
            notion_status: Status option name from Notion

        Returns:
            Internal status string (TODO, IN_PROGRESS, IN_REVIEW, DONE, BACKLOG)
        """
        if not notion_status:
            return "TODO"

        # Use base class mapping which handles common patterns
        return self.map_external_status_to_internal(notion_status)

    def _map_internal_status_to_notion(self, internal_status: str) -> Optional[str]:
        """
        Map internal status to Notion status option name.

        Uses fuzzy matching to find best match from available options.

        Args:
            internal_status: Internal status (TODO, IN_PROGRESS, etc.)

        Returns:
            Notion status option name or None
        """
        if not self.status_options:
            return None

        internal_lower = internal_status.lower()

        # Define patterns for each internal status
        patterns = {
            "todo": ["to do", "todo", "backlog", "not started", "planned", "open"],
            "in_progress": [
                "in progress",
                "doing",
                "working",
                "in development",
                "active",
            ],
            "in_review": ["in review", "testing", "qa", "review", "in test"],
            "done": ["done", "completed", "finished", "closed", "resolved"],
            "backlog": ["backlog", "new", "planned"],
        }

        target_patterns = patterns.get(internal_lower, [])

        # Try exact match first
        for pattern in target_patterns:
            for option in self.status_options:
                if pattern == option.lower():
                    return option

        # Try partial match
        for pattern in target_patterns:
            for option in self.status_options:
                if pattern in option.lower() or option.lower() in pattern:
                    return option

        # Fallback: return first option
        if self.status_options:
            logger.warning(
                f"Could not find match for status '{internal_status}', "
                f"using first option: {self.status_options[0]}"
            )
            return self.status_options[0]

        return None

    def _string_to_ticket_status(self, status_string: str) -> TicketStatus:
        """Convert status string to TicketStatus enum"""
        status_map = {
            "TODO": TicketStatus.TODO,
            "IN_PROGRESS": TicketStatus.IN_PROGRESS,
            "IN_REVIEW": TicketStatus.IN_REVIEW,
            "DONE": TicketStatus.DONE,
            "BACKLOG": TicketStatus.BACKLOG,
        }
        return status_map.get(status_string.upper(), TicketStatus.TODO)
