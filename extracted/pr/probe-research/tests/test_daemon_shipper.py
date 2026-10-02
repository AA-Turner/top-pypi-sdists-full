"""The trace shipper (`probe/daemon/shipper.py`): the file is the queue, the
cursor moves only on 202, nothing blocks a bite, orphans drain, huge lines go."""

from __future__ import annotations

import asyncio
import fcntl
import json
import time
from pathlib import Path
from typing import Any

import pytest

from probe.daemon import shipper as ship
from probe.daemon import store as store_mod
from probe.daemon import trace as trace_mod

SID = "11111111-2222-3333-4444-555555555555"
OTHER = "99999999-2222-3333-4444-555555555555"


@pytest.fixture(autouse=True)
def _state(tmp_path, monkeypatch):
    monkeypatch.setenv("XDG_STATE_HOME", str(tmp_path / "state"))
    monkeypatch.delenv(ship.ENV_UPLOAD, raising=False)


class Server:
    """What `POST /v1/companion/traces` answers, and everything it was sent."""

    def __init__(self, *answers: tuple[int, Any]) -> None:
        self.answers = list(answers) or [(202, {"received": 0, "sent": 0, "dark": False})]
        self.bodies: list[dict[str, Any]] = []
        self.delay = 0.0

    async def __call__(self, url: str, body: dict[str, Any], headers: dict[str, str]) -> tuple[int, Any]:
        assert url.endswith(ship.ROUTE) and headers["Authorization"] == "Bearer k"
        await asyncio.sleep(self.delay)
        self.bodies.append(body)
        return self.answers.pop(0) if len(self.answers) > 1 else self.answers[0]

    @property
    def lines(self) -> list[dict[str, Any]]:
        return [item for body in self.bodies for item in body["lines"]]


def _trace(session: str = SID, n: int = 3, agent: str = "writer") -> Path:
    trace = trace_mod.TraceFile(session, agent)
    trace.start_run(1, trigger="turn end")
    for i in range(n - 1):
        trace.write({"type": "call", "round": i + 1, "input": [{"part_kind": "user-prompt", "content": f"q{i}"}]})
    return trace.path


def _stamp(folder: Path, base_url: str, key: str) -> None:
    """What `shipper.bind` wrote when the folder's worker started."""
    (folder / ship.META).write_text(json.dumps({"base_url": base_url, "key": ship._key_id(key)}))


def _shipper(server: Server, clock=time.monotonic, *, stamp: bool = True) -> ship.Shipper:
    """A shipper whose server and key recorded every folder there is now."""
    shipper = ship.Shipper(SID, base_url="https://api.example", key="k", post=server, clock=clock)
    if stamp and trace_mod.sessions_dir().exists():
        for folder in trace_mod.sessions_dir().iterdir():
            _stamp(folder, "https://api.example", "k")
    return shipper


def test_complete_lines_go_with_their_offsets_and_the_cursor_moves_on_202():
    path = _trace()
    server = Server()
    assert asyncio.run(_shipper(server).ship_once()) == 3
    raw = path.read_bytes().splitlines(keepends=True)
    offsets = [sum(len(r) for r in raw[:i]) for i in range(len(raw))]
    assert [item["offset"] for item in server.lines] == offsets
    assert [item["line"]["type"] for item in server.lines] == ["run_start", "call", "call"]
    assert server.bodies[0]["session_id"] == SID and server.bodies[0]["agent"] == "writer"
    assert ship.read_cursor(path) == path.stat().st_size
    assert asyncio.run(_shipper(server).ship_once()) == 0, "nothing new: nothing sent"
    assert len(server.bodies) == 1


def test_a_partial_last_line_waits_for_its_end_and_junk_is_stepped_over(tmp_path):
    path = _trace(n=1)
    with path.open("ab") as handle:
        handle.write(b"not json\n[1, 2]\n{\"type\": \"call\", \"ro")
    server = Server()
    asyncio.run(_shipper(server).ship_once())
    assert [item["line"]["type"] for item in server.lines] == ["run_start"]
    cursor = ship.read_cursor(path)
    assert path.read_bytes()[cursor:] == b"{\"type\": \"call\", \"ro", "the partial line is next"
    with path.open("ab") as handle:
        handle.write(b"und\": 1}\n")
    asyncio.run(_shipper(server).ship_once())
    assert server.lines[-1]["line"] == {"type": "call", "round": 1}


def test_a_refused_batch_keeps_the_cursor_and_backs_off():
    path = _trace()
    now = [1000.0]
    server = Server((503, None))
    shipper = _shipper(server, clock=lambda: now[0])
    assert asyncio.run(shipper.ship_once()) == 0
    assert ship.read_cursor(path) == 0 and shipper.wait_until == 1000.0 + ship.BACKOFF_MIN_S
    assert asyncio.run(shipper.ship_once()) == 0 and len(server.bodies) == 1, "waiting: no call"
    now[0] += ship.BACKOFF_MIN_S
    server.answers = [(202, {"dark": False})]
    assert asyncio.run(shipper.ship_once()) == 3 and ship.read_cursor(path) == path.stat().st_size


@pytest.mark.parametrize("answer", [(202, {"dark": True}), (404, None), (401, None), (403, None),
                                    (422, {"detail": [{"loc": ["body", "lines"], "msg": "unknown shape"}]})])
def test_dark_or_refused_waits_an_hour_and_keeps_the_lines(answer):
    path = _trace()
    now = [0.0]
    shipper = _shipper(Server(answer), clock=lambda: now[0])
    asyncio.run(shipper.ship_once())
    assert ship.read_cursor(path) == 0 and shipper.wait_until == ship.LONG_WAIT_S


def test_batches_stay_under_the_limit(monkeypatch):
    monkeypatch.setattr(ship, "BATCH_BYTES", 400)
    path = _trace(n=12)
    server = Server()
    asyncio.run(_shipper(server).ship_once())
    assert len(server.bodies) > 1
    for body in server.bodies:
        assert sum(len(json.dumps(i["line"])) for i in body["lines"]) <= 400 or len(body["lines"]) == 1
    assert ship.read_cursor(path) == path.stat().st_size


def test_a_huge_call_line_keeps_its_shape_and_numbers_when_trimmed():
    trace = trace_mod.TraceFile(SID, "writer")
    trace.start_run(1)
    trace.write({"type": "call", "round": 1, "input": [{"part_kind": "user-prompt", "content": "\u4e2d" * 600_000}],
                 "output": {"parts": [{"part_kind": "text", "content": "ok"}], "model_name": "m",
                            "usage": {"input_tokens": 5, "output_tokens": 1}}})
    server = Server()
    asyncio.run(_shipper(server).ship_once())
    call = server.lines[-1]["line"]
    assert ship._size(call) <= ship.LINE_MAX_BYTES and call["trace_truncated"] is True
    assert isinstance(call["input"], list) and call["input"][0]["part_kind"] == "user-prompt"
    assert call["output"]["usage"] == {"input_tokens": 5, "output_tokens": 1} and call["output"]["model_name"] == "m"
    assert ship._size(call) > ship.LINE_MAX_BYTES * 0.7, "most of the room is used"


@pytest.mark.parametrize("key, value", [("args", {"q": '"' * 1_500_000}), ("result", "x" * 3_000_000)])
def test_no_single_field_can_keep_a_line_over_the_limit(key, value):
    out = ship.fit_line({"type": "tool", "call_id": "c1", key: value})
    assert ship._size(out) <= ship.LINE_MAX_BYTES and out["call_id"] == "c1"


def test_a_line_with_nan_is_sent_as_json_with_null():
    path = _trace(n=1)
    with path.open("ab") as handle:
        handle.write(b'{"type": "tool", "round": 1, "result": {"loss": NaN}}\n')
    server = Server()
    asyncio.run(_shipper(server).ship_once())
    assert server.lines[-1]["line"]["result"] == {"loss": None}
    json.dumps(server.bodies[-1], allow_nan=False)


def test_a_batch_the_server_refuses_is_split_and_a_line_refused_alone_is_skipped():
    path = _trace(n=4)

    class Picky(Server):
        async def __call__(self, url, body, headers):
            if any(item["line"].get("round") == 2 for item in body["lines"]):
                self.refused = getattr(self, "refused", 0) + 1
                return 422, {"detail": {"code": ship.REJECTED_CODE}}
            return await super().__call__(url, body, headers)

    server = Picky()
    asyncio.run(_shipper(server).ship_once())
    assert [item["line"].get("round") for item in server.lines] == [None, 1, 3]
    assert ship.read_cursor(path) == path.stat().st_size, "the refused line never blocks the file"


def test_a_folder_recorded_under_another_server_or_key_never_ships():
    _trace(session=OTHER)
    _trace()
    server = Server()
    shipper = _shipper(server, stamp=False)
    _stamp(trace_mod.session_dir(SID), "https://api.example", "k")
    _stamp(trace_mod.session_dir(OTHER), "https://selfhost.example", "other-key")
    asyncio.run(shipper.ship_once())
    assert {body["session_id"] for body in server.bodies} == {SID}
    unstamped = trace_mod.session_dir("22222222-2222-3333-4444-555555555555")
    unstamped.mkdir(parents=True)
    assert not shipper.bound_here(unstamped), "an unstamped folder is nobody's to send"


def test_start_runs_a_shipper_on_the_real_client_and_stamps_the_folder(monkeypatch, tmp_path):
    monkeypatch.setenv("PROBE_CONFIG_PATH", str(tmp_path / "none.json"))
    monkeypatch.setenv("PROBE_DAEMON_KEY", "k")
    monkeypatch.setenv("PROBE_BASE_URL", "https://api.example")

    async def go():
        ship.bind(SID, "https://api.example", "k")  # what the worker does first
        shipper = ship.start(SID)
        try:
            assert shipper is not None and shipper._post is ship._http_post and shipper._task is not None
            assert shipper.bound_here(trace_mod.session_dir(SID))
        finally:
            await shipper.stop(budget_s=0.1)

    asyncio.run(go())


def test_the_real_post_sends_json_and_reads_the_answer(monkeypatch):
    import httpx

    seen = {}

    def handler(request):
        seen["body"] = json.loads(request.content)
        seen["raw"] = request.content.decode("utf-8")
        seen["type"] = request.headers["content-type"]
        seen["auth"] = request.headers["authorization"]
        return httpx.Response(202, json={"received": 1, "sent": 1, "dark": False})

    real = httpx.AsyncClient

    def client(**kwargs):
        return real(transport=httpx.MockTransport(handler), **kwargs)

    monkeypatch.setattr(httpx, "AsyncClient", client)
    status, payload = asyncio.run(ship._http_post("https://api.example/v1/companion/traces",
                                                  {"session_id": SID, "agent": "writer",
                                                   "lines": [{"offset": 0, "line": {"text": "é"}}]},
                                                  {"Authorization": "Bearer k"}))
    assert status == 202 and payload["sent"] == 1 and seen["auth"] == "Bearer k"
    assert seen["body"]["session_id"] == SID and seen["type"] == "application/json"
    assert "é" in seen["raw"], "sent as UTF-8, the way its size was measured"


def test_a_huge_line_is_trimmed_before_it_goes_and_the_file_keeps_it():
    trace = trace_mod.TraceFile(SID, "writer")
    trace.start_run(1)
    trace.write({"type": "tool", "round": 1, "call_id": "c1", "args": {"path": "x"}, "result": "R" * 2_000_000})
    server = Server()
    asyncio.run(_shipper(server).ship_once())
    tool = server.lines[-1]["line"]
    assert tool["trace_truncated"] is True and len(json.dumps(tool)) <= ship.LINE_MAX_BYTES
    assert tool["args"] == {"path": "x"} and tool["result"].startswith("RRR")
    assert "R" * 2_000_000 in trace.path.read_text(), "the local file keeps the whole line"


def test_another_sessions_unshipped_trace_drains_at_start_unless_its_worker_runs():
    other = _trace(session=OTHER)
    live = _trace(session="77777777-2222-3333-4444-555555555555")
    lock_path = store_mod.state_dir() / "77777777-2222-3333-4444-555555555555.lock"
    lock_path.parent.mkdir(parents=True, exist_ok=True)
    held = lock_path.open("a")
    fcntl.flock(held.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
    try:
        _trace()
        server = Server()
        asyncio.run(_shipper(server).ship_once())
    finally:
        held.close()
    sessions = {body["session_id"] for body in server.bodies}
    assert sessions == {SID, OTHER}
    assert ship.read_cursor(other) == other.stat().st_size and ship.read_cursor(live) == 0


def test_a_slow_upload_never_holds_up_the_worker_and_stop_is_bounded():
    _trace()
    server = Server()
    server.delay = 30.0

    async def go() -> float:
        shipper = _shipper(server)
        shipper.start()
        await asyncio.sleep(0.05)
        started = time.monotonic()
        await asyncio.sleep(0.01)  # the worker's own work runs meanwhile
        await shipper.stop(budget_s=0.2)
        return time.monotonic() - started

    assert asyncio.run(go()) < 1.0


def test_no_shipper_without_a_key_or_when_turned_off(monkeypatch, tmp_path):
    monkeypatch.setenv("PROBE_CONFIG_PATH", str(tmp_path / "none.json"))
    monkeypatch.delenv("PROBE_DAEMON_KEY", raising=False)
    assert ship.start(SID) is None
    monkeypatch.setenv(ship.ENV_UPLOAD, "off")
    monkeypatch.setenv("PROBE_DAEMON_KEY", "k")
    assert ship.start(SID) is None


def test_a_folder_is_bound_only_while_empty_uploads_on_or_off(monkeypatch):
    monkeypatch.setenv(ship.ENV_UPLOAD, "off")
    ship.bind(SID, "https://api.example", "k")
    shipper = ship.Shipper(SID, base_url="https://api.example", key="k", post=Server())
    assert shipper.bound_here(trace_mod.session_dir(SID)), "bound at the start, whatever the upload switch"
    _trace(session=OTHER)
    ship.bind(OTHER, "https://api.example", "k")
    assert not shipper.bound_here(trace_mod.session_dir(OTHER)), "traces of unknown origin are never adopted"


def test_orphan_recovery_carries_on_after_an_outage():
    _trace(session=OTHER)
    now = [0.0]
    server = Server((503, None))
    shipper = _shipper(server, clock=lambda: now[0])
    asyncio.run(shipper.ship_once())
    assert shipper.drained_others is False, "an orphan left behind is tried again"
    now[0] += ship.BACKOFF_MAX_S
    server.answers = [(202, {"dark": False})]
    asyncio.run(shipper.ship_once())
    assert shipper.drained_others is True
    assert ship.read_cursor(trace_mod.session_dir(OTHER) / "writer.jsonl") > 0


def test_a_session_resumed_under_another_account_leaves_its_folder_local_for_good():
    assert ship.bind(SID, "https://api.example", "key-a") is True
    assert ship.bind(SID, "https://api.example", "key-a") is True, "the same account resumes"
    assert ship.bind(SID, "https://api.example", "key-b") is False, "another account's lines would mix in"
    assert ship.bind(SID, "https://api.example", "key-a") is False, "mixed now: not even the first account ships it"
    _trace()
    server = Server()
    shipper = ship.Shipper(SID, base_url="https://api.example", key="key-a", post=server)
    asyncio.run(shipper.ship_once())
    assert server.bodies == [] and trace_mod.session_dir(SID).joinpath("writer.jsonl").exists()


def test_one_broken_folder_never_stops_the_others_or_the_sessions_own(monkeypatch):
    _trace(session=OTHER)
    _trace(session="77777777-2222-3333-4444-555555555555")
    _trace()
    server = Server()
    shipper = _shipper(server)
    real = shipper.ship_folder

    async def flaky(folder, session, **kwargs):
        if session == OTHER:
            raise PermissionError("unreadable")
        return await real(folder, session, **kwargs)

    monkeypatch.setattr(shipper, "ship_folder", flaky)
    asyncio.run(shipper.ship_once())
    assert {body["session_id"] for body in server.bodies} == {SID, "77777777-2222-3333-4444-555555555555"}
    assert shipper.drained_others is False, "the broken one is tried again later"


def test_a_partial_last_line_is_not_behind(tmp_path):
    path = _trace()
    shipper = _shipper(Server())
    asyncio.run(shipper.ship_once())
    with path.open("a") as handle:
        handle.write('{"type": "call", "rou')
    assert not shipper._behind(path.parent), "still being written: nothing to catch up"
    with path.open("a") as handle:
        handle.write('nd": 9}\n')
    assert shipper._behind(path.parent)
