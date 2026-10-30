"""Run alerts reach the agent through the daemon (run-alerts-to-agent, PR 2, D1-D2).

The worker's run-alert poller (`probe.daemon.run_alerts`) asks the server for the
session's alerts every RUN_ALERT_POLL_S on its own asyncio task, and hands what
is new to the mailbox as ONE `alert` message per poll: published first, then
recorded. The server is never reached here: `probe_api.run_alerts` runs against
an httpx MockTransport, and the lane against a fake of it.
"""

from __future__ import annotations

import asyncio
import json
import os
import shutil
import time
from pathlib import Path

import httpx
import pytest

# The worker imports the daemon's model harness (the `daemon` extra), as in
# test_daemon_worker.py; agent-ci installs the package without it.
pytest.importorskip("pydantic_ai")

from probe.daemon import lease, mailbox, probe_api  # noqa: E402
from probe.daemon import reader_lane as rl  # noqa: E402
from probe.daemon import run_alerts as ra  # noqa: E402
from probe.daemon import worker as worker_mod  # noqa: E402
from probe.daemon.events import READER_STREAM  # noqa: E402

SID = "11111111-2222-3333-4444-555555555555"
LATER = "2099-01-01T00:00:00Z"
ENV = {"PROBE_TOKEN": "pk_test", "PROBE_BASE_URL": "http://probe.test", "PROBE_DAEMON_SESSION": SID}


def _line(obj: dict) -> str:
    return json.dumps(obj) + "\n"


@pytest.fixture(autouse=True)
def _isolated(tmp_path, monkeypatch):
    """No real config (so no real key), no MCP, the state under tmp."""
    monkeypatch.setenv("PROBE_CONFIG_PATH", str(tmp_path / "no-config.json"))
    monkeypatch.delenv("PROBE_DAEMON_KEY", raising=False)
    monkeypatch.setenv("PROBE_DAEMON_MCP", "0")
    monkeypatch.delenv(mailbox.ENV_READS, raising=False)
    monkeypatch.setenv("XDG_STATE_HOME", str(tmp_path / "state"))
    (tmp_path / "state" / "probe" / "sessions").mkdir(parents=True)
    _set_state("daemon")


def _set_state(state: str) -> None:
    """The session's switch; `read-only` counts only in a daemon-profile session."""
    (lease.sessions_dir() / f"{SID}.state").write_text(state)
    (lease.sessions_dir() / f"{SID}.profile").write_text("daemon")


def _worker(tmp_path: Path) -> worker_mod.Worker:
    work = tmp_path / "home" / "work"
    work.mkdir(parents=True, exist_ok=True)
    transcript = tmp_path / f"{SID}.jsonl"
    if not transcript.exists():
        transcript.write_text(_line({"type": "user", "message": {"content": "train the digits SVM"},
                                     "cwd": str(work), "timestamp": LATER}))
    return worker_mod.Worker(worker_mod.Session(SID, transcript, work, "claude_code", home=tmp_path / "home"))


def _alert(n: int, *, kind: str = "still_running") -> dict:
    return {"id": n, "run_id": f"00000000-0000-0000-0000-{n:012d}", "kind": kind,
            "text": f"digits-svm-{n} (digits-svm-{n}) is still running. loss went to 9.1 at step {n}00.",
            "created_at": "2026-10-13T12:00:00Z"}


def _alerts_waiting() -> list[mailbox.Message]:
    return [m for _, m in mailbox.waiting(SID) if m.kind == mailbox.Kind.ALERT]


# ---------------------------------------------------------------------------
# The message.
# ---------------------------------------------------------------------------


def test_a_sixty_run_incident_is_one_message_listing_ten_and_how_many_more(tmp_path):
    lane = ra.RunAlertLane(_worker(tmp_path))
    msg = lane.hand_over([_alert(n) for n in range(1, 61)])
    assert [m.id for m in _alerts_waiting()] == [msg.id]
    lines = msg.rendered().split("\n")
    assert lines[0] == "[Probe] Run alert"
    assert lines[1:11] == [_alert(n)["text"] for n in range(1, 11)]
    assert lines[11:] == ["and 50 more runs."]
    assert msg.alerts == list(range(1, 61)), "every id is the message's, listed or not"
    assert lane.store.delivered_run_alerts(list(range(1, 61))) == set(range(1, 61))


def test_one_more_is_one_more_run_and_a_short_batch_has_no_tail():
    eleven = ra.alert_message(SID, ra.usable([_alert(n) for n in range(1, 12)]), made_at=1.0)
    assert eleven.text.split("\n")[-1] == "and 1 more run."
    three = ra.alert_message(SID, ra.usable([_alert(n) for n in (3, 1, 2)]), made_at=1.0)
    assert three.text == "\n".join(_alert(n)["text"] for n in (1, 2, 3)), "oldest first, nothing after"


def test_the_message_is_kept_and_waits_half_a_day():
    msg = ra.alert_message(SID, ra.usable([_alert(1)]), made_at=1000.0)
    assert (msg.kind, msg.keep) == (mailbox.Kind.ALERT, True)
    mailbox.publish(msg)
    ((_, waiting),) = mailbox.waiting(SID, now=1000.0)
    assert waiting.expires_at == 1000.0 + mailbox.ALERT_TTL_S == 1000.0 + 12 * 3600


def test_only_whole_alerts_are_sent_each_on_one_line():
    rows = [_alert(1), {"id": True, "text": "a bool is no id"}, {"id": "2", "text": "a string is no id"},
            {"id": 3}, {"id": 4, "text": "   "}, "not a row", {"id": 5, "text": "two\nlines\tand  gaps"},
            {"id": 6, "text": "x" * 900}, _alert(1)]
    got = ra.usable(rows)
    assert [i for i, _ in got] == [1, 5, 6]
    assert got[1][1] == "two lines and gaps"
    assert len(got[2][1]) == ra.ALERT_TEXT_CHARS and got[2][1].endswith("...")


# ---------------------------------------------------------------------------
# Dedupe and the crash-safe hand-off.
# ---------------------------------------------------------------------------


def test_an_alert_is_sent_once_however_often_the_server_lists_it(tmp_path):
    lane = ra.RunAlertLane(_worker(tmp_path))
    first = lane.hand_over([_alert(1), _alert(2)])
    assert lane.hand_over([_alert(1), _alert(2)]) is None, "the same two: nothing new"
    second = lane.hand_over([_alert(1), _alert(2), _alert(3)])
    assert second.alerts == [3] and second.text == _alert(3)["text"]
    assert [m.id for m in _alerts_waiting()] == [first.id, second.id]
    rows = lane.store.read_messages([first.id, second.id])
    assert {r["kind"] for r in rows.values()} == {mailbox.Kind.ALERT}
    assert lane.store.unpublished_read_messages() == [], "recorded as published: the reader never posts it again"


def test_the_message_id_is_the_batchs_and_never_names_a_dash():
    a = mailbox.alert_message_id([3, 1, 2])
    assert a == mailbox.alert_message_id([1, 2, 3]) != mailbox.alert_message_id([1, 2])
    assert a.startswith(mailbox.ALERT_ID_PREFIX) and "-" not in a


@pytest.mark.parametrize("claimed_first", [False, True])
def test_a_worker_that_died_between_publish_and_record_sends_nothing_twice(tmp_path, monkeypatch, claimed_first):
    """Published, then the store write failed (the worker died there). The next
    poll sees an unrecorded id, finds the message file -- still waiting, or
    already claimed by a hook -- and records it: the agent is told once."""
    lane = ra.RunAlertLane(_worker(tmp_path))
    real = lane._record

    def die(msg):
        raise RuntimeError("killed between the publish and the record")

    monkeypatch.setattr(lane, "_record", die)
    with pytest.raises(RuntimeError):
        lane.hand_over([_alert(1), _alert(2)])
    monkeypatch.setattr(lane, "_record", real)
    ((path, orphan),) = mailbox.waiting(SID)
    assert lane.store.delivered_run_alerts([1, 2]) == set()
    if claimed_first:
        assert mailbox.claim(SID, path, by="UserPromptSubmit") is not None

    # A new alert arrived meanwhile: the batch the server lists has grown.
    again = lane.hand_over([_alert(1), _alert(2), _alert(3)])
    assert again.alerts == [3], "1 and 2 went out in the first message"
    assert lane.store.delivered_run_alerts([1, 2, 3]) == {1, 2, 3}
    assert set(lane.store.read_messages([orphan.id, again.id])) == {orphan.id, again.id}
    assert lane.hand_over([_alert(1), _alert(2), _alert(3)]) is None
    waiting_ids = [m.id for m in _alerts_waiting()]
    assert waiting_ids == ([again.id] if claimed_first else [orphan.id, again.id])


def test_a_new_worker_records_an_orphan_before_any_new_alert(tmp_path, monkeypatch):
    """Recovery runs when the lane starts, not only when a new alert arrives: a
    session that hears of no further alert still gets the orphan recorded, so
    the writer reads the agent's claim of it (review of #2754)."""
    lane = ra.RunAlertLane(_worker(tmp_path))

    def die(msg):
        raise RuntimeError("killed between the publish and the record")

    monkeypatch.setattr(lane, "_record", die)
    with pytest.raises(RuntimeError):
        lane.hand_over([_alert(1), _alert(2)])

    fresh = ra.RunAlertLane(_worker(tmp_path))

    async def no_poll():
        return None

    monkeypatch.setattr(fresh, "tick", no_poll)

    async def start_and_stop():
        fresh.start()
        await asyncio.sleep(0.05)
        await fresh.stop()

    asyncio.run(start_and_stop())
    assert fresh.store.delivered_run_alerts([1, 2]) == {1, 2}


def test_the_writer_reads_the_agents_claim_of_an_alert(tmp_path):
    w = _worker(tmp_path)
    msg = ra.RunAlertLane(w).hand_over([_alert(7, kind="crashed")])
    ((path, _),) = mailbox.waiting(SID)
    mailbox.claim(SID, path, by="Stop")
    w.read_new()
    texts = [ev.text for ev in w.store.events_between(1) if ev.stream == READER_STREAM]
    assert texts == [msg.rendered()]


# ---------------------------------------------------------------------------
# Asking the server: quiet on everything but an answer.
# ---------------------------------------------------------------------------


def _serve(monkeypatch, handler) -> list[httpx.Request]:
    seen: list[httpx.Request] = []

    def record(request: httpx.Request) -> httpx.Response:
        seen.append(request)
        return handler(request)

    async def client(env):
        return httpx.AsyncClient(base_url="http://probe.test", transport=httpx.MockTransport(record))

    monkeypatch.setattr(probe_api, "_client", client)
    return seen


def test_the_poll_reads_the_sessions_alerts(monkeypatch):
    seen = _serve(monkeypatch, lambda r: httpx.Response(200, json={"alerts": [_alert(1), "junk"]}))
    assert asyncio.run(probe_api.run_alerts(ENV, SID)) == [_alert(1)]
    assert [(r.method, r.url.path) for r in seen] == [("GET", f"/v1/sessions/{SID}/run-alerts")]


@pytest.mark.parametrize("answer", [
    lambda r: httpx.Response(404, json={"detail": "Not Found"}),  # a server from before the route
    lambda r: httpx.Response(422, json={"detail": "malformed session id"}),
    lambda r: httpx.Response(500, text="boom"),
    lambda r: httpx.Response(503, text="deploying"),
    lambda r: httpx.Response(200, text="not json"),
    lambda r: httpx.Response(200, json={"alerts": "not a list"}),
    lambda r: httpx.Response(200, json=[1, 2]),
])
def test_anything_but_a_listing_is_no_answer(monkeypatch, answer):
    _serve(monkeypatch, answer)
    assert asyncio.run(probe_api.run_alerts(ENV, SID)) is None


@pytest.mark.parametrize("error", [httpx.ConnectError("refused"), httpx.ReadTimeout("slow")])
def test_no_network_is_no_answer(monkeypatch, error):
    def fail(request):
        raise error

    _serve(monkeypatch, fail)
    assert asyncio.run(probe_api.run_alerts(ENV, SID)) is None


def test_a_refused_key_raises_as_every_daemon_read_does(monkeypatch):
    _serve(monkeypatch, lambda r: httpx.Response(401, json={"detail": "invalid token"}))
    with pytest.raises(probe_api.KeyRefused):
        asyncio.run(probe_api.run_alerts(ENV, SID))


def test_a_poll_with_no_answer_or_a_refused_key_never_raises_into_the_worker(tmp_path, monkeypatch):
    lane = ra.RunAlertLane(_worker(tmp_path))
    monkeypatch.setattr(worker_mod, "probe_env", lambda sid: dict(ENV))
    _serve(monkeypatch, lambda r: httpx.Response(503, text="deploying"))
    assert asyncio.run(lane.tick()) is None and _alerts_waiting() == []

    seen = _serve(monkeypatch, lambda r: httpx.Response(401, json={"detail": "invalid token"}))
    assert asyncio.run(lane.tick()) is None
    assert lane.next_poll_at > lane.clock() + ra.RUN_ALERT_REFUSED_WAIT_S - 5
    assert asyncio.run(lane.tick()) is None
    assert len(seen) == 1, "a refused key waits before it is tried again"

    lane.next_poll_at = 0.0
    _serve(monkeypatch, lambda r: httpx.Response(200, json={"alerts": [_alert(4)]}))
    assert asyncio.run(lane.tick()).alerts == [4]


def test_no_key_no_request(tmp_path, monkeypatch):
    lane = ra.RunAlertLane(_worker(tmp_path))
    seen = _serve(monkeypatch, lambda r: httpx.Response(200, json={"alerts": [_alert(1)]}))
    assert asyncio.run(lane.tick()) is None  # no config: the wizard never paired a key
    assert seen == []


# ---------------------------------------------------------------------------
# The lane in the worker.
# ---------------------------------------------------------------------------


def _no_reader(monkeypatch) -> None:
    """The reader starts beside the poller; its model is not this file's subject."""
    async def stop(self):
        return None

    monkeypatch.setattr(rl.ReaderLane, "start", lambda self: None)
    monkeypatch.setattr(rl.ReaderLane, "stop", stop)


@pytest.mark.parametrize("state,polls", [("daemon", True), ("read-only", True), ("off", False)])
def test_the_poller_runs_beside_a_bite_in_on_and_read_only(tmp_path, monkeypatch, state, polls):
    """Its own task: `tick` stands in for a bite that never ends (and for the
    read-only tick that returns early), and the alert still goes out at once."""
    pytest.importorskip("pydantic_ai")  # the worker's loop makes the audit lane (the `daemon` extra)
    monkeypatch.setenv(mailbox.ENV_READS, "on")
    _no_reader(monkeypatch)
    _set_state(state)
    asked: list[str] = []

    async def fake(env, session_id):
        asked.append(session_id)
        return [_alert(9)]

    monkeypatch.setattr(probe_api, "run_alerts", fake)
    monkeypatch.setattr(worker_mod, "probe_env", lambda sid: dict(ENV))
    monkeypatch.setattr(worker_mod, "POLL_S", 0.01)
    w = _worker(tmp_path)
    bite_running = asyncio.Event()

    async def a_bite_that_never_ends():
        bite_running.set()
        await asyncio.sleep(3600)

    monkeypatch.setattr(w, "tick", a_bite_that_never_ends)

    async def run():
        task = asyncio.ensure_future(w.loop())
        await asyncio.wait_for(bite_running.wait(), 10)
        for _ in range(100):
            if _alerts_waiting():
                break
            await asyncio.sleep(0.02)
        lane = w.run_alerts
        task.cancel()
        try:
            await task
        except asyncio.CancelledError:
            pass
        return lane

    lane = asyncio.run(run())
    assert lane is not None and w.run_alerts is None, "started with the reader, stopped with the worker"
    assert [m.alerts for m in _alerts_waiting()] == ([[9]] if polls else [])
    assert asked == ([SID] if polls else []), "asked at start, then every RUN_ALERT_POLL_S"
    assert ra.RUN_ALERT_POLL_S == 30.0


def test_no_poller_without_the_mailbox(tmp_path, monkeypatch):
    """The daemon serves reads for this agent only on the daemon profile (or the
    developer switch): no mailbox, no alerts (decision 2: no daemon, no alert)."""
    pytest.importorskip("pydantic_ai")
    monkeypatch.setattr(worker_mod, "POLL_S", 0.01)
    w = _worker(tmp_path)
    ticks: list[int] = []

    async def tick():
        ticks.append(1)
        return None

    monkeypatch.setattr(w, "tick", tick)

    async def run():
        task = asyncio.ensure_future(w.loop())
        while len(ticks) < 5:
            await asyncio.sleep(0.01)
        started = w.run_alerts
        task.cancel()
        try:
            await task
        except asyncio.CancelledError:
            pass
        return started

    assert asyncio.run(run()) is None


def test_a_session_that_is_ending_polls_no_more(tmp_path, monkeypatch):
    lane = ra.RunAlertLane(_worker(tmp_path))

    async def never(env, session_id):
        raise AssertionError("asked after the session ended")

    monkeypatch.setattr(probe_api, "run_alerts", never)
    monkeypatch.setattr(worker_mod, "probe_env", lambda sid: dict(ENV))
    lane.w.stopping = True
    assert asyncio.run(lane.tick()) is None


# ---------------------------------------------------------------------------
# One poll for the machine: the Probe service's hand-off (plan Q2).
# ---------------------------------------------------------------------------


def _handoff(alerts: "list | None", *, age: float = 0.0, refused_until: "float | None" = None) -> None:
    """What `probe.service.alertpoll` leaves for the session's worker."""
    path = mailbox.alerts_handoff_path(SID)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps({"sid": SID, "polled_at": time.time() - age, "alerts": alerts,
                                "refused_until": refused_until, "pid": 1}))


def _offered(tmp_path) -> ra.RunAlertLane:
    lane = ra.RunAlertLane(_worker(tmp_path))
    mailbox.mark_worker_accepts(SID)  # the worker's start (`worker.main`)
    lane.offer()
    return lane


def _marker() -> dict:
    return json.loads(mailbox.worker_marker_path(SID).read_text())


def test_the_lane_offers_the_service_the_poll_with_the_config_it_reads_and_takes_it_back(tmp_path):
    lane = _offered(tmp_path)
    assert lane.offered == str(tmp_path / "no-config.json")
    assert _marker() == {"pid": os.getpid(), "requests": 1, "request_chars": mailbox.REQUEST_MAX_CHARS, "run_alerts": 1, "config": lane.offered}
    asyncio.run(lane.stop())
    assert lane.offered is None
    assert _marker() == {"pid": os.getpid(), "requests": 1, "request_chars": mailbox.REQUEST_MAX_CHARS}, "the offer goes, the marker stays"
    assert mailbox.accepts_requests(SID)


def test_a_worker_writes_its_lost_marker_again_at_its_next_poll(tmp_path):
    """#3616: an SDK's dead-run recovery deleted the whole `requests/` folder,
    marker included: `probe ask --writer` refused the live worker as one from
    before requests, and the service stopped polling its alerts. Its next poll
    writes the marker back as it was. A worker `run_session` did not start
    (a replay, a test's) writes none."""
    lane = _offered(tmp_path)
    w = lane.w
    w.run_alerts, before = lane, _marker()
    shutil.rmtree(mailbox.requests_dir(SID).parent)
    _set_state("off")  # the shortest poll: it ends the worker, after the mailbox
    assert asyncio.run(w.tick()) == 0
    assert not mailbox.worker_marker_path(SID).exists()
    w.marks_requests = True
    assert asyncio.run(w.tick()) == 0
    assert _marker() == before and mailbox.accepts_requests(SID)


@pytest.mark.parametrize("name", ["PROBE_DAEMON_KEY", "PROBE_BASE_URL"])
def test_a_worker_whose_key_or_endpoint_comes_from_its_environment_offers_nothing(tmp_path, monkeypatch, name):
    """The service starts with a clean environment: it would ask with another key."""
    monkeypatch.setenv(name, "https://staging.example.test" if name == "PROBE_BASE_URL" else "pk_env")
    lane = _offered(tmp_path)
    assert lane.offered is None and "run_alerts" not in _marker()


def test_the_services_answer_is_taken_without_asking_each_once(tmp_path, monkeypatch):
    lane = _offered(tmp_path)

    async def never(env, session_id):
        raise AssertionError("asked while the service polls for the session")

    monkeypatch.setattr(probe_api, "run_alerts", never)
    monkeypatch.setattr(worker_mod, "probe_env", lambda sid: dict(ENV))
    _handoff([_alert(1), _alert(2)])
    assert asyncio.run(lane.tick()).alerts == [1, 2]
    assert asyncio.run(lane.tick()) is None, "the same hand-off is taken once"
    time.sleep(0.01)
    _handoff([_alert(1), _alert(2), _alert(3)])
    assert asyncio.run(lane.tick()).alerts == [3], "deduped by id, as the lane's own poll is"
    time.sleep(0.01)
    _handoff(None, refused_until=time.time() + 300)
    assert asyncio.run(lane.tick()) is None, "the service holds back: so does the lane"
    assert [m.alerts for m in _alerts_waiting()] == [[1, 2], [3]]


@pytest.mark.parametrize("offered", [True, False])
def test_with_no_fresh_handoff_or_no_offer_the_lane_asks_itself(tmp_path, monkeypatch, offered):
    lane = _offered(tmp_path) if offered else ra.RunAlertLane(_worker(tmp_path))
    asked: list[str] = []

    async def fake(env, session_id):
        asked.append(session_id)
        return [_alert(5)]

    monkeypatch.setattr(probe_api, "run_alerts", fake)
    monkeypatch.setattr(worker_mod, "probe_env", lambda sid: dict(ENV))
    _handoff([_alert(4)], age=ra.HANDOFF_FRESH_S + 5 if offered else 0.0)
    assert asyncio.run(lane.tick()).alerts == [5]
    assert asked == [SID]


def test_a_new_handoff_cuts_the_lanes_wait_short(tmp_path, monkeypatch):
    monkeypatch.setattr(ra, "HANDOFF_CHECK_S", 0.05)
    lane = _offered(tmp_path)

    async def run() -> float:
        waiting = asyncio.ensure_future(lane.pause())
        await asyncio.sleep(0.3)
        assert not waiting.done(), "nothing new: it waits for the next poll"
        started = time.monotonic()
        _handoff([_alert(6)])
        await asyncio.wait_for(waiting, 5)
        return time.monotonic() - started

    assert asyncio.run(run()) < 1.0


def test_the_lane_looks_again_when_the_services_next_round_is_due(tmp_path, monkeypatch):
    """It sleeps until the last hand-off's `polled_at` plus the service's `every`
    (no stat in between), then takes the next one at once."""
    monkeypatch.setattr(ra, "HANDOFF_CHECK_S", 0.05)
    lane = _offered(tmp_path)
    path = mailbox.alerts_handoff_path(SID)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps({"sid": SID, "polled_at": time.time(), "alerts": [], "refused_until": None,
                                "every": 0.6, "pid": 1}))

    async def run() -> float:
        waiting = asyncio.ensure_future(lane.pause())
        await asyncio.sleep(0.7)
        started = time.monotonic()
        _handoff([_alert(7)])
        await asyncio.wait_for(waiting, 5)
        return time.monotonic() - started

    assert asyncio.run(run()) < 1.0

