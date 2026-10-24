"""Agent-facing messages through the Probe service (plan Q2).

The reads mailbox, the approvals board and the run alerts stay plain files; the
service only watches them for the machine (`mailwatch.py`), polls the run
alerts once for every daemon session (`alertpoll.py`), and says when to look
again. These tests run the real pieces: the service as a process in its own
HOME (`service_harness`), the Stop waiter as Claude Code runs it (a subprocess
with a payload on stdin), the mailbox and board through their own modules, and
an HTTP server standing in for Probe. Every waiter test runs with a service and
without one: the files are the truth either way.
"""

from __future__ import annotations

import asyncio
import fcntl
import http.server
import json
import os
import subprocess
import sys
import threading
import time
from pathlib import Path

import pytest

from probe.daemon import approvals as appr
from probe.daemon import mailbox
from probe.daemon.mailbox import Kind
from probe.daemon.store import store_path
from probe.service import alertpoll, client, mailwatch
from probe.service.protocol import ErrorCode, MailboxPart, Method, Mode, RpcError, Topic
from tests.service_harness import kill_agent, service_home, spawn_agent, wait_for  # noqa: F401 -- a fixture

pytestmark = pytest.mark.skipif(sys.platform == "win32", reason="the service is POSIX-only (plan S8)")

AGENT_ROOT = Path(__file__).resolve().parents[1]
HOOK = AGENT_ROOT / "plugins" / "probe-research" / "hooks" / "reads_hook.py"
APPROVALS_HOOK = AGENT_ROOT / "plugins" / "probe-research" / "hooks" / "approvals_hook.py"
SID = "11111111-2222-3333-4444-555555555555"
OTHER = "99999999-8888-7777-6666-555555555555"
ATTENDED = {"CLAUDE_CODE_SESSION_ATTENDED": "1"}


# ---------------------------------------------------------------------------
# Helpers.
# ---------------------------------------------------------------------------


def _state_dir() -> Path:
    return Path(os.environ["XDG_STATE_HOME"]) / "probe"


def _hook_env(**extra: str) -> dict:
    env = {"PATH": os.environ.get("PATH", "/usr/bin:/bin"), "HOME": os.environ["HOME"],
           "XDG_STATE_HOME": os.environ["XDG_STATE_HOME"]}
    env.update(extra)
    return env


def _payload(event: str, sid: str = SID, **fields) -> str:
    body = {"hook_event_name": event, "session_id": sid, "cwd": "/tmp",
            "transcript_path": f"/home/u/.claude/projects/-tmp/{sid}.jsonl", "permission_mode": "default"}
    body.update(fields)
    return json.dumps(body)


def _start(event: str, sid: str = SID, hook: Path = HOOK, **env: str) -> subprocess.Popen:
    proc = subprocess.Popen([sys.executable, str(hook)], stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE, text=True, env=_hook_env(**env))
    proc.stdin.write(_payload(event, sid))
    proc.stdin.close()
    proc.stdin = None
    return proc


def _run(event: str, sid: str = SID, hook: Path = HOOK, **env: str) -> subprocess.CompletedProcess:
    return subprocess.run([sys.executable, str(hook)], input=_payload(event, sid), capture_output=True, text=True,
                          env=_hook_env(**env), timeout=30)


def _answer(ask: mailbox.Ask, text: str = "lr=3e-4, from run digits-7") -> mailbox.Message:
    return mailbox.Message(id=mailbox.new_message_id(), session=ask.session, kind=Kind.ANSWER, ask=ask.id,
                           question=ask.question, text=text)


def _alert(ids: "list[int] | None" = None, sid: str = SID) -> mailbox.Message:
    ids = ids or [7]
    return mailbox.Message(id=mailbox.alert_message_id(ids), session=sid, kind=Kind.ALERT,
                           text="digits-svm (digits-svm-7) crashed at step 900: OutOfMemoryError.", keep=True,
                           alerts=ids)


def _daemon_serves(sid: str = SID):
    """The reader's status file and the worker's lock, held here as the worker holds it."""
    status = mailbox.status_path(sid)
    status.parent.mkdir(parents=True, exist_ok=True)
    status.write_text('{"state": "ok", "reason": "", "since": 1}')
    lock = store_path(sid).with_suffix(".lock")
    lock.parent.mkdir(parents=True, exist_ok=True)
    handle = lock.open("a")
    fcntl.flock(handle.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
    return handle


def _watched(sh) -> int:
    return (sh.status() or {}).get("watched", 0)


@pytest.fixture
def home(service_home, monkeypatch):
    """The service's HOME, with the session state inside it (XDG_STATE_HOME)."""
    monkeypatch.setenv("XDG_STATE_HOME", str(service_home.home / "state"))
    monkeypatch.delenv("PROBE_AGENT", raising=False)
    monkeypatch.delenv("CLAUDE_CODE_SESSION_ATTENDED", raising=False)
    return service_home


@pytest.fixture(params=["service", "no service"])
def maybe_service(request, home):
    """Each waiter test, with the service running and without one."""
    if request.param == "service":
        home.start()
    return request.param == "service"


def _subscribe(conn: client.Connection, sessions=None, topics=(Topic.MAILBOX_CHANGED,), state=None) -> object:
    params: dict = {"topics": list(topics)}
    if sessions is not None:
        params["sessions"] = sessions
        params["state_dir"] = str(state or _state_dir())
    return conn.call(Method.EVENTS_SUBSCRIBE, params)


def _next(conn: client.Connection, timeout: float, topic: str) -> "dict | None":
    """The first `topic` event within `timeout`, or None."""
    deadline = time.monotonic() + timeout
    while (left := deadline - time.monotonic()) > 0:
        ev = conn.next_event(left)
        if ev is None:
            return None
        if ev.get("topic") == topic:
            return ev
    return None


def _events(conn: client.Connection, timeout: float, topic: str) -> list[dict]:
    """Every `topic` event within `timeout`."""
    out = []
    deadline = time.monotonic() + timeout
    while (left := deadline - time.monotonic()) > 0:
        ev = conn.next_event(left)
        if ev is None:
            break
        if ev.get("topic") == topic:
            out.append(ev)
    return out


# ---------------------------------------------------------------------------
# The watch, in-process.
# ---------------------------------------------------------------------------


def test_each_part_of_a_mailbox_changes_its_own_part_of_the_signature(tmp_path, monkeypatch):
    monkeypatch.setenv("XDG_STATE_HOME", str(tmp_path))
    target = mailwatch.Target(SID, str(tmp_path / "probe"))
    before = mailwatch.mailbox_signature(target)
    ask = mailbox.write_ask(SID, "what LR?")
    after_ask = mailwatch.mailbox_signature(target)
    assert {p for p in after_ask if after_ask[p] != before[p]} == {MailboxPart.ASKS}
    mailbox.publish(_answer(ask))
    after_answer = mailwatch.mailbox_signature(target)
    assert {p for p in after_answer if after_answer[p] != after_ask[p]} == {MailboxPart.MESSAGES}
    ((path, _),) = mailbox.waiting(SID)
    mailbox.claim(SID, path, by="test")
    claimed = mailwatch.mailbox_signature(target)
    assert {p for p in claimed if claimed[p] != after_answer[p]} == {MailboxPart.MESSAGES, MailboxPart.CLAIMED}
    mailbox.turn_path(SID).parent.mkdir(parents=True, exist_ok=True)
    mailbox.turn_path(SID).write_text("t1")
    turned = mailwatch.mailbox_signature(target)
    assert {p for p in turned if turned[p] != claimed[p]} == {MailboxPart.TURN}
    assert mailwatch.mailbox_signature(mailwatch.Target(OTHER, str(tmp_path / "probe")))[MailboxPart.MESSAGES] is None


def test_a_second_message_in_the_same_second_still_changes_the_signature(tmp_path, monkeypatch):
    """Names, not the folder's mtime: an mtime one second coarse (HFS+, some
    network homes) would hide the second message."""
    monkeypatch.setenv("XDG_STATE_HOME", str(tmp_path))
    target = mailwatch.Target(SID, str(tmp_path / "probe"))
    mailbox.publish(_alert([1]))
    folder = mailbox.messages_dir(SID)
    os.utime(folder, (1_000_000, 1_000_000))
    first = mailwatch.mailbox_signature(target)
    mailbox.publish(_alert([2]))
    os.utime(folder, (1_000_000, 1_000_000))
    assert mailwatch.mailbox_signature(target)[MailboxPart.MESSAGES] != first[MailboxPart.MESSAGES]


def _question(sid: str, rid: str) -> appr.Request:
    q = appr.Question(header=f"Probe {rid}", question="Delete run digits-7, made by Ana?", yes_label="Delete it",
                      no_label="Keep it")
    return appr.Request(id=rid, policy="delete.others_data", session_id=sid, question=q, facts={}, fingerprint="f",
                        held={"kind": "probe", "argv": ["probe", "run", "delete", "digits-7"]},
                        asked_at=time.time(), expires_at=time.time() + 3600)


def test_the_board_names_the_session_of_each_question_filed_answered_or_removed(tmp_path, monkeypatch):
    monkeypatch.setenv("XDG_STATE_HOME", str(tmp_path))
    state = str(tmp_path / "probe")
    board = appr.Board()
    seen, changed = mailwatch.board_scan(state, None)
    assert changed == {}, "a first look is a baseline"
    board.save(_question(SID, "q1"))
    board.save(_question(OTHER, "q2"))
    seen, changed = mailwatch.board_scan(state, seen)
    assert changed == {SID: {"q1"}, OTHER: {"q2"}}
    seen, changed = mailwatch.board_scan(state, seen)
    assert changed == {}, "nothing changed: nothing re-read"
    assert board.answer("q1", "Delete it", channel="question-tool")
    seen, changed = mailwatch.board_scan(state, seen)
    assert changed == {SID: {"q1"}}
    (board.root / "requests" / "q2.json").unlink()
    seen, changed = mailwatch.board_scan(state, seen)
    assert changed == {OTHER: {"q2"}}


def test_a_session_seen_for_the_first_time_is_only_baselined(tmp_path, monkeypatch):
    monkeypatch.setenv("XDG_STATE_HOME", str(tmp_path))
    mailbox.publish(_alert())
    watch = mailwatch.MailWatch(loop_getter=lambda: None, emit=lambda *a: None, targets=set, log=print)
    target = mailwatch.Target(SID, str(tmp_path / "probe"))
    assert watch.scan({target}) == []
    assert watch.scan({target}) == []
    mailbox.publish(_alert([8]))
    assert watch.scan({target}) == [(Topic.MAILBOX_CHANGED, {"sid": SID, "parts": [MailboxPart.MESSAGES]})]


def _in_time(fn, *args, timeout: float = 5.0):
    """`fn(*args)` on a daemon thread, or a failure if it does not return in time."""
    out: list = []
    thread = threading.Thread(target=lambda: out.append(fn(*args)), daemon=True)
    thread.start()
    thread.join(timeout)
    assert out, f"{fn.__name__} blocked for {timeout} s"
    return out[0]


def test_a_planted_fifo_or_a_bottomless_file_never_stops_the_watch(tmp_path, monkeypatch):
    """Files are opened without blocking and parsed with a guard: a FIFO where a
    request goes, or JSON nested deep enough to overflow the parser, costs
    nothing, and the mailbox events of the same look still go out."""
    monkeypatch.setenv("XDG_STATE_HOME", str(tmp_path))
    board = appr.Board()
    os.mkfifo(board.root / "requests" / "fifo.json")
    (board.root / "requests" / "deep.json").write_text("[" * 200_000)
    assert mailwatch.read_regular(str(board.root / "requests" / "fifo.json"), 1024) is None
    watch = mailwatch.MailWatch(loop_getter=lambda: None, emit=lambda *a: None, targets=set, log=lambda m: None)
    target = mailwatch.Target(SID, str(tmp_path / "probe"))
    assert _in_time(watch.scan, {target}) == []
    board.save(_question(SID, "q1"))
    mailbox.publish(_alert())
    assert _in_time(watch.scan, {target}) == [
        (Topic.MAILBOX_CHANGED, {"sid": SID, "parts": [MailboxPart.MESSAGES]}),
        (Topic.APPROVALS_CHANGED, {"sid": SID, "ids": ["q1"]}),
    ]
    mailbox.mark_worker_accepts(SID)
    marker = mailbox.worker_marker_path(SID)
    marker.unlink()
    os.mkfifo(marker)
    assert _in_time(alertpoll.wanted, str(tmp_path / "probe"), SID) is None


def test_the_board_is_looked_at_only_while_someone_wants_it(tmp_path, monkeypatch):
    monkeypatch.setenv("XDG_STATE_HOME", str(tmp_path))
    watch = mailwatch.MailWatch(loop_getter=lambda: None, emit=lambda *a: None, targets=set, log=lambda m: None)
    target = mailwatch.Target(SID, str(tmp_path / "probe"))
    watch.scan({target}, False)
    appr.Board().save(_question(SID, "q1"))
    assert watch.scan({target}, False) == []
    assert watch.scan({target}, True) == [], "a board first looked at is a baseline"


def test_the_watch_runs_on_a_thread_the_exit_never_waits_for():
    lane = mailwatch.DaemonLane("test-lane")
    assert lane.submit(lambda x: x + 1, 41).result(5) == 42
    assert lane._thread.daemon  # noqa: SLF001
    lane.close()
    with pytest.raises(RuntimeError):
        lane.submit(lambda: None)


# ---------------------------------------------------------------------------
# The service's watch, over its socket.
# ---------------------------------------------------------------------------


def _bare_service(tmp_path, monkeypatch):
    from probe.service import server, updater
    from probe.service.registry import Registry

    monkeypatch.setattr(updater, "_hosted_live", updater._hosted_live)  # noqa: SLF001 -- Service sets it
    return server, server.Service(registry=Registry(tmp_path / "sessions.json"))


def test_a_caller_in_a_sandbox_watches_only_registered_sessions_where_they_live(tmp_path, monkeypatch):
    from probe.service import caller

    server, service = _bare_service(tmp_path, monkeypatch)
    monkeypatch.setattr(caller, "sandboxed", lambda pid: True)
    conn = server.Connection(None, peer_pid=os.getpid())
    registered = str(tmp_path / "registered" / "probe")
    service.registry.register(SID, "claude_code", Mode.DAEMON, None, 1, registered)

    def subscribe(**params):
        return asyncio.run(service._subscribe(conn, {"topics": [Topic.MAILBOX_CHANGED], **params}))  # noqa: SLF001

    with pytest.raises(RpcError, match="must name its sessions"):
        subscribe()
    with pytest.raises(RpcError, match="not registered"):
        subscribe(sessions=[OTHER])
    assert conn.topics == set() and conn.sessions == {}, "a refused subscription watches nothing"
    assert subscribe(sessions=[SID], state_dir="/somewhere/it/chose") == {}
    assert conn.sessions == {SID: registered}, "watched where the session registered its files"
    service.mailwatch.close()


def test_a_connection_watches_at_most_its_share_of_sessions(tmp_path, monkeypatch):
    server, service = _bare_service(tmp_path, monkeypatch)
    conn = server.Connection(None, peer_pid=os.getpid())
    service.connections.add(conn)
    state = str(tmp_path / "probe")
    first = [f"s{i}" for i in range(64)]
    assert asyncio.run(service._subscribe(conn, {"topics": [Topic.MAILBOX_CHANGED], "sessions": first,  # noqa: SLF001
                                                 "state_dir": state})) == {}
    with pytest.raises(RpcError, match="at most 64"):
        asyncio.run(service._subscribe(conn, {"topics": [Topic.MAILBOX_CHANGED], "sessions": ["one-more"],  # noqa: SLF001
                                              "state_dir": state}))
    assert len(service._watch_targets()) == 64  # noqa: SLF001
    service.mailwatch.close()


def test_a_subscriber_hears_of_its_sessions_mailbox_and_of_no_other(home):
    home.start()
    with home.connect() as conn, home.connect() as everyone:
        assert _subscribe(conn, [SID]) == {}
        assert _watched(home) == 1
        mailbox.publish(_alert(sid=OTHER))
        assert _events(conn, 1.0, Topic.MAILBOX_CHANGED) == [], "another session's mailbox"
        started = time.monotonic()
        mailbox.publish(_alert())
        ev = _next(conn, 2.0, Topic.MAILBOX_CHANGED)
        took = time.monotonic() - started
        assert ev == {"topic": Topic.MAILBOX_CHANGED, "sid": SID, "parts": [MailboxPart.MESSAGES]}
        assert took < mailwatch.WATCH_S + 0.5, f"heard {took:.2f} s after the publish"
        assert _subscribe(everyone, topics=(Topic.SESSION_ENDED,)) == {}
    assert wait_for(lambda: _watched(home) == 0, 3.0), "nobody watches once the subscriber is gone"


def test_a_subscriber_hears_of_a_held_question_filed_and_answered(home):
    home.start()
    board = appr.Board()
    with home.connect() as conn:
        assert _subscribe(conn, [SID], topics=(Topic.APPROVALS_CHANGED,)) == {}
        board.save(_question(OTHER, "q0"))
        board.save(_question(SID, "q1"))
        assert _events(conn, 2.0, Topic.APPROVALS_CHANGED)[:1] == [
            {"topic": Topic.APPROVALS_CHANGED, "sid": SID, "ids": ["q1"]}]
        board.answer("q1", "Keep it", channel="question-tool")
        assert _events(conn, 2.0, Topic.APPROVALS_CHANGED)[:1] == [
            {"topic": Topic.APPROVALS_CHANGED, "sid": SID, "ids": ["q1"]}]


def test_a_subscription_naming_too_many_sessions_or_a_relative_folder_is_refused(home):
    home.start()
    with home.connect() as conn:
        with pytest.raises(client.ServiceError) as err:
            _subscribe(conn, [f"s{i}" for i in range(65)])
        assert err.value.code == ErrorCode.INVALID_PARAMS
        with pytest.raises(client.ServiceError) as err:
            conn.call(Method.EVENTS_SUBSCRIBE, {"topics": [Topic.MAILBOX_CHANGED], "sessions": [SID],
                                                "state_dir": "state/probe"})
        assert err.value.code == ErrorCode.INVALID_PARAMS


# ---------------------------------------------------------------------------
# The Stop waiter, with and without the service.
# ---------------------------------------------------------------------------


def test_the_waiter_wakes_the_agent_with_an_answer(maybe_service, home):
    ask = mailbox.write_ask(SID, "what LR did the last sweep use?")
    waiter = _start("Stop", **ATTENDED)
    if maybe_service:
        assert wait_for(lambda: _watched(home) == 1, 5.0), "the waiter subscribed"
    time.sleep(0.5)
    assert waiter.poll() is None, "the waiter waits while the ask is open"
    answer = _answer(ask)
    mailbox.publish(answer)
    stdout, stderr = waiter.communicate(timeout=15)
    assert (waiter.returncode, stdout, stderr) == (2, "", answer.rendered())
    assert mailbox.open_asks(SID) == []


def test_the_waiter_wakes_an_idle_agent_for_a_run_alert(maybe_service, home):
    holder = _daemon_serves()
    try:
        waiter = _start("Stop", **ATTENDED)
        if maybe_service:
            assert wait_for(lambda: _watched(home) == 1, 5.0)
        time.sleep(0.5)
        assert waiter.poll() is None
        alert = _alert()
        mailbox.publish(alert)
        stdout, stderr = waiter.communicate(timeout=15)
    finally:
        holder.close()
    assert (waiter.returncode, stdout, stderr) == (2, "", alert.rendered())


def test_the_waiter_exits_quietly_when_a_new_prompt_arrives(maybe_service, home):
    holder = _daemon_serves()
    try:
        waiter = _start("Stop", **ATTENDED)
        if maybe_service:
            assert wait_for(lambda: _watched(home) == 1, 5.0)
        time.sleep(0.5)
        mailbox.turn_path(SID).write_text("a-new-turn")  # what the prompt's shell writes
        stdout, stderr = waiter.communicate(timeout=10)
    finally:
        holder.close()
    assert (waiter.returncode, stdout, stderr) == (0, "", "")


def test_the_waiter_ignores_another_sessions_message_and_a_receipt(maybe_service, home):
    ask = mailbox.write_ask(SID, "any OOM on 8xA100?")
    waiter = _start("Stop", **ATTENDED)
    if maybe_service:
        assert wait_for(lambda: _watched(home) == 1, 5.0)
    mailbox.publish(_alert(sid=OTHER))
    mailbox.publish(mailbox.Message(id=mailbox.new_message_id(), session=SID, kind=Kind.MESSAGE, text="noted",
                                    origin=mailbox.ORIGIN_WRITER))
    time.sleep(1.5)
    assert waiter.poll() is None, "neither ends the wait"
    answer = _answer(ask, "no OOM in the last 30 runs")
    mailbox.publish(answer)
    stdout, stderr = waiter.communicate(timeout=15)
    assert (waiter.returncode, stderr) == (2, answer.rendered())


def test_the_waiter_goes_back_to_its_own_poll_when_the_service_stops(home):
    home.start()
    holder = _daemon_serves()
    try:
        waiter = _start("Stop", **ATTENDED)
        assert wait_for(lambda: _watched(home) == 1, 5.0)
        pid = home.status()["pid"]
        home.call(Method.STOP)
        assert home.wait_exit(pid, 5.0)
        time.sleep(0.5)
        assert waiter.poll() is None, "a service that went away does not end the wait"
        alert = _alert()
        mailbox.publish(alert)
        stdout, stderr = waiter.communicate(timeout=15)
    finally:
        holder.close()
    assert (waiter.returncode, stderr) == (2, alert.rendered())


def test_an_event_wakes_the_waiter_within_the_services_look(home):
    """With the service the waiter is woken by its event, not by its own poll:
    an alert reaches it well inside the 2 s it polled for alerts."""
    home.start()
    holder = _daemon_serves()
    try:
        waiter = _start("Stop", **ATTENDED)
        assert wait_for(lambda: _watched(home) == 1, 5.0)
        time.sleep(2.5)  # past a poll round: the next look would be the waiter's own
        started = time.monotonic()
        mailbox.publish(_alert())
        waiter.communicate(timeout=15)
        took = time.monotonic() - started
    finally:
        holder.close()
    assert waiter.returncode == 2
    assert took < 1.5, f"woken {took:.2f} s after the alert"


def test_the_approvals_nudge_reads_the_board_with_and_without_a_service(maybe_service, home):
    appr.Board().save(_question(SID, "q9"))
    result = _run("UserPromptSubmit", hook=APPROVALS_HOOK)
    assert result.returncode == 0
    context = json.loads(result.stdout)["hookSpecificOutput"]["additionalContext"]
    assert '"header": "Probe q9"' in context


# ---------------------------------------------------------------------------
# Run alerts: one poll for the machine.
# ---------------------------------------------------------------------------


class _Probe(http.server.BaseHTTPRequestHandler):
    """Stands in for Probe's `GET /v1/sessions/{sid}/run-alerts`."""

    protocol_version = "HTTP/1.1"

    def do_GET(self):  # noqa: N802 -- http.server's name
        server = self.server
        server.seen.append({"path": self.path, "auth": self.headers.get("Authorization"),
                            "peer": self.client_address[1]})
        status, body, headers = server.answer(self.path)
        data = json.dumps(body).encode()
        self.send_response(status)
        for name, value in headers.items():
            self.send_header(name, value)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def log_message(self, *args):  # quiet
        return


@pytest.fixture
def probe_api():
    server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), _Probe)
    server.seen = []
    server.answer = lambda path: (200, {"alerts": [{"id": 1, "run_id": "r", "kind": "crashed",
                                                     "text": f"{path.split('/')[3]} crashed.",
                                                     "created_at": "2026-10-22T00:00:00Z"}]}, {})
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        yield server
    finally:
        server.shutdown()
        server.server_close()


def _config(path: Path, base_url: str, key: "str | None" = "pk_daemon_test", v1: bool = False) -> str:
    row = {"base_url": base_url, "token": "pk_user"}
    if key:
        row["companion_token"] = key
    data = row if v1 else {"version": 2, "current_context": "default", "contexts": {"default": row}}
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data))
    return str(path)


def _offer(sid: str, config: "str | None", pid: "int | None" = None) -> None:
    mailbox.mark_worker_accepts(sid, pid)
    assert mailbox.offer_run_alerts(sid, config, pid)


def test_only_a_running_worker_that_asked_is_polled_for(tmp_path, monkeypatch):
    monkeypatch.setenv("XDG_STATE_HOME", str(tmp_path))
    state = str(tmp_path / "probe")
    assert alertpoll.wanted(state, SID) is None, "no worker"
    mailbox.mark_worker_accepts(SID)
    assert alertpoll.wanted(state, SID) is None, "a worker that did not ask"
    assert mailbox.offer_run_alerts(SID, "/home/u/.config/probe/config.json")
    assert alertpoll.wanted(state, SID) == "/home/u/.config/probe/config.json"
    assert not mailbox.offer_run_alerts(SID, None, pid=12345), "only the worker's own marker"
    assert mailbox.offer_run_alerts(SID, None)
    assert alertpoll.wanted(state, SID) is None, "the offer taken back"
    _offer(OTHER, "/c.json", pid=2**22 + 17)  # a pid that runs nothing
    assert alertpoll.wanted(state, OTHER) is None, "a worker that died"


def test_the_key_and_endpoint_are_the_named_configs(tmp_path):
    v2 = _config(tmp_path / "v2.json", "https://api.example.test/")
    assert alertpoll.endpoint(v2) == alertpoll.Endpoint("https://api.example.test", "pk_daemon_test")
    v1 = _config(tmp_path / "v1.json", "https://api.example.test", v1=True)
    assert alertpoll.endpoint(v1) == alertpoll.Endpoint("https://api.example.test", "pk_daemon_test")
    assert alertpoll.endpoint(_config(tmp_path / "nokey.json", "https://x.test", key=None)) is None
    assert alertpoll.endpoint(str(tmp_path / "missing.json")) is None


def _poller(answers: list, tmp_path, clock=time.time) -> tuple[alertpoll.AlertPoller, list]:
    asked: list = []

    def fetch(ep, sid):
        asked.append(sid)
        return answers.pop(0) if answers else (alertpoll.Answer.LISTING, [])

    poller = alertpoll.AlertPoller(loop_getter=lambda: None, sessions=list, log=lambda m: None, fetch=fetch,
                                   poll_s=30.0, clock=clock)
    return poller, asked


def test_a_round_hands_each_session_its_answer(tmp_path, monkeypatch):
    monkeypatch.setenv("XDG_STATE_HOME", str(tmp_path))
    state = str(tmp_path / "probe")
    config = _config(tmp_path / "config.json", "https://api.example.test")
    _offer(SID, config)
    _offer(OTHER, config)
    rows = [{"id": 3, "text": "a crashed."}]
    poller, asked = _poller([(alertpoll.Answer.LISTING, rows), (alertpoll.Answer.NONE, None)], tmp_path)
    assert poller.poll_round([(SID, state), (OTHER, state), ("not-asked", state)]) == {
        "asked": 2, "handed": 2, "skipped": 1}
    assert asked == [SID, OTHER]
    mine = mailbox.read_alerts_handoff(SID)
    assert mine["alerts"] == rows and mine["refused_until"] is None and time.time() - mine["polled_at"] < 5
    assert mailbox.read_alerts_handoff(OTHER)["alerts"] is None, "no answer from the server: no listing"


def test_a_refused_key_pauses_its_endpoint_and_the_handoff_says_until_when(tmp_path, monkeypatch):
    monkeypatch.setenv("XDG_STATE_HOME", str(tmp_path))
    state = str(tmp_path / "probe")
    _offer(SID, _config(tmp_path / "config.json", "https://api.example.test"))
    poller, asked = _poller([(alertpoll.Answer.REFUSED, alertpoll.REFUSED_WAIT_S)], tmp_path)
    poller.poll_round([(SID, state)])
    poller.poll_round([(SID, state)])
    assert asked == [SID], "asked once, then held back"
    until = mailbox.read_alerts_handoff(SID)["refused_until"]
    assert until is not None and until > time.time() + alertpoll.REFUSED_WAIT_S - 10
    assert mailbox.read_alerts_handoff(SID)["alerts"] is None


def test_an_endpoint_that_does_not_answer_leaves_the_poll_to_the_workers(tmp_path, monkeypatch):
    """No hand-off: this service may lack the proxy or the CA bundle the
    worker's environment names, and the worker's own poll takes over."""
    monkeypatch.setenv("XDG_STATE_HOME", str(tmp_path))
    state = str(tmp_path / "probe")
    _offer(SID, _config(tmp_path / "config.json", "https://api.example.test"))
    now = [1000.0]
    poller, asked = _poller([(alertpoll.Answer.UNREACHED, None)] * 3, tmp_path, clock=lambda: now[0])
    assert poller.poll_round([(SID, state)])["handed"] == 0
    assert mailbox.read_alerts_handoff(SID) is None
    now[0] += 30.0
    poller.poll_round([(SID, state)])
    assert len(asked) == 2, "asked again at the next round"
    now[0] += 30.0
    poller.poll_round([(SID, state)])
    assert len(asked) == 2, "then less often"
    now[0] += 30.0
    poller.poll_round([(SID, state)])
    assert len(asked) == 3


def test_a_refused_key_pauses_only_that_key(tmp_path, monkeypatch):
    """Two CLI configs at one address (a worktree's own config): one key's
    refusal never holds back the other's sessions."""
    monkeypatch.setenv("XDG_STATE_HOME", str(tmp_path))
    state = str(tmp_path / "probe")
    _offer(SID, _config(tmp_path / "revoked.json", "https://api.example.test", key="pk_revoked"))
    _offer(OTHER, _config(tmp_path / "valid.json", "https://api.example.test", key="pk_valid"))
    asked: list = []

    def fetch(ep, sid):
        asked.append(ep.key)
        if ep.key == "pk_revoked":
            return alertpoll.Answer.REFUSED, alertpoll.REFUSED_WAIT_S
        return alertpoll.Answer.LISTING, []

    now = [1000.0]
    poller = alertpoll.AlertPoller(loop_getter=lambda: None, sessions=list, log=lambda m: None, fetch=fetch,
                                   poll_s=30.0, clock=lambda: now[0])
    for _ in range(3):
        poller.poll_round([(SID, state), (OTHER, state)])
        now[0] += 30.0
    assert asked == ["pk_revoked", "pk_valid", "pk_valid", "pk_valid"]
    assert mailbox.read_alerts_handoff(OTHER)["refused_until"] is None
    assert mailbox.read_alerts_handoff(SID)["refused_until"] is not None


def test_a_session_that_breaks_its_round_costs_only_its_own_answer(tmp_path, monkeypatch):
    monkeypatch.setenv("XDG_STATE_HOME", str(tmp_path))
    state = str(tmp_path / "probe")
    for bad in ("https://", "https://api.example.test:port", "ftp://api.example.test"):
        assert alertpoll.endpoint(_config(tmp_path / "bad.json", bad)) is None, bad
    assert alertpoll.endpoint(_config(tmp_path / "bad.json", "https://x.test", key="pk\r\nX-Evil: 1")) is None
    config = _config(tmp_path / "config.json", "https://api.example.test")
    _offer(SID, config)
    _offer(OTHER, config)

    def fetch(ep, sid):
        if sid == SID:
            raise RuntimeError("a bug in one session's answer")
        return alertpoll.Answer.LISTING, []

    poller = alertpoll.AlertPoller(loop_getter=lambda: None, sessions=list, log=lambda m: None, fetch=fetch,
                                   poll_s=30.0)
    poller.poll_round([(SID, state), (OTHER, state)])
    assert mailbox.read_alerts_handoff(SID) is None
    assert mailbox.read_alerts_handoff(OTHER)["alerts"] == []


def test_an_endpoint_that_never_sends_a_listing_is_left_to_the_workers(tmp_path, monkeypatch):
    """A gateway that answers this service (and not the worker's proxy) with a
    403 or a 502 page: after NONE_LIMIT rounds the workers ask again."""
    monkeypatch.setenv("XDG_STATE_HOME", str(tmp_path))
    state = str(tmp_path / "probe")
    _offer(SID, _config(tmp_path / "config.json", "https://api.example.test"))
    now = [1000.0]
    poller, asked = _poller([(alertpoll.Answer.NONE, None)] * 10, tmp_path, clock=lambda: now[0])
    for _ in range(alertpoll.NONE_LIMIT - 1):
        poller.poll_round([(SID, state)])
        now[0] += 30.0
    assert mailbox.read_alerts_handoff(SID) is not None
    mailbox.alerts_handoff_path(SID).unlink()
    poller.poll_round([(SID, state)])
    assert mailbox.read_alerts_handoff(SID) is None, "no hand-off: the worker's own poll takes over"


def test_the_backoff_and_the_key_check_hold_at_their_edges(tmp_path):
    poller, _ = _poller([], tmp_path)
    assert poller._backoff(5000) <= poller.clock() + alertpoll.REFUSED_WAIT_S  # noqa: SLF001 -- no OverflowError
    assert alertpoll.endpoint(_config(tmp_path / "k.json", "https://x.test", key="pk_ünïcode")) is None


def test_a_server_that_drips_its_answer_is_cut_at_the_request_deadline(monkeypatch):
    """Headers one byte at a time, each inside the socket timeout: the request
    still ends at REQUEST_DEADLINE_S, and the next session is asked."""
    import socket as socketlib

    monkeypatch.setattr(alertpoll, "REQUEST_DEADLINE_S", 1.0)
    listener = socketlib.socket()
    listener.bind(("127.0.0.1", 0))
    listener.listen(1)
    stop = threading.Event()

    def drip():
        conn, _ = listener.accept()
        with conn:
            conn.recv(65536)
            for byte in b"HTTP/1.1 200 OK\r\nX-Slow: " + b"a" * 100:
                if stop.wait(0.2):
                    return
                try:
                    conn.send(bytes([byte]))
                except OSError:
                    return

    threading.Thread(target=drip, daemon=True).start()
    fetch = alertpoll.Fetcher("0.0.0")
    started = time.monotonic()
    try:
        kind, _ = fetch(alertpoll.Endpoint(f"http://127.0.0.1:{listener.getsockname()[1]}", "k"), SID)
    finally:
        stop.set()
        fetch.close()
        listener.close()
    assert kind == alertpoll.Answer.UNREACHED
    assert time.monotonic() - started < 4.0


def test_the_watch_goes_fast_at_once_and_queues_nothing_behind_a_stuck_look(tmp_path):
    target = mailwatch.Target(SID, str(tmp_path / "probe"))

    async def run():
        loop = asyncio.get_running_loop()
        watch = mailwatch.MailWatch(loop_getter=lambda: loop, emit=lambda *a: None, targets=lambda: {target},
                                    log=lambda m: None)
        watch.changed()
        assert watch._handle.when() > loop.time() + 1.0, "idle: the next look at the idle pace"  # noqa: SLF001
        watch._go_fast()  # noqa: SLF001 -- a change seen, or a new subscription
        assert watch._handle.when() <= loop.time() + mailwatch.WATCH_S + 0.01  # noqa: SLF001
        watch._inflight, watch._inflight_since = 1, time.monotonic() - 10  # noqa: SLF001 -- a hung folder
        assert await watch.baseline() is False
        assert watch._inflight == 1, "nothing queued behind it"  # noqa: SLF001
        watch.close()

    asyncio.run(run())


def test_the_fetcher_keeps_one_connection_and_reads_each_answer(probe_api):
    base = f"http://127.0.0.1:{probe_api.server_address[1]}"
    ep = alertpoll.Endpoint(base, "pk_daemon_test")
    fetch = alertpoll.Fetcher("0.289.0")
    try:
        assert fetch(ep, SID)[0] == alertpoll.Answer.LISTING
        kind, rows = fetch(ep, OTHER)
        assert kind == alertpoll.Answer.LISTING and rows[0]["text"] == f"{OTHER} crashed."
        assert [s["path"] for s in probe_api.seen] == [f"/v1/sessions/{SID}/run-alerts",
                                                       f"/v1/sessions/{OTHER}/run-alerts"]
        assert {s["auth"] for s in probe_api.seen} == {"Bearer pk_daemon_test"}
        assert len({s["peer"] for s in probe_api.seen}) == 1, "one kept connection"
        for status, body, kind in [
            (401, {"detail": "invalid token"}, alertpoll.Answer.REFUSED),
            (403, {"detail": "missing scope read"}, alertpoll.Answer.NONE),
            (403, {"detail": {"message": "the key was revoked"}}, alertpoll.Answer.REFUSED),
            (404, {"detail": "Not Found"}, alertpoll.Answer.NONE),
            (200, {"no": "listing"}, alertpoll.Answer.NONE),
        ]:
            probe_api.answer = lambda path, s=status, b=body: (s, b, {})
            assert fetch(ep, SID)[0] == kind, (status, body)
        probe_api.answer = lambda path: (429, {"detail": "slow down"}, {"Retry-After": "120"})
        assert fetch(ep, SID) == (alertpoll.Answer.LIMITED, 120.0)
    finally:
        fetch.close()
    assert alertpoll.Fetcher("0.0.0")(alertpoll.Endpoint("http://127.0.0.1:1", "k"), SID)[0] == (
        alertpoll.Answer.UNREACHED)


@pytest.mark.parametrize("confined", [False, True])
def test_a_session_registered_from_a_sandbox_is_never_polled_for(tmp_path, monkeypatch, confined):
    """The registrant names the state folder the answers go to: the service
    polls with the user's own key only for one outside any sandbox."""
    from probe.service import caller, server, updater
    from probe.service.registry import Registry

    monkeypatch.setattr(updater, "_hosted_live", updater._hosted_live)  # noqa: SLF001 -- Service sets it
    monkeypatch.setattr(caller, "sandboxed", lambda pid: confined)
    service = server.Service(registry=Registry(tmp_path / "sessions.json"))
    conn = server.Connection(None, peer_pid=os.getpid())
    params = {"sid": SID, "harness": "claude_code", "mode": Mode.DAEMON, "owner": None, "generation": 1,
              "state_dir": str(tmp_path / "probe")}
    assert service._register(conn, params) == {"alive": True}  # noqa: SLF001
    assert service._daemon_sessions() == ([] if confined else [(SID, str(tmp_path / "probe"))])  # noqa: SLF001
    monkeypatch.setattr(caller, "sandboxed", lambda pid: True)
    service._register(conn, params)  # noqa: SLF001 -- a heartbeat from inside a sandbox
    assert service._daemon_sessions() == [], "each register says it again"  # noqa: SLF001


def test_a_restarted_service_polls_again_at_the_sessions_next_heartbeat(home, probe_api, monkeypatch):
    """A restart (an update, an idle stop) brings the sessions back from
    `sessions.json`, unconfirmed: the next register, a heartbeat of the same
    generation, starts the rounds again (review H1)."""
    monkeypatch.setenv("PROBE_SERVICE_ALERT_POLL_S", "0.5")
    config = _config(home.home / ".config" / "probe" / "config.json",
                     f"http://127.0.0.1:{probe_api.server_address[1]}")
    proc, owner = spawn_agent()
    params = {"sid": SID, "harness": "claude_code", "mode": Mode.DAEMON, "owner": owner, "generation": 1,
              "state_dir": str(_state_dir())}
    try:
        _offer(SID, config)
        home.start()
        assert home.call(Method.SESSION_REGISTER, params)["alive"]
        assert wait_for(lambda: mailbox.read_alerts_handoff(SID), 10.0)
        pid = home.status()["pid"]
        home.call(Method.STOP)
        assert home.wait_exit(pid, 5.0)
        mailbox.alerts_handoff_path(SID).unlink()
        home.start()
        assert home.registry_file()["sessions"], "the session came back from sessions.json"
        assert home.call(Method.SESSION_REGISTER, params)["alive"]  # the tap's heartbeat
        assert wait_for(lambda: mailbox.read_alerts_handoff(SID), 10.0), "polled again after the restart"
    finally:
        kill_agent(proc)


def test_the_service_polls_every_daemon_session_once_and_hands_the_answers_over(home, probe_api, monkeypatch):
    monkeypatch.setenv("PROBE_SERVICE_ALERT_POLL_S", "0.5")
    config = _config(home.home / ".config" / "probe" / "config.json",
                     f"http://127.0.0.1:{probe_api.server_address[1]}")
    home.start()
    agents = []
    try:
        for n, sid in enumerate((SID, OTHER, "inline-session")):
            proc, owner = spawn_agent()
            agents.append(proc)
            mode = Mode.INLINE if sid == "inline-session" else Mode.DAEMON
            assert home.call(Method.SESSION_REGISTER, {"sid": sid, "harness": "claude_code", "mode": mode,
                                                       "owner": owner, "generation": n + 1,
                                                       "state_dir": str(_state_dir())})["alive"]
            _offer(sid, config)
        assert wait_for(lambda: mailbox.read_alerts_handoff(SID) and mailbox.read_alerts_handoff(OTHER), 10.0)
        assert mailbox.read_alerts_handoff(SID)["alerts"][0]["text"] == f"{SID} crashed."
        assert mailbox.read_alerts_handoff("inline-session") is None, "only daemon sessions"
        paths = {s["path"] for s in probe_api.seen}
        assert paths == {f"/v1/sessions/{SID}/run-alerts", f"/v1/sessions/{OTHER}/run-alerts"}
        # The worker took its offer back: the service asks for it no more.
        assert mailbox.offer_run_alerts(OTHER, None)
        time.sleep(1.2)
        mark = len(probe_api.seen)
        time.sleep(1.2)
        later = [s["path"] for s in probe_api.seen[mark:]]
        assert later and set(later) == {f"/v1/sessions/{SID}/run-alerts"}
        assert len({s["peer"] for s in probe_api.seen}) <= 2, "kept connections, not one per poll"
    finally:
        for proc in agents:
            kill_agent(proc)


# ---------------------------------------------------------------------------
# The service owns delivery: posts and claims through it, the files the store.
# ---------------------------------------------------------------------------


def _log_entries(sid: str = SID) -> list[dict]:
    path = mailbox.claim_log_path(sid)
    return [json.loads(line) for line in path.read_text().splitlines()] if path.exists() else []


def _context(result: subprocess.CompletedProcess) -> str:
    assert result.returncode == 0, result.stderr
    return json.loads(result.stdout)["hookSpecificOutput"]["additionalContext"] if result.stdout else ""


def _run_payload(hook: Path, payload: dict, **env: str) -> subprocess.CompletedProcess:
    return subprocess.run([sys.executable, str(hook)], input=json.dumps(payload), capture_output=True, text=True,
                          env=_hook_env(**env), timeout=30)


def test_a_worker_posts_through_the_service_and_the_hook_claims_through_it(home):
    home.start()
    ask = mailbox.write_ask(SID, "what LR did the last sweep use?")
    answer = _answer(ask)
    with home.connect() as conn:
        assert _subscribe(conn, [SID]) == {}
        started = time.monotonic()
        assert mailbox.post_via_service(answer), "the service wrote it"
        assert _next(conn, 2.0, Topic.MAILBOX_CHANGED) is not None
        assert time.monotonic() - started < 0.2, "told at once, not at the watch's next look"
    assert [m.id for _, m in mailbox.waiting(SID)] == [answer.id]
    assert _context(_run("UserPromptSubmit")) == answer.rendered()
    (entry,) = _log_entries()
    assert entry["by"] == "UserPromptSubmit" and entry.get("token"), "claimed by the service, for this hook"


def test_a_post_is_the_same_file_however_it_is_written_and_never_twice(home):
    home.start()
    alert = _alert([3])
    assert mailbox.post_via_service(alert)
    mailbox.publish_here(alert)  # a caller that fell back after all: the same file
    mailbox.publish(alert)
    assert [m.id for _, m in mailbox.waiting(SID)] == [alert.id]


def test_a_service_killed_between_post_and_claim_loses_nothing(home):
    import signal

    status = home.start()
    alert = _alert([4])
    assert mailbox.post_via_service(alert)
    os.kill(status["pid"], signal.SIGKILL)
    assert home.wait_exit(status["pid"], 5.0)
    started = time.monotonic()
    assert _context(_run("UserPromptSubmit")) == alert.rendered(), "claimed here, from the file"
    assert time.monotonic() - started < 3.0
    assert [e["id"] for e in _log_entries()] == [alert.id] and "token" not in _log_entries()[0]
    assert _context(_run("UserPromptSubmit")) == "", "and only once"


def test_an_older_worker_writing_beside_the_service_is_delivered_through_it(home):
    home.start()
    alert = _alert([5])
    mailbox.publish_here(alert)  # a worker from before the service owned delivery
    assert _context(_run("UserPromptSubmit")) == alert.rendered()
    assert _log_entries()[0].get("token"), "claimed through the service"


def test_a_hint_and_a_reader_message_through_the_service_both_go_out_once(home):
    """Plan probe-hints R2 on the service's path (`mailbox.post` / `mailbox.claim`
    run the mailbox's own functions): a hint never replaces the reader's message
    nor it the hint, a newer hint replaces the older, the hook hands one of each
    over in one turn, and the claim log says which was the hint."""
    home.start()
    now = time.time()

    def message(text: str, made_at: float, origin: "str | None" = None) -> mailbox.Message:
        return mailbox.Message(id=mailbox.new_message_id(), session=SID, kind=Kind.MESSAGE, text=text,
                               made_at=made_at, origin=origin)

    reader = message("The team's digits-sweep covered C in [0.1, 10].", now - 3)
    old_hint = message("[Probe] an older hint", now - 2, mailbox.ORIGIN_HINT)
    hint = message("[Probe] The team's records near this: Michael, 10-21, RFD4-Proteina.pdf", now - 1,
                   mailbox.ORIGIN_HINT)
    for m in (reader, old_hint, hint):
        assert mailbox.post_via_service(m), "the service wrote it"
    assert sorted(m.id for _, m in mailbox.waiting(SID)) == sorted([reader.id, hint.id])
    assert _context(_run("UserPromptSubmit")) == reader.rendered() + "\n\n" + hint.text
    entries = _log_entries()
    assert {e["id"]: e.get("origin") for e in entries} == {reader.id: None, hint.id: mailbox.ORIGIN_HINT}
    assert all(e.get("token") for e in entries), "claimed through the service"
    assert _context(_run("UserPromptSubmit")) == "", "and only once"


def test_hooks_claiming_through_the_service_and_directly_deliver_each_message_once(home):
    home.start()
    alerts = [_alert([n]) for n in range(10, 16)]
    for alert in alerts:
        mailbox.publish(alert)
    procs = [
        subprocess.Popen([sys.executable, str(HOOK)], stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE, text=True,
                         env=_hook_env(**({"PROBE_HOOK_SERVICE": "off"} if n % 2 else {})))
        for n in range(8)
    ]
    for proc in procs:
        proc.stdin.write(_payload("PostToolUse", tool_name="Bash", tool_input={"command": "ls"},
                                  tool_response={"stdout": ""}, tool_use_id=f"t{id(proc)}"))
        proc.stdin.close()
        proc.stdin = None
    delivered = []
    for proc in procs:
        out, err = proc.communicate(timeout=30)
        assert proc.returncode == 0, err
        if out:
            delivered += json.loads(out)["hookSpecificOutput"]["additionalContext"].split("\n\n")
    assert sorted(delivered) == sorted(a.rendered() for a in alerts), "each once, whoever claimed it"
    assert sorted(e["id"] for e in _log_entries()) == sorted(a.id for a in alerts)


def test_a_stalled_service_never_costs_a_claim_it_made(home):
    """A service that claims and then never answers (stalled, or killed before
    its answer went out): the hook waits out the request's deadline, finds by
    its token what was claimed for it, and delivers that, once."""
    import socket as socketlib

    from probe.service import paths

    answer_ask = mailbox.write_ask(SID, "any OOM on 8xA100?")
    answer = _answer(answer_ask, "no OOM in the last 30 runs")
    mailbox.publish_here(answer)
    sock_path = paths.socket_path()
    server = socketlib.socket(socketlib.AF_UNIX, socketlib.SOCK_STREAM)
    server.bind(str(sock_path))
    server.listen(4)
    tokens: list = []

    def serve():
        while True:
            try:
                conn, _ = server.accept()
            except OSError:
                return
            buf = b""
            with conn:
                while True:
                    chunk = conn.recv(65536)
                    if not chunk:
                        break
                    buf += chunk
                    while b"\n" in buf:
                        line, buf = buf.split(b"\n", 1)
                        req = json.loads(line)
                        if req["method"] == "service.hello":
                            conn.sendall(json.dumps({"jsonrpc": "2.0", "id": req["id"], "result": {}}).encode()
                                         + b"\n")
                        elif req["method"] == "mailbox.claim":
                            p = req["params"]
                            for name in p["names"]:
                                mailbox.claim(SID, mailbox.messages_dir(SID) / name, by=p["by"], token=p["token"])
                            tokens.append(p["token"])  # ...and no answer

    threading.Thread(target=serve, daemon=True).start()
    try:
        started = time.monotonic()
        result = _run("UserPromptSubmit")
        took = time.monotonic() - started
    finally:
        server.close()
        os.unlink(sock_path)
    assert _context(result) == answer.rendered()
    assert tokens and [e.get("token") for e in _log_entries()] == tokens, "claimed once, by the stalled service"
    assert took < 5.0


def test_a_post_past_its_deadline_writes_nothing_and_a_bad_one_is_refused(home):
    home.start()
    alert = _alert([6])
    from dataclasses import asdict

    late = home.call(Method.MAILBOX_POST, {"sid": SID, "state_dir": str(_state_dir()), "message": asdict(alert),
                                           "deadline": time.time() - 1})
    assert late == {"posted": None, "late": True}
    assert mailbox.waiting(SID) == []
    for bad in ({**asdict(alert), "session": OTHER}, {**asdict(alert), "id": "../../escape"}):
        with pytest.raises(client.ServiceError) as err:
            home.call(Method.MAILBOX_POST, {"sid": SID, "state_dir": str(_state_dir()), "message": bad})
        assert err.value.code == ErrorCode.INVALID_PARAMS
    with pytest.raises(client.ServiceError):
        home.call(Method.MAILBOX_CLAIM, {"sid": SID, "names": ["../x.json"], "by": "x", "token": "t"})


def test_a_caller_in_a_sandbox_writes_and_claims_its_mailbox_itself(tmp_path, monkeypatch):
    from probe.service import caller

    server, service = _bare_service(tmp_path, monkeypatch)
    monkeypatch.setattr(caller, "sandboxed", lambda pid: True)
    conn = server.Connection(None, peer_pid=os.getpid())
    from dataclasses import asdict

    params = {"sid": SID, "state_dir": str(tmp_path / "probe"), "message": asdict(_alert())}
    with pytest.raises(RpcError) as err:
        asyncio.run(service._mailbox_post(conn, params))  # noqa: SLF001
    assert err.value.code == ErrorCode.REFUSED
    service.mailhost.close()


def test_a_held_question_is_posted_through_the_service_and_its_watchers_told(home):
    home.start()
    board = appr.Board()
    with home.connect() as conn:
        assert _subscribe(conn, [SID], topics=(Topic.APPROVALS_CHANGED,)) == {}
        started = time.monotonic()
        board.file(_question(SID, "q7"))
        assert _next(conn, 2.0, Topic.APPROVALS_CHANGED) == {"topic": Topic.APPROVALS_CHANGED, "sid": SID,
                                                              "ids": ["q7"]}
        assert time.monotonic() - started < 0.2
    assert board.get("q7").session_id == SID


def _ask_the_question(rid: str, choice: str) -> None:
    q = _question(SID, rid).question
    tool_input = {"questions": [{"header": q.header, "question": q.question, "multiSelect": False,
                                 "options": [{"label": q.yes_label, "description": ""},
                                             {"label": q.no_label, "description": ""}]}]}
    base = {"session_id": SID, "cwd": "/tmp", "tool_name": "AskUserQuestion", "tool_input": tool_input,
            "tool_use_id": f"tu-{rid}"}
    assert _run_payload(APPROVALS_HOOK, {**base, "hook_event_name": "PreToolUse"}).stdout == ""
    done = _run_payload(APPROVALS_HOOK, {**base, "hook_event_name": "PostToolUse",
                                         "tool_response": {"answers": {q.question: choice}}})
    assert done.returncode == 0, done.stderr


def _claim_request(path: Path, budget: float, token: str = "tok1") -> dict:
    from probe.service import protocol

    request = protocol.need_mailbox_claim({"sid": SID, "state_dir": str(_state_dir()), "names": [path.name],
                                           "by": "PostToolUse", "token": token, "budget": budget})
    request["state"] = request["state_dir"]
    return request


def test_a_step_that_started_is_waited_for_and_never_answered_late(tmp_path, monkeypatch):
    """A slow disk: the rename is done, the claimed file's read and the log line
    are not when the wait runs out. The answer waits for the step and carries
    the claim (review: `late` used to drop it, and the hook's own claim then
    found the file gone)."""
    from probe.service.mailhost import MailHost

    monkeypatch.setenv("XDG_STATE_HOME", str(tmp_path))
    path = mailbox.publish_here(_alert([21]))
    real = mailbox._read_json  # noqa: SLF001
    monkeypatch.setattr(mailbox, "_read_json", lambda p: (time.sleep(0.5), real(p))[1])

    async def run():
        host = MailHost(log=lambda m: None)
        try:
            return await host.run(MailHost.claim, _claim_request(path, 0.1))
        finally:
            host.close()

    answer = asyncio.run(run())
    assert [row["name"] for row in answer["claimed"]] == [path.name]
    assert (mailbox.claimed_dir(SID) / f"{path.stem}.tok1.json").exists(), "claimed for the request, its receipt pending"


def test_a_step_never_started_by_its_deadline_is_taken_back_and_one_stuck_turns_the_rest_away(tmp_path,
                                                                                              monkeypatch):
    from probe.service import mailhost
    from probe.service.mailhost import MailHost

    monkeypatch.setenv("XDG_STATE_HOME", str(tmp_path))
    monkeypatch.setattr(mailhost, "STUCK_S", 0.3)
    path = mailbox.publish_here(_alert([22]))
    release = threading.Event()

    def stuck(request):
        release.wait(10)
        return {}

    async def run():
        host = MailHost(log=lambda m: None)
        try:
            blocker = asyncio.ensure_future(host.run(stuck, {"deadline_mono": time.monotonic() + 5}))
            await asyncio.sleep(0.05)
            queued = await host.run(MailHost.claim, _claim_request(path, 0.05))
            await asyncio.sleep(0.4)
            started = time.monotonic()
            refused = await host.run(MailHost.claim, _claim_request(path, 0.5, "tok2"))
            took = time.monotonic() - started
            release.set()
            await blocker
            return queued, refused, took
        finally:
            host.close()

    queued, refused, took = asyncio.run(run())
    assert queued == {"late": True}, "taken back from the queue: nothing was done"
    assert refused is None and took < 0.1, "behind a stuck step: turned away at once, nothing queued"
    assert [m.id for _, m in mailbox.waiting(SID)] == [mailbox.alert_message_id([22])], "still there to claim"


def test_a_planted_fifo_in_a_mailbox_is_no_message_and_blocks_no_read(tmp_path, monkeypatch):
    monkeypatch.setenv("XDG_STATE_HOME", str(tmp_path))
    mailbox.publish_here(_alert([23]))
    os.mkfifo(mailbox.messages_dir(SID) / "00000000000000000001-mfifo.json")
    assert [m.id for _, m in _in_time(mailbox.waiting, SID)] == [mailbox.alert_message_id([23])]


def test_a_service_that_does_not_answer_is_left_alone_for_a_while(home, monkeypatch):
    """The worker's loop pays a stalled service's wait once, not on every message."""
    import socket as socketlib

    from probe.service import paths

    monkeypatch.setattr(mailbox, "POST_WAIT_S", 0.2)
    monkeypatch.setattr(mailbox, "POST_GRACE_S", 0.1)
    monkeypatch.setattr(mailbox, "_service_quiet_until", 0.0)
    sock_path = paths.socket_path()
    server = socketlib.socket(socketlib.AF_UNIX, socketlib.SOCK_STREAM)
    server.bind(str(sock_path))
    server.listen(8)

    def serve():
        while True:
            try:
                conn, _ = server.accept()
            except OSError:
                return
            data = conn.recv(65536)
            req = json.loads(data.split(b"\n", 1)[0])
            conn.sendall(json.dumps({"jsonrpc": "2.0", "id": req["id"], "result": {}}).encode() + b"\n")
            # ...and the post itself is never answered.

    threading.Thread(target=serve, daemon=True).start()
    try:
        started = time.monotonic()
        mailbox.publish(_alert([24]))
        first = time.monotonic() - started
        started = time.monotonic()
        mailbox.publish(_alert([25]))
        second = time.monotonic() - started
    finally:
        server.close()
        os.unlink(sock_path)
    assert first >= 0.3, "waited out the deadline before writing it here"
    assert second < 0.1, "then asked the service nothing"
    assert len(mailbox.waiting(SID)) == 2


def test_a_board_outside_its_state_folder_is_filed_where_it_is(home, tmp_path):
    home.start()
    board = appr.Board(tmp_path / "board")
    board.file(_question(SID, "q9"))
    assert board.get("q9") is not None


def test_the_sooner_of_the_deadline_and_the_budget_holds(monkeypatch):
    from probe.service import protocol

    base = {"sid": SID, "names": ["1-a.json"], "by": "x", "token": "t"}
    soon = protocol.need_mailbox_claim({**base, "deadline": time.time() + 30, "budget": 0.5})["deadline_mono"]
    assert soon - time.monotonic() < 0.6, "a clock stepped back is held by the budget"
    late = protocol.need_mailbox_claim({**base, "deadline": time.time() + 0.5, "budget": 30})["deadline_mono"]
    assert late - time.monotonic() < 0.6, "a request that arrives late is held by the deadline"
    capped = protocol.need_mailbox_claim({**base, "budget": 999})["deadline_mono"]
    assert capped - time.monotonic() <= protocol.MAX_MAILBOX_WAIT_S


def _hook_against(host, loop, state: str):
    """reads_hook loaded in-process, its line to the service replaced by one to
    `host` (a MailHost on `loop`) that keeps the hook's own timeouts."""
    import importlib.util

    from probe.service import protocol

    spec = importlib.util.spec_from_file_location("_reads_hook_q2", HOOK)
    hook = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(hook)

    class Failed(Exception):
        def __init__(self, message, *, answered):
            super().__init__(message)
            self.answered = answered

    class Rpc:
        @classmethod
        def connect(cls):
            return cls()

        def call(self, method, params, *, timeout):
            from probe.service.mailhost import MailHost

            request = protocol.need_mailbox_claim(params)
            request["state"] = state
            future = asyncio.run_coroutine_threadsafe(host.run(MailHost.claim, request), loop)
            try:
                return future.result(timeout)
            except Exception:  # noqa: BLE001 -- what the real Rpc raises on a timeout
                raise Failed("no answer in time", answered=False) from None

        def close(self):
            return None

    hook._rpc = lambda: type("M", (), {"Rpc": Rpc})
    return hook


def test_a_claim_still_running_when_the_hook_gives_up_is_still_delivered_once(tmp_path, monkeypatch):
    """The claimed file's read stalls 1.5 s on the service (renamed, not read
    yet) and the hook's own wait (1.2 s) runs out: the service logged its token
    right after the rename, so the hook finds the claim and delivers it, once
    (review: the hook used to come back empty and the message sat in claimed/)."""
    from probe.service.mailhost import MailHost

    monkeypatch.setenv("XDG_STATE_HOME", str(tmp_path))
    path = mailbox.publish_here(_alert([31]))
    real = mailbox._read_json  # noqa: SLF001

    def slow(p):
        if "/claimed/" in str(p):
            time.sleep(1.5)
        return real(p)

    monkeypatch.setattr(mailbox, "_read_json", slow)
    loop = asyncio.new_event_loop()
    threading.Thread(target=loop.run_forever, daemon=True).start()
    host = MailHost(log=lambda m: None)
    try:
        hook = _hook_against(host, loop, str(tmp_path / "probe"))
        got = hook.claim_all(SID, [path], "PostToolUse")
    finally:
        host.close()
        loop.call_soon_threadsafe(loop.stop)
    assert [m["id"] for m in got.values()] == [mailbox.alert_message_id([31])]
    time.sleep(1.6)
    assert [e["id"] for e in _log_entries()] == [mailbox.alert_message_id([31])], "claimed once"


def test_a_service_killed_between_its_claim_and_its_log_line_still_delivers_once(tmp_path, monkeypatch):
    """(a) The service dies right after its rename, before the claim-log line:
    the file's name says whom it was claimed for, and the hook that lost the
    answer takes it by that name, shows it once, and writes the ledger line."""
    from probe.service.mailhost import MailHost

    monkeypatch.setenv("XDG_STATE_HOME", str(tmp_path))
    path = mailbox.publish_here(_alert([41]))

    def killed(*args, **kwargs):
        raise SystemExit("killed between the rename and the log line")

    monkeypatch.setattr(mailbox, "_log_claim", killed)
    loop = asyncio.new_event_loop()
    threading.Thread(target=loop.run_forever, daemon=True).start()
    host = MailHost(log=lambda m: None)
    try:
        hook = _hook_against(host, loop, str(tmp_path / "probe"))
        got = hook.claim_all(SID, [path], "PostToolUse")
    finally:
        host.close()
        loop.call_soon_threadsafe(loop.stop)
    assert [m["id"] for m in got.values()] == [mailbox.alert_message_id([41])]
    assert sorted(p.name for p in mailbox.claimed_dir(SID).glob("*.json")) == [path.name], "received: the plain name"
    assert [e["id"] for e in _log_entries()] == [mailbox.alert_message_id([41])], "the ledger has it once"
    assert hook.claim_all(SID, [path], "PostToolUse") == {} and hook.deliver_orphans(SID, "x") == []


def _orphan_claim(path: Path, *, age_s: float, token_rest: str = "late") -> Path:
    """A service rename that landed after its caller had given up: the message
    sits under a token whose deadline is `age_s` gone."""
    token = "%d_%s" % (int((time.time() - age_s) * 1000), token_rest)
    claimed = mailbox.claimed_dir(SID) / f"{path.stem}.{token}.json"
    claimed.parent.mkdir(parents=True, exist_ok=True)
    os.rename(path, claimed)
    return claimed


def test_a_service_claim_that_lands_after_its_caller_gave_up_is_delivered_next_time_once(tmp_path, monkeypatch):
    """(b) The hook fell back and finished (the file was gone when it looked);
    the service's rename landed after. The next deliverer, service or not,
    delivers it once, and not before its caller could still have taken it."""
    import importlib.util

    monkeypatch.setenv("XDG_STATE_HOME", str(tmp_path))
    monkeypatch.setenv("PROBE_HOOK_SERVICE", "off")
    spec = importlib.util.spec_from_file_location("_reads_hook_orphans", HOOK)
    hook = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(hook)
    a42 = _alert([42])
    fresh = _orphan_claim(mailbox.publish_here(a42), age_s=0.0, token_rest="fresh")
    assert hook.deliver_orphans(SID, "PostToolUse") == [], "its caller may still take it"
    _orphan_claim(mailbox.publish_here(_alert([43])), age_s=5.0)
    (msg,) = hook.deliver_orphans(SID, "PostToolUse")
    assert msg["id"] == mailbox.alert_message_id([43])
    assert hook.deliver_orphans(SID, "PostToolUse") == [], "once"
    assert fresh.exists() and [e["id"] for e in _log_entries()] == [msg["id"]]
    assert mailbox.claimed_ids(SID) == {mailbox.alert_message_id([42]), mailbox.alert_message_id([43])}
    assert set(mailbox.alert_paths(SID)) == mailbox.claimed_ids(SID), "ids read back from either name"
    mailbox.publish(a42)
    assert mailbox.waiting(SID) == [], "a claimed message, receipt pending, is never published again"


def test_two_deliverers_on_one_orphan_show_it_once(home):
    """(c) Eight hooks at once over one orphaned service claim: the receipt
    rename picks one."""
    alert = _alert([44])
    _orphan_claim(mailbox.publish_here(alert), age_s=5.0)
    procs = [subprocess.Popen([sys.executable, str(HOOK)], stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE, text=True, env=_hook_env(PROBE_HOOK_SERVICE="off"))
             for _ in range(8)]
    for n, proc in enumerate(procs):
        proc.stdin.write(_payload("PostToolUse", tool_name="Bash", tool_input={"command": "ls"},
                                  tool_response={"stdout": ""}, tool_use_id=f"t{n}"))
        proc.stdin.close()
        proc.stdin = None
    shown = []
    for proc in procs:
        out, err = proc.communicate(timeout=30)
        assert proc.returncode == 0, err
        if out:
            shown.append(json.loads(out)["hookSpecificOutput"]["additionalContext"])
    assert shown == [alert.rendered()]
    assert [e["id"] for e in _log_entries()] == [alert.id]


def _route(plugin: str, event: str) -> str:
    """The reads route's command for `event`, as `routes.json` gives it to the harness."""
    hooks = json.loads((AGENT_ROOT / "plugins" / plugin / "hooks" / "routes.json").read_text())["hooks"]
    (command,) = [h["command"] for group in hooks.get(event, []) for h in group["hooks"]
                  if "reads_hook.py" in h["command"]]
    return command


@pytest.mark.parametrize("plugin", ["probe-research", "probe-research-daemon"])
@pytest.mark.parametrize("event", ["UserPromptSubmit", "PostToolUse"])
@pytest.mark.parametrize("named", [True, False], ids=["session-id", "no-session-id"])
def test_an_orphaned_claim_alone_still_reaches_the_agent_through_the_real_route(tmp_path, monkeypatch, plugin,
                                                                                event, named):
    """Codex P2 on 90f86ead6: with nothing in messages/ and no status change,
    the route's shell fast path exited before Python, and a service claim whose
    caller gave up sat for the rest of the task (Codex has no Stop wake)."""
    monkeypatch.setenv("XDG_STATE_HOME", str(tmp_path))
    alert = _alert([51])
    _orphan_claim(mailbox.publish_here(alert), age_s=5.0)
    env = {"PATH": os.environ.get("PATH", "/usr/bin:/bin"), "HOME": str(tmp_path / "home"),
           "XDG_STATE_HOME": str(tmp_path), "CLAUDE_PLUGIN_ROOT": str(AGENT_ROOT / "plugins" / plugin),
           "PROBE_HOOK_SERVICE": "off"}
    if named:
        env["CLAUDE_CODE_SESSION_ID"] = SID
    payload = {"hook_event_name": event, "session_id": SID, "cwd": "/tmp"}
    if event == "PostToolUse":
        payload.update(tool_name="Bash", tool_input={"command": "ls"}, tool_response={"stdout": ""}, tool_use_id="t1")
    done = subprocess.run(["/bin/bash", "-c", _route(plugin, event)], input=json.dumps(payload),
                          capture_output=True, text=True, env=env, timeout=30)
    assert done.returncode == 0, done.stderr
    assert _context(done) == alert.rendered()


def test_the_dispatchers_reads_gate_passes_for_an_orphaned_claim(tmp_path, monkeypatch):
    """dispatch.py's copy of the post-tool fast path (`reads_waiting`)."""
    import importlib.util

    monkeypatch.setenv("XDG_STATE_HOME", str(tmp_path))
    spec = importlib.util.spec_from_file_location("_dispatch_q2", HOOK.parent / "dispatch.py")
    dispatch = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(dispatch)
    _orphan_claim(mailbox.publish_here(_alert([52])), age_s=5.0)
    monkeypatch.setenv("CLAUDE_CODE_SESSION_ID", SID)
    assert dispatch.reads_waiting()
    monkeypatch.delenv("CLAUDE_CODE_SESSION_ID")
    monkeypatch.delenv("CODEX_THREAD_ID", raising=False)
    assert dispatch.reads_waiting(), "no session id: any session's"


def test_a_receipt_between_a_publish_retrys_looks_never_brings_a_message_back(tmp_path, monkeypatch):
    """Codex P2 on 90f86ead6: a retry of a post checked messages/ and the plain
    claimed name, the hook's receipt then renamed the token claim to the plain
    name, the retry's token look found nothing, and it published again: shown
    twice. The receipt is forced in exactly there."""
    import pathlib

    monkeypatch.setenv("XDG_STATE_HOME", str(tmp_path))
    alert = _alert([53])
    token_claim = _orphan_claim(mailbox.publish_here(alert), age_s=0.0, token_rest="mid")
    real_glob = pathlib.Path.glob

    def glob(self, pattern, *args, **kwargs):
        if self == mailbox.claimed_dir(SID) and pattern.startswith(token_claim.name.split(".", 1)[0]):
            if token_claim.exists():
                os.rename(token_claim, mailbox.claimed_dir(SID) / f"{token_claim.name.split('.', 1)[0]}.json")
        return real_glob(self, pattern, *args, **kwargs)

    monkeypatch.setattr(pathlib.Path, "glob", glob)
    mailbox.publish_here(alert)  # the retry
    monkeypatch.setattr(pathlib.Path, "glob", real_glob)
    assert mailbox.waiting(SID) == [], "never published again: it was delivered"


def test_a_claim_token_never_carries_a_dot_or_a_path(tmp_path, monkeypatch):
    from probe.service import protocol

    monkeypatch.setenv("XDG_STATE_HOME", str(tmp_path))
    path = mailbox.publish_here(_alert([45]))
    for bad in ("a.b", "../x", "a/b", ""):
        with pytest.raises(ValueError):
            mailbox.claim(SID, path, by="x", token=bad)
        with pytest.raises(RpcError):
            protocol.need_mailbox_claim({"sid": SID, "names": [path.name], "by": "x", "token": bad})
    assert path.exists(), "nothing was claimed"


def test_a_post_that_runs_past_its_deadline_writes_nothing(tmp_path, monkeypatch):
    """Its caller writes it then: the service's own write never lands after it
    (review: it could, and a hook claiming in between saw it twice)."""
    from dataclasses import asdict

    from probe.service import protocol
    from probe.service.mailhost import MailHost

    monkeypatch.setenv("XDG_STATE_HOME", str(tmp_path))
    alert = _alert([32])
    real = mailbox._file_name  # noqa: SLF001
    monkeypatch.setattr(mailbox, "_file_name", lambda msg: (time.sleep(0.3), real(msg))[1])
    request = protocol.need_mailbox_post({"sid": SID, "state_dir": str(tmp_path / "probe"),
                                          "message": asdict(alert), "budget": 0.1})
    request["state"] = request["state_dir"]
    assert MailHost.post(request) == {"posted": None, "late": True}
    assert mailbox.waiting(SID) == [] and mailbox.claimed_ids(SID) == set()


def test_a_post_past_its_deadline_deletes_nothing_either(tmp_path, monkeypatch):
    """A stalled post of unasked message U2, whose worker since wrote U2 and a
    newer U3 itself: the step must not delete U3 as U2's replacement (review)."""
    from dataclasses import asdict

    from probe.service import protocol
    from probe.service.mailhost import MailHost

    monkeypatch.setenv("XDG_STATE_HOME", str(tmp_path))

    def unasked(text: str, at: float) -> mailbox.Message:
        return mailbox.Message(id=mailbox.new_message_id(), session=SID, kind=Kind.MESSAGE, text=text, made_at=at)

    u2, u3 = unasked("u2", time.time()), unasked("u3", time.time() + 1)
    mailbox.publish_here(u3)  # the worker's own, after it gave up on the service
    real = mailbox._read_json  # noqa: SLF001
    monkeypatch.setattr(mailbox, "_read_json", lambda p: (time.sleep(0.3), real(p))[1])
    request = protocol.need_mailbox_post({"sid": SID, "state_dir": str(tmp_path / "probe"),
                                          "message": asdict(u2), "budget": 0.1})
    request["state"] = request["state_dir"]
    assert MailHost.post(request) == {"posted": None, "late": True}
    assert [m.id for _, m in mailbox.waiting(SID)] == [u3.id], "the newest unasked message is still there"


def test_a_held_question_already_on_the_board_is_never_written_over(tmp_path, monkeypatch):
    from probe.service import protocol
    from probe.service.mailhost import MailHost

    monkeypatch.setenv("XDG_STATE_HOME", str(tmp_path))
    board = appr.Board()
    question = _question(SID, "q10")
    board.save(question)
    board.resolve(question, state=appr.DENIED, outcome="no")  # the worker moved on
    request = protocol.need_mailbox_post({"sid": SID, "state_dir": str(tmp_path / "probe"),
                                          "question": _question(SID, "q10").to_json()})
    request["state"] = request["state_dir"]
    assert MailHost.post(request)["posted"] == "q10"
    assert board.get("q10").state == appr.DENIED, "not asked again"


def test_the_researchers_pick_is_recorded_with_and_without_a_service(maybe_service, home):
    board = appr.Board()
    board.save(_question(SID, "q8"))
    _ask_the_question("q8", "Delete it")
    assert board.take_answer("q8")["answer"] == appr.YES
    # Written by `Board.answer` (the service's step: indented JSON) or by the hook itself (one line).
    written = (board.root / "answers" / "q8.json").read_text()
    assert ("\n" in written.strip()) is maybe_service
