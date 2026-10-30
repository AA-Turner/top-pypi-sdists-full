"""`probe session delete|undelete <sid>` and the SDK under them (research-os 0411,
#3628): a researcher deletes one of their own captured sessions, undoable for 7
days.

The CLI is the researcher's alone (R24): refused before any request from inside
a coding agent's shell or by the Probe daemon, and it asks for the id's first 8
characters typed back after showing what it will delete.
"""

from __future__ import annotations

import importlib
import json

import httpx
import pytest
from typer.testing import CliRunner

from probe.cli.main import app as cli_app
from probe.daemon import precheck
from probe.sdk import agent_session

from tests.conftest import make_client

SID = "643ce138-4801-4409-b69c-ca30ab7605bc"
PURGE = "2026-11-05T12:00:00+00:00"


def _preview(state: str | None = None) -> dict:
    return {
        "session_id": SID, "agent": "claude_code", "state": state, "dry_run": state is None,
        "requested_at": None, "purge_after": PURGE, "can_undo": state == "pending",
        "cancelled_at": None, "erased_at": None,
        "first_seen_at": "2026-10-28T09:00:00+00:00", "last_seen_at": "2026-10-28T11:00:00+00:00",
        "note": "not deleted yet" if state is None else "hidden from search",
    }


def _server(app, tmp_path, monkeypatch, *, state: str | None = None):
    """A client whose server answers the deletion routes; the requests it saw."""
    seen: list[httpx.Request] = []
    real = app.handler

    def handler(request: httpx.Request) -> httpx.Response:
        path = request.url.path
        if path == f"/v1/sessions/{SID}" and request.method == "DELETE":
            seen.append(request)
            if request.url.params.get("dry_run") == "true":
                return httpx.Response(200, json=_preview(state))
            return httpx.Response(202, json={**_preview("pending"), "dry_run": False})
        if path == f"/v1/sessions/{SID}/undelete" and request.method == "POST":
            seen.append(request)
            return httpx.Response(200, json={**_preview("cancelled"), "dry_run": False})
        return real(request)

    app.handler = handler
    client = make_client(app, tmp_spool=tmp_path / "spool")
    monkeypatch.setattr(importlib.import_module("probe.cli.main"), "_client", lambda **_: client)
    monkeypatch.delenv(agent_session.DAEMON_SESSION_ENV, raising=False)
    return seen


def test_delete_shows_the_session_then_deletes_once_the_id_is_typed_back(
    app, tmp_path, monkeypatch
) -> None:
    seen = _server(app, tmp_path, monkeypatch)
    result = CliRunner().invoke(cli_app, ["session", "delete", SID], input=f"{SID[:8]}\n")
    assert result.exit_code == 0, result.output
    assert [(r.method, dict(r.url.params)) for r in seen] == [
        ("DELETE", {"dry_run": "true"}),
        ("DELETE", {}),
    ]
    # CliRunner echoes the typed input into stdout; a terminal echoes it itself.
    assert json.loads(result.stdout.strip().splitlines()[-1])["state"] == "pending"
    assert f"claude_code session {SID}" in result.stderr and "not deleted yet" in result.stderr
    assert f"Type {SID[:8]} to delete it" in result.stderr


def test_a_wrong_confirmation_deletes_nothing(app, tmp_path, monkeypatch) -> None:
    seen = _server(app, tmp_path, monkeypatch)
    result = CliRunner().invoke(cli_app, ["session", "delete", SID], input="yes\n")
    assert result.exit_code == 1
    assert "nothing changed" in result.stderr
    assert [dict(r.url.params) for r in seen] == [{"dry_run": "true"}], "only the preview"


def test_a_session_already_asked_for_prints_where_it_stands(app, tmp_path, monkeypatch) -> None:
    seen = _server(app, tmp_path, monkeypatch, state="pending")
    result = CliRunner().invoke(cli_app, ["session", "delete", SID])
    assert result.exit_code == 0, result.output
    assert json.loads(result.stdout)["state"] == "pending"
    assert len(seen) == 1, "no second request, no prompt"


def test_undelete_posts_and_prints_the_answer(app, tmp_path, monkeypatch) -> None:
    seen = _server(app, tmp_path, monkeypatch)
    result = CliRunner().invoke(cli_app, ["session", "undelete", SID])
    assert result.exit_code == 0, result.output
    assert json.loads(result.stdout)["state"] == "cancelled"
    assert [(r.method, r.url.path) for r in seen] == [("POST", f"/v1/sessions/{SID}/undelete")]


@pytest.mark.parametrize("verb", ["delete", "undelete"])
@pytest.mark.parametrize(
    "variable", ["CLAUDE_CODE_SESSION_ID", "CODEX_THREAD_ID", agent_session.DAEMON_SESSION_ENV]
)
def test_an_agents_shell_or_the_daemon_is_refused_before_any_request(
    app, tmp_path, monkeypatch, verb, variable
) -> None:
    seen = _server(app, tmp_path, monkeypatch)
    monkeypatch.setenv(variable, "0f8e1a52-7c1d-4a8e-9d43-5b2a1c3e4f60")
    result = CliRunner().invoke(cli_app, ["session", verb, SID], input=f"{SID[:8]}\n")
    assert result.exit_code == 2
    assert f"`probe session {verb}` was refused" in result.stderr
    assert seen == []


def test_both_are_the_researchers_never_the_daemons() -> None:
    assert precheck.OWNERS["session delete"] == precheck.RESEARCHER
    assert precheck.OWNERS["session undelete"] == precheck.RESEARCHER


def test_the_sdk_sends_a_dry_run_as_a_query_flag(app, tmp_path, monkeypatch) -> None:
    seen = _server(app, tmp_path, monkeypatch)
    client = importlib.import_module("probe.cli.main")._client()
    assert client.delete_session(SID, dry_run=True)["dry_run"] is True
    assert client.delete_session(SID)["state"] == "pending"
    assert [dict(r.url.params) for r in seen] == [{"dry_run": "true"}, {}]
