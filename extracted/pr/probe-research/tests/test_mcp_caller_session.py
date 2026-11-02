"""The hosted MCP searches AS its caller's coding-agent session (plan W4, O5).

`search_performed` names the session that searched, read off the request's
`X-Probe-Agent` / `X-Probe-Agent-Session`. Hosted, the SDK transport would put
THIS server process's own session there (it reads the pod's environment), so
the MCP binds its caller's validated pair around the `/v1/search` call
(`accounting.caller_session_scope`). The backend half -- the route reading
these headers, else the body's `exclude_agent_session` -- is
research-os `tests/unit/knowledge/search/test_search_caller_identity.py`, which builds its
requests from the same SDK constants.
"""

from __future__ import annotations

import uuid
from collections.abc import Iterator
from contextlib import contextmanager

import pytest

from probe.mcp.delivery import accounting
from probe.mcp.tools.tools import ResearchReadService
from probe.mcp.source.source import ResearchOSSource
from probe.sdk.delivery import transport as transport_mod
from probe.sdk.agent_session import AGENT_HEADER, AGENT_SESSION_HEADER
from tests.conftest import search_response

CALLER = str(uuid.uuid4())
OTHER = str(uuid.uuid4())
#: The session this PROCESS runs inside, when it runs inside one.
PROCESS = str(uuid.uuid4())


@contextmanager
def _hosted(agent: str | None = "claude_code", session: str | None = CALLER) -> Iterator[None]:
    """One hosted request's holder, bound exactly as `with_auth_and_health` binds it."""
    state = accounting.begin_request(agent, session, {})
    try:
        yield
    finally:
        accounting.end_request(state)


@pytest.fixture
def process_session(monkeypatch: pytest.MonkeyPatch) -> None:
    """This process sits inside a session of its own -- what the O5 review found
    the hosted transport would lend every caller."""
    monkeypatch.setattr(
        transport_mod.headers,
        "agent_session_headers",
        lambda env=None: {AGENT_HEADER: "codex", AGENT_SESSION_HEADER: PROCESS},
    )


def _search(app, client, **kwargs) -> tuple[dict, dict[str, str]]:
    app.search_response = search_response()
    ResearchReadService(ResearchOSSource(client)).search("dockq", **kwargs)
    request = [r for r in app.requests if r.url.path == "/v1/search"][-1]
    session = {
        name: request.headers[name]
        for name in (AGENT_HEADER, AGENT_SESSION_HEADER)
        if name in request.headers
    }
    return app.search_requests[-1], session


def test_a_hosted_search_names_the_callers_session(app, client, process_session) -> None:
    with _hosted():
        body, session = _search(app, client)
    assert session == {AGENT_HEADER: "claude_code", AGENT_SESSION_HEADER: CALLER}
    assert body["exclude_agent_session"] == CALLER


def test_an_explicit_exclusion_does_not_rename_the_caller(app, client, process_session) -> None:
    """`exclude_session` says which session to LEAVE OUT; the session that
    searched is still the caller's own."""
    with _hosted():
        body, session = _search(app, client, exclude_session=OTHER)
    assert session[AGENT_SESSION_HEADER] == CALLER
    assert body["exclude_agent_session"] == OTHER


def test_a_caller_with_no_session_header_borrows_none(app, client, process_session) -> None:
    """Codex connects before it has a thread id: no header. The search then
    names no session at all -- never this process's -- and the API falls back
    to the `exclude_session` its agent passed (CODEX_THREAD_ID)."""
    with _hosted(agent=None, session=None):
        body, session = _search(app, client, exclude_session=OTHER)
    assert session == {}
    assert body["exclude_agent_session"] == OTHER


def test_stdio_keeps_sending_its_own_session(app, client, process_session) -> None:
    """No hosted holder: the stdio MCP runs inside its caller's session and
    already sends it; nothing here changes that."""
    _, session = _search(app, client)
    assert session == {AGENT_HEADER: "codex", AGENT_SESSION_HEADER: PROCESS}


def test_only_the_search_call_speaks_for_the_caller(app, client, process_session) -> None:
    """The scope ends with the search: a later call in the same request sends
    what it always sent."""
    with _hosted():
        _search(app, client)
        client.transport.get("/v1/me")
    me = [r for r in app.requests if r.url.path == "/v1/me"][-1]
    assert me.headers.get(AGENT_SESSION_HEADER) == PROCESS
