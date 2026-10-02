"""The daemon removes ITS OWN links without asking (lineage plan L9, R9).

Every `edge remove` was held for the researcher (`delete.permanent`: an edge has
no trash), so the daemon could not revisit a link it made as the session went
on. Now it reads the edge first (`GET /v1/edges/{id}`): a link the server
stamped `meta.via = "daemon"` with `meta.by` = the user this daemon's key
answers to runs at once. Another researcher's daemon's link, a person's link,
and anything it cannot read -- an old server without the route included -- still
ask: FAIL CLOSED, like the cascade-delete check.
"""

from __future__ import annotations

import asyncio
import time

import httpx
import pytest

from probe.daemon import approvals as appr
from probe.daemon import lease, probe_api, tools
from probe.daemon.store import Store

SID = "11111111-2222-3333-4444-555555555555"
ME = "aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa"
COLLEAGUE = "bbbbbbbb-bbbb-4bbb-8bbb-bbbbbbbbbbbb"
EDGE_ID = "cccccccc-cccc-4ccc-8ccc-cccccccccccc"
REMOVE = ["edge", "remove", EDGE_ID]


@pytest.fixture(autouse=True)
def _state(tmp_path, monkeypatch):
    monkeypatch.setenv("XDG_STATE_HOME", str(tmp_path / "state"))
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path / "config"))
    monkeypatch.delenv("PROBE_AGENT", raising=False)
    monkeypatch.setattr(probe_api, "_features", None)


def _edge(meta: dict) -> dict:
    return {"id": EDGE_ID, "source_type": "run", "source_id": "r2", "relation": "derived_from",
            "target_type": "run", "target_id": "r1", "provenance": "inferred", "meta": meta}


def _probe(monkeypatch, routes: dict) -> list[str]:
    """A Probe that answers each (method, path) with (status, body); the trash on."""
    seen: list[str] = []
    routes = {("GET", "/v1/server/features"): (200, {"features": ["trash"]}),
              ("GET", "/v1/me"): (200, {"user_id": ME}), **routes}

    def handler(request: httpx.Request) -> httpx.Response:
        seen.append(f"{request.method} {request.url.path}")
        status, body = routes.get((request.method, request.url.path), (404, {"detail": "Not Found"}))
        return httpx.Response(status, json=body)

    async def client(env):
        return httpx.AsyncClient(base_url="http://probe.test", transport=httpx.MockTransport(handler))

    monkeypatch.setattr(probe_api, "_client", client)
    return seen


def _deps(tmp_path, monkeypatch, *, bypass=False) -> tuple[tools.Deps, list[list[str]]]:
    ran: list[list[str]] = []

    async def run(deps, argv, op_id, *, cwd=None):
        ran.append(list(argv))
        return tools.ProbeResult(0, "null")

    monkeypatch.setattr(tools, "run_probe_process", run)
    lease.sessions_dir().mkdir(parents=True, exist_ok=True)
    (lease.sessions_dir() / f"{SID}.state").write_text("daemon")
    assert lease.renew(SID)
    work = tmp_path / "work"
    work.mkdir(exist_ok=True)
    deps = tools.Deps(store=Store(tmp_path / "s.sqlite", clock=time.time), board=appr.Board(tmp_path / "appr"),
                      session_id=SID, cwd=work, workdirs=[work], home=tmp_path, write_dirs=[],
                      probe_env={"PROBE_BASE_URL": "http://probe.test", "PROBE_TOKEN": "k"}, bypass=bypass,
                      mode_known=True, bite_id=1, replay=None)
    return deps, ran


def _remove(deps) -> str:
    return asyncio.run(tools.run_probe_command(deps, REMOVE, why="the later events show B did not use A"))


def test_this_daemons_own_link_is_removed_without_a_question(tmp_path, monkeypatch):
    seen = _probe(monkeypatch, {("GET", f"/v1/edges/{EDGE_ID}"): (200, _edge({"via": "daemon", "by": ME}))})
    deps, ran = _deps(tmp_path, monkeypatch)
    out = _remove(deps)
    assert out.startswith("[exit 0]") and ran == [REMOVE], out
    assert deps.board.all() == []
    [row] = deps.store.db.execute("SELECT status, reason FROM writes")
    assert row["status"] == "ran"
    assert row["reason"] == "own link (L9): the later events show B did not use A"  # no question was asked
    assert f"GET /v1/edges/{EDGE_ID}" in seen and "GET /v1/me" in seen


def test_the_by_stamp_may_name_the_user_either_way(tmp_path, monkeypatch):
    _probe(monkeypatch, {("GET", f"/v1/edges/{EDGE_ID}"): (200, _edge({"via": "daemon", "by": f"user:{ME}"}))})
    deps, ran = _deps(tmp_path, monkeypatch)
    assert _remove(deps).startswith("[exit 0]") and ran == [REMOVE]


@pytest.mark.parametrize("answer", [
    (200, _edge({"via": "daemon", "by": COLLEAGUE})),  # another researcher's daemon (R9)
    (200, _edge({"via": "daemon"})),                    # a daemon link with no author
    (200, _edge({})),                                   # a person's link
    (200, _edge({"via": "daemon ", "by": ME})),         # not exactly the stamp
    (200, dict(_edge({"via": "daemon", "by": ME}), provenance="human")),  # the stamp sets `inferred` too
    (200, dict(_edge({"via": "daemon", "by": ME}), provenance=None)),
    (404, {"detail": "Not Found"}),                     # an old server: no such route
    (404, {"detail": "edge not found"}),
    (500, {"detail": "boom"}),
    (200, ["not", "an", "edge"]),
], ids=["colleague", "no-by", "person", "near-stamp", "human-provenance", "no-provenance", "old-server", "gone",
        "5xx", "shape"])
def test_anything_else_still_asks(tmp_path, monkeypatch, answer):
    _probe(monkeypatch, {("GET", f"/v1/edges/{EDGE_ID}"): answer})
    deps, ran = _deps(tmp_path, monkeypatch)
    out = _remove(deps)
    assert "held for the researcher" in out and ran == [], out
    [req] = deps.board.all()
    assert req.policy == "delete.permanent"


def test_who_this_daemon_is_unreadable_still_asks(tmp_path, monkeypatch):
    _probe(monkeypatch, {("GET", f"/v1/edges/{EDGE_ID}"): (200, _edge({"via": "daemon", "by": ME})),
                         ("GET", "/v1/me"): (503, {"detail": "down"})})
    deps, ran = _deps(tmp_path, monkeypatch)
    assert "held for the researcher" in _remove(deps) and ran == []


def test_no_answer_at_all_still_asks(tmp_path, monkeypatch):
    async def unreachable(env):
        def handler(request):
            if request.url.path == "/v1/server/features":
                return httpx.Response(200, json={"features": ["trash"]})
            raise httpx.ConnectError("connection refused")

        return httpx.AsyncClient(base_url="http://probe.test", transport=httpx.MockTransport(handler))

    monkeypatch.setattr(probe_api, "_client", unreachable)
    deps, ran = _deps(tmp_path, monkeypatch)
    assert "held for the researcher" in _remove(deps) and ran == []


def test_probe_refusing_the_key_on_the_edge_read_stops_the_bite(tmp_path, monkeypatch):
    _probe(monkeypatch, {("GET", f"/v1/edges/{EDGE_ID}"): (401, {"detail": "invalid token"})})
    deps, ran = _deps(tmp_path, monkeypatch)
    out = _remove(deps)
    assert ran == [] and deps.key_refused and deps.board.all() == [], out


def test_bypass_mode_reads_nothing_and_runs(tmp_path, monkeypatch):
    seen = _probe(monkeypatch, {})
    deps, ran = _deps(tmp_path, monkeypatch, bypass=True)
    assert appr.AUTO in _remove(deps) and ran == [REMOVE]
    assert not any(s.startswith("GET /v1/edges") for s in seen)


def test_only_edge_remove_is_exempt(tmp_path, monkeypatch):
    """A note, a paper, a view the daemon wrote still asks: only links carry the stamp."""
    _probe(monkeypatch, {("GET", f"/v1/edges/{EDGE_ID}"): (200, _edge({"via": "daemon", "by": ME}))})
    deps, ran = _deps(tmp_path, monkeypatch)
    out = asyncio.run(tools.run_probe_command(deps, ["paper", "remove", EDGE_ID]))
    assert "held for the researcher" in out and ran == []


def test_the_replay_bench_answers_through_its_own_hook(tmp_path):
    class Replay:
        def __init__(self, own):
            self.own, self.calls = own, []

        async def run(self, argv, op_id):
            self.calls.append(list(argv))
            return 0, "null"

        def server_features(self):
            return {"trash"}

        def edge_is_this_daemons(self, edge_id):
            return self.own

    class AsyncReplay(Replay):
        async def edge_is_this_daemons(self, edge_id):
            return self.own

    for kind, own, held in ((Replay, True, False), (Replay, False, True), (AsyncReplay, True, False),
                            (AsyncReplay, False, True), (Replay, "yes", True)):
        replay = kind(own)
        deps = tools.Deps(store=Store(tmp_path / f"{kind.__name__}{own}.sqlite", clock=time.time),
                          board=appr.Board(tmp_path / f"appr-{kind.__name__}{own}"), session_id="s", cwd=tmp_path,
                          workdirs=[tmp_path], home=tmp_path, write_dirs=[], probe_env={}, bypass=False,
                          mode_known=True, bite_id=1, replay=replay)
        out = asyncio.run(tools.run_probe_command(deps, REMOVE))
        assert ("held for the researcher" in out) is held and (replay.calls == []) is held, out
