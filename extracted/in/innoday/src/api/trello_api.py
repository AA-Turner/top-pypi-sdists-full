from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

import httpx

from src.domain.ticket import Ticket, TicketStatus
from src.utils.time_windows import parse_iso_naive


def _now_naive() -> datetime:
    """UTC now, naive, matching the columns these tickets land in.

    A one-liner with a name because it replaced
    `datetime.now(timezone.utc).isoformat()` used as a `dict.get` default --
    which built an ISO string on *every* card just to parse it straight back,
    and produced an aware value for a naive column.
    """
    return datetime.now(timezone.utc).replace(tzinfo=None)


class TrelloAPI:
    """API client for interacting with Trello"""

    def __init__(
        self, api_key: str, token: str, base_url: str = "https://api.trello.com/1"
    ):
        """
        Initialize Trello API client.

        Args:
            api_key: Trello API key
            token: Trello token
            base_url: Trello API base URL
        """
        self.base_url = base_url
        self.api_key = api_key
        self.token = token

        if not (self.api_key and self.token):
            raise ValueError("Trello API key and token are required")

        self.auth_params = {"key": self.api_key, "token": self.token}

    async def get_tickets_by_board(self, board_id: str) -> List[Ticket]:
        """
        Fetch all cards (tickets) from a Trello board and convert them to Ticket objects

        Args:
            board_id: The ID of the Trello board

        Returns:
            List of Ticket objects
        """
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/boards/{board_id}/cards", params=self.auth_params
            )

            if response.status_code != 200:
                raise Exception(f"Failed to fetch cards: {response.text}")

            cards = response.json()
            tickets = []

            for card in cards:
                # Map Trello list to ticket status
                status = self._map_list_to_status(card.get("idList", ""))

                # organization_id/project_id are transient placeholders -- this
                # Ticket is a data carrier only, never persisted directly. The
                # caller (board_sync_service.py) always sets the real values.
                ticket = Ticket(
                    summary=card.get("name", ""),
                    description=card.get("desc", ""),
                    assignee=self._get_member_name(card.get("idMembers", [])),
                    status=status,
                    # `parse_iso_naive`: `Ticket.created_at` is a naive column,
                    # and this parses a Trello payload -- a malformed
                    # `dateLastActivity` should cost one card its timestamp, not
                    # raise partway through a board sync.
                    created_at=parse_iso_naive(card.get("dateLastActivity"))
                    or _now_naive(),
                    updated_at=_now_naive(),
                    url=card.get("url", None),
                    organization_id="",
                    project_id="",
                )
                tickets.append(ticket)

            return tickets

    async def get_ticket(self, card_id: str) -> Optional[Ticket]:
        """
        Fetch a specific card (ticket) from Trello

        Args:
            card_id: The ID of the Trello card

        Returns:
            Ticket object or None if not found
        """
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/cards/{card_id}", params=self.auth_params
            )

            if response.status_code != 200:
                return None

            card = response.json()
            status = self._map_list_to_status(card.get("idList", ""))

            # organization_id/project_id are transient placeholders -- see note
            # in get_tickets_by_board above.
            return Ticket(
                summary=card.get("name", ""),
                description=card.get("desc", ""),
                assignee=self._get_member_name(card.get("idMembers", [])),
                status=status,
                created_at=parse_iso_naive(card.get("dateLastActivity"))
                or _now_naive(),
                updated_at=datetime.now(timezone.utc),
                url=card.get("url", None),
                organization_id="",
                project_id="",
            )

    async def create_ticket(
        self, board_id: str, list_id: str, ticket_data: Dict[str, Any]
    ) -> Ticket:
        """
        Create a new card (ticket) in Trello

        Args:
            board_id: The ID of the Trello board
            list_id: The ID of the Trello list to add the card to
            ticket_data: Dictionary containing ticket data

        Returns:
            Created Ticket object
        """
        card_data = {
            "idList": list_id,
            "name": ticket_data.get("summary", ""),
            "desc": ticket_data.get("description", ""),
            **self.auth_params,
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(f"{self.base_url}/cards", json=card_data)

            if response.status_code not in (200, 201):
                raise Exception(f"Failed to create card: {response.text}")

            card = response.json()

            # organization_id/project_id are transient placeholders here --
            # board_ticket_creation_service.py overwrites both (along with
            # board_registration_id) before persisting this ticket.
            return Ticket(
                summary=card.get("name", ""),
                description=card.get("desc", ""),
                status=self._map_list_to_status(list_id),
                created_at=datetime.now(timezone.utc),
                updated_at=datetime.now(timezone.utc),
                url=card.get("url", None),
                organization_id="",
                project_id="",
            )

    async def update_status(self, card_id: str, status: TicketStatus) -> bool:
        """
        Update the status of a card (ticket) by moving it to a different list

        Args:
            card_id: The ID of the Trello card
            status: The new TicketStatus

        Returns:
            True if successful, False otherwise
        """
        # Map the TicketStatus to a Trello list ID
        list_id = self._map_status_to_list(status)

        if not list_id:
            return False

        update_data = {"idList": list_id, **self.auth_params}

        async with httpx.AsyncClient() as client:
            response = await client.put(
                f"{self.base_url}/cards/{card_id}", json=update_data
            )

            return response.status_code == 200

    async def _get_member_name(self, member_ids: List[str]) -> Optional[str]:
        """Get the name of the first member in the list"""
        if not member_ids:
            return None

        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/members/{member_ids[0]}", params=self.auth_params
            )

            if response.status_code != 200:
                return None

            member = response.json()
            return member.get("fullName", None)

    def _map_list_to_status(self, list_id: str) -> TicketStatus:
        """Map a Trello list ID to a TicketStatus"""
        # This is a placeholder - in a real implementation, you would
        # fetch the lists for the board and map them to statuses
        # For now, we'll return a default status
        return TicketStatus.BACKLOG

    def _map_status_to_list(self, status: TicketStatus) -> Optional[str]:
        """Map a TicketStatus to a Trello list ID"""
        # This is a placeholder - in a real implementation, you would
        # have a mapping of statuses to list IDs
        # For now, we'll return None
        return None

    async def get_board(self, board_id: str) -> Optional[Dict[str, Any]]:
        """
        Get board information

        Args:
            board_id: The ID of the Trello board

        Returns:
            Board information or None if not found
        """
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/boards/{board_id}", params=self.auth_params
            )

            if response.status_code != 200:
                return None

            return response.json()

    async def get_lists(self, board_id: str) -> List[Dict[str, Any]]:
        """
        Get all lists for a board

        Args:
            board_id: The ID of the Trello board

        Returns:
            List of list objects
        """
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/boards/{board_id}/lists", params=self.auth_params
            )

            if response.status_code != 200:
                raise Exception(f"Failed to fetch lists: {response.text}")

            return response.json()

    async def get_board_members(self, board_id: str) -> List[Dict[str, Any]]:
        """
        Get all members of a board

        Args:
            board_id: The ID of the Trello board

        Returns:
            List of member objects
        """
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/boards/{board_id}/members", params=self.auth_params
            )

            if response.status_code != 200:
                raise Exception(f"Failed to fetch members: {response.text}")

            return response.json()

    async def get_labels(self, board_id: str) -> List[Dict[str, Any]]:
        """
        Get all labels for a board

        Args:
            board_id: The ID of the Trello board

        Returns:
            List of label objects
        """
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/boards/{board_id}/labels", params=self.auth_params
            )

            if response.status_code != 200:
                raise Exception(f"Failed to fetch labels: {response.text}")

            return response.json()

    async def update_card(
        self, card_id: str, updates: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Update a card

        Args:
            card_id: The ID of the Trello card
            updates: Dictionary of fields to update

        Returns:
            Updated card object
        """
        update_params = {**self.auth_params, **updates}

        async with httpx.AsyncClient() as client:
            response = await client.put(
                f"{self.base_url}/cards/{card_id}", params=update_params
            )

            if response.status_code != 200:
                raise Exception(f"Failed to update card: {response.text}")

            return response.json()

    async def add_comment(self, card_id: str, text: str) -> Dict[str, Any]:
        """
        Add a comment to a card

        Args:
            card_id: The ID of the Trello card
            text: The comment text

        Returns:
            Created comment object
        """
        comment_data = {**self.auth_params, "text": text}

        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/cards/{card_id}/actions/comments", params=comment_data
            )

            if response.status_code not in (200, 201):
                raise Exception(f"Failed to add comment: {response.text}")

            return response.json()
