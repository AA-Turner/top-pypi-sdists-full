"""
Jira adapter implementation

Handles Jira-specific operations while working with existing domain objects.
"""

import logging
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Tuple

import httpx
from sqlmodel import Session

from src.adapters.base_adapter import BaseBoardAdapter, BoardAdapterError
from src.adapters.board_assignee import BoardAssignee, attach_board_assignee
from src.api.jira_api import JiraAPI, adf_to_plain_text
from src.database import engine
from src.domain import BoardRegistration, Ticket, TicketStatus
from src.services.jira_oauth_service import ensure_fresh_jira_token
from src.utils.time_windows import parse_iso_naive

logger = logging.getLogger(__name__)


class JiraBoardAdapter(BaseBoardAdapter):
    """
    Jira-specific implementation of board adapter.

    This adapter handles the unique aspects of Jira:
    - Issues have status fields (not physical position)
    - Workflow-enforced status transitions
    - Rich custom field system
    - Project-based organization
    """

    def __init__(self, api: JiraAPI, board_registration: BoardRegistration):
        """
        Initialize the Jira adapter.

        Args:
            api: JiraAPI instance
            board_registration: BoardRegistration domain object
        """
        super().__init__(board_registration)
        self.api = api
        self.project_key: Optional[str] = None
        self.workflow_map: Dict[str, List[Dict]] = {}  # status -> transitions
        self._initialized = False
        #: Why the last `validate_connection()` said no. See that method.
        self.last_validation_error: Optional[str] = None

    async def initialize(self, token: str) -> None:
        """Initialize the adapter and get project configuration"""
        try:
            # Validate connection first
            if not await self.validate_connection():
                raise BoardAdapterError(
                    "Failed to validate Jira connection"
                    + (
                        f": {self.last_validation_error}"
                        if self.last_validation_error
                        else ""
                    )
                )

            # Get project key from board configuration
            await self._init_project_config()
            self._initialized = True

            logger.info(f"Initialized Jira adapter for board {self.board_id}")

        except Exception as e:
            logger.error(f"Failed to initialize Jira adapter: {e}")
            raise BoardAdapterError(f"Initialization failed: {e}")

    async def get_tickets(
        self, board_id: str, since: Optional[datetime] = None
    ) -> List[Ticket]:
        """
        Get all tickets (issues) from the Jira board.

        Returns existing Ticket domain objects from JiraAPI.

        `since` is accepted for the interface and **not yet honoured**: pushing
        it down means adding a JQL `updated >= …` clause to
        `JiraAPI.get_tickets_by_board`, which serves several other callers.
        Ignoring it is safe — `since` is advisory (see `BaseBoardAdapter`) — and
        silently narrowing nothing is far better than silently narrowing wrongly.
        """
        try:
            await self._refresh_api_auth_if_oauth()
            # JiraAPI already returns Ticket objects
            return await self.api.get_tickets_by_board(board_id)

        except Exception as e:
            logger.error(f"Failed to get Jira tickets: {e}")
            raise BoardAdapterError(f"Failed to get tickets: {e}")

    async def get_ticket(self, ticket_id: str) -> Optional[Ticket]:
        """Get a specific ticket (issue) by ID or key"""
        try:
            # For Jira, we need to get the full issue details
            issue = await self._get_issue(ticket_id)
            if not issue:
                return None

            # Convert to Ticket object
            return self._issue_to_ticket(issue)

        except Exception as e:
            logger.error(f"Failed to get Jira issue {ticket_id}: {e}")
            raise BoardAdapterError(f"Failed to get ticket: {e}")

    async def create_ticket(self, board_id: str, ticket_data: Dict[str, Any]) -> Ticket:
        """Create a new ticket (issue) in Jira"""
        try:
            # Use provided project key or default
            project_key = ticket_data.get("project_key") or self.project_key
            if not project_key:
                raise BoardAdapterError(
                    "Project key is required for Jira issue creation"
                )

            # Create issue using existing JiraAPI
            await self._refresh_api_auth_if_oauth()
            created_ticket = await self.api.create_ticket(
                project_key=project_key,
                summary=ticket_data.get("summary", "Untitled"),
                description=ticket_data.get("description"),
                assignee=ticket_data.get("assignee"),
                issue_type=ticket_data.get("issue_type", "Task"),
            )

            if not created_ticket:
                raise BoardAdapterError("Failed to create Jira issue")

            return created_ticket

        except Exception as e:
            logger.error(f"Failed to create Jira issue: {e}")
            raise BoardAdapterError(f"Failed to create ticket: {e}")

    async def update_ticket(self, ticket: Ticket, updates: Dict[str, Any]) -> Ticket:
        """Update an existing ticket (issue)"""
        try:
            if not ticket.external_ticket_id:
                raise BoardAdapterError("Ticket missing external_ticket_id")

            # Prepare update fields for Jira
            update_fields = {}

            if "summary" in updates:
                update_fields["summary"] = updates["summary"]
            if "description" in updates:
                update_fields["description"] = updates["description"]
            if "assignee" in updates:
                update_fields["assignee"] = (
                    {"accountId": updates["assignee"]} if updates["assignee"] else None
                )
            if "priority" in updates:
                update_fields["priority"] = {"name": updates["priority"]}
            if "due_date" in updates:
                due_date = updates["due_date"]
                update_fields["duedate"] = (
                    due_date.date().isoformat() if due_date else None
                )

            # Update via Jira API if we have fields to update
            if update_fields:
                await self._update_issue(ticket.external_ticket_id, update_fields)

            # Update local ticket object
            for key, value in updates.items():
                if hasattr(ticket, key):
                    setattr(ticket, key, value)

            ticket.updated_at = datetime.now(timezone.utc)
            return ticket

        except Exception as e:
            logger.error(f"Failed to update Jira issue: {e}")
            raise BoardAdapterError(f"Failed to update ticket: {e}")

    async def update_ticket_status(self, ticket: Ticket, new_status: str) -> Ticket:
        """Update ticket status using Jira workflow transitions"""
        try:
            if not ticket.external_ticket_id:
                raise BoardAdapterError("Ticket missing external_ticket_id")

            # Get available transitions
            transitions = await self._get_transitions(ticket.external_ticket_id)

            # Find matching transition
            transition_id = None
            mapped_status = self.map_external_status_to_internal(new_status)

            for transition in transitions:
                to_status = transition.get("to", {}).get("name", "")
                # Check if this transition leads to our target status
                if self.map_external_status_to_internal(to_status) == mapped_status:
                    transition_id = transition["id"]
                    break

            if not transition_id:
                # Try exact name match as fallback
                for transition in transitions:
                    if (
                        transition.get("to", {}).get("name", "").lower()
                        == new_status.lower()
                    ):
                        transition_id = transition["id"]
                        break

            if not transition_id:
                available = [t.get("to", {}).get("name") for t in transitions]
                raise BoardAdapterError(
                    f"No valid transition to status '{new_status}'. Available: {', '.join(available)}"
                )

            # Execute transition
            await self._do_transition(ticket.external_ticket_id, transition_id)

            # Update ticket object - map to proper enum value
            status_map = {
                "TODO": TicketStatus.TODO,
                "IN_PROGRESS": TicketStatus.IN_PROGRESS,
                "IN_REVIEW": TicketStatus.IN_REVIEW,
                "DONE": TicketStatus.DONE,
                "BACKLOG": TicketStatus.BACKLOG,
            }
            ticket.status = status_map.get(mapped_status, TicketStatus.TODO)
            ticket.updated_at = datetime.now(timezone.utc)

            return ticket

        except Exception as e:
            logger.error(f"Failed to update Jira issue status: {e}")
            raise BoardAdapterError(f"Failed to update ticket status: {e}")

    async def add_comment(self, ticket: Ticket, comment: str) -> bool:
        """Add a comment to a ticket (issue)"""
        try:
            if not ticket.external_ticket_id:
                raise BoardAdapterError("Ticket missing external_ticket_id")

            await self._refresh_api_auth_if_oauth()
            return await self.api.add_comment(ticket.external_ticket_id, comment)

        except BoardAdapterError:
            # An exception written **to be read** reaches the caller as itself.
            # Re-wrapping it here loses the type the caller uses to tell "this
            # board can never do that" from "that did not work this time", and
            # the second is recorded and retried where the first must not be.
            raise
        except Exception as e:
            logger.error(f"Failed to add comment to Jira issue: {e}")
            raise BoardAdapterError(f"Failed to add comment: {e}")

    async def get_board_metadata(self) -> Dict[str, Any]:
        """Get Jira board metadata"""
        try:
            # Get board configuration
            config = await self._get_board_config()

            # Get project statuses
            statuses = await self._get_project_statuses()

            # Update metadata cache
            self.metadata_cache = {
                "project_key": self.project_key,
                "statuses": statuses,
                "board_config": config,
            }
            self.last_metadata_sync = datetime.now(timezone.utc)

            return self.metadata_cache

        except Exception as e:
            logger.error(f"Failed to get Jira board metadata: {e}")
            raise BoardAdapterError(f"Failed to get board metadata: {e}")

    async def validate_connection(self) -> bool:
        """Validate connection to Jira.

        The reason is kept on `self.last_validation_error` as well as logged.
        Callers turn a False here into "Failed to validate Jira connection",
        which is recorded on the sync-history row and is the only thing anyone
        reads later -- and it does not distinguish an expired token from a
        revoked one from `401 Unauthorized; scope does not match`, which is a
        *re-consent*, not a retry. Losing Jira's own sentence there costs a
        debugging session every time.
        """
        try:
            # Try to get board configuration
            config = await self._get_board_config()
            if config is None:
                self.last_validation_error = (
                    f"Jira returned no board configuration for board {self.board_id}"
                )
                return False
            self.last_validation_error = None
            return True
        except Exception as e:
            self.last_validation_error = str(e)[:500]
            logger.error(f"Failed to validate Jira connection: {e}")
            return False

    # Private helper methods

    async def _init_project_config(self) -> None:
        """Initialize project configuration from board"""
        try:
            config = await self._get_board_config()
            if config:
                # Extract project key from board config
                # Confirmed live against /rest/agile/1.0/board/{id}/configuration:
                # the project key is at location.key, not location.projectKey
                # (which doesn't exist in the actual response shape at all --
                # this line always returned None, silently, since nothing
                # downstream distinguished "no project key found" from "found
                # a real one").
                self.project_key = config.get("location", {}).get("key")

                # NOTE: previously this also tried to persist project_key into
                # `self.board_registration.metadata["project_key"] = ...` --
                # but BoardRegistration has no `metadata` field; that name
                # resolved to SQLAlchemy's own Base.metadata class attribute
                # (present on every model), raising
                # "'MetaData' object does not support item assignment" on
                # every single call, silently swallowed by the except below.
                # self.project_key already caches this for the adapter
                # instance's lifetime (one request), which is all that's
                # needed here -- there's no cross-request cache to persist to
                # without adding a real column/relationship, which is out of
                # scope for this fix.

                logger.info(f"Initialized project config: {self.project_key}")

        except Exception as e:
            logger.error(f"Failed to initialize project config: {e}")
            # Continue without project key - will need to be provided in requests

    def _is_oauth_mode(self) -> bool:
        """OAuth-mode JiraAPI instances have self.auth == None (no Basic
        Auth tuple) -- see JiraAPI.__init__'s access_token/cloud_id path.
        Basic Auth instances always have a real (email, api_token) tuple,
        so this never misclassifies a legacy adapter."""
        return getattr(self.api, "auth", None) is None

    async def _jira_request_context(
        self,
    ) -> Tuple[str, Optional[tuple], Dict[str, str]]:
        """
        Resolve (base_url, auth, headers) for the next Jira HTTP call.

        Dual-mode: Basic Auth adapters return self.api's static
        base_url/auth/headers completely unchanged -- no extra DB calls,
        no behavior change. OAuth-mode adapters call
        ensure_fresh_jira_token first (refreshing if the stored token is
        expired or within its safety margin) and return a Bearer-header
        base_url built from the (possibly rotated) access_token/cloud_id
        instead of the static tuple set once at construction time.
        """
        if not self._is_oauth_mode():
            return self.api.base_url, self.api.auth, self.api.headers

        with Session(engine) as session:
            access_token, cloud_id = await ensure_fresh_jira_token(
                session, self.board_registration.id
            )

        base_url = f"https://api.atlassian.com/ex/jira/{cloud_id}"
        headers = dict(self.api.headers)
        headers["Authorization"] = f"Bearer {access_token}"
        return base_url, None, headers

    async def _refresh_api_auth_if_oauth(self) -> None:
        """
        Refresh-aware counterpart to _jira_request_context for the three
        methods that delegate straight to a JiraAPI method
        (get_tickets_by_board / create_ticket / add_comment) instead of
        building their own httpx call in this adapter.

        Those three JiraAPI methods read self.base_url/self.auth/self.headers
        off the JiraAPI *instance* -- set once at JiraAPI.__init__ time --
        with no way to pass overrides in per-call. In OAuth mode, that
        instance's Bearer header is never refreshed on its own, so a sync
        that runs longer than the access token's lifetime (or starts after
        the stored token already expired) would silently 401 here even
        though _get_board_config's refresh-aware check just succeeded.

        Basic Auth mode: no-op, no extra DB call, self.api left untouched --
        identical behavior to before this method existed.

        OAuth mode: calls ensure_fresh_jira_token (refreshing if needed) and
        mutates self.api.base_url/headers in place so the delegated JiraAPI
        call picks up the fresh Bearer token. Mutating the shared JiraAPI
        instance is safe here because JiraBoardAdapter owns a 1:1, per-request
        JiraAPI instance (see board_service construction) -- it is never
        shared concurrently across adapters/requests, so there's no cross-
        request interleaving risk from updating it in place.
        """
        if not self._is_oauth_mode():
            return

        base_url, _auth, headers = await self._jira_request_context()
        self.api.base_url = base_url
        self.api.headers = headers

    async def _get_board_config(self) -> Optional[Dict[str, Any]]:
        """Get board configuration from Jira"""
        base_url, auth, headers = await self._jira_request_context()

        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{base_url}/rest/agile/1.0/board/{self.board_id}/configuration",
                auth=auth,
                headers=headers,
                timeout=30.0,
            )
            if response.status_code == 200:
                return response.json()
        return None

    async def _get_project_statuses(self) -> List[Dict[str, Any]]:
        """Get available statuses for the project"""
        if not self.project_key:
            return []

        base_url, auth, headers = await self._jira_request_context()

        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{base_url}/rest/api/3/project/{self.project_key}/statuses",
                auth=auth,
                headers=headers,
                timeout=30.0,
            )
            if response.status_code == 200:
                data = response.json()
                # Extract unique statuses
                statuses = {}
                for issue_type in data:
                    for status in issue_type.get("statuses", []):
                        statuses[status["id"]] = status
                return list(statuses.values())
        return []

    async def _get_issue(self, issue_key: str) -> Optional[Dict[str, Any]]:
        """Get issue details from Jira"""
        base_url, auth, headers = await self._jira_request_context()

        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{base_url}/rest/api/3/issue/{issue_key}",
                auth=auth,
                headers=headers,
                timeout=30.0,
            )
            if response.status_code == 200:
                return response.json()
        return None

    async def _update_issue(self, issue_key: str, fields: Dict[str, Any]) -> None:
        """Update issue fields in Jira"""
        update_data = {"fields": fields}

        base_url, auth, headers = await self._jira_request_context()

        async with httpx.AsyncClient() as client:
            response = await client.put(
                f"{base_url}/rest/api/3/issue/{issue_key}",
                auth=auth,
                headers=headers,
                json=update_data,
                timeout=30.0,
            )
            if response.status_code not in (200, 204):
                raise Exception(f"Failed to update issue: {response.text}")

    async def _get_transitions(self, issue_key: str) -> List[Dict[str, Any]]:
        """Get available transitions for an issue"""
        base_url, auth, headers = await self._jira_request_context()

        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{base_url}/rest/api/3/issue/{issue_key}/transitions",
                auth=auth,
                headers=headers,
                timeout=30.0,
            )
            if response.status_code == 200:
                return response.json().get("transitions", [])
        return []

    async def _do_transition(self, issue_key: str, transition_id: str) -> None:
        """Execute a workflow transition"""
        transition_data = {"transition": {"id": transition_id}}

        base_url, auth, headers = await self._jira_request_context()

        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{base_url}/rest/api/3/issue/{issue_key}/transitions",
                auth=auth,
                headers=headers,
                json=transition_data,
                timeout=30.0,
            )
            if response.status_code not in (200, 204):
                raise Exception(f"Failed to transition issue: {response.text}")

    def _issue_to_ticket(self, issue: Dict[str, Any]) -> Ticket:
        """Convert Jira issue to Ticket domain object"""
        fields = issue.get("fields", {})

        # Extract basic fields
        summary = fields.get("summary", "Untitled")
        description = adf_to_plain_text(fields.get("description", ""))

        # Get status
        status_name = fields.get("status", {}).get("name", "Unknown")
        mapped_status = self.map_external_status_to_internal(status_name)
        status_map = {
            "TODO": TicketStatus.TODO,
            "IN_PROGRESS": TicketStatus.IN_PROGRESS,
            "IN_REVIEW": TicketStatus.IN_REVIEW,
            "DONE": TicketStatus.DONE,
            "BACKLOG": TicketStatus.BACKLOG,
        }
        status = status_map.get(mapped_status, TicketStatus.TODO)

        # Get assignee. emailAddress is frequently absent -- Atlassian hides it
        # per the account's privacy settings -- and absent is fine: board sync
        # falls back to a registered handle, or leaves the ticket unmatched.
        assignee_data = fields.get("assignee") or {}
        assignee = assignee_data.get("displayName") or None

        # Dates via `parse_iso_naive`: these land in naive columns, and the
        # previous form both stripped an offset rather than converting it (a
        # Jira site in a non-UTC timezone returns real offsets, not `Z`) and
        # raised on a malformed value instead of degrading. The fallbacks are
        # naive for the same reason -- one function should not produce an aware
        # value down one branch and a naive one down the other.
        now_naive = datetime.now(timezone.utc).replace(tzinfo=None)
        created_at = parse_iso_naive(fields.get("created")) or now_naive
        updated_at = parse_iso_naive(fields.get("updated")) or now_naive

        # Create Ticket object
        ticket = Ticket(
            summary=summary,
            description=description,
            status=status,
            assignee=assignee,
            external_ticket_id=issue.get("key"),
            url=f"{self.api.base_url}/browse/{issue.get('key')}",
            created_at=created_at,
            updated_at=updated_at,
            organization_id=self.board_registration.organization_id,
            project_id=self.board_registration.project_id,
            board_registration_id=self.board_registration.id,
        )

        # Add priority if available
        if fields.get("priority"):
            ticket.priority = fields["priority"].get("name")

        # Add fix version as release if available
        if fields.get("fixVersions"):
            versions = fields["fixVersions"]
            if versions:
                ticket.release = versions[0].get("name")

        # Set completed_at if status is DONE
        if status == TicketStatus.DONE:
            ticket.completed_at = (
                parse_iso_naive(fields.get("resolutiondate")) or updated_at
            )

        # Ticket.assignee stays Jira's display name; the address and accountId
        # ride alongside for identity resolution. See board_assignee.py.
        attach_board_assignee(
            ticket,
            BoardAssignee(
                display_name=assignee,
                email=assignee_data.get("emailAddress"),
                board_user_id=assignee_data.get("accountId"),
            ),
        )

        return ticket
