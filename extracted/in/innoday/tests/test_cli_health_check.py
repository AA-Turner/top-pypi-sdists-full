"""A sync the server refuses is not a health failure.

`scripts/cli_health_check.py` answers one question: "is my setup stale or
broken right now?" It probes every board of every visible org with a
`board sync --dry-run`. Since #622 the CLI exits **1** when the server answers
429 -- correct there, because the caller asked for a sync and did not get one.

Here it is wrong. `--dry-run` does not exempt the caller: the server's guard is
`if not sync_request.force`, and its `dry_run.is_(False)` filter applies to the
*blocking* row, not to the incoming request. So a probe that lands while any
real sync is in flight was refused, exited 1, and turned the whole health check
red -- on the strongest possible evidence that the system is working.

The other half matters just as much: fixing the false alarm by making the sync
check unable to fail would be worse than the bug, so the genuine-error case is
asserted here alongside it, from the same fake, one message apart.

The exit code cannot carry this distinction -- 1 is the CLI's single failure
code -- so the script classifies on the message. `TestTheMarkersMatchTheRealCli`
is what keeps that from silently rotting: it drives the CLI's actual 429 branch,
in both its wordings, and asserts the script still recognises what comes out.
"""

from __future__ import annotations

import argparse
import importlib.util
import subprocess
import sys
from pathlib import Path

import pytest

_SCRIPT_PATH = (
    Path(__file__).resolve().parent.parent / "scripts" / "cli_health_check.py"
)
_spec = importlib.util.spec_from_file_location("cli_health_check", _SCRIPT_PATH)
cli_health_check = importlib.util.module_from_spec(_spec)
sys.modules["cli_health_check"] = cli_health_check
_spec.loader.exec_module(cli_health_check)


# The server's own detail, from `src/routers/boards.py`'s 429.
SERVER_DETAIL = (
    "Sync already in progress for this board: run abc-123 started 4 minutes "
    "ago and has not reported yet. If it is stuck, sync again with "
    '`innoday board sync --force` (API: "force": true).'
)
# What a genuine failure looks like instead: the sync was attempted and broke.
GENUINE_ERROR = "Failed to sync board: {'detail': 'Board credential not found'}"


def _completed(returncode: int, stdout: str = "", stderr: str = "") -> object:
    return subprocess.CompletedProcess(
        args=["innoday"], returncode=returncode, stdout=stdout, stderr=stderr
    )


def _fake_run(sync_result):
    """Answer the four commands the org loop issues, with `sync_result` last."""

    def run(cmd: list[str]) -> object:
        if "orgs" in cmd:
            return _completed(0, stdout='[{"name": "Haviland", "slug": "hs"}]')
        if "tickets" in cmd:
            return _completed(0, stdout="PF-1 something")
        if cmd[-1] == "list":  # board list
            return _completed(0, stdout='[{"id": "board-1", "name": "Board One"}]')
        assert "sync" in cmd, cmd
        return sync_result

    return run


class TestARefusalIsHealthy:
    def test_a_refused_sync_does_not_fail_the_health_check(self, capsys, monkeypatch):
        monkeypatch.setattr(
            cli_health_check, "_run", _fake_run(_completed(1, stdout=SERVER_DETAIL))
        )

        ok = cli_health_check.check_org_access_and_sync(skip_sync=False)

        out = capsys.readouterr().out
        assert ok is True, out
        assert "SKIP: sync (board Board One)" in out, out
        assert "FAIL" not in out, out

    def test_the_refusal_is_still_reported_not_swallowed(self, capsys, monkeypatch):
        """SKIP, not PASS: the operator is told which board and why."""
        monkeypatch.setattr(
            cli_health_check, "_run", _fake_run(_completed(1, stdout=SERVER_DETAIL))
        )

        cli_health_check.check_org_access_and_sync(skip_sync=False)

        out = capsys.readouterr().out
        assert "already running" in out, out
        assert "abc-123" in out, "the server's detail did not reach the operator"


class TestAGenuineFailureStillFails:
    def test_a_real_sync_error_fails_the_health_check(self, capsys, monkeypatch):
        monkeypatch.setattr(
            cli_health_check, "_run", _fake_run(_completed(1, stdout=GENUINE_ERROR))
        )

        ok = cli_health_check.check_org_access_and_sync(skip_sync=False)

        out = capsys.readouterr().out
        assert ok is False, out
        assert "FAIL: sync (board Board One)" in out, out
        assert "SKIP: sync" not in out, out

    def test_a_successful_sync_still_passes(self, capsys, monkeypatch):
        """The third case, so a red above is specific to how a 1 is read."""
        monkeypatch.setattr(
            cli_health_check, "_run", _fake_run(_completed(0, stdout="Sync queued"))
        )

        ok = cli_health_check.check_org_access_and_sync(skip_sync=False)

        out = capsys.readouterr().out
        assert ok is True, out
        assert "PASS: sync (board Board One, dry-run)" in out, out


class TestTheClassifier:
    @pytest.mark.parametrize(
        "output",
        [
            SERVER_DETAIL,
            "Sync already in progress for this board.",  # the CLI's fallback
            # rich hard-wraps to 80 columns when it is not writing to a tty --
            # which is how this script captures the CLI -- so a marker can
            # arrive split across lines.
            "⚠️  Sync already\nin progress for this board: run abc-123",
        ],
    )
    def test_a_refusal_is_recognised(self, output):
        assert cli_health_check._is_sync_refusal(output) is True

    @pytest.mark.parametrize(
        "output",
        [
            GENUINE_ERROR,
            "Sync failed: connection refused",
            "Board not found",
            "",
        ],
    )
    def test_a_failure_is_not_mistaken_for_a_refusal(self, output):
        assert cli_health_check._is_sync_refusal(output) is False


class TestTheMarkersMatchTheRealCli:
    """Pin the script's markers against what the CLI actually prints.

    The script shells out to the installed `innoday`, so it cannot import a
    shared constant -- the coupling is textual and would otherwise rot in
    silence, returning this script to reporting FAIL on a healthy system. These
    drive the real 429 branch of both CLI paths and assert the script still
    recognises the output, so rewording the refusal turns this red.
    """

    class _Response:
        def __init__(self, status_code, payload):
            self.status_code = status_code
            self._payload = payload
            self.content = b"{}"

        def json(self):
            return self._payload

    class _Client:
        def __init__(self, payload):
            self._payload = payload

        async def get(self, path, params=None):
            return TestTheMarkersMatchTheRealCli._Response(
                200,
                [{"id": "board-1", "board_name": "Board One", "board_type": "linear"}],
            )

        async def post(self, path, json=None):
            return TestTheMarkersMatchTheRealCli._Response(429, self._payload)

    class _Config:
        def get_current_organization(self):
            return "hs"

        def get_organization_id(self, alias=None):
            return "org-1"

        def get_current_project_id(self):
            return "proj-1"

    @pytest.mark.parametrize(
        "payload",
        [
            {"detail": SERVER_DETAIL},  # the server's wording
            {},  # no detail -> the CLI's own fallback wording
        ],
        ids=["server-detail", "cli-fallback"],
    )
    @pytest.mark.asyncio
    async def test_board_sync_refusal_output_is_recognised(self, capsys, payload):
        from src.cli.commands.boards import BoardCommands

        args = argparse.Namespace(
            board_command="sync",
            board_id="board-1",
            full=False,
            dry_run=True,
            force=False,
        )
        rc = await BoardCommands._handle_sync(
            args, self._Client(payload), self._Config()
        )

        out = capsys.readouterr().out
        assert rc == 1, "the refusal stopped exiting 1 -- #622"
        assert cli_health_check._is_sync_refusal(out), (
            f"the health check no longer recognises the CLI's refusal: {out!r}"
        )

    @pytest.mark.asyncio
    async def test_the_cli_s_other_failure_output_is_not_recognised(self, capsys):
        """The same path, one status code apart, must not read as a refusal."""
        from src.cli.commands.boards import BoardCommands

        class _Failing(self._Client):
            async def post(self, path, json=None):
                return TestTheMarkersMatchTheRealCli._Response(
                    500, {"detail": "Board credential not found"}
                )

        args = argparse.Namespace(
            board_command="sync",
            board_id="board-1",
            full=False,
            dry_run=True,
            force=False,
        )
        rc = await BoardCommands._handle_sync(args, _Failing({}), self._Config())

        out = capsys.readouterr().out
        assert rc == 1
        assert not cli_health_check._is_sync_refusal(out), out
