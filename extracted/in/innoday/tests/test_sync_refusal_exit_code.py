"""A refused sync must not exit 0.

The server answers **429** when a sync is already running for a board: it did
not queue anything. Both CLI paths that can receive that -- `innoday sync`
(`SyncCommands._sync_board`) and `innoday board sync`
(`BoardCommands._handle_sync`) -- printed the server's detail and then returned
**0**, so a script could not tell a refusal from a sync that started. #613 fixed
what the two *said*; the exit code was left because changing one is a contract
change. It is the half that machines read.

`1` is this CLI's failure code -- every other "I could not do that" branch in
both modules returns it, and `main.py` reserves `130` for an interrupt. The
cascade in `_handle_cascade` already propagates a `1` from the board stage.

Each test asserts the exit code **and** that the server's own detail reached the
operator, so a `1` returned by some earlier guard -- a missing org, an
unresolvable board -- cannot be mistaken for the refusal path. The 200 cases are
the other half of that: the same fakes, one status code apart, must still exit 0,
which is what makes a red here specific to the refusal.
"""

from __future__ import annotations

import argparse

import pytest

DETAIL = "A sync is already running for this board (started 2026-08-14T09:00:00Z). Use --force to override."


class _Response:
    def __init__(self, status_code, payload):
        self.status_code = status_code
        self._payload = payload
        self.content = b"{}"

    def json(self):
        return self._payload


class _Client:
    """Answers the board listing, then the sync POST with `sync_status`."""

    def __init__(self, sync_status, sync_payload):
        self._sync_status = sync_status
        self._sync_payload = sync_payload
        self.posted = []

    async def get(self, path, params=None):
        return _Response(
            200,
            [{"id": "board-1", "board_name": "Board One", "board_type": "linear"}],
        )

    async def post(self, path, json=None):
        self.posted.append((path, json))
        return _Response(self._sync_status, self._sync_payload)


class _Config:
    def get_current_organization(self):
        return "hs"

    def get_organization_id(self, alias=None):
        return "org-1"

    def get_current_project_id(self):
        return "proj-1"


def _refused_client():
    return _Client(429, {"detail": DETAIL})


def _queued_client():
    return _Client(200, {"sync_id": "sync-1", "status": "PENDING"})


# --------------------------------------------------------------- innoday sync


@pytest.mark.asyncio
async def test_cascade_board_sync_exits_non_zero_when_refused(capsys):
    from src.cli.commands.sync import SyncCommands

    client = _refused_client()
    rc = await SyncCommands._sync_board(client, "org-1", "proj-1", _Config())

    out = capsys.readouterr().out
    assert "already running" in out, out
    assert rc != 0, "a refused sync reported success"


@pytest.mark.asyncio
async def test_cascade_board_sync_exits_zero_when_queued(capsys):
    from src.cli.commands.sync import SyncCommands

    client = _queued_client()
    rc = await SyncCommands._sync_board(client, "org-1", "proj-1", _Config())

    assert "sync-1" in capsys.readouterr().out
    assert rc == 0


# ---------------------------------------------------------- innoday board sync


def _board_sync_args():
    return argparse.Namespace(
        board_command="sync",
        board_id="board-1",
        full=False,
        dry_run=False,
        force=False,
    )


@pytest.mark.asyncio
async def test_board_sync_exits_non_zero_when_refused(capsys):
    from src.cli.commands.boards import BoardCommands

    client = _refused_client()
    rc = await BoardCommands._handle_sync(_board_sync_args(), client, _Config())

    out = capsys.readouterr().out
    assert "already running" in out, out
    assert rc != 0, "a refused sync reported success"


@pytest.mark.asyncio
async def test_board_sync_exits_zero_when_queued(capsys):
    from src.cli.commands.boards import BoardCommands

    client = _queued_client()
    rc = await BoardCommands._handle_sync(_board_sync_args(), client, _Config())

    assert "sync-1" in capsys.readouterr().out
    assert rc == 0


def test_the_refusal_uses_the_cli_wide_failure_code():
    """Not just "non-zero" -- the same `1` every other failure returns.

    Asserted on the source of both branches so the two paths cannot drift into
    two different codes for one refusal, which is how they came to disagree
    about the sync-status hint in the first place (#613).
    """
    from pathlib import Path

    import src.cli.commands.boards as boards_module
    import src.cli.commands.sync as sync_module

    for module in (boards_module, sync_module):
        source = Path(module.__file__).read_text()
        head, _, tail = source.partition("status_code == 429")
        assert tail, f"{module.__name__} no longer handles a 429"
        branch = tail.split("else:")[0]
        assert "return 1" in branch, (
            f"{module.__name__}'s 429 branch does not exit 1: {branch[-200:]}"
        )
        assert "return 0" not in branch, f"{module.__name__}'s 429 branch still exits 0"
