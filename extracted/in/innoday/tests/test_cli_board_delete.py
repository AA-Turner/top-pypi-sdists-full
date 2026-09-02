"""Tests for `innoday board delete` — soft-deletes a board registration in
InnoDay (calls DELETE /boards/{id}, which is an InnoDay-only soft-delete that
never touches the external board)."""

import argparse
from unittest.mock import patch

import pytest


def _fake_config():
    class C:
        def get_current_organization(self):
            return "bp"

        def get_organization_id(self, alias):
            return "org-1"

    return C()


def _fake_client(status_code, payload):
    class Resp:
        status_code = None

        def json(self):
            return payload

    resp = Resp()
    resp.status_code = status_code

    class Client:
        called_with = None

        async def delete(self, endpoint, **kwargs):
            self.called_with = endpoint
            return resp

    return Client()


@pytest.mark.asyncio
async def test_board_delete_calls_delete_endpoint_and_reports_cleared():
    from src.cli.commands.boards import BoardCommands

    args = argparse.Namespace(board_command="delete", board_id="board-99", yes=True)
    config = _fake_config()
    client = _fake_client(
        200, {"message": "Board registration deleted successfully", "cleared": 445}
    )

    rc = await BoardCommands._handle_delete(args, client, config)

    assert rc == 0
    # It must hit the DELETE /boards/{id} endpoint (InnoDay-only soft-delete)
    assert client.called_with == "/organizations/org-1/boards/board-99"


@pytest.mark.asyncio
async def test_board_delete_confirmation_declined_aborts():
    from src.cli.commands.boards import BoardCommands

    args = argparse.Namespace(board_command="delete", board_id="board-99", yes=False)
    config = _fake_config()
    client = _fake_client(200, {"cleared": 445})

    with patch("src.cli.commands.boards.Confirm.ask", return_value=False):
        rc = await BoardCommands._handle_delete(args, client, config)

    assert rc == 0
    # Declined → must NOT have called the endpoint
    assert client.called_with is None


@pytest.mark.asyncio
async def test_board_delete_nonzero_on_error():
    from src.cli.commands.boards import BoardCommands

    args = argparse.Namespace(board_command="delete", board_id="board-99", yes=True)
    config = _fake_config()
    client = _fake_client(404, {"detail": "Board registration not found"})

    rc = await BoardCommands._handle_delete(args, client, config)

    assert rc == 1
