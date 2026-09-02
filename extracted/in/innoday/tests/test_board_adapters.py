"""
Tests for board adapters (Trello and Jira)
"""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from src.adapters.base_adapter import (
    BaseBoardAdapter,
    BoardAdapterError,
    BoardCapabilityError,
)
from src.adapters.jira_adapter import JiraBoardAdapter
from src.adapters.linear_adapter import LinearBoardAdapter
from src.adapters.notion_adapter import NotionBoardAdapter
from src.adapters.trello_adapter import TrelloBoardAdapter
from src.api.jira_api import JiraAPI
from src.api.linear_api import LinearAPI
from src.api.notion_api import NotionAPI
from src.api.trello_api import TrelloAPI
from src.domain.board import BoardRegistration, BoardType
from src.domain.ticket import Ticket, TicketStatus


@pytest.fixture
def mock_board_registration():
    """Create a mock board registration"""
    return BoardRegistration(
        id="test-board-id",
        board_name="Test Board",
        board_type=BoardType.TRELLO,
        board_url="https://trello.com/b/abc123",
        board_external_id="ext-123",
        organization_id="org-123",
        is_active=True,
        metadata={},
    )


@pytest.fixture
def mock_jira_board_registration():
    """Create a mock Jira board registration"""
    return BoardRegistration(
        id="test-jira-board-id",
        board_name="Test Jira Board",
        board_type=BoardType.JIRA,
        board_url="https://company.atlassian.net/jira/software/projects/TEST/boards/1",
        board_external_id="1",
        organization_id="org-123",
        is_active=True,
        metadata={},
    )


#: Which API call each adapter's `add_comment` reaches, so one parametrised test
#: can drive all four. Named here rather than branched inside the test, because a
#: chain of `if board == …` is where a board quietly stops being covered.
_COMMENT_API_CALL = {
    "linear": (LinearBoardAdapter, LinearAPI, "add_comment"),
    "trello": (TrelloBoardAdapter, TrelloAPI, "add_comment"),
    "jira": (JiraBoardAdapter, JiraAPI, "add_comment"),
    "notion": (NotionBoardAdapter, NotionAPI, "append_block_children"),
}


def _adapter_for(board, *, side_effect=None, return_value=None):
    adapter_cls, api_cls, method = _COMMENT_API_CALL[board]
    api = AsyncMock(spec=api_cls)
    call = getattr(api, method)
    if side_effect is not None:
        call.side_effect = side_effect
    else:
        call.return_value = return_value
    if board == "notion":
        # Notion builds a block from the comment text before it calls out; the
        # builder is a plain (non-async) helper on the API object.
        api._build_text_block = MagicMock(return_value={"paragraph": {}})
    registration = MagicMock()
    registration.board_external_id = "board-1"
    adapter = adapter_cls(api, registration)
    if board == "jira":
        # The OAuth refresh hook is a no-op for a Basic-auth board and is not
        # what this test is about.
        adapter._refresh_api_auth_if_oauth = AsyncMock(return_value=None)
    return adapter


def _adapter_whose_api_raises(board, error):
    return _adapter_for(board, side_effect=error)


def _adapter_whose_api_returns(board, answer):
    return _adapter_for(board, return_value=answer)


class TestBaseBoardAdapter:
    """Test the base adapter functionality"""

    def test_map_external_status_to_internal(self):
        """Test status mapping from external to internal"""
        # Use TrelloBoardAdapter as concrete implementation to test base methods
        mock_api = MagicMock(spec=TrelloAPI)
        mock_board_reg = MagicMock()
        adapter = TrelloBoardAdapter(mock_api, mock_board_reg)

        # Test various status mappings
        assert adapter.map_external_status_to_internal("To Do") == "TODO"
        assert adapter.map_external_status_to_internal("In Progress") == "IN_PROGRESS"
        assert adapter.map_external_status_to_internal("Testing") == "IN_REVIEW"
        assert adapter.map_external_status_to_internal("Done") == "DONE"
        assert adapter.map_external_status_to_internal("Completed") == "DONE"
        assert (
            adapter.map_external_status_to_internal("Unknown Status") == "TODO"
        )  # Default is TODO


class TestTrelloBoardAdapter:
    """Test Trello adapter implementation"""

    @pytest.mark.asyncio
    async def test_initialize(self, mock_board_registration):
        """Test adapter initialization"""
        mock_api = AsyncMock(spec=TrelloAPI)
        mock_api.get_board.return_value = {"id": "board-123", "name": "Test Board"}
        mock_api.get_lists.return_value = [
            {"id": "list-1", "name": "To Do"},
            {"id": "list-2", "name": "In Progress"},
            {"id": "list-3", "name": "Done"},
        ]

        adapter = TrelloBoardAdapter(mock_api, mock_board_registration)
        await adapter.initialize("test-token")

        assert adapter._initialized
        assert adapter.list_mapping["list-1"] == "TODO"
        assert adapter.list_mapping["list-2"] == "IN_PROGRESS"
        assert adapter.list_mapping["list-3"] == "DONE"
        assert adapter.status_to_list["TODO"] == "list-1"

    @pytest.mark.asyncio
    async def test_get_tickets(self, mock_board_registration):
        """Test getting tickets from Trello"""
        mock_api = AsyncMock(spec=TrelloAPI)

        # Mock tickets from API - don't use metadata field since it's SQLModel MetaData
        mock_tickets = [
            Ticket(
                id=1,
                summary="Test Ticket 1",
                status=TicketStatus.TODO,
                external_ticket_id="card-1",
            ),
            Ticket(
                id=2,
                summary="Test Ticket 2",
                status=TicketStatus.IN_PROGRESS,
                external_ticket_id="card-2",
            ),
        ]
        mock_api.get_tickets_by_board.return_value = mock_tickets

        adapter = TrelloBoardAdapter(mock_api, mock_board_registration)
        adapter.list_mapping = {"list-1": "TODO", "list-2": "IN_PROGRESS"}

        tickets = await adapter.get_tickets("board-123")

        assert len(tickets) == 2
        assert tickets[0].summary == "Test Ticket 1"
        assert tickets[0].status == TicketStatus.TODO
        assert tickets[1].status == TicketStatus.IN_PROGRESS

    @pytest.mark.asyncio
    async def test_create_ticket(self, mock_board_registration):
        """Test creating a ticket in Trello"""
        mock_api = AsyncMock(spec=TrelloAPI)
        mock_api.get_lists.return_value = [{"id": "list-1", "name": "To Do"}]

        created_ticket = Ticket(
            id=1,
            summary="New Ticket",
            description="Test description",
            status=TicketStatus.TODO,
            external_ticket_id="new-card-1",
        )
        mock_api.create_ticket.return_value = created_ticket

        adapter = TrelloBoardAdapter(mock_api, mock_board_registration)
        adapter.list_mapping = {"list-1": "TODO"}
        adapter.status_to_list = {"TODO": "list-1"}

        ticket_data = {
            "summary": "New Ticket",
            "description": "Test description",
            "status": "TODO",
        }

        result = await adapter.create_ticket("board-123", ticket_data)

        assert result.summary == "New Ticket"
        assert result.status == TicketStatus.TODO
        mock_api.create_ticket.assert_called_once()

    @pytest.mark.asyncio
    async def test_update_ticket_status(self, mock_board_registration):
        """Test updating ticket status (moving cards between lists)"""
        mock_api = AsyncMock(spec=TrelloAPI)
        mock_api.update_card.return_value = True

        adapter = TrelloBoardAdapter(mock_api, mock_board_registration)
        adapter.list_mapping = {"list-1": "TODO", "list-2": "IN_PROGRESS"}
        adapter.status_to_list = {"TODO": "list-1", "IN_PROGRESS": "list-2"}

        ticket = Ticket(
            id=1,
            summary="Test Ticket",
            status=TicketStatus.TODO,
            external_ticket_id="card-123",
        )

        # Pass a status that will be mapped correctly
        updated = await adapter.update_ticket_status(ticket, "In Progress")

        assert updated.status == TicketStatus.IN_PROGRESS
        mock_api.update_card.assert_called_with("card-123", {"idList": "list-2"})


class TestJiraBoardAdapter:
    """Test Jira adapter implementation"""

    @pytest.mark.asyncio
    async def test_initialize(self, mock_jira_board_registration):
        """Test Jira adapter initialization"""
        mock_api = MagicMock(spec=JiraAPI)
        mock_api.base_url = "https://company.atlassian.net"
        mock_api.auth = ("test@example.com", "token")
        mock_api.headers = {"Accept": "application/json"}

        adapter = JiraBoardAdapter(mock_api, mock_jira_board_registration)

        with patch("httpx.AsyncClient") as mock_client:
            mock_response = MagicMock()
            mock_response.status_code = 200
            # location.key is the real field in Jira's board-configuration
            # response; location.projectKey does not exist (see
            # jira_adapter.py's _init_project_config).
            mock_response.json.return_value = {"location": {"key": "TEST"}}

            mock_client.return_value.__aenter__.return_value.get.return_value = (
                mock_response
            )

            await adapter.initialize("test-token")

            assert adapter._initialized
            assert adapter.project_key == "TEST"
            assert adapter.project_key == "TEST"

    @pytest.mark.asyncio
    async def test_get_tickets(self, mock_jira_board_registration):
        """Test getting tickets from Jira"""
        mock_api = AsyncMock(spec=JiraAPI)
        # Basic Auth mode: adapter._is_oauth_mode() checks self.api.auth is
        # None to decide whether to route through the refresh-aware path.
        mock_api.auth = ("test@example.com", "token")
        mock_api.base_url = "https://company.atlassian.net"
        mock_api.headers = {"Accept": "application/json"}

        mock_tickets = [
            Ticket(
                id=1,
                summary="JIRA-1: Test Issue",
                status=TicketStatus.TODO,
                external_ticket_id="JIRA-1",
            ),
            Ticket(
                id=2,
                summary="JIRA-2: Another Issue",
                status=TicketStatus.IN_PROGRESS,
                external_ticket_id="JIRA-2",
            ),
        ]
        mock_api.get_tickets_by_board.return_value = mock_tickets

        adapter = JiraBoardAdapter(mock_api, mock_jira_board_registration)
        tickets = await adapter.get_tickets("1")

        assert len(tickets) == 2
        assert tickets[0].external_ticket_id == "JIRA-1"
        assert tickets[1].external_ticket_id == "JIRA-2"

    @pytest.mark.asyncio
    async def test_create_ticket(self, mock_jira_board_registration):
        """Test creating a ticket in Jira"""
        mock_api = AsyncMock(spec=JiraAPI)
        # Basic Auth mode: see test_get_tickets above.
        mock_api.auth = ("test@example.com", "token")
        mock_api.base_url = "https://company.atlassian.net"
        mock_api.headers = {"Accept": "application/json"}

        created_ticket = Ticket(
            id=1,
            summary="New Jira Issue",
            description="Test description",
            status=TicketStatus.TODO,
            external_ticket_id="JIRA-100",
            url="https://company.atlassian.net/browse/JIRA-100",
        )
        mock_api.create_ticket.return_value = created_ticket

        adapter = JiraBoardAdapter(mock_api, mock_jira_board_registration)
        adapter.project_key = "TEST"

        ticket_data = {
            "summary": "New Jira Issue",
            "description": "Test description",
            "issue_type": "Task",
        }

        result = await adapter.create_ticket("1", ticket_data)

        assert result.summary == "New Jira Issue"
        assert result.external_ticket_id == "JIRA-100"
        mock_api.create_ticket.assert_called_once()

    @pytest.mark.asyncio
    async def test_update_ticket_status_with_transitions(
        self, mock_jira_board_registration
    ):
        """Test updating ticket status using workflow transitions"""
        mock_api = MagicMock(spec=JiraAPI)
        mock_api.base_url = "https://company.atlassian.net"
        mock_api.auth = ("test@example.com", "token")
        mock_api.headers = {"Accept": "application/json"}

        adapter = JiraBoardAdapter(mock_api, mock_jira_board_registration)

        ticket = Ticket(
            id=1,
            summary="Test Issue",
            status=TicketStatus.TODO,
            external_ticket_id="JIRA-1",
        )

        with patch("httpx.AsyncClient") as mock_client:
            # Mock getting transitions
            transitions_response = MagicMock()
            transitions_response.status_code = 200
            transitions_response.json.return_value = {
                "transitions": [
                    {
                        "id": "21",
                        "name": "Start Progress",
                        "to": {"name": "In Progress"},
                    },
                    {"id": "31", "name": "Close", "to": {"name": "Done"}},
                ]
            }

            # Mock executing transition
            transition_response = MagicMock()
            transition_response.status_code = 204

            mock_async_client = mock_client.return_value.__aenter__.return_value
            mock_async_client.get.return_value = transitions_response
            mock_async_client.post.return_value = transition_response

            updated = await adapter.update_ticket_status(ticket, "In Progress")

            assert updated.status == TicketStatus.IN_PROGRESS

            # Verify transition was called
            mock_async_client.post.assert_called_with(
                "https://company.atlassian.net/rest/api/3/issue/JIRA-1/transitions",
                auth=mock_api.auth,
                headers=mock_api.headers,
                json={"transition": {"id": "21"}},
                timeout=30.0,
            )

    @pytest.mark.asyncio
    async def test_add_comment(self, mock_jira_board_registration):
        """Test adding a comment to a Jira issue"""
        mock_api = AsyncMock(spec=JiraAPI)
        # Basic Auth mode: see test_get_tickets above.
        mock_api.auth = ("test@example.com", "token")
        mock_api.base_url = "https://company.atlassian.net"
        mock_api.headers = {"Accept": "application/json"}
        mock_api.add_comment.return_value = True

        adapter = JiraBoardAdapter(mock_api, mock_jira_board_registration)

        ticket = Ticket(id=1, summary="Test Issue", external_ticket_id="JIRA-1")

        result = await adapter.add_comment(ticket, "This is a test comment")

        assert result is True
        mock_api.add_comment.assert_called_with("JIRA-1", "This is a test comment")


class TestBoardAdapterErrors:
    """Test error handling in adapters"""

    @pytest.mark.asyncio
    async def test_trello_adapter_connection_failure(self, mock_board_registration):
        """Test Trello adapter handles connection failures"""
        mock_api = AsyncMock(spec=TrelloAPI)
        mock_api.get_board.side_effect = Exception("Connection failed")

        adapter = TrelloBoardAdapter(mock_api, mock_board_registration)

        with pytest.raises(BoardAdapterError, match="Initialization failed"):
            await adapter.initialize("test-token")

    @pytest.mark.asyncio
    async def test_jira_adapter_missing_ticket_id(self, mock_jira_board_registration):
        """Test Jira adapter handles missing external ticket ID"""
        mock_api = MagicMock(spec=JiraAPI)
        adapter = JiraBoardAdapter(mock_api, mock_jira_board_registration)

        ticket = Ticket(
            id=1,
            summary="Test Issue",
            status=TicketStatus.TODO,
            # Missing external_ticket_id
        )

        with pytest.raises(BoardAdapterError, match="missing external_ticket_id"):
            await adapter.update_ticket_status(ticket, "IN_PROGRESS")

    @pytest.mark.asyncio
    async def test_trello_adapter_invalid_status(self, mock_board_registration):
        """Test Trello adapter handles invalid status transitions"""
        mock_api = AsyncMock(spec=TrelloAPI)
        adapter = TrelloBoardAdapter(mock_api, mock_board_registration)
        adapter.status_to_list = {"TODO": "list-1"}  # Only TODO is mapped

        ticket = Ticket(
            id=1,
            summary="Test Ticket",
            status=TicketStatus.TODO,
            external_ticket_id="card-123",
        )

        # Try to move to a status that has no list mapping
        # "Done" maps to "DONE" internally but we don't have a list for it
        with pytest.raises(BoardAdapterError, match="Cannot map status"):
            await adapter.update_ticket_status(ticket, "Done")


class TestAddCommentContract:
    """What `add_comment` promises its one caller, on every board type.

    `services/ticket_comment_service.py` is `add_comment`'s first live caller in
    this repo's history -- every adapter has implemented it for as long as the
    adapters have existed and nothing outside them ever called one. It depends on
    two properties that no adapter was written to hold, so they are pinned here
    rather than only against a stub written in the same change.
    """

    @pytest.mark.asyncio
    async def test_a_board_type_that_cannot_comment_says_so_as_a_capability(self):
        """The base default is a `BoardCapabilityError`, like `set_board_assignee`.

        While `add_comment` was abstract, an adapter for a board with no comments
        had two options and both were wrong: return `True` for a comment it never
        posted, or raise a plain `BoardAdapterError` that the caller records and
        retries forever for something that can never succeed. The third answer --
        "this board type has nowhere to put one" -- had no way to be said.
        """

        class _CommentlessBoard(BaseBoardAdapter):
            async def initialize(self, token):  # pragma: no cover - not exercised
                return True

            async def get_tickets(self):  # pragma: no cover
                return []

            async def get_ticket(self, external_id):  # pragma: no cover
                return None

            async def create_ticket(self, ticket, **kw):  # pragma: no cover
                return ticket

            async def update_ticket(self, ticket, **kw):  # pragma: no cover
                return ticket

            async def update_ticket_status(
                self, ticket, new_status
            ):  # pragma: no cover
                return ticket

            async def get_board_metadata(self):  # pragma: no cover
                return {}

            async def validate_connection(self):  # pragma: no cover
                return True

        adapter = _CommentlessBoard(MagicMock())
        with pytest.raises(BoardCapabilityError):
            await adapter.add_comment(Ticket(id=1, summary="t"), "hello")

    @pytest.mark.asyncio
    @pytest.mark.parametrize("board", ["linear", "trello", "jira", "notion"])
    async def test_an_exception_written_to_be_read_is_not_downgraded(self, board):
        """A `BoardCapabilityError` reaches the caller **as itself**.

        Every adapter wraps its body in `except Exception -> raise
        BoardAdapterError(...)`, so without an explicit re-raise a capability
        refusal is flattened into a plain failure on the way out -- and the caller
        keys on the *type* to tell "this can never work" (notice, nothing stored)
        from "this did not work this time" (recorded, retried). Downgrading turns
        a permanent fact into a retry that runs forever.

        Notion is in this list for a second reason: it used to `return False` for
        every exception, which converted a message written for a person into a
        bare falsy answer with no reason attached.
        """
        refusal = BoardCapabilityError("this board has nowhere to put a comment")
        ticket = Ticket(id=1, summary="t", external_ticket_id="X-1")

        adapter = _adapter_whose_api_raises(board, refusal)
        with pytest.raises(BoardCapabilityError):
            await adapter.add_comment(ticket, "hello")

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        ("board", "api_answer", "expected"),
        [
            ("linear", False, False),
            ("linear", True, True),
            ("jira", False, False),
            ("jira", True, True),
            # Trello's API returns the created comment object and raises on
            # failure; Notion's returns the append response.
            ("trello", {}, False),
            ("trello", {"id": "c1"}, True),
            ("notion", {}, False),
            ("notion", {"results": [1]}, True),
        ],
    )
    async def test_the_board_s_own_answer_is_what_comes_back(
        self, board, api_answer, expected
    ):
        """**A falsy return means the board did not take it.**

        `LinearAPI.add_comment` hands back `commentCreate.success` verbatim and
        `JiraAPI.add_comment` a status-code check, so a board that *declines* a
        comment raises nothing at all -- and the caller reports it as delivered
        unless the answer is read.

        Trello and Notion used to `return True` unconditionally, discarding what
        their API had said. That made them the two boards where the contract
        failed *silently*, which is the worse half of the same defect.
        """
        adapter = _adapter_whose_api_returns(board, api_answer)
        got = await adapter.add_comment(
            Ticket(id=1, summary="t", external_ticket_id="X-1"), "hello"
        )
        # `bool(...)`, not `is`: Trello and Notion answer with the API's object
        # rather than a literal, and the contract is truthiness -- "did the board
        # take it" -- not the identity of what it handed back.
        assert bool(got) is expected
