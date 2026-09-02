import logging
from datetime import datetime
from typing import Any, Dict, List, Optional

import httpx

from src.api._base import BaseAPIClient
from src.domain.ticket import Ticket, TicketStatus

logger = logging.getLogger(__name__)


def plain_text_to_adf(text: str) -> Dict[str, Any]:
    """
    Wrap plain text in the minimal single-paragraph Atlassian Document
    Format (ADF) shape Jira Cloud's v3 API requires for description fields.
    A bare string is rejected with 400 "not valid Atlassian Document Format
    (ADF) content" (confirmed live). Used by create_ticket below; also
    needed if/when update_ticket ever writes a description (it doesn't
    today -- update_ticket only reads description, never sets it).
    """
    return {
        "type": "doc",
        "version": 1,
        "content": [{"type": "paragraph", "content": [{"type": "text", "text": text}]}],
    }


def adf_to_plain_text(description: Any) -> str:
    """
    Extract plain text from a Jira ADF description (or pass through
    unchanged if it's already a plain string/empty). Jira Cloud always
    returns descriptions in ADF; a raw ADF dict cannot be stored in
    Ticket.description (a plain string column) -- confirmed live via
    psycopg2.ProgrammingError: can't adapt type 'dict'.
    """
    if not isinstance(description, dict):
        return description or ""
    text_parts = []
    for block in description.get("content", []):
        if block.get("type") == "paragraph":
            for item in block.get("content", []):
                if item.get("type") == "text":
                    text_parts.append(item.get("text", ""))
    return "\n".join(text_parts)


class JiraAPI(BaseAPIClient):
    def __init__(
        self,
        base_url: Optional[str] = None,
        email: Optional[str] = None,
        api_token: Optional[str] = None,
        company_slug: Optional[str] = None,
        access_token: Optional[str] = None,
        cloud_id: Optional[str] = None,
    ):
        """
        Two mutually exclusive construction paths:

        - Basic Auth (existing, unaffected): base_url/company_slug +
          email + api_token -- self.auth becomes the (email, api_token)
          tuple httpx's `auth=` kwarg expects, base_url stays the
          `https://{company}.atlassian.net` host.
        - OAuth 2.0 3LO (new, GitHub issue #296): access_token + cloud_id
          -- self.auth is None (no Basic Auth tuple), base_url becomes
          `https://api.atlassian.com/ex/jira/{cloud_id}`, and an
          `Authorization: Bearer {access_token}` header is set instead.
          Used when Atlassian's edge rejects Basic Auth from this app's
          hosting platform's egress IPs (401 demanding OAuth) -- see
          src.services.jira_oauth_service for the refresh-aware caller
          path.
        """
        if access_token or cloud_id:
            if not (access_token and cloud_id):
                raise ValueError(
                    "Jira OAuth mode requires both access_token and cloud_id"
                )

            self.base_url = f"https://api.atlassian.com/ex/jira/{cloud_id}"
            self.auth = None
            super().__init__(
                headers={
                    "Accept": "application/json",
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {access_token}",
                }
            )
            return

        # An `organization_alias` parameter used to sit here, filling in missing
        # base_url/email/api_token from the CLI's config file plus the OS keyring.
        # It was armed but never reached: the OAuth path returns above it, and
        # `board_adapter_factory` -- the sole constructor -- always supplies all
        # three from Vault on the Basic Auth path. On a deployed server that
        # lookup returns nothing silently, so the only way it could ever have
        # fired was to turn a Vault misconfiguration into an empty result
        # instead of an error. Removed in #525; CLAUDE.md's claim that "JiraAPI
        # reads no keyring at all" is now literally true rather than nearly so.
        if not base_url and company_slug:
            base_url = f"https://{company_slug}.atlassian.net"

        if not all([base_url, email, api_token]):
            raise ValueError(
                "Jira base URL (or company slug), email, and API token are required"
            )

        self.base_url = base_url
        self.auth = (email, api_token)
        super().__init__(
            headers={
                "Accept": "application/json",
                "Content-Type": "application/json",
            }
        )

    async def get_tickets_by_board(self, board_id: str) -> List[Ticket]:
        """
        Get all tickets (issues) from a specific Jira board.

        Args:
            board_id: The ID of the Jira board

        Returns:
            A list of Ticket objects
        """
        async with httpx.AsyncClient() as client:
            # First get all issues from the board
            # Support pagination by getting up to 1000 issues
            all_issues = []
            start_at = 0
            max_results = 100

            while True:
                response = await client.get(
                    f"{self.base_url}/rest/agile/1.0/board/{board_id}/issue",
                    params={
                        "startAt": start_at,
                        "maxResults": max_results,
                        "fields": "summary,status,assignee,priority,created,updated,fixVersions,description",
                    },
                    auth=self.auth,
                    headers=self.headers,
                    timeout=30.0,
                )

                if response.status_code != 200:
                    break

                data = response.json()
                issues_batch = data.get("issues", [])
                all_issues.extend(issues_batch)

                # Check if we've retrieved all issues
                total = data.get("total", 0)
                if (
                    start_at + len(issues_batch) >= total
                    or len(issues_batch) < max_results
                ):
                    break

                start_at += max_results

            tickets = []
            for issue in all_issues:
                # Map Jira issue to our Ticket model
                ticket = self._map_issue_to_ticket(issue)
                if ticket:
                    tickets.append(ticket)

            return tickets

    async def create_ticket(
        self,
        project_key: str,
        summary: str,
        description: str = None,
        assignee: str = None,
        issue_type: str = "Task",
    ) -> Optional[Ticket]:
        """
        Create a new ticket (issue) in Jira.

        Args:
            project_key: The key of the Jira project
            summary: The summary/title of the issue
            description: The description of the issue
            assignee: The account ID of the assignee
            issue_type: The type of issue (e.g., "Bug", "Task")

        Returns:
            A Ticket object if creation was successful, None otherwise
        """
        issue_data = {
            "fields": {
                "project": {"key": project_key},
                "summary": summary,
                "issuetype": {"name": issue_type},
            }
        }

        if description:
            issue_data["fields"]["description"] = plain_text_to_adf(description)

        if assignee:
            issue_data["fields"]["assignee"] = {"id": assignee}

        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/rest/api/3/issue",
                auth=self.auth,
                headers=self.headers,
                json=issue_data,
            )

            if response.status_code not in (200, 201):
                logger.error(
                    f"Jira issue creation failed: {response.status_code} {response.text}"
                )
                return None

            # Get the created issue
            issue_key = response.json().get("key")
            if not issue_key:
                return None

            issue_response = await client.get(
                f"{self.base_url}/rest/api/3/issue/{issue_key}",
                auth=self.auth,
                headers=self.headers,
            )

            if issue_response.status_code != 200:
                return None

            return self._map_issue_to_ticket(issue_response.json())

    async def add_comment(self, issue_key: str, comment: str) -> bool:
        """
        Add a comment to a Jira issue.

        Args:
            issue_key: The key of the issue (e.g., "PROJECT-123")
            comment: The comment text to add

        Returns:
            True if the comment was added successfully, False otherwise
        """
        # The shared helper, not a second hand-rolled copy of the same ADF
        # shape. There used to be two `add_comment` definitions in this class
        # whose payloads were equal; the later one silently won at import time,
        # so editing the earlier one would have changed nothing.
        comment_data = {"body": plain_text_to_adf(comment)}

        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/rest/api/3/issue/{issue_key}/comment",
                auth=self.auth,
                headers=self.headers,
                json=comment_data,
                timeout=30.0,
            )

            return response.status_code in (200, 201)

    async def update_status(self, issue_key: str, status: TicketStatus) -> bool:
        """
        Update the status of a Jira issue.

        Args:
            issue_key: The key of the issue (e.g., "PROJECT-123")
            status: The new status for the issue

        Returns:
            True if the status was updated successfully, False otherwise
        """
        # First, get the available transitions for this issue
        async with httpx.AsyncClient() as client:
            transitions_response = await client.get(
                f"{self.base_url}/rest/api/3/issue/{issue_key}/transitions",
                auth=self.auth,
                headers=self.headers,
            )

            if transitions_response.status_code != 200:
                return False

            transitions = transitions_response.json().get("transitions", [])

            # Map our TicketStatus to Jira transition ID
            transition_id = self._map_status_to_transition(status, transitions)

            if not transition_id:
                return False

            # Perform the transition
            transition_data = {"transition": {"id": transition_id}}

            response = await client.post(
                f"{self.base_url}/rest/api/3/issue/{issue_key}/transitions",
                auth=self.auth,
                headers=self.headers,
                json=transition_data,
            )

            return response.status_code == 204

    def _map_issue_to_ticket(self, issue: Dict[str, Any]) -> Optional[Ticket]:
        """Map a Jira issue to our Ticket model"""
        try:
            fields = issue.get("fields", {})

            # Get assignee if available
            assignee = None
            if fields.get("assignee"):
                assignee = fields["assignee"].get("displayName")

            # Map Jira status to our TicketStatus
            status_name = fields.get("status", {}).get("name", "").lower()
            status = self._map_jira_status_to_ticket_status(status_name)

            # Get priority if available
            priority = None
            if fields.get("priority"):
                priority = fields["priority"].get("name")

            fix_versions = fields.get("fixVersions", [])
            release = fix_versions[0].get("name") if fix_versions else None

            description = adf_to_plain_text(fields.get("description", ""))

            # organization_id/project_id are transient placeholders here -- this
            # Ticket is a data carrier only, never persisted directly. Callers
            # (board_sync_service.py's sync path, board_ticket_creation_service.py's
            # create path) always set the real values before/instead of persisting
            # this object.
            return Ticket(
                summary=fields.get("summary", ""),
                description=description,
                assignee=assignee,
                status=status,
                priority=priority,
                release=release,
                external_ticket_id=issue.get("key"),
                created_at=datetime.fromisoformat(
                    fields.get("created", "").replace("Z", "+00:00")
                ),
                updated_at=datetime.fromisoformat(
                    fields.get("updated", "").replace("Z", "+00:00")
                ),
                url=f"{self.base_url}/browse/{issue.get('key')}",
                organization_id="",
                project_id="",
            )
        except Exception:
            return None

    def _map_jira_status_to_ticket_status(self, jira_status: str) -> TicketStatus:
        """Map a Jira status to our TicketStatus enum via the canonical mapper."""
        from src.adapters.base_adapter import BaseBoardAdapter

        return BaseBoardAdapter.map_external_status(jira_status)

    def _map_status_to_transition(
        self, status: TicketStatus, transitions: List[Dict[str, Any]]
    ) -> Optional[str]:
        """Map our TicketStatus to a Jira transition ID"""
        # This mapping depends on your Jira workflow configuration
        # You'll need to adjust this based on your specific Jira setup
        status_names = {
            TicketStatus.BACKLOG: ["backlog", "to do"],
            TicketStatus.TODO: ["to do", "open"],
            TicketStatus.IN_PROGRESS: ["in progress", "development"],
            TicketStatus.IN_REVIEW: ["in review", "testing", "qa"],
            TicketStatus.DONE: ["done", "closed", "resolved"],
        }

        target_names = status_names.get(status, [])

        for transition in transitions:
            to_status = transition.get("to", {}).get("name", "").lower()
            if any(name in to_status for name in target_names):
                return transition.get("id")

        return None
