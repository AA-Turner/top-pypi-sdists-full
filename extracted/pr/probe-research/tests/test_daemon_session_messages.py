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

    async def poll(self, env, session_id, instance, held=None):
        self.polls += 1
        self.instances.add(instance)
        self.held = list(held or [])
        rows = [{k: v for k, v in r.items() if k != "shown"} for r in self.rows.values() if not r.get("shown")]
        return {"messages": rows, "revoked": []}

    async def ack(self, env, session_id, message_id, state, instance):
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

    async def ack(env, sid, mid, state, instance):
        order.append(state)
        return await real_ack(env, sid, mid, state, instance)

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

    async def die(env, sid, mid, state, instance):
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
    assert probe.acks == [(row["id"], probe_api.ACK_ACKED), (row["id"], probe_api.ACK_DELIVERED_TO_AGENT)]
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

    async def refused(env, sid, instance, held=None):
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
    if answer(seen[0]).status_code != 200:  # an ack's answer body is not read: a 200 is recorded
        assert asyncio.run(probe_api.ack_session_message(ENV, SID, str(uuid.uuid4()), "acked", MACHINE)) is (
            probe_api.AckResult.RETRY)


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

    async def poll(self, env, session_id, instance, held=None):
        row = self.row
        messages = []
        if not row["shown"] and (row["leased_by"] in (None, instance) or row["lapsed"]):
            row["leased_by"], row["lapsed"] = instance, False
            messages = [{k: row[k] for k in ("id", "body", "created_at", "acked_at", "sender")}]
        revoked = [h for h in held or [] if not (h == row["id"] and self._mine(instance))]
        return {"messages": messages, "revoked": revoked}

    async def ack(self, env, session_id, message_id, state, instance):
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
