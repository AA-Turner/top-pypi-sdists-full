"""Messages sent to the session through Probe reach its agent (swarm visibility G7).

The worker's run-alert lane also polls `GET /v1/sessions/{sid}/messages` on its
tick (`probe.daemon.session_messages`): each message not yet in the mailbox is
PUBLISHED first, then acked `acked`; once a hook has claimed it the poller acks
`delivered_to_agent`. The server is never reached: `probe_api` runs against an
httpx MockTransport, and the lane against a fake server holding the rows.
"""

from __future__ import annotations

import asyncio
import json
import os
import time
import uuid
from datetime import datetime
from pathlib import Path

import httpx
import pytest

# The worker imports the daemon's model harness (the `daemon` extra), as in
# test_daemon_run_alerts.py; agent-ci installs the package without it.
pytest.importorskip("pydantic_ai")

from probe._compat import UTC  # noqa: E402
from probe.daemon import lease, mailbox, probe_api  # noqa: E402
from probe.daemon import run_alerts as ra  # noqa: E402
from probe.daemon import session_messages as sm  # noqa: E402
from probe.daemon import worker as worker_mod  # noqa: E402

SID = "11111111-2222-3333-4444-555555555555"
LATER = "2099-01-01T00:00:00Z"
ENV = {"PROBE_TOKEN": "pk_test", "PROBE_BASE_URL": "http://probe.test", "PROBE_DAEMON_SESSION": SID}
MACHINE = "machine-a-" + "a" * 16


@pytest.fixture(autouse=True)
def _isolated(tmp_path, monkeypatch):
    monkeypatch.setenv("PROBE_CONFIG_PATH", str(tmp_path / "no-config.json"))
    monkeypatch.delenv("PROBE_DAEMON_KEY", raising=False)
    monkeypatch.setenv("PROBE_DAEMON_MCP", "0")
    monkeypatch.setenv(mailbox.SERVICE_ENV, "off")
    monkeypatch.delenv(mailbox.ENV_READS, raising=False)
    monkeypatch.setenv("XDG_STATE_HOME", str(tmp_path / "state"))
    (tmp_path / "state" / "probe" / "sessions").mkdir(parents=True)
    (lease.sessions_dir() / f"{SID}.state").write_text("daemon")
    (lease.sessions_dir() / f"{SID}.profile").write_text("daemon")
    monkeypatch.setattr(worker_mod, "probe_env", lambda sid: dict(ENV))


def _worker(tmp_path: Path) -> worker_mod.Worker:
    work = tmp_path / "home" / "work"
    work.mkdir(parents=True, exist_ok=True)
    transcript = tmp_path / f"{SID}.jsonl"
    if not transcript.exists():
        transcript.write_text(json.dumps({"type": "user", "message": {"content": "run the sweep"},
                                          "cwd": str(work), "timestamp": LATER}) + "\n")
    return worker_mod.Worker(worker_mod.Session(SID, transcript, work, "claude_code", home=tmp_path / "home"))


def _row(body: str = "stop the lr=3e-3 run", *, kind: str = "person", title: "str | None" = None,
         acked: bool = False) -> dict:
    return {"id": str(uuid.uuid4()), "body": body, "created_at": datetime.now(UTC).isoformat(),
            "acked_at": datetime.now(UTC).isoformat() if acked else None,
            "sender": {"kind": kind, "name": "Richard Wei", "session_title": title}}


class FakeProbe:
    """The four routes' behaviour the poller relies on: the poll lists every row
    not yet shown, whatever was acked; an ack is idempotent."""

    def __init__(self, monkeypatch, rows: "list[dict] | None" = None) -> None:
        self.rows = {r["id"]: dict(r) for r in rows or []}
        self.acks: list[tuple[str, str]] = []
        self.polls = 0
        self.instances: set[str] = set()
        self.fail_acks = False
        #: Another daemon of the session holds these (its ack is 409).
        self.lost: set[str] = set()
        monkeypatch.setattr(probe_api, "session_messages", self.poll)
        monkeypatch.setattr(probe_api, "ack_session_message", self.ack)

    async def poll(self, env, session_id, instance, held=None, active_at=None):
        self.polls += 1
        self.instances.add(instance)
        self.held = list(held or [])
        self.active_at = active_at
        rows = [{k: v for k, v in r.items() if k != "shown"} for r in self.rows.values() if not r.get("shown")]
        return {"messages": rows, "revoked": []}

    async def ack(self, env, session_id, message_id, state, instance, timeout=None):
        self.instances.add(instance)
        if self.fail_acks:
            return probe_api.AckResult.RETRY
        if message_id in self.lost:
            return probe_api.AckResult.LEASE_LOST
        self.acks.append((message_id, state))
        row = self.rows[message_id]
        row["acked_at"] = row.get("acked_at") or datetime.now(UTC).isoformat()
        if state == probe_api.ACK_DELIVERED_TO_AGENT:
            row["shown"] = True
        return probe_api.AckResult.RECORDED


def _inbox_waiting() -> list[mailbox.Message]:
    return [m for _, m in mailbox.waiting(SID) if m.from_inbox]


def _tick(lane: ra.RunAlertLane) -> int:
    lane.messages.next_poll_at = 0.0
    return asyncio.run(lane.messages.tick())


# ---------------------------------------------------------------------------
# The delivered text (approved 2026-10-25, ~/plans/swarm-visibility-gaps/PROPOSED-track-work.md).
# ---------------------------------------------------------------------------


def test_the_person_is_named_only_for_a_dashboard_message():
    person = {"kind": "person", "name": "Richard Wei"}
    assert sm.delivered_text(person, "ship it") == (
        "[Probe] Message from Richard Wei (dashboard): ship it")
    agent = {"kind": "agent", "name": "Richard Wei", "session_title": "Swarm orchestrator"}
    assert sm.delivered_text(agent, "ship it") == (
        '[Probe] Message from Richard Wei\'s agent session "Swarm orchestrator": ship it')
    assert sm.delivered_text({"kind": "agent", "name": "Richard Wei"}, "ship it") == (
        "[Probe] Message from Richard Wei's agent session: ship it")


@pytest.mark.parametrize("sender", [{"kind": "Person", "name": "R"}, {"kind": None, "name": "R"},
                                    {"name": "R"}, "person", None])
def test_anything_but_the_servers_person_reads_as_an_agent_session(sender):
    text = sm.delivered_text(sender, "x")
    assert text.startswith(mailbox.INBOX_PREFIX) and "'s agent session" in text and "(dashboard)" not in text


def test_a_long_or_quoted_title_is_cut_and_never_closes_the_label_early():
    text = sm.delivered_text({"kind": "agent", "name": "R", "session_title": 'say "hi"\nnow ' + "t" * 300}, "x")
    title = text.split('session "', 1)[1].split('": ', 1)[0]
    assert len(title) == sm.TITLE_MAX_CHARS and title.endswith("...") and '"' not in title and "\n" not in title


def test_only_whole_messages_are_taken_each_id_once():
    good = _row("ok")
    rows = [good, {"id": "not-a-uuid", "body": "x"}, {"id": str(uuid.uuid4()), "body": "  "},
            {"id": str(uuid.uuid4())}, "junk", dict(good), {**_row(), "body": "y" * 2500}]
    got = sm.usable(rows)
    assert [r["body"][:2] for r in got] == ["ok", "yy"]
    assert len(got[1]["body"]) == sm.BODY_MAX_CHARS


def test_the_mailbox_message_is_kept_named_by_its_id_and_dated_when_sent():
    row = {**_row(), "created_at": "2026-10-25T12:00:00+00:00"}
    msg = sm.inbox_message(SID, row, now=datetime(2026, 10, 25, 13, tzinfo=UTC).timestamp())
    assert (msg.kind, msg.origin, msg.keep) == (mailbox.Kind.MESSAGE, mailbox.ORIGIN_INBOX, True)
    assert msg.id == "s" + uuid.UUID(row["id"]).hex and "-" not in msg.id
    assert msg.made_at == datetime(2026, 10, 25, 12, tzinfo=UTC).timestamp()
    mailbox.publish(msg)
    ((_, waiting),) = mailbox.waiting(SID, now=msg.made_at)
    assert waiting.expires_at == msg.made_at + 12 * 3600
    assert waiting.rendered() == msg.text == sm.delivered_text(row["sender"], row["body"])


# ---------------------------------------------------------------------------
# Publish, then ack (R6).
# ---------------------------------------------------------------------------


def test_a_message_is_published_then_acked_then_reported_shown_once_a_hook_took_it(tmp_path, monkeypatch):
    row = _row()
    probe = FakeProbe(monkeypatch, [row])
    lane = ra.RunAlertLane(_worker(tmp_path))
    order: list[str] = []
    real_publish = mailbox.publish
    monkeypatch.setattr(mailbox, "publish", lambda m: (order.append("publish"), real_publish(m))[1])
    real_ack = probe.ack

    async def ack(env, sid, mid, state, instance, **kw):
        order.append(state)
        return await real_ack(env, sid, mid, state, instance, **kw)

    monkeypatch.setattr(probe_api, "ack_session_message", ack)
    assert _tick(lane) == 1
    assert order == ["publish", probe_api.ACK_ACKED], "published BEFORE the ack"
    (msg,) = _inbox_waiting()
    assert msg.id == mailbox.inbox_message_id(row["id"])

    assert _tick(lane) == 0 and order == ["publish", probe_api.ACK_ACKED], "waiting: nothing more to say"
    ((path, _),) = mailbox.waiting(SID)
    assert mailbox.claim(SID, path, by="UserPromptSubmit") is not None
    assert _tick(lane) == 0
    assert order[-1] == probe_api.ACK_DELIVERED_TO_AGENT
    assert probe.rows[row["id"]]["shown"] and _tick(lane) == 0 and probe.polls == 4


def test_a_crash_between_publish_and_ack_delivers_the_message_once(tmp_path, monkeypatch):
    row = _row()
    probe = FakeProbe(monkeypatch, [row])
    lane = ra.RunAlertLane(_worker(tmp_path))

    async def die(env, sid, mid, state, instance, **kw):
        raise RuntimeError("killed between the publish and the ack")

    monkeypatch.setattr(probe_api, "ack_session_message", die)
    with pytest.raises(RuntimeError):
        _tick(lane)
    assert len(_inbox_waiting()) == 1 and probe.rows[row["id"]]["acked_at"] is None

    # A new worker: the server lists it again (it was never acked).
    monkeypatch.setattr(probe_api, "ack_session_message", probe.ack)
    fresh = ra.RunAlertLane(_worker(tmp_path))
    assert _tick(fresh) == 0, "the mailbox has it: nothing published twice"
    assert len(_inbox_waiting()) == 1
    assert probe.acks == [(row["id"], probe_api.ACK_ACKED)]


def test_a_crash_between_publish_and_ack_after_the_hook_took_it_is_reported_shown(tmp_path, monkeypatch):
    row = _row()
    probe = FakeProbe(monkeypatch, [row])
    lane = ra.RunAlertLane(_worker(tmp_path))
    probe.fail_acks = True
    _tick(lane)
    ((path, _),) = mailbox.waiting(SID)
    mailbox.claim(SID, path, by="Stop")
    probe.fail_acks = False
    assert _tick(lane) == 0
    # The hook's claim is reported before the poll (delivered implies acked),
    # and the poll lists it no more: nothing left to ack.
    assert probe.acks == [(row["id"], probe_api.ACK_DELIVERED_TO_AGENT)]
    assert mailbox.waiting(SID) == []


def test_a_crash_before_the_publish_loses_nothing(tmp_path, monkeypatch):
    row = _row()
    probe = FakeProbe(monkeypatch, [row])
    lane = ra.RunAlertLane(_worker(tmp_path))
    real = mailbox.publish

    def die(msg):
        raise OSError("disk full")

    monkeypatch.setattr(mailbox, "publish", die)
    with pytest.raises(OSError):
        _tick(lane)
    assert probe.acks == [] and _inbox_waiting() == [], "nothing acked that was not published"
    monkeypatch.setattr(mailbox, "publish", real)
    assert _tick(lane) == 1
    assert [m.id for m in _inbox_waiting()] == [mailbox.inbox_message_id(row["id"])]


def test_a_service_claim_not_yet_received_is_not_shown(tmp_path, monkeypatch):
    row = _row()
    probe = FakeProbe(monkeypatch, [row])
    lane = ra.RunAlertLane(_worker(tmp_path))
    _tick(lane)
    ((path, _),) = mailbox.waiting(SID)
    mailbox.claim(SID, path, by="mailbox.claim", token="1_abc")
    assert mailbox.where(SID, mailbox.inbox_message_id(row["id"])) is mailbox.Where.WAITING
    _tick(lane)
    assert probe.acks == [(row["id"], probe_api.ACK_ACKED)], "not shown until its deliverer's receipt"


def test_a_failed_ack_is_said_again_at_the_next_poll(tmp_path, monkeypatch):
    row = _row()
    probe = FakeProbe(monkeypatch, [row])
    lane = ra.RunAlertLane(_worker(tmp_path))
    probe.fail_acks = True
    assert _tick(lane) == 1
    probe.fail_acks = False
    assert _tick(lane) == 0
    assert probe.acks == [(row["id"], probe_api.ACK_ACKED)] and len(_inbox_waiting()) == 1


def test_several_messages_go_out_oldest_first_each_on_its_own(tmp_path, monkeypatch):
    rows = [_row("first"), _row("second", kind="agent", title="Swarm orchestrator"), _row("third")]
    FakeProbe(monkeypatch, rows)
    lane = ra.RunAlertLane(_worker(tmp_path))
    assert _tick(lane) == 3
    assert [m.text.rsplit(": ", 1)[1] for m in _inbox_waiting()] == ["first", "second", "third"]


def test_the_poll_waits_its_interval_and_a_refused_key_waits_longer(tmp_path, monkeypatch):
    FakeProbe(monkeypatch, [])
    lane = ra.RunAlertLane(_worker(tmp_path))
    assert asyncio.run(lane.messages.tick()) == 0
    asked = lane.messages.next_poll_at
    assert asked >= lane.clock() + ra.RUN_ALERT_POLL_S - 1
    assert asyncio.run(lane.messages.tick()) == 0 and lane.messages.next_poll_at == asked, "not due yet"

    async def refused(env, sid, instance, held=None, active_at=None):
        raise probe_api.KeyRefused("GET /v1/sessions/x/messages: HTTP 401")

    monkeypatch.setattr(probe_api, "session_messages", refused)
    lane.messages.next_poll_at = 0.0
    assert asyncio.run(lane.messages.tick()) == 0
    assert lane.messages.next_poll_at > lane.clock() + ra.RUN_ALERT_REFUSED_WAIT_S - 5


def test_no_key_no_request(tmp_path, monkeypatch):
    probe = FakeProbe(monkeypatch, [_row()])
    monkeypatch.setattr(worker_mod, "probe_env", lambda sid: {"PROBE_DAEMON_SESSION": SID})
    assert _tick(ra.RunAlertLane(_worker(tmp_path))) == 0 and probe.polls == 0


def test_a_failing_message_poll_never_stops_the_run_alert_poll(tmp_path, monkeypatch):
    lane = ra.RunAlertLane(_worker(tmp_path))
    ticks: list[str] = []

    async def alert_tick():
        ticks.append("alerts")

    async def broken():
        ticks.append("messages")
        raise RuntimeError("boom")

    monkeypatch.setattr(lane, "tick", alert_tick)
    monkeypatch.setattr(lane.messages, "tick", broken)
    monkeypatch.setattr(ra, "RUN_ALERT_POLL_S", 0.01)

    async def go():
        task = asyncio.ensure_future(lane.run())
        while ticks.count("alerts") < 3:
            await asyncio.sleep(0.01)
        task.cancel()
        try:
            await task
        except asyncio.CancelledError:
            pass

    asyncio.run(go())
    assert ticks[:4] == ["alerts", "messages", "alerts", "messages"]


# ---------------------------------------------------------------------------
# Asking the server.
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


def test_the_poll_and_the_ack_hit_the_owner_bound_routes(monkeypatch):
    row = _row()
    gone = str(uuid.uuid4())
    seen = _serve(monkeypatch, lambda r: httpx.Response(200, json={"messages": [row, "junk"], "revoked": [gone, 7]})
                  if r.method == "GET" else httpx.Response(200, json={"id": row["id"]}))
    assert asyncio.run(probe_api.session_messages(ENV, SID, MACHINE, [gone])) == {"messages": [row], "revoked": [gone]}
    assert seen[0].url.params.get_list("held") == [gone]
    assert asyncio.run(probe_api.ack_session_message(ENV, SID, row["id"], probe_api.ACK_ACKED, MACHINE)) is (
        probe_api.AckResult.RECORDED)
    assert [(r.method, r.url.path) for r in seen] == [
        ("GET", f"/v1/sessions/{SID}/messages"), ("POST", f"/v1/sessions/{SID}/messages/{row['id']}/ack")]
    assert json.loads(seen[1].content) == {"state": "acked"}
    assert {r.headers.get(probe_api.DAEMON_INSTANCE_HEADER) for r in seen} == {MACHINE}, "both name this daemon"


@pytest.mark.parametrize("answer", [
    lambda r: httpx.Response(404, json={"detail": "Not Found"}),  # a server from before the route
    lambda r: httpx.Response(404, json={"detail": {"code": "SESSION_NOT_FOUND",
                                                   "message": "Probe has no record of this session."}}),
    lambda r: httpx.Response(403, json={"detail": {"code": "NOT_YOUR_SESSION", "message": (
        "Only the person whose session this is, and their own agent sessions, can message it.")}}),
    lambda r: httpx.Response(500, text="boom"),
    lambda r: httpx.Response(200, json={"messages": "not a list"}),
    lambda r: httpx.Response(200, text="not json"),
])
def test_anything_but_a_listing_is_no_answer_and_an_owner_refusal_is_no_refused_key(monkeypatch, answer):
    seen = _serve(monkeypatch, answer)
    assert asyncio.run(probe_api.session_messages(ENV, SID, MACHINE)) is None
    status = answer(seen[0]).status_code
    if status != 200:  # an ack's answer body is not read: a 200 is recorded
        # A 404 is no such message (erased, or a server from before the route):
        # saying it again changes nothing. Anything else is said again.
        assert asyncio.run(probe_api.ack_session_message(ENV, SID, str(uuid.uuid4()), "acked", MACHINE)) is (
            probe_api.AckResult.GONE if status == 404 else probe_api.AckResult.RETRY)


def test_a_refused_key_raises_on_the_poll_and_the_ack(monkeypatch):
    _serve(monkeypatch, lambda r: httpx.Response(401, json={"detail": "invalid token"}))
    with pytest.raises(probe_api.KeyRefused):
        asyncio.run(probe_api.session_messages(ENV, SID, MACHINE))
    with pytest.raises(probe_api.KeyRefused):
        asyncio.run(probe_api.ack_session_message(ENV, SID, str(uuid.uuid4()), "acked", MACHINE))


@pytest.mark.parametrize("error", [httpx.ConnectError("refused"), httpx.ReadTimeout("slow")])
def test_no_network_is_no_answer(monkeypatch, error):
    def fail(request):
        raise error

    _serve(monkeypatch, fail)
    assert asyncio.run(probe_api.session_messages(ENV, SID, MACHINE)) is None
    assert asyncio.run(probe_api.ack_session_message(ENV, SID, str(uuid.uuid4()), "acked", MACHINE)) is (
        probe_api.AckResult.RETRY)


def test_the_ack_states_are_the_servers():
    """`app/sessions/messages.py` AckState."""
    assert (probe_api.ACK_ACKED, probe_api.ACK_DELIVERED_TO_AGENT) == ("acked", "delivered_to_agent")
    assert sm.SENDER_PERSON == "person"


# ---------------------------------------------------------------------------
# The server's delivery lease (review of #3451): one daemon delivers it.
# ---------------------------------------------------------------------------


def test_a_resumed_session_publishes_what_the_last_machine_received_but_never_showed(tmp_path, monkeypatch):
    """Machine A received it (acked) and went quiet; its lease lapsed and this
    machine's poll is handed the row: its mailbox lacks the file, so it publishes."""
    row = _row("the run diverged, stop it", acked=True)
    probe = FakeProbe(monkeypatch, [row])
    lane = ra.RunAlertLane(_worker(tmp_path))
    assert _tick(lane) == 1
    assert [m.id for m in _inbox_waiting()] == [mailbox.inbox_message_id(row["id"])]
    assert probe.acks == [(row["id"], probe_api.ACK_ACKED)], "acked here, so this daemon holds it"
    assert _tick(lane) == 0 and len(_inbox_waiting()) == 1, "published once"


def test_a_copy_another_daemon_holds_is_dropped(tmp_path, monkeypatch):
    row = _row()
    probe = FakeProbe(monkeypatch, [row])
    lane = ra.RunAlertLane(_worker(tmp_path))
    probe.fail_acks = True
    assert _tick(lane) == 1 and len(_inbox_waiting()) == 1
    probe.fail_acks = False
    probe.lost.add(row["id"])  # meanwhile another machine's daemon took the lease
    assert _tick(lane) == 0
    assert _inbox_waiting() == [], "the waiting copy goes: the other daemon delivers it"


def test_the_daemon_names_itself_by_this_machines_device_id(tmp_path, monkeypatch):
    from probe.sdk import device_identity

    probe = FakeProbe(monkeypatch, [_row()])
    monkeypatch.setattr(device_identity, "device_instance_id", lambda: "device-" + "d" * 20)
    _tick(ra.RunAlertLane(_worker(tmp_path)))
    assert probe.instances == {"device-" + "d" * 20}
    monkeypatch.setattr(device_identity, "device_instance_id", lambda: None)
    monkeypatch.setattr(sm, "_PROCESS_INSTANCE", None)
    first = sm.daemon_instance()
    assert first.startswith("daemon-") and len(first) >= 16 and sm.daemon_instance() == first


class LeaseServer:
    """The server's delivery lease and revocation, in memory: what
    `app/sessions/messages.py` does, for two machines' daemons."""

    def __init__(self, monkeypatch, row: dict) -> None:
        self.row = dict(row, leased_by=None, lapsed=False, shown=False)
        monkeypatch.setattr(probe_api, "session_messages", self.poll)
        monkeypatch.setattr(probe_api, "ack_session_message", self.ack)

    def _mine(self, instance) -> bool:
        return self.row["leased_by"] == instance and not self.row["shown"]

    async def poll(self, env, session_id, instance, held=None, active_at=None):
        row = self.row
        messages = []
        if not row["shown"] and (row["leased_by"] in (None, instance) or row["lapsed"]):
            row["leased_by"], row["lapsed"] = instance, False
            messages = [{k: row[k] for k in ("id", "body", "created_at", "acked_at", "sender")}]
        revoked = [h for h in held or [] if not (h == row["id"] and self._mine(instance))]
        return {"messages": messages, "revoked": revoked}

    async def ack(self, env, session_id, message_id, state, instance, timeout=None):
        if self.row["leased_by"] != instance:
            return probe_api.AckResult.LEASE_LOST
        self.row["acked_at"] = self.row.get("acked_at") or datetime.now(UTC).isoformat()
        if state == probe_api.ACK_DELIVERED_TO_AGENT:
            self.row["shown"] = True
        return probe_api.AckResult.RECORDED


def test_the_old_machines_copy_goes_once_another_machine_took_the_message(tmp_path, monkeypatch):
    """Codex's sequence: A publishes and acks (its hook has not taken it), A goes
    quiet past its lease, B takes the lease and publishes, A polls again: A's
    copy is revoked and dropped, and the agent is shown ONE copy."""
    server = LeaseServer(monkeypatch, _row("stop the lr=3e-3 run"))
    machine_a, machine_b = "machine-a-" + "a" * 16, "machine-b-" + "b" * 16
    state_a, state_b = tmp_path / "a" / "state", tmp_path / "b" / "state"

    def on(state, instance):
        monkeypatch.setenv("XDG_STATE_HOME", str(state))
        (state / "probe" / "sessions").mkdir(parents=True, exist_ok=True)
        (lease.sessions_dir() / f"{SID}.state").write_text("daemon")
        (lease.sessions_dir() / f"{SID}.profile").write_text("daemon")
        lane = ra.RunAlertLane(_worker(state.parent))
        lane.messages.instance = instance
        return lane

    lane_a = on(state_a, machine_a)
    assert _tick(lane_a) == 1 and len(_inbox_waiting()) == 1 and server.row["acked_at"]
    server.row["lapsed"] = True  # A stopped polling for over two minutes

    lane_b = on(state_b, machine_b)
    assert _tick(lane_b) == 1, "B is handed the received message its mailbox lacks"
    assert server.row["leased_by"] == machine_b

    on(state_a, machine_a)
    assert _tick(lane_a) == 0
    assert _inbox_waiting() == [], "A's copy was revoked and dropped"

    shown = []
    for state in (state_a, state_b):
        monkeypatch.setenv("XDG_STATE_HOME", str(state))
        for path, _ in mailbox.waiting(SID):
            if mailbox.claim(SID, path, by="UserPromptSubmit") is not None:
                shown.append(str(state))
    assert shown == [str(state_b)], "one copy shown, on the machine that holds it"


# ---------------------------------------------------------------------------
# One session live on two machines (the G7 known limits, fixed).
# ---------------------------------------------------------------------------


def test_a_restarted_daemon_reports_every_message_its_hook_took_before_it_polls(tmp_path, monkeypatch):
    """The hook showed a message and its own report never reached Probe; the
    daemon died before its next poll. The next daemon says it was shown before
    it asks for anything -- whatever its poll answers -- once."""
    shown, waiting = _row("shown here"), _row("still waiting")
    probe = FakeProbe(monkeypatch, [shown, waiting])
    lane = ra.RunAlertLane(_worker(tmp_path))
    assert _tick(lane) == 2
    assert {m.daemon_instance for m in _inbox_waiting()} == {lane.messages.instance}, "the file names its holder"
    (path,) = [p for p, m in mailbox.waiting(SID) if m.id == mailbox.inbox_message_id(shown["id"])]
    assert mailbox.claim(SID, path, by="PostToolUse") is not None

    calls: list = []
    real_ack = probe.ack

    async def silent_poll(env, sid, instance, held=None, active_at=None):
        calls.append("poll")
        return None  # Probe did not answer the poll this time

    async def ack(env, sid, mid, state, instance, **kw):
        calls.append((mid, state))
        return await real_ack(env, sid, mid, state, instance, **kw)

    monkeypatch.setattr(probe_api, "session_messages", silent_poll)
    monkeypatch.setattr(probe_api, "ack_session_message", ack)
    restarted = ra.RunAlertLane(_worker(tmp_path))
    _tick(restarted)
    assert calls == [(shown["id"], probe_api.ACK_DELIVERED_TO_AGENT), "poll"], "before the poll"
    _tick(restarted)
    assert calls[2:] == ["poll"], "said once by this daemon"
    _tick(ra.RunAlertLane(_worker(tmp_path)))
    assert calls[3:] == [(shown["id"], probe_api.ACK_DELIVERED_TO_AGENT), "poll"], "and by the next (idempotent)"
    assert probe.rows[shown["id"]]["shown"] and not probe.rows[waiting["id"]].get("shown")

    # Neither a message past its half day nor a service claim not yet received
    # (not shown) is reported.
    assert mailbox.shown_inbox_ids(SID, now=time.time() + mailbox.INBOX_TTL_S + 60) == []
    ((path, _),) = mailbox.waiting(SID)
    mailbox.claim(SID, path, by="mailbox.claim", token="1_abc")
    assert mailbox.shown_inbox_ids(SID) == [shown["id"]]


def test_a_report_probe_settles_is_not_said_again_and_one_it_missed_is(tmp_path, monkeypatch):
    monkeypatch.setattr(sm, "RECEIPT_BACKOFF_S", 0.0)  # a missed one is said again at once
    row = _row()
    probe = FakeProbe(monkeypatch, [row])
    lane = ra.RunAlertLane(_worker(tmp_path))
    _tick(lane)
    ((path, _),) = mailbox.waiting(SID)
    mailbox.claim(SID, path, by="Stop")
    probe.fail_acks = True
    _tick(lane)
    assert lane.messages.reported == set(), "no answer: said again"
    probe.fail_acks = False
    probe.lost.add(row["id"])  # another daemon holds it now: nothing to say
    _tick(lane)
    assert lane.messages.reported == {row["id"]}
    before = len(probe.acks)
    _tick(lane)
    assert len(probe.acks) == before


def _transcript(tmp_path: Path, *stamps: str) -> None:
    work = tmp_path / "home" / "work"
    work.mkdir(parents=True, exist_ok=True)
    (tmp_path / f"{SID}.jsonl").write_text("".join(
        json.dumps({"type": "user", "message": {"content": f"step {n}"}, "cwd": str(work), "timestamp": stamp}) + "\n"
        for n, stamp in enumerate(stamps)))


def test_the_poll_says_when_this_sessions_agent_was_last_active(tmp_path, monkeypatch):
    probe = FakeProbe(monkeypatch, [])
    _transcript(tmp_path, "2026-10-26T09:00:00Z", "2026-10-26T09:05:00.500Z")
    worker = _worker(tmp_path)
    lane = ra.RunAlertLane(worker)
    _tick(lane)
    assert probe.active_at is None, "nothing read yet: no header, as a daemon from before it"
    worker.read_new()
    _tick(lane)
    assert probe.active_at == "2026-10-26T09:05:00.500000+00:00"
    assert worker.agent_active_at() == datetime(2026, 10, 26, 9, 5, 0, 500000, tzinfo=UTC).timestamp()


def test_the_activity_rides_the_poll_as_its_header(monkeypatch):
    seen = _serve(monkeypatch, lambda r: httpx.Response(200, json={"messages": [], "revoked": []}))
    asyncio.run(probe_api.session_messages(ENV, SID, MACHINE, [], active_at="2026-10-26T09:05:00+00:00"))
    asyncio.run(probe_api.session_messages(ENV, SID, MACHINE, []))
    assert [r.headers.get(probe_api.AGENT_ACTIVE_HEADER) for r in seen] == ["2026-10-26T09:05:00+00:00", None]
    assert probe_api.AGENT_ACTIVE_HEADER == "X-Probe-Agent-Active-At"  # app/sessions/messages.py


class ActivityLeaseServer(LeaseServer):
    """LeaseServer, plus `app/sessions/messages.py`'s move: a message not yet
    shown goes to a daemon whose agent was active more than ACTIVITY_LEAD_S
    after the holder's, both having said when."""

    ACTIVITY_LEAD_S = 60.0

    def __init__(self, monkeypatch, row: dict) -> None:
        super().__init__(monkeypatch, row)
        self.row["active"] = None

    async def poll(self, env, session_id, instance, held=None, active_at=None):
        row = self.row
        at = sm._epoch(active_at)
        if (not row["shown"] and row["leased_by"] not in (None, instance) and at is not None
                and row["active"] is not None and at > row["active"] + self.ACTIVITY_LEAD_S):
            row["lapsed"] = True  # the holder's agent is not where the researcher is
        answer = await super().poll(env, session_id, instance, held, active_at)
        if row["leased_by"] == instance:
            row["active"] = at
        return answer


def _machine(monkeypatch, tmp_path: Path, name: str, instance: str, active: "float | None") -> ra.RunAlertLane:
    """One machine's daemon for the session: its own state folder (made current
    by `_on`), its device id, and when its agent was last active."""
    state = tmp_path / name / "state"
    _on(monkeypatch, state)
    lane = ra.RunAlertLane(_worker(state.parent))
    lane.messages.instance = instance
    lane.w.agent_active_at = lambda: active  # the transcript's newest line on this machine
    lane.state = state  # type: ignore[attr-defined]
    return lane


def _on(monkeypatch, state: Path) -> None:
    monkeypatch.setenv("XDG_STATE_HOME", str(state))
    (state / "probe" / "sessions").mkdir(parents=True, exist_ok=True)
    (lease.sessions_dir() / f"{SID}.state").write_text("daemon")
    (lease.sessions_dir() / f"{SID}.profile").write_text("daemon")


def _tick_on(monkeypatch, lane: ra.RunAlertLane) -> int:
    _on(monkeypatch, lane.state)  # type: ignore[attr-defined]
    return _tick(lane)


def test_the_researcher_moved_to_b_so_b_takes_the_unshown_message_and_a_drops_its_copy(tmp_path, monkeypatch):
    """A's daemon keeps polling, but the researcher works on B now: the message A
    received and never showed moves to B, A's copy goes, and ONE copy is shown."""
    server = ActivityLeaseServer(monkeypatch, _row("stop the lr=3e-3 run"))
    a = _machine(monkeypatch, tmp_path, "a", "machine-a-" + "a" * 16, active=1_000_000.0)
    b = _machine(monkeypatch, tmp_path, "b", "machine-b-" + "b" * 16, active=1_000_030.0)
    assert _tick_on(monkeypatch, a) == 1 and server.row["leased_by"] == a.messages.instance
    assert _tick_on(monkeypatch, b) == 0, "30 s newer is no move: A keeps it"
    b.w.agent_active_at = lambda: 1_000_600.0
    assert _tick_on(monkeypatch, b) == 1, "the researcher is on B"
    assert server.row["leased_by"] == b.messages.instance

    assert _tick_on(monkeypatch, a) == 0
    assert _inbox_waiting() == [], "A's unshown copy was revoked and dropped"
    shown = []
    for lane in (a, b):
        _on(monkeypatch, lane.state)  # type: ignore[attr-defined]
        for path, _ in mailbox.waiting(SID):
            if mailbox.claim(SID, path, by="UserPromptSubmit") is not None:
                shown.append(lane.messages.instance)
    assert shown == [b.messages.instance]


def test_a_holder_whose_agent_is_the_newer_keeps_the_message_until_it_is_not(tmp_path, monkeypatch):
    server = ActivityLeaseServer(monkeypatch, _row("ship it"))
    a = _machine(monkeypatch, tmp_path, "a", "machine-a-" + "a" * 16, active=1_000_600.0)
    b = _machine(monkeypatch, tmp_path, "b", "machine-b-" + "b" * 16, active=1_000_000.0)
    silent = _machine(monkeypatch, tmp_path, "c", "machine-c-" + "c" * 16, active=None)
    assert _tick_on(monkeypatch, a) == 1
    assert _tick_on(monkeypatch, b) == 0 and _tick_on(monkeypatch, silent) == 0
    assert server.row["leased_by"] == a.messages.instance
    assert _tick_on(monkeypatch, a) == 0 and len(_inbox_waiting()) == 1, "A's copy stays"
    # The researcher goes to B: A's agent is the older one now.
    b.w.agent_active_at = lambda: 1_000_700.0
    assert _tick_on(monkeypatch, b) == 1 and server.row["leased_by"] == b.messages.instance


# ---------------------------------------------------------------------------
# End to end over HTTP: the hook's own report, then the daemon dies.
# ---------------------------------------------------------------------------

HOOK = Path(__file__).resolve().parents[1] / "plugins" / "probe-research" / "hooks" / "reads_hook.py"


class HttpProbe:
    """Probe's poll and ack for ONE session's messages on 127.0.0.1, with the
    lease rules of `app/sessions/messages.py` (holder-only acks, a lapsed lease
    retaken, a shown message never handed out again)."""

    def __init__(self, rows: list[dict]) -> None:
        import http.server
        import threading
        from urllib.parse import parse_qs, urlparse

        self.rows = {r["id"]: dict(r, leased_by=None, lapsed=False, shown=False) for r in rows}
        self.acks: list[tuple[str, str, str, str]] = []  # (id, state, instance, bearer)
        self.lock = threading.Lock()
        owner = self

        class Handler(http.server.BaseHTTPRequestHandler):
            def _answer(self, status: int, body: dict) -> None:
                data = json.dumps(body).encode()
                self.send_response(status)
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", str(len(data)))
                self.end_headers()
                self.wfile.write(data)

            def do_GET(self):  # noqa: N802
                url = urlparse(self.path)
                instance = self.headers.get("X-Probe-Daemon-Instance")
                held = parse_qs(url.query).get("held", [])
                with owner.lock:
                    out = []
                    for row in owner.rows.values():
                        if not row["shown"] and (row["leased_by"] in (None, instance) or row["lapsed"]):
                            row["leased_by"], row["lapsed"] = instance, False
                            out.append({k: row[k] for k in ("id", "body", "created_at", "acked_at", "sender")})
                    revoked = [h for h in held if not (h in owner.rows and owner.rows[h]["leased_by"] == instance
                                                       and not owner.rows[h]["shown"])]
                self._answer(200, {"messages": out, "revoked": revoked})

            def do_POST(self):  # noqa: N802
                mid = self.path.rstrip("/").split("/")[-2]
                state = json.loads(self.rfile.read(int(self.headers.get("Content-Length") or 0)))["state"]
                instance = self.headers.get("X-Probe-Daemon-Instance")
                with owner.lock:
                    owner.acks.append((mid, state, instance, self.headers.get("Authorization")))
                    row = owner.rows.get(mid)
                    if row is None:
                        return self._answer(404, {"detail": {"code": "MESSAGE_NOT_FOUND"}})
                    if row["leased_by"] != instance:
                        return self._answer(409, {"detail": {"code": "LEASE_LOST"}})
                    row["acked_at"] = row.get("acked_at") or datetime.now(UTC).isoformat()
                    row["shown"] = row["shown"] or state == "delivered_to_agent"
                self._answer(200, {"id": mid})

            def log_message(self, *_args):
                pass

        self.server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        self.server.daemon_threads = True
        threading.Thread(target=self.server.serve_forever, daemon=True).start()
        self.url = f"http://127.0.0.1:{self.server.server_address[1]}"

    def close(self) -> None:
        self.server.shutdown()
        self.server.server_close()


def test_a_message_as_hook_showed_never_reaches_b_after_as_daemon_died(tmp_path, monkeypatch):
    """A's daemon leases and publishes it; A's hook shows it and tells Probe
    itself; A's daemon dies before saying so; A's lease lapses. B's daemon, on
    the same session, is never handed it."""
    import subprocess
    import sys

    row = _row("stop the lr=3e-3 run")
    probe = HttpProbe([row])
    try:
        monkeypatch.setattr(worker_mod, "probe_env", lambda sid: {"PROBE_TOKEN": "pk_daemon",
                                                                  "PROBE_BASE_URL": probe.url,
                                                                  "PROBE_DAEMON_SESSION": SID})
        a = _machine(monkeypatch, tmp_path, "a", "machine-a-" + "a" * 16, active=None)
        assert _tick_on(monkeypatch, a) == 1
        config = tmp_path / "a" / "config.json"
        config.write_text(json.dumps({"contexts": {"default": {"companion_token": "pk_daemon",
                                                               "base_url": probe.url}}}))
        payload = json.dumps({"hook_event_name": "PostToolUse", "session_id": SID, "cwd": "/tmp",
                              "transcript_path": f"/home/u/.claude/projects/-tmp/{SID}.jsonl",
                              "tool_name": "Bash", "tool_input": {"command": "ls"}, "tool_response": {"stdout": ""},
                              "tool_use_id": "t1"})
        env = {"PATH": os.environ.get("PATH", "/usr/bin:/bin"), "HOME": str(tmp_path / "a" / "home"),
               "XDG_STATE_HOME": str(a.state), "PROBE_CONFIG_PATH": str(config)}  # type: ignore[attr-defined]
        hook = subprocess.run([sys.executable, str(HOOK)], input=payload, capture_output=True, text=True,
                              env=env, timeout=30)
        assert hook.returncode == 0 and "stop the lr=3e-3 run" in hook.stdout
        assert (row["id"], "delivered_to_agent", a.messages.instance, "Bearer pk_daemon") in probe.acks
        # A's daemon is gone: no more ticks from it, and its lease lapses.
        probe.rows[row["id"]]["lapsed"] = True

        b = _machine(monkeypatch, tmp_path, "b", "machine-b-" + "b" * 16, active=None)
        assert _tick_on(monkeypatch, b) == 0
        assert _inbox_waiting() == [] and mailbox.shown_inbox_ids(SID) == [], "B never has it"
        assert probe.rows[row["id"]]["leased_by"] == a.messages.instance
    finally:
        probe.close()


# ---------------------------------------------------------------------------
# Review of #3530: receipts within a budget; only what a hook showed is reported.
# ---------------------------------------------------------------------------


def _hook_module():
    import importlib.util

    spec = importlib.util.spec_from_file_location("_reads_hook_for_daemon_tests", HOOK)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _hook_takes(row: dict, *, shown: bool) -> str:
    """A current hook claims the inbox copy of `row` (its claim line says it
    writes `shown` lines) and, when `shown`, marks it shown once its output went
    out. Its mailbox id."""
    hook = _hook_module()
    message_id = mailbox.inbox_message_id(row["id"])
    mailbox.touch_alive(SID, by="PostToolUse")
    (path,) = [p for p, m in mailbox.waiting(SID) if m.id == message_id]
    assert hook.claim(SID, path, "PostToolUse") is not None
    if shown:
        hook.mark_shown(SID, [message_id], "PostToolUse")
    return message_id


def test_receipts_never_hold_the_poll_past_their_budget(tmp_path, monkeypatch):
    """Twenty receipts at 10 s each held the poll (and the run alerts on the
    same task) past the lease: now they get RECEIPT_BUDGET_S in all, and the
    rest is said at the next tick."""
    rows = [_row(f"shown {n}") for n in range(5)]
    probe = FakeProbe(monkeypatch, rows)
    lane = ra.RunAlertLane(_worker(tmp_path))
    assert _tick(lane) == 5
    for row in rows:
        _hook_takes(row, shown=True)
    assert sm.RECEIPT_BUDGET_S <= 3.0 and sm.RECEIPT_TIMEOUT_S < sm.RECEIPT_BUDGET_S
    monkeypatch.setattr(sm, "RECEIPT_BUDGET_S", 0.4)
    monkeypatch.setattr(sm, "RECEIPT_TIMEOUT_S", 0.3)
    timeouts: list[float] = []

    async def silent_ack(env, sid, mid, state, instance, timeout=None):
        timeouts.append(timeout)
        await asyncio.sleep(10)  # Probe takes the request and never answers

    monkeypatch.setattr(probe_api, "ack_session_message", silent_ack)
    restarted = ra.RunAlertLane(_worker(tmp_path))
    restarted.messages.next_poll_at = 0.0
    before, started = probe.polls, time.monotonic()
    asyncio.run(asyncio.wait_for(restarted.messages.tick(), 5))
    took = time.monotonic() - started
    assert probe.polls == before + 1, "the poll ran"
    assert took < 0.4 + 0.5, f"the receipts held the poll {took:.1f}s"
    assert timeouts and all(t <= 0.3 for t in timeouts), "each receipt short"
    assert restarted.messages.reported == set(), "nothing settled: said again at the next tick"

    monkeypatch.setattr(probe_api, "ack_session_message", probe.ack)
    restarted.messages.receipt_misses.clear()  # their backoff over
    _tick(restarted)
    assert restarted.messages.reported == {row["id"] for row in rows}


def test_back_off_state_is_kept_only_for_receipts_still_owed(tmp_path, monkeypatch):
    """Final review of #3530: a message that expired or settled leaves the
    back-off map, so it never grows past the mailbox."""
    FakeProbe(monkeypatch, [])
    lane = ra.RunAlertLane(_worker(tmp_path))
    lane.messages.receipt_misses["expired-long-ago"] = (5, time.monotonic() + 600)
    _tick(lane)
    assert "expired-long-ago" not in lane.messages.receipt_misses


def test_a_claim_never_marked_shown_is_put_back_and_never_reported(tmp_path, monkeypatch):
    """The claim (the rename) comes before the hook's output: a hook that died
    or whose output never went out leaves a claim with no `shown` line. That one
    is never reported shown -- neither before the poll nor when the poll lists
    it -- and goes back to waiting after UNSHOWN_RETURN_S, for the next hook."""
    row = _row("stop the lr=3e-3 run")
    probe = FakeProbe(monkeypatch, [row])
    lane = ra.RunAlertLane(_worker(tmp_path))
    assert _tick(lane) == 1
    message_id = _hook_takes(row, shown=False)
    assert _tick(lane) == 0
    assert probe.acks == [(row["id"], probe_api.ACK_ACKED)], "never reported shown"
    assert mailbox.where(SID, message_id) is mailbox.Where.CLAIMED, "within the grace: still claimed"

    monkeypatch.setattr(mailbox, "UNSHOWN_RETURN_S", 0.0)
    assert _tick(lane) == 0
    assert [m.id for m in _inbox_waiting()] == [message_id], "it waits again"
    assert probe.acks == [(row["id"], probe_api.ACK_ACKED)]

    _hook_takes(row, shown=True)  # the next hook shows it
    _tick(lane)
    assert probe.acks[-1] == (row["id"], probe_api.ACK_DELIVERED_TO_AGENT)


@pytest.mark.parametrize(("claim_lines", "shown_line", "shown"), [
    ([{"by": "PostToolUse", "shows": 1}], True, True),       # marked shown
    ([{"by": "PostToolUse", "shows": 1}], False, False),     # a current hook, never marked
    ([{"by": "mailbox.claim", "token": "1_abc"},
      {"by": "PostToolUse", "shows": 1, "receipt": "1_abc"}], False, False),  # a service claim a current hook received
    ([{"by": "PostToolUse"}], False, True),                  # a hook from before shown lines
    ([{"by": "mailbox.claim", "token": "1_abc"}], False, True),  # a service claim an older hook received
    ([{"by": "PostToolUse"}, {"by": "PostToolUse", "shows": 1}], False, False),  # put back, claimed again by a current one
    ([], False, True),                                       # no line left: as before, the claim is all there is
])
@pytest.mark.parametrize("heartbeat", [True, False])
def test_each_claim_is_held_to_its_own_marker(claim_lines, shown_line, shown, heartbeat):
    """Per claim (review of #3530): its latest claim line's marker (`shows: 1`)
    says whether its deliverer marks what it showed. The session's heartbeat
    plays no part: one session can hold claims of an older and a current hook."""
    message_id = "s" + uuid.uuid4().hex
    mailbox.claimed_dir(SID).mkdir(parents=True, exist_ok=True)
    with mailbox.claim_log_path(SID).open("a", encoding="utf-8") as log:
        for line in claim_lines:
            log.write(json.dumps({"id": message_id, "at": time.time(), **line}) + "\n")
    if shown_line:
        mailbox.mark_shown(SID, [message_id], by="PostToolUse")
    if heartbeat:
        mailbox.touch_alive(SID, by="PostToolUse")
    assert mailbox.InboxClaims(SID).shown_here(message_id) is shown


def test_two_receipts_that_always_time_out_never_starve_the_rest(tmp_path, monkeypatch):
    """Every tick restarted from the same sorted ids, so two failing receipts
    used up the budget for good (review of #3530): a missed one backs off and
    goes after those not tried, and no receipt waits past RECEIPT_TIMEOUT_S."""
    ids = ["00000000-0000-4000-8000-000000000001", "00000000-0000-4000-8000-000000000002",
           "00000000-0000-4000-8000-000000000003"]
    rows = [{**_row(f"shown {n}"), "id": server_id} for n, server_id in enumerate(ids)]
    FakeProbe(monkeypatch, rows)
    lane = ra.RunAlertLane(_worker(tmp_path))
    assert _tick(lane) == 3
    for row in rows:
        _hook_takes(row, shown=True)
    monkeypatch.setattr(sm, "RECEIPT_TIMEOUT_S", 0.2)
    monkeypatch.setattr(sm, "RECEIPT_BUDGET_S", 0.4)  # room for two timeouts, as 1.5 s and 3 s
    took: dict[str, list[float]] = {}

    async def ack(env, sid, mid, state, instance, timeout=None):
        started = time.monotonic()
        try:
            if mid in ids[:2]:
                await asyncio.sleep(10)  # never answered
            return probe_api.AckResult.RECORDED
        finally:
            took.setdefault(mid, []).append(time.monotonic() - started)

    monkeypatch.setattr(probe_api, "ack_session_message", ack)
    restarted = ra.RunAlertLane(_worker(tmp_path))
    for _ in range(2):
        restarted.messages.next_poll_at = 0.0
        asyncio.run(asyncio.wait_for(restarted.messages.tick(), 5))
    assert ids[2] in restarted.messages.reported, "the healthy one is reported within two ticks"
    assert ids[0] not in restarted.messages.reported and ids[1] not in restarted.messages.reported
    assert all(t <= 0.2 + 0.1 for times in took.values() for t in times), took
    assert sm.RECEIPT_BACKOFF_S >= 30.0


def _claim_lines(message_id: str) -> list[dict]:
    path = mailbox.claim_log_path(SID)
    lines = [json.loads(line) for line in path.read_text().splitlines()] if path.exists() else []
    return [e for e in lines if e.get("id") == message_id]


def test_a_current_hooks_claim_never_marked_shown_waits_again_even_with_no_heartbeat(tmp_path, monkeypatch):
    """(i) Per claim: the marker on a current hook's claim holds it to its `shown`
    line whether or not the session has a deliverer heartbeat."""
    row = _row("stop the lr=3e-3 run")
    probe = FakeProbe(monkeypatch, [row])
    lane = ra.RunAlertLane(_worker(tmp_path))
    assert _tick(lane) == 1
    hook = _hook_module()
    message_id = mailbox.inbox_message_id(row["id"])
    ((path, _),) = mailbox.waiting(SID)
    assert hook.claim(SID, path, "PostToolUse") is not None  # no heartbeat touched
    assert mailbox.read_alive(SID) is None and _claim_lines(message_id)[-1]["shows"] == 1
    monkeypatch.setattr(mailbox, "UNSHOWN_RETURN_S", 0.0)
    assert _tick(lane) == 0
    assert [m.id for m in _inbox_waiting()] == [message_id], "it waits again"
    assert (row["id"], probe_api.ACK_DELIVERED_TO_AGENT) not in probe.acks


def test_an_older_hooks_service_claim_counts_as_shown_beside_a_current_hooks_heartbeat(tmp_path, monkeypatch):
    """(ii) An older hook received a Probe service claim (the service's line has
    no marker, and the hook writes no line of its own) in a session where a
    current hook also beats: it counts as shown, is reported, and never waits again."""
    row = _row("ship it")
    probe = FakeProbe(monkeypatch, [row])
    lane = ra.RunAlertLane(_worker(tmp_path))
    assert _tick(lane) == 1
    message_id = mailbox.inbox_message_id(row["id"])
    ((path, _),) = mailbox.waiting(SID)
    claimed = mailbox.claim(SID, path, by="mailbox.claim", token="1_abc")  # the service's claim for it
    assert claimed is not None
    (token_file,) = mailbox.claimed_dir(SID).glob(f"*-{message_id}.1_abc.json")
    os.rename(token_file, token_file.with_name(path.name))  # the older hook's receipt, no line of its own
    mailbox.touch_alive(SID, by="PostToolUse")  # a current hook ran here too
    monkeypatch.setattr(mailbox, "UNSHOWN_RETURN_S", 0.0)
    assert _tick(lane) == 0
    assert _inbox_waiting() == [], "never put back"
    assert (row["id"], probe_api.ACK_DELIVERED_TO_AGENT) in probe.acks


def test_a_current_hook_marks_a_service_claim_it_receives(tmp_path, monkeypatch):
    """The receipt of a Probe service claim by a current hook writes its marker,
    so that claim too is held to its `shown` line."""
    row = _row("from the dashboard")
    FakeProbe(monkeypatch, [row])
    lane = ra.RunAlertLane(_worker(tmp_path))
    assert _tick(lane) == 1
    hook = _hook_module()
    message_id = mailbox.inbox_message_id(row["id"])
    ((path, _),) = mailbox.waiting(SID)
    mailbox.claim(SID, path, by="mailbox.claim", token="1_abc")
    (token_file,) = mailbox.claimed_dir(SID).glob(f"*-{message_id}.1_abc.json")
    assert hook.receive(SID, token_file, "PostToolUse", ledger=False) is not None
    last = _claim_lines(message_id)[-1]
    assert (last["shows"], last["receipt"]) == (1, "1_abc")
    assert not mailbox.InboxClaims(SID).shown_here(message_id)
