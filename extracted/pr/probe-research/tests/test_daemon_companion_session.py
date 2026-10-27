"""Every `/v1/companion/*` call names the session the daemon watches (swarm
visibility A20, D5).

The server settles each model-gateway call's dollars into the coding-agent
session named by `X-Probe-Agent` + `X-Probe-Agent-Session`
(`app/runs/agent_session.agent_session_from_request`), the pair the reader's
MCP calls already carry. The worker binds its session at start
(`model.bind_session`); the daemon's one HTTP client adds the pair to every
companion request (the chat gateway, the command check), and the
trace shipper sends it with the session's own traces -- never with another
session's orphans.
"""

from __future__ import annotations

import asyncio
import json
import threading

import httpx
import pytest

from probe.daemon import command_check, runctx
from probe.daemon import model as model_mod
from probe.daemon import shipper as ship
from probe.daemon import trace as trace_mod
# The real one: the suite's conftest stands a no-answer in for every test.
from probe.daemon.command_check import ask_probe as real_command_check
from probe.sdk.agent_session import AGENT_HEADER, AGENT_SESSION_HEADER

SID = "11111111-2222-3333-4444-555555555555"
OTHER = "99999999-2222-3333-4444-555555555555"
BASE = "https://api.example.test"


@pytest.fixture(autouse=True)
def _isolated(tmp_path, monkeypatch):
    monkeypatch.setenv("XDG_STATE_HOME", str(tmp_path / "state"))
    monkeypatch.setenv("PROBE_BASE_URL", BASE)
    monkeypatch.setenv(model_mod.ENV_KEY, "k")
    monkeypatch.delenv(ship.ENV_UPLOAD, raising=False)
    monkeypatch.setattr(model_mod, "_WATCHED", None)
    monkeypatch.setattr(model_mod, "_HTTP_CLIENT", None)
    monkeypatch.setattr(model_mod, "_PREFERRED_MODEL", None)


@pytest.fixture
def wire(monkeypatch):
    """The daemon's real HTTP client (its event hooks included) on a fake wire:
    every request it sends, and a 200 for each."""
    sent: list[httpx.Request] = []

    def answer(request: httpx.Request) -> httpx.Response:
        sent.append(request)
        if request.url.path.endswith("/command-check"):
            return httpx.Response(200, json={"approve": True, "scores": {"q": 0.9}, "mode": "on"})
        return httpx.Response(200, json={})

    monkeypatch.setattr(httpx, "AsyncHTTPTransport", lambda **_: httpx.MockTransport(answer))
    return sent


def _named(request: httpx.Request) -> tuple[str | None, str | None]:
    return request.headers.get(AGENT_HEADER), request.headers.get(AGENT_SESSION_HEADER)


def test_the_command_check_and_the_gateway_name_the_watched_session(wire):
    model_mod.bind_session("claude_code", SID)

    async def calls() -> None:
        await real_command_check(command="ls", cwd="/w", reason="look", working_folders=["/w"])
        await model_mod._http_client().post(f"{BASE}{model_mod.ROUTE_PREFIX}/chat/completions", json={})

    asyncio.run(calls())
    assert [r.url.path for r in wire] == [command_check.ROUTE, f"{model_mod.ROUTE_PREFIX}/chat/completions"]
    assert all(_named(r) == ("claude_code", SID) for r in wire)


def test_no_bound_session_names_none_and_other_routes_are_untouched(wire):
    async def calls() -> None:
        await model_mod._http_client().post(f"{BASE}{model_mod.ROUTE_PREFIX}/chat/completions", json={})
        model_mod.bind_session("codex", SID)
        await model_mod._http_client().get(f"{BASE}/v1/runs")

    asyncio.run(calls())
    assert [_named(r) for r in wire] == [(None, None), (None, None)]


@pytest.mark.parametrize(
    "agent,session",
    [
        ("claude_code", "short"),  # not a session id
        ("claude_code", "a b\r\nX-Evil: 1"),
        ("Claude Code", SID),  # not an agent label
        ("", SID),
        (None, SID),
        ("pi", None),
    ],
)
def test_a_malformed_pair_names_nothing(agent, session):
    model_mod.bind_session(agent, session)
    assert model_mod.session_headers() == {}


def test_a_session_the_caller_named_is_kept():
    model_mod.bind_session("claude_code", SID)
    request = httpx.Request(
        "POST", f"{BASE}{command_check.ROUTE}",
        headers={AGENT_HEADER: "pi", AGENT_SESSION_HEADER: OTHER},
    )
    asyncio.run(model_mod._name_watched_session(request))
    assert _named(request) == ("pi", OTHER)


def test_a_server_under_a_path_prefix_still_gets_the_pair():
    model_mod.bind_session("kimi_code", SID)
    request = httpx.Request("POST", f"https://self.host/api{model_mod.ROUTE_PREFIX}/chat/completions")
    asyncio.run(model_mod._name_watched_session(request))
    assert _named(request) == ("kimi_code", SID)


def test_each_hosted_run_names_its_own_session():
    """The daemon host runs several sessions in one process: each run's binding
    is its own (`runctx.Shared`), never the last one bound."""
    seen: dict[str, dict[str, str]] = {}
    ready = threading.Barrier(2)

    def run(sid: str, agent: str) -> None:
        with runctx.enter(runctx.Run(sid)):
            model_mod.bind_session(agent, sid)
            ready.wait(timeout=5)
            seen[sid] = model_mod.session_headers()

    threads = [threading.Thread(target=run, args=(SID, "claude_code")),
               threading.Thread(target=run, args=(OTHER, "codex"))]
    for t in threads:
        t.start()
    for t in threads:
        t.join(timeout=10)
    assert seen[SID] == {AGENT_HEADER: "claude_code", AGENT_SESSION_HEADER: SID}
    assert seen[OTHER] == {AGENT_HEADER: "codex", AGENT_SESSION_HEADER: OTHER}
    assert model_mod.session_headers() == {}, "outside a run: nothing bound"


def _trace(session: str) -> None:
    trace = trace_mod.TraceFile(session, "writer")
    trace.start_run(1, trigger="turn end")
    folder = trace_mod.session_dir(session)
    (folder / ship.META).write_text(json.dumps({"base_url": BASE, "key": ship._key_id("k")}))


def test_the_sessions_own_traces_name_it_and_an_orphans_do_not():
    _trace(SID)
    _trace(OTHER)
    model_mod.bind_session("claude_code", SID)
    posted: list[tuple[str, dict[str, str]]] = []

    async def post(url, body, headers):
        posted.append((body["session_id"], headers))
        return 202, {"dark": False}

    shipper = ship.Shipper(SID, base_url=BASE, key="k", post=post, session_headers=model_mod.session_headers())
    asyncio.run(shipper.ship_once())
    by_session = dict(posted)
    assert set(by_session) == {SID, OTHER}
    assert by_session[SID][AGENT_SESSION_HEADER] == SID and by_session[SID][AGENT_HEADER] == "claude_code"
    assert AGENT_SESSION_HEADER not in by_session[OTHER], "an orphan is another session's: never ours"
    assert all(h["Authorization"] == "Bearer k" for _, h in posted)


def test_the_shipper_the_worker_starts_carries_the_bound_session(monkeypatch):
    monkeypatch.setattr(trace_mod, "enabled", lambda: True)
    monkeypatch.setattr(ship.Shipper, "start", lambda self: None)
    model_mod.bind_session("pi", SID)
    started = ship.start(SID)
    assert started is not None
    assert started.session_headers == {AGENT_HEADER: "pi", AGENT_SESSION_HEADER: SID}
