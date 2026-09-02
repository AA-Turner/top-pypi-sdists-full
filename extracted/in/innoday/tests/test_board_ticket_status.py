"""Unit tests for status handling in BoardTicketCreationService.create_ticket_on_board.

The external-board create path historically hardcoded status "TODO" and board
adapters (e.g. Linear) create the ticket in the board's default workflow state
without honouring a status on create -- so a caller-supplied status was silently
dropped. create_board_ticket now accepts an optional `status`; these tests lock
in that (a) the default is still "TODO" and (b) an explicit status triggers the
adapter's separate status transition.
"""

from unittest.mock import AsyncMock, MagicMock

import pytest

from src.domain.board import BoardType
from src.services import board_adapter_factory as factory
from src.services.board_ticket_creation_service import (
    BoardTicketCreationService,
    TicketCreateRequest,
)


def _make_created_ticket():
    """A minimal object standing in for the adapter's returned Ticket."""
    t = MagicMock()
    t.id = 1
    t.external_ticket_id = "PF-999"
    t.url = "https://linear.app/x/issue/PF-999"
    t.summary = "Test ticket"
    t.description = None
    t.status = "todo"
    t.created_at = __import__("datetime").datetime(2026, 7, 20)
    return t


def _service_with_mocked_adapter(adapter, monkeypatch):
    """Build a service whose session, token resolution, and adapter are mocked."""
    board_reg = MagicMock()
    board_reg.id = "board-1"
    board_reg.is_active = True
    board_reg.organization_id = "org-1"
    board_reg.board_type = BoardType.LINEAR
    board_reg.board_external_id = "team-uuid"
    board_reg.project_id = "proj-1"
    board_reg.board_name = "PixelFuel (PF)"

    org = MagicMock()
    org.alias = "hs"

    session = MagicMock()
    # .get(BoardRegistration, id) then .get(Organization, id)
    session.get.side_effect = [board_reg, org]

    service = BoardTicketCreationService(session)
    # Stubbed at the **vault read**, which is the seam that actually moved --
    # #643 lifted the chain into `board_adapter_factory.resolve_board_token` and
    # left `_resolve_token` a delegate. Replacing the delegate instead would skip
    # the chain's own logic (caller-token-wins, and the refusal when nothing is
    # stored), so this test would keep passing over a broken one.
    monkeypatch.setattr(
        factory,
        "get_board_credential_payload",
        lambda session, board_id: {"token": "tok"},
    )
    # _get_adapter is async now that it shares the board-adapter factory, whose
    # Jira OAuth branch has to await a token refresh.
    service._get_adapter = AsyncMock(return_value=adapter)
    return service


def _make_adapter():
    adapter = MagicMock()
    adapter.initialize = AsyncMock()
    created = _make_created_ticket()
    adapter.create_ticket = AsyncMock(return_value=created)
    adapter.update_ticket_status = AsyncMock(return_value=created)
    return adapter


class TestBoardTicketStatus:
    @pytest.mark.asyncio
    async def test_default_status_is_todo_and_no_transition(self, monkeypatch):
        adapter = _make_adapter()
        service = _service_with_mocked_adapter(adapter, monkeypatch)

        await service.create_ticket_on_board(
            board_registration_id="board-1",
            ticket_data=TicketCreateRequest(summary="Test ticket"),
            user_id="user-1",
        )

        # Adapter created with the default status...
        _, adapter_data = adapter.create_ticket.call_args[0]
        assert adapter_data["status"] == "TODO"
        # ...and no separate status transition was attempted.
        adapter.update_ticket_status.assert_not_awaited()

    @pytest.mark.asyncio
    async def test_explicit_status_triggers_transition(self, monkeypatch):
        adapter = _make_adapter()
        service = _service_with_mocked_adapter(adapter, monkeypatch)

        await service.create_ticket_on_board(
            board_registration_id="board-1",
            ticket_data=TicketCreateRequest(summary="Test ticket", status="Done"),
            user_id="user-1",
        )

        # The explicit status is passed to the adapter's create payload...
        _, adapter_data = adapter.create_ticket.call_args[0]
        assert adapter_data["status"] == "Done"
        # ...and then applied via the separate transition call.
        adapter.update_ticket_status.assert_awaited_once()
        assert adapter.update_ticket_status.call_args[0][1] == "Done"

    @pytest.mark.asyncio
    async def test_status_transition_failure_does_not_fail_create(self, monkeypatch):
        adapter = _make_adapter()
        adapter.update_ticket_status = AsyncMock(
            side_effect=Exception("Unknown Linear workflow state: 'Done'")
        )
        service = _service_with_mocked_adapter(adapter, monkeypatch)

        # Should not raise -- the ticket was created, only the transition failed.
        resp = await service.create_ticket_on_board(
            board_registration_id="board-1",
            ticket_data=TicketCreateRequest(summary="Test ticket", status="Done"),
            user_id="user-1",
        )
        assert resp.external_id == "PF-999"
