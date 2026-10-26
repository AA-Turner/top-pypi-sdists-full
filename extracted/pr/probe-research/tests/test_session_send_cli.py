"""`probe session send <sid> "..."` and the SDK under it (swarm visibility G7): a
message to one of the researcher's own running sessions, which its Probe daemon
hands to the agent (`probe.daemon.session_messages`).
"""

from __future__ import annotations

import importlib
import json

import httpx
from typer.testing import CliRunner

from probe.cli.main import app as cli_app
from probe.daemon import precheck
from probe.sdk import session_marker
from probe.sdk.key_refusal import credential_refused

from tests.conftest import make_client

SID = "643ce138-4801-4409-b69c-ca30ab7605bc"


def _sending(app, tmp_path, answer):
    """A client whose server answers the send with `answer(request)`."""
    sent: list[httpx.Request] = []
    real = app.handler

    def handler(request: httpx.Request) -> httpx.Response:
        if request.url.path == f"/v1/sessions/{SID}/messages" and request.method == "POST":
            sent.append(request)
            return answer(request)
        return real(request)

    app.handler = handler
    return make_client(app, tmp_spool=tmp_path / "spool"), sent


def _queued(request: httpx.Request) -> httpx.Response:
    return httpx.Response(201, json={"id": "2d1c6e0e-1111-2222-3333-444455556666", "session_id": SID,
                                     "body": json.loads(request.content)["body"], "sender": "agent",
                                     "state": "queued", "reachable": True})


def test_send_posts_the_body_and_prints_the_answer(app, tmp_path, monkeypatch) -> None:
    client, sent = _sending(app, tmp_path, _queued)
    monkeypatch.setattr(importlib.import_module("probe.cli.main"), "_client", lambda **_: client)
    result = CliRunner().invoke(cli_app, ["session", "send", SID, "stop the lr=3e-3 run"])
    assert result.exit_code == 0, result.output
    assert json.loads(result.output)["state"] == "queued"
    (request,) = sent
    assert json.loads(request.content) == {"body": "stop the lr=3e-3 run"}


def test_a_refusal_is_the_cli_s_error_and_nothing_is_retried(app, tmp_path, monkeypatch) -> None:
    refusal = {"detail": {"code": "NOT_YOUR_SESSION", "message": (
        "Only the person whose session this is, and their own agent sessions, can message it.")}}
    client, sent = _sending(app, tmp_path, lambda r: httpx.Response(403, json=refusal))
    monkeypatch.setattr(importlib.import_module("probe.cli.main"), "_client", lambda **_: client)
    result = CliRunner().invoke(cli_app, ["session", "send", SID, "hi"])
    assert result.exit_code != 0
    assert "Only the person whose session this is" in str(result.exception)
    assert not credential_refused(403, str(result.exception)), "an owner refusal is no refused key"
    assert len(sent) == 1


def test_a_send_that_lost_its_answer_is_not_sent_twice(app, tmp_path, monkeypatch) -> None:
    client, sent = _sending(app, tmp_path, lambda r: httpx.Response(503, text="deploying"))
    monkeypatch.setattr(importlib.import_module("probe.cli.main"), "_client", lambda **_: client)
    assert CliRunner().invoke(cli_app, ["session", "send", SID, "hi"]).exit_code != 0
    assert len(sent) == 1, "a message is not idempotent: never retried"


def test_it_is_the_researchers_never_the_daemons_and_the_daemon_profile_agent_may_run_it() -> None:
    assert precheck.OWNERS["session send"] == precheck.RESEARCHER
    assert session_marker.classify_probe_args(["session", "send", SID, "x"])[0] is None
    assert session_marker.daemon_profile_allows(["session", "send", SID, "x"]) == (True, "probe session send")
