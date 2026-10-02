"""The client half of the research-os version contract (plan (i)).

Two signals, both from the server, and both about THIS client being old:

* ``X-Probe-Client-Status: unsupported`` on any response -> ONE stderr line per
  process, never an error (the server refuses nothing by version, D14);
* a body ``code: "client_too_old"`` (a retired route's 410) ->
  ``ClientTooOldError``: raised where a caller waits (``probe.init``),
  permanent in the outbox. Keyed on the code, because the trash answers 410
  too and must stay an ordinary error.
"""

from __future__ import annotations

import httpx
import pytest

from probe.client_headers import client_headers_scope
from probe.sdk import client_status, errors
from probe.sdk.config import Settings
from probe.sdk.session_marker import WIZARD_HINT
from probe.sdk.journal import classify
from probe.sdk.transport import Transport
from tests.conftest import make_client

_UNSUPPORTED = {"X-Probe-Client-Status": "unsupported", "X-Probe-Min-Version": "0.177.0"}
_TOO_OLD = {
    "detail": "The /v1/experiments API is retired ... Upgrade to probe-research 0.177.0.",
    "code": "client_too_old",
    "min_version": "0.177.0",
}
_IN_TRASH = {"detail": "in_trash", "message": "This run is in the trash since ...", "kind": "run"}


@pytest.fixture(autouse=True)
def _fresh_notice():
    client_status._reset_for_tests()
    yield
    client_status._reset_for_tests()


def _transport(responses: list[httpx.Response], surface: str = "sdk") -> Transport:
    def handle(_request: httpx.Request) -> httpx.Response:
        return responses.pop(0)

    return Transport(
        Settings(base_url="http://test", token="test-token"),
        client=httpx.Client(base_url="http://test", transport=httpx.MockTransport(handle)),
        surface=surface,
        client_headers={"X-Probe-Client": surface, "X-Probe-Client-Version": "0.170.0"},
    )


def test_unsupported_prints_one_line_once(capsys) -> None:
    transport = _transport([httpx.Response(200, json={}, headers=_UNSUPPORTED) for _ in range(3)])
    for _ in range(3):
        transport.get("/v1/me")
    err = capsys.readouterr().err
    assert err.count("\n") == 1, err
    assert "0.170.0" in err and "0.177.0" in err and "pip install -U probe-research" in err


@pytest.mark.parametrize(
    ("surface", "command", "not_command"),
    [
        # `import probe` lives in the script's own environment.
        ("sdk", "`pip install -U probe-research`", WIZARD_HINT),
        # The CLI (and the local MCP server it runs) is a `uv tool` install, and
        # setup (updates included) is the wizard's alone.
        ("cli", WIZARD_HINT, "pip install"),
        ("mcp", WIZARD_HINT, "pip install"),
    ],
)
def test_the_upgrade_command_matches_how_it_was_installed(
    capsys, surface, command, not_command
) -> None:
    transport = _transport([httpx.Response(200, json={}, headers=_UNSUPPORTED)], surface)
    transport.get("/v1/me")
    err = capsys.readouterr().err
    assert command in err and not_command not in err, err


def test_the_line_also_rides_an_error_response(capsys) -> None:
    transport = _transport(
        [httpx.Response(404, json={"detail": "run not found"}, headers=_UNSUPPORTED)]
    )
    with pytest.raises(errors.NotFoundError):
        transport.get("/v1/runs/r-1")
    assert capsys.readouterr().err.count("\n") == 1


@pytest.mark.parametrize("status", ["ok", "update", None])
def test_anything_but_unsupported_is_silent(capsys, status) -> None:
    """The negative control: `update` is the banner's business, not a line on
    every script's stderr, and an absent header is "no opinion"."""
    headers = {"X-Probe-Client-Status": status} if status else {}
    transport = _transport([httpx.Response(200, json={}, headers=headers)])
    transport.get("/v1/me")
    assert capsys.readouterr().err == ""


def test_speaking_for_someone_else_is_silent(capsys) -> None:
    """The hosted MCP forwards its CALLER's version; the status grades that
    caller, and this process's stderr is the wrong place to say so."""
    transport = _transport([httpx.Response(200, json={}, headers=_UNSUPPORTED)])
    with client_headers_scope({"X-Probe-Client": "cli", "X-Probe-Client-Version": "0.100.0"}):
        transport.get("/v1/me")
    assert capsys.readouterr().err == ""


def test_a_hostile_min_version_is_not_echoed(capsys) -> None:
    hostile = {"X-Probe-Client-Status": "unsupported", "X-Probe-Min-Version": "1.0\x1b[2J"}
    transport = _transport([httpx.Response(200, json={}, headers=hostile)])
    transport.get("/v1/me")
    err = capsys.readouterr().err
    assert "\x1b" not in err and err.count("\n") == 1, err


def test_a_client_too_old_410_is_typed() -> None:
    transport = _transport([httpx.Response(410, json=_TOO_OLD)])
    with pytest.raises(errors.ClientTooOldError) as raised:
        transport.post("/v1/experiments", {"name": "x"})
    assert raised.value.min_version == "0.177.0"
    assert raised.value.status == 410
    assert "0.177.0" in str(raised.value)


def test_a_trash_410_is_not_client_too_old() -> None:
    """Same status, different meaning: keyed on the code, never the status."""
    transport = _transport([httpx.Response(410, json=_IN_TRASH)])
    with pytest.raises(errors.RosError) as raised:
        transport.post("/v1/runs/r-1/metrics", {"points": []})
    assert not isinstance(raised.value, errors.ClientTooOldError)
    assert "in the trash" in str(raised.value)


def test_client_too_old_is_permanent_in_the_outbox() -> None:
    """Resending the op can never land: dead-letter it, never park the queue.

    No branch of its own in `classify`: the generic "any other 4xx is permanent"
    rule already answers this, and this test is what keeps it answered.
    """
    exc = errors.ClientTooOldError("retired", status=410, min_version="0.177.0")
    assert classify(exc) == "permanent"


def test_probe_init_raises_client_too_old(app, tmp_path) -> None:
    """Where a caller is waiting, the typed error reaches them as-is."""
    import probe

    fake = app.handler

    def handler(request: httpx.Request) -> httpx.Response:
        if request.method == "POST" and request.url.path == "/v1/runs":
            return httpx.Response(410, json=_TOO_OLD)
        return fake(request)

    app.handler = handler
    client = make_client(app, tmp_spool=tmp_path / "spool")
    with pytest.raises(errors.ClientTooOldError) as raised:
        probe.init(client=client, description="x")
    assert raised.value.min_version == "0.177.0"
