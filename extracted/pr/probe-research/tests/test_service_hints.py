"""The Probe service's hint lane (Probe hints T3, `probe.service.hints`).

The lane is run in-process with fake clocks and a stand-in for `/v1/hints`
(a transport that records each request and answers from a script), against
real files: Claude Code transcripts the daemon's adapter parses, the reads
mailbox the hint is posted to, the plugin's reads hook that hands it over,
and a daemon worker's store for the ML gate's facts. One test runs the lane's
own threads end to end.
"""

from __future__ import annotations

import contextlib
import dataclasses
import json
import os
import re
import sqlite3
import subprocess
import sys
import threading
import time
from datetime import datetime, timezone
from pathlib import Path
from types import SimpleNamespace

import pytest

from probe.daemon import mailbox
from probe.daemon.events import PEER_TOOL, Event, Kind
from probe.service import hints, recorders
from probe.service.alertpoll import Endpoint
from probe.service.protocol import Mode
from probe.service.registry import Session

pytestmark = pytest.mark.skipif(os.name != "posix", reason="the service is POSIX-only until R3")

AGENT_ROOT = Path(__file__).resolve().parents[1]
READS_HOOK = AGENT_ROOT / "plugins" / "probe-research" / "hooks" / "reads_hook.py"
SID = "11111111-2222-3333-4444-555555555555"
OTHER = "99999999-8888-7777-6666-555555555555"
PEER = "abcdefab-0000-1111-2222-333333333333"
OLD_PEER = "fedcba98-0000-1111-2222-333333333333"
SOCKET = "/run/user/1000/cc-socks/1068870.sock"
OLD_SOCKET = "/tmp/cc-socks/11957.sock"
VERSION = "0.297.0"
SHADOW = {"mode": "shadow", "fire": False, "reason": "below_cutoff", "top_score": 0.61, "records": []}


def _on(hint: str = "[Probe] Team records near this:\n- Michael, 10-21, RFD4-Proteina review", *records) -> dict:
    records = records or ({"doc_id": "doc-1", "date": "10-21", "kind": "page"},)
    return {"mode": "on", "fire": True, "hint": hint, "reason": "ok", "top_score": 0.81, "records": list(records)}


class Clock:
    def __init__(self) -> None:
        self.now = 1000.0

    def __call__(self) -> float:
        return self.now


class Api:
    """`/v1/hints`: records each request, answers from `script` (then `default`)."""

    def __init__(self, default=(200, SHADOW)) -> None:
        self.bodies: list[dict] = []
        self.keys: list[str] = []
        self.script: list = []
        self.default = default

    def __call__(self, ep: Endpoint, body: dict):
        self.bodies.append(json.loads(json.dumps(body)))
        self.keys.append(ep.key)
        answer = self.script.pop(0) if self.script else self.default
        if isinstance(answer, BaseException):
            raise answer
        return answer


@pytest.fixture
def state(tmp_path, monkeypatch) -> Path:
    """The session's `<XDG_STATE_HOME>/probe` (the reads hook finds its mailbox there)."""
    monkeypatch.setenv("XDG_STATE_HOME", str(tmp_path / "xdg"))
    folder = tmp_path / "xdg" / "probe"
    folder.mkdir(parents=True)
    return folder


def _session(tmp_path: Path, state: Path, sid: str = SID, mode: str = Mode.INLINE, **env) -> hints.Followed:
    cwd = tmp_path / "project"
    cwd.mkdir(exist_ok=True)
    return hints.Followed(sid=sid, harness="claude_code", mode=mode, state=str(state), cwd=str(cwd),
                          transcript=str(tmp_path / f"{sid}.jsonl"), transcript_dir=None, env=dict(env))


def _lane(tmp_path: Path, sessions: list, api: Api, clock: Clock | None = None, **kw) -> tuple[hints.HintLane, list]:
    logs: list[str] = []
    kw.setdefault("senders", hints.Senders(sessions_dir=lambda env: tmp_path / "claude" / "sessions"))
    lane = hints.HintLane(sessions=lambda: sessions, log=logs.append, version=VERSION, environ={}, transport=api,
                          endpoint_of=lambda env: Endpoint("https://api.example.test", "pk_read"),
                          ledger_dir=tmp_path / "ledger", clock=clock or Clock(), poll_s=0.05, **kw)
    return lane, logs


def _claude_session(tmp_path: Path, pid: int, sid: str, socket: str | None) -> None:
    """Claude Code's record of a running session (`~/.claude/sessions/<pid>.json`)."""
    folder = tmp_path / "claude" / "sessions"
    folder.mkdir(parents=True, exist_ok=True)
    record = {"pid": pid, "sessionId": sid, "cwd": "/work", "startedAt": 1}
    if socket is not None:
        record["messagingSocketPath"] = socket
    (folder / f"{pid}.json").write_text(json.dumps(record))


def _stamp(ago: float = 0.0) -> str:
    return datetime.fromtimestamp(time.time() - ago, tz=timezone.utc).isoformat().replace("+00:00", "Z")


def _user(text: str, cwd: str, ago: float = 0.0) -> dict:
    return {"type": "user", "message": {"role": "user", "content": text}, "timestamp": _stamp(ago), "cwd": cwd,
            "sessionId": SID}


def _tool(name: str, tool_input: dict, cwd: str) -> dict:
    return {"type": "assistant", "timestamp": _stamp(), "cwd": cwd, "sessionId": SID,
            "message": {"role": "assistant", "content": [{"type": "tool_use", "id": "toolu_1", "name": name,
                                                          "input": tool_input}]}}


def _append(session: hints.Followed, *lines: dict) -> None:
    with open(session.transcript, "a", encoding="utf-8") as out:
        for line in lines:
            out.write(json.dumps(line) + "\n")


def _seen(lane: hints.HintLane, session: hints.Followed) -> None:
    """The lane's first look at the session (its transcript empty): on from here."""
    Path(session.transcript).touch()
    lane.read_once()


def _waiting(session: hints.Followed) -> list:
    with mailbox.rooted(session.state):
        return [msg for _path, msg in mailbox.waiting(session.sid)]


def _hook(event: str, tmp_path: Path, sid: str = SID) -> subprocess.CompletedProcess:
    payload = {"hook_event_name": event, "session_id": sid, "cwd": str(tmp_path), "permission_mode": "default",
               "transcript_path": str(tmp_path / f"{sid}.jsonl")}
    env = {"PATH": os.environ.get("PATH", "/usr/bin:/bin"), "HOME": os.environ["HOME"],
           "XDG_STATE_HOME": os.environ["XDG_STATE_HOME"], "PROBE_READS_SERVICE": "off"}
    return subprocess.run([sys.executable, str(READS_HOOK)], input=json.dumps(payload), capture_output=True,
                          text=True, env=env, timeout=30)


# ---------------------------------------------------------------------------
# Triggers, read from a transcript with the daemon's adapter.
# ---------------------------------------------------------------------------


def test_a_researcher_prompt_asks_with_trigger_prompt(tmp_path, state):
    session = _session(tmp_path, state)
    api = Api()
    lane, logs = _lane(tmp_path, [session], api)
    _seen(lane, session)
    _append(session, _user("benchmark NVIDIA RFD4-Proteina on our set", session.cwd))
    lane.read_once()
    assert lane.run_due() == 1
    assert api.bodies == [{
        "text": "benchmark NVIDIA RFD4-Proteina on our set", "trigger": "prompt", "session_id": SID,
        "exclude_session_ids": [], "exclude_doc_ids": [], "ml": None,
        "client": {"harness": "claude_code", "mode": "inline", "cli": VERSION},
    }]
    assert api.keys == ["pk_read"]
    line = [m for m in logs if m.startswith(f"hints: session {SID} prompt")]
    assert line and "mode=shadow fire=False reason=below_cutoff top=0.610" in line[0]
    assert "RFD4" not in "".join(logs), "the log never carries the text"


def _cross_session(socket: str, name: str, body: str) -> str:
    return (f'<cross-session-message from="uds:{socket}" from-name="{name}" from-mode="prompting">\n'
            f"{body}\n</cross-session-message>")


def test_another_sessions_message_asks_with_trigger_peer_and_excludes_its_session(tmp_path, state):
    """Both shapes Claude Code writes (lane B's adapter, its fixtures' lines):
    queued while the agent worked, and a `user` line while it was idle. The
    sender is found from its socket: by the path its record names, or by the
    socket's pid in a build that records no path."""
    _claude_session(tmp_path, 2222, PEER, SOCKET)  # a record named for another pid: found by its path
    _claude_session(tmp_path, 11957, OLD_PEER, None)  # an older build: found by the socket's pid
    session = _session(tmp_path, state)
    api = Api()
    clock = Clock()
    lane, _ = _lane(tmp_path, [session], api, clock)
    _seen(lane, session)
    body = "Benchmark NVIDIA RFD4-Proteina on the held-out set."
    origin = {"kind": "peer", "from": f"uds:{SOCKET}", "name": "Unconditional Generation", "body": body}
    _append(session, {"type": "attachment", "timestamp": _stamp(), "cwd": session.cwd, "isSidechain": False,
                      "attachment": {"type": "queued_command", "commandMode": "prompt", "isMeta": True,
                                     "origin": origin, "prompt": _cross_session(SOCKET, "Unconditional Generation",
                                                                                body)}})
    lane.read_once()
    lane.run_due()
    clock.now += hints.SESSION_GAP_S
    idle = {"kind": "peer", "from": f"uds:{OLD_SOCKET}", "name": "Eval runner", "body": "the eval finished"}
    _append(session, {"type": "user", "isMeta": True, "origin": idle, "timestamp": _stamp(), "cwd": session.cwd,
                      "isSidechain": False, "message": {"role": "user", "content": (
                          "Another Claude session sent a message:\n"
                          + _cross_session(OLD_SOCKET, "Eval runner", "the eval finished"))}})
    lane.read_once()
    lane.run_due()
    assert [(b["trigger"], b["text"], b["exclude_session_ids"]) for b in api.bodies] == [
        ("peer", body, [PEER]), ("peer", "the eval finished", [OLD_PEER])]


def test_a_helper_agents_report_asks_as_a_peer_and_excludes_nothing_it_cannot_name(tmp_path, state):
    session = _session(tmp_path, state)
    api = Api()
    lane, _ = _lane(tmp_path, [session], api)
    _seen(lane, session)
    report = "#2262 is ready for review: head 02a0b92fd."
    origin = {"kind": "peer", "from": "a3a576ef6cb57568e", "name": "general-purpose", "body": report}
    _append(session, {"type": "attachment", "timestamp": _stamp(), "cwd": session.cwd, "isSidechain": False,
                      "attachment": {"type": "queued_command", "commandMode": "prompt", "isMeta": True,
                                     "origin": origin, "prompt": (f'<agent-message from="a3a576ef6cb57568e">\n'
                                                                  f"{report}\n</agent-message>")}})
    lane.read_once()
    lane.run_due()
    assert [(b["trigger"], b["text"], b["exclude_session_ids"]) for b in api.bodies] == [("peer", report, [])]


def test_a_sender_is_found_once_and_an_unreadable_record_finds_nothing(tmp_path):
    folder = tmp_path / "claude" / "sessions"
    _claude_session(tmp_path, 1068870, PEER, SOCKET)
    clock = Clock()
    senders = hints.Senders(sessions_dir=lambda env: folder, clock=clock)
    assert senders.resolve(f"uds:{SOCKET}", {}) == PEER
    (folder / "1068870.json").unlink()
    assert senders.resolve(f"uds:{SOCKET}", {}) == PEER, "remembered"
    clock.now += hints.SENDER_KEEP_S
    assert senders.resolve(f"uds:{SOCKET}", {}) is None, "gone, and looked for again"
    assert senders.resolve(PEER, {}) == PEER, "a session id is one"
    assert senders.resolve("a3a576ef6cb57568e", {}) is None and senders.resolve("/root/review_api", {}) is None
    (folder / "4242.json").mkdir()
    (folder / "5151.json").write_text("{not json")
    (folder / "6161.json").write_text(json.dumps({"sessionId": "not-a-uuid", "messagingSocketPath": "/x/6161.sock"}))
    _claude_session(tmp_path, 7171, PEER, "/elsewhere/7171.sock")
    for address in ("/s/4242.sock", "/s/5151.sock", "/x/6161.sock", "/s/7171.sock", "/s/9999.sock"):
        assert senders.resolve(f"uds:{address}", {}) is None, address
    missing = hints.Senders(sessions_dir=lambda env: tmp_path / "nowhere")
    assert missing.resolve(f"uds:{SOCKET}", {}) is None


def test_claude_codes_session_records_follow_the_sessions_config_dir(tmp_path):
    assert hints.claude_sessions_dir({"HOME": "/home/u"}) == Path("/home/u/.claude/sessions")
    assert hints.claude_sessions_dir({"HOME": "/home/u", "CLAUDE_CONFIG_DIR": "/c"}) == Path("/c/sessions")


def test_a_peer_sender_is_read_from_its_event():
    named = Event(kind=Kind.META, stream="main", offset=1, text="hi", tool=PEER_TOOL,
                  tool_input={"command": f"lead (uds:{SOCKET})", "from": f"uds:{SOCKET}", "from_name": "lead"})
    assert hints.trigger_of(named) == ("peer", "hi", [f"uds:{SOCKET}"])
    bare = Event(kind=Kind.META, stream="main", offset=1, text="hi", tool=PEER_TOOL,
                 tool_input={"command": f"lead (uds:{SOCKET})"})
    assert hints.sender_of(bare) == f"uds:{SOCKET}"
    nobody = Event(kind=Kind.META, stream="main", offset=1, text="hi", tool=PEER_TOOL)
    assert hints.trigger_of(nobody) == ("peer", "hi", [])
    other_meta = Event(kind=Kind.META, stream="main", offset=1, text="<task-notification>")
    assert hints.trigger_of(other_meta) is None
    helper = Event(kind=Kind.PROMPT, stream="subagent:x", offset=1, text="hi")
    assert hints.trigger_of(helper) is None


def test_a_web_search_or_fetch_asks_with_trigger_search(tmp_path, state):
    session = _session(tmp_path, state)
    api = Api()
    clock = Clock()
    lane, _ = _lane(tmp_path, [session], api, clock)
    _seen(lane, session)
    _append(session, _tool("WebSearch", {"query": "RFD4-Proteina benchmark"}, session.cwd))
    lane.read_once()
    lane.run_due()
    clock.now += hints.SESSION_GAP_S
    _append(session, _tool("WebFetch", {"url": "https://arxiv.org/abs/2501.1", "prompt": "the training data"},
                           session.cwd))
    lane.read_once()
    lane.run_due()
    assert [(b["trigger"], b["text"]) for b in api.bodies] == [
        ("search", "RFD4-Proteina benchmark"), ("search", "https://arxiv.org/abs/2501.1\nthe training data")]


def test_only_a_probe_command_that_starts_a_run_asks(tmp_path, state):
    session = _session(tmp_path, state)
    api = Api()
    clock = Clock()
    lane, _ = _lane(tmp_path, [session], api, clock)
    _seen(lane, session)
    for command in ("probe runs list", "ls -la", "probe exec rfd4-7 -- python eval.py", "probe run start --help",
                    "probe exec --project rfd -- python train.py --config cfg/rfd4.yaml"):
        _append(session, _tool("Bash", {"command": command}, session.cwd))
        lane.read_once()
        lane.run_due()
        clock.now += hints.SESSION_GAP_S
    assert [(b["trigger"], b["text"]) for b in api.bodies] == [
        ("command", "probe exec --project rfd -- python train.py --config cfg/rfd4.yaml")]


def test_a_researchers_own_shell_command_and_its_output_never_ask(tmp_path, state):
    """A `!command` (Claude Code's `<bash-input>`/`<bash-stdout>` turns, Codex's
    `<user_shell_command>`) is no prompt: what it printed is withheld from the
    capture (the consent screen), so it never goes out as a lookup. Nor does a
    `[Probe]` message the agent was handed."""
    session = _session(tmp_path, state)
    api = Api()
    clock = Clock()
    lane, _ = _lane(tmp_path, [session], api, clock)
    _seen(lane, session)
    for text in ("<bash-input>cat data/patients.csv</bash-input>",
                 "<bash-stdout>id,name\n1,Ada Lovelace</bash-stdout><bash-stderr></bash-stderr>",
                 "<user_shell_command>\n<command>cat notes.txt</command>\n<result>\nOutput:\nsecret notes\n</result>",
                 "[Probe] Team records near this:\n- Michael, 10-21, RFD4-Proteina review"):
        _append(session, _user(text, session.cwd))
        lane.read_once()
        lane.run_due()
        clock.now += hints.SESSION_GAP_S
    _append(session, _user("now benchmark it", session.cwd))
    lane.read_once()
    lane.run_due()
    assert [b["text"] for b in api.bodies] == ["now benchmark it"]


def test_a_shell_line_too_long_to_read_quickly_is_no_launch():
    """`shell_part` is quadratic in heredoc markers: a line past MAX_COMMAND_CHARS
    is never parsed (the tail thread reads every session)."""
    assert hints.launches_run("probe exec -- python train.py # " + "x" * hints.MAX_COMMAND_CHARS) is False
    assert hints.launches_run("probe exec -- python train.py\n" + "<<T\n" * 30_000) is False


@pytest.mark.parametrize("command, starts", [
    ("probe exec -- python train.py", True),
    ("probe exec --project p -- python train.py", True),
    ("probe exec --name sweep-3 --config lr=3e-4 -- python train.py", True),
    ("probe exec --detached-launcher -- sbatch job.sh", True),
    ("probe exec --project p python train.py", True),
    ("cd /work && PROBE_PROJECT=p uv run probe exec -- python train.py 2>&1 | tee log", True),
    ("nohup ~/.local/bin/probe exec -- python train.py &", True),
    ("probe run start --name a --experiment e", True),
    ("probe exec RUN -- python train.py", False),
    ("probe exec rfd4-7 python train.py", False),
    ("probe exec --help", False),
    ("probe exec", False),
    ("probe run start -h", False),
    ("probe runs list", False),
    ("probe run get abc", False),
    ("echo probe exec -- python x", False),
    ("git commit -m 'probe exec -- python train.py'", False),
    ("cat <<EOF > notes.md\nprobe exec -- python train.py\nEOF", False),
    ("python -c 'import subprocess; subprocess.run([\"probe\", \"exec\"])'", False),
    ("ls", False),
    ("probe exec --project 'unbalanced", False),
    ("cd /work/rfd\nprobe exec --project rfd -- python train.py", True),
    ("cd /work/rfd && \\\n  probe exec -- python train.py", True),
    ("cat <<'EOF' > run.sh\nprobe exec -- python train.py\nEOF\nchmod +x run.sh", False),
    ("echo 'one\nprobe exec -- python train.py'", False),
    ("echo \"unterminated\nprobe exec -- python train.py", False),
])
def test_launches_run(command, starts):
    assert hints.launches_run(command) is starts


def test_a_session_first_seen_asks_only_about_lines_younger_than_fresh_s(tmp_path, state):
    session = _session(tmp_path, state)
    api = Api()
    lane, _ = _lane(tmp_path, [session], api)
    _append(session, _user("an old prompt of a resumed session", session.cwd, ago=3600),
            _user("the first prompt, just written", session.cwd))
    lane.read_once()
    lane.run_due()
    assert [b["text"] for b in api.bodies] == ["the first prompt, just written"]


def test_a_prompt_in_a_folder_probe_config_turns_off_never_asks(tmp_path, state):
    session = _session(tmp_path, state)
    secret = Path(session.cwd) / "secret"
    secret.mkdir()
    (Path(session.cwd) / ".probe.config").write_text("secret/\n")
    api = Api()
    clock = Clock()
    lane, _ = _lane(tmp_path, [session], api, clock)
    _seen(lane, session)
    _append(session, _user("work in the secret folder", str(secret)))
    lane.read_once()
    clock.now += hints.SESSION_GAP_S
    _append(session, _user("work in the project", session.cwd))
    lane.read_once()
    lane.run_due()
    assert [b["text"] for b in api.bodies] == ["work in the project"]
    assert lane.stats["excluded"] == 1


# ---------------------------------------------------------------------------
# Limits (R10, R16).
# ---------------------------------------------------------------------------


def test_triggers_inside_the_session_gap_coalesce_to_the_latest(tmp_path, state):
    session = _session(tmp_path, state)
    api = Api()
    clock = Clock()
    lane, _ = _lane(tmp_path, [session], api, clock)
    lane.trigger(session, "prompt", "first")
    assert lane.run_due() == 1
    clock.now += 2
    lane.trigger(session, "search", "second")
    clock.now += 3
    lane.trigger(session, "search", "third")
    assert lane.run_due() == 0, "inside the gap"
    clock.now += 5
    assert lane.run_due() == 1
    assert [b["text"] for b in api.bodies] == ["first", "third"]


def test_a_search_or_command_never_replaces_a_waiting_prompt(tmp_path, state):
    """Prompts (and peers' messages) are the better question: the agent's
    WebSearch right after a prompt is usually its own step toward that prompt,
    and must not take the prompt's place."""
    session = _session(tmp_path, state)
    api = Api()
    clock = Clock()
    lane, _ = _lane(tmp_path, [session], api, clock)
    lane.trigger(session, "search", "an earlier search")
    lane.run_due()
    clock.now += 2
    assert lane.trigger(session, "prompt", "benchmark RFD4-Proteina") is True
    assert lane.trigger(session, "search", "RFD4-Proteina benchmark") is False
    assert lane.trigger(session, "command", "probe exec -- python eval.py") is False
    clock.now += hints.SESSION_GAP_S
    lane.run_due()
    assert [b["text"] for b in api.bodies] == ["an earlier search", "benchmark RFD4-Proteina"]


def test_the_machines_token_bucket_spaces_a_burst(tmp_path, state):
    sessions = [_session(tmp_path, state, sid=f"{i:08d}-0000-0000-0000-000000000000") for i in range(7)]
    api = Api()
    clock = Clock()
    lane, _ = _lane(tmp_path, sessions, api, clock)
    for session in sessions:
        lane.trigger(session, "prompt", f"prompt of {session.sid}")
    assert lane.run_due() == hints.BUCKET_BURST
    with lane._cv:
        job, wait = lane.take_due(False)
    assert job is None and wait == pytest.approx(60.0 / hints.BUCKET_PER_MIN)
    clock.now += 60.0 / hints.BUCKET_PER_MIN
    assert lane.run_due() == 1
    clock.now += 60.0 / hints.BUCKET_PER_MIN
    assert lane.run_due() == 1
    assert len(api.bodies) == 7


def _keyed(env: dict) -> Endpoint:
    """Each session's endpoint from its env (`BASE`, `KEY`): sessions of several keys and servers."""
    return Endpoint(env.get("BASE", "https://api.example.test"), env.get("KEY", "pk_read"))


def test_a_429_holds_its_key_on_its_server_for_limited_s(tmp_path, state):
    first, second = _session(tmp_path, state), _session(tmp_path, state, sid=OTHER)
    api = Api()
    api.script = [(429, {"detail": "slow down"})]
    clock = Clock()
    lane, logs = _lane(tmp_path, [first, second], api, clock)
    lane.trigger(first, "prompt", "one")
    lane.run_due()
    clock.now += 30
    lane.trigger(second, "prompt", "two")
    assert lane.run_due() == 0
    clock.now += hints.LIMITED_S - 30
    assert lane.run_due() == 1
    assert [b["text"] for b in api.bodies] == ["one", "two"]
    assert any("answered 429" in m for m in logs)


@pytest.mark.parametrize("status, wait", [(401, hints.REFUSED_S), (403, hints.REFUSED_S), (404, hints.MISSING_S)])
def test_a_refused_key_or_a_server_without_the_route_holds_it_for_a_while(tmp_path, state, status, wait):
    session = _session(tmp_path, state)
    api = Api(default=(status, {"detail": "no"}))
    clock = Clock()
    lane, _ = _lane(tmp_path, [session], api, clock)
    lane.trigger(session, "prompt", "one")
    lane.run_due()
    clock.now += wait - 1
    lane.trigger(session, "prompt", "two")
    assert lane.run_due() == 0
    clock.now += 1
    assert lane.run_due() == 1


@pytest.mark.parametrize("status, held", [
    (401, {SID, PEER}), (403, {SID, PEER}),  # the key, on every server
    (404, {SID, OTHER}),  # the server, for every key
    (429, {SID}),  # that key on that server
])
def test_a_hold_is_for_its_key_or_its_server_never_the_machine(tmp_path, state, status, held):
    """As `alertpoll`: a refused key waits wherever it is used, a server without
    the route waits for every key, a 429 holds that key there; the rest ask."""
    a = _session(tmp_path, state, sid=SID, KEY="pk_a")
    b = _session(tmp_path, state, sid=OTHER, KEY="pk_b")
    c = _session(tmp_path, state, sid=PEER, KEY="pk_a", BASE="https://probe.self-hosted.test")
    api = Api()
    api.script = [(status, {"detail": "no"})]
    clock = Clock()
    lane, _ = _lane(tmp_path, [a, b, c], api, clock)
    lane.endpoint_of = _keyed
    lane.trigger(a, "prompt", "one")
    lane.run_due()
    clock.now += hints.SESSION_GAP_S
    for session in (a, b, c):
        lane.trigger(session, "prompt", f"two of {session.sid}")
    lane.run_due()
    assert {body["session_id"] for body in api.bodies[1:]} == {SID, OTHER, PEER} - held
    clock.now += max(hints.REFUSED_S, hints.MISSING_S, hints.LIMITED_S)
    lane.run_due()
    assert {body["session_id"] for body in api.bodies[1:]} == {SID, OTHER, PEER}


def _live(session: hints.Followed) -> Path:
    with mailbox.rooted(session.state):
        return mailbox.hints_live_path(session.sid)


def test_a_served_sessions_hint_marker_is_touched_at_most_every_beat(tmp_path, state):
    """The session's daemon skips its reader's turn at a prompt only while this
    marker is fresh (`model.hints_live`): touched while the lane can hint the
    session, at most every HINTS_LIVE_BEAT_S; a session that left is not."""
    session = _session(tmp_path, state)
    clock = Clock()
    sessions = [session]
    lane, _ = _lane(tmp_path, sessions, Api(), clock)
    _seen(lane, session)
    path = _live(session)
    assert path.is_file()
    os.utime(path, (1, 1))
    clock.now += hints.HINTS_LIVE_BEAT_S - 1
    lane.read_once()
    assert path.stat().st_mtime == 1, "not again inside the beat"
    clock.now += 1
    lane.read_once()
    assert path.stat().st_mtime > 1
    os.utime(path, (1, 1))
    sessions.clear()  # its recorder let go of it
    clock.now += hints.HINTS_LIVE_BEAT_S
    lane.read_once()
    assert path.stat().st_mtime == 1, "left to go stale"


@pytest.mark.parametrize("why, answer", [
    ("its own key or address", None),
    ("a refused key", (401, {"detail": "no"})),
    ("a server without the route", (404, {"detail": "no"})),
    ("hints off for the team", (200, {"mode": "off", "fire": False, "reason": "off"})),
])
def test_no_marker_where_the_lane_cannot_hint(tmp_path, state, why, answer):
    """No hint can come, so the reader keeps its turn at each prompt there."""
    session = _session(tmp_path, state)
    clock = Clock()
    lane, _ = _lane(tmp_path, [session], Api(default=answer or (200, SHADOW)), clock)
    if answer is None:
        lane.endpoint_of = lambda env: None
    else:
        lane.trigger(session, "prompt", "one")
        lane.run_due()
    lane.read_once()
    assert not _live(session).exists(), why


def test_a_busy_server_still_counts_as_hinting(tmp_path, state):
    """A 429 holds that key on that server a while: hints come back, so the
    marker stays fresh and the reader does not take prompt turns meanwhile."""
    session = _session(tmp_path, state)
    lane, _ = _lane(tmp_path, [session], Api(default=(429, {"detail": "slow down"})), Clock())
    lane.trigger(session, "prompt", "one")
    lane.run_due()
    lane.read_once()
    assert _live(session).is_file()


def test_mode_off_quiets_its_key_on_its_server_for_off_recheck_s(tmp_path, state):
    """A team that never turned hints on: at most one request per key per
    server per OFF_RECHECK_S from this machine, whatever its sessions."""
    session, sibling = _session(tmp_path, state, KEY="pk_a"), _session(tmp_path, state, sid=OTHER, KEY="pk_a")
    other_team = _session(tmp_path, state, sid=PEER, KEY="pk_b")
    api = Api(default=(200, {"mode": "off", "fire": False, "reason": "off"}))
    clock = Clock()
    lane, _ = _lane(tmp_path, [session, sibling, other_team], api, clock)
    lane.endpoint_of = _keyed
    lane.trigger(session, "prompt", "one")
    lane.run_due()
    clock.now += hints.SESSION_GAP_S
    assert lane.trigger(session, "prompt", "two") is False
    assert lane.trigger(sibling, "prompt", "a new session of the same key") is False
    assert lane.trigger(other_team, "prompt", "another key") is True
    lane.run_due()
    clock.now += hints.OFF_RECHECK_S
    assert lane.trigger(sibling, "prompt", "three") is True
    lane.run_due()
    assert [b["text"] for b in api.bodies] == ["one", "another key", "three"]


def test_an_identical_text_is_not_sent_again(tmp_path, state):
    session = _session(tmp_path, state)
    api = Api()
    clock = Clock()
    lane, _ = _lane(tmp_path, [session], api, clock)
    lane.trigger(session, "prompt", "continue")
    lane.run_due()
    clock.now += hints.SESSION_GAP_S
    assert lane.trigger(session, "prompt", "continue") is False
    assert lane.trigger(session, "search", "continue") is True, "another trigger is another question"
    lane.run_due()
    assert [(b["trigger"], b["text"]) for b in api.bodies] == [("prompt", "continue"), ("search", "continue")]


def test_a_long_text_is_cut_to_the_contracts_limit(tmp_path, state):
    session = _session(tmp_path, state)
    api = Api()
    lane, _ = _lane(tmp_path, [session], api)
    lane.trigger(session, "prompt", "x" * 20000)
    lane.run_due()
    assert len(api.bodies[0]["text"]) == hints.MAX_TEXT_CHARS


def test_a_credential_in_the_text_never_leaves_the_machine(tmp_path, state):
    """Transcript text leaves this machine only through the capture's one
    detector (`probe.tap_core.secrets`, as the daemon's store and the tap's
    journal do), and a credential the contract's cut would split is found whole."""
    session = _session(tmp_path, state)
    api = Api()
    clock = Clock()
    lane, _ = _lane(tmp_path, [session], api, clock)
    key = "hf_abcdefghijklmnopqrstuvwxyzABCDEFGH"
    lane.trigger(session, "command", f"HF_TOKEN={key} probe exec --project p -- python train.py")
    lane.run_due()
    clock.now += hints.SESSION_GAP_S
    lane.trigger(session, "prompt", "x" * (hints.MAX_TEXT_CHARS - 10) + " sk-ant-api03-" + "a" * 80)
    lane.run_due()
    command, prompt = (b["text"] for b in api.bodies)
    assert key not in command and "probe exec --project p -- python train.py" in command
    assert "sk-ant" not in prompt and len(prompt) <= hints.MAX_TEXT_CHARS


def test_a_request_past_its_deadline_is_never_sent_again(monkeypatch):
    """The cutoff's shutdown at TIMEOUT_S is no kept connection the server
    closed: no second try, so a slow server is never asked twice nor waited on
    past the deadline."""
    from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

    seen: list = []
    release = threading.Event()

    class Slow(BaseHTTPRequestHandler):
        protocol_version = "HTTP/1.1"

        def log_message(self, *args) -> None:
            pass

        def do_POST(self) -> None:
            self.rfile.read(int(self.headers.get("Content-Length") or 0))
            seen.append(self.path)
            release.wait(5)

    server = ThreadingHTTPServer(("127.0.0.1", 0), Slow)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    monkeypatch.setattr(hints, "TIMEOUT_S", 0.3)
    monkeypatch.setattr(hints.HintFetcher, "timeout", 0.3)
    try:
        fetch = hints.HintFetcher(VERSION)
        answer = fetch(Endpoint(f"http://127.0.0.1:{server.server_address[1]}", "pk_read"), {"text": "slow"})
    finally:
        release.set()
        server.shutdown()
        server.server_close()
    assert answer == (None, None) and seen == ["/v1/hints"]


# ---------------------------------------------------------------------------
# Delivery (R2, R3, R5).
# ---------------------------------------------------------------------------


def test_a_hint_that_fires_reaches_the_agent_through_the_reads_hook(tmp_path, state):
    session = _session(tmp_path, state)
    api = Api(default=(200, _on()))
    posted: list = []
    lane, logs = _lane(tmp_path, [session], api, posted=posted.append)
    lane.trigger(session, "prompt", "benchmark RFD4-Proteina")
    lane.run_due()
    waiting = _waiting(session)
    assert [(m.kind, m.origin, m.text) for m in waiting] == [("message", mailbox.ORIGIN_HINT, _on()["hint"])]
    assert posted == [SID], "the server is told, to wake the session's watchers"
    assert any("posted" in m and "after the trigger" in m for m in logs)
    done = _hook("PostToolUse", tmp_path)
    out = json.loads(done.stdout)
    assert out["hookSpecificOutput"]["additionalContext"] == _on()["hint"], "shown as Probe rendered it"
    assert _waiting(session) == []


def test_a_hint_is_posted_as_probe_rendered_it_and_one_over_the_cap_is_dropped_whole(tmp_path, state):
    """The mailbox shows a hint as-is only when it starts with `[Probe] `, so
    the lane adds and strips nothing; a longer hint than MAX_HINT_CHARS is
    never cut mid-line into the agent's context: it is not posted at all."""
    session = _session(tmp_path, state)
    head = "[Probe] Team records near this:\n"
    exact = head + "x" * (hints.MAX_HINT_CHARS - len(head))
    api = Api()
    api.script = [(200, _on(exact + "y")), (200, _on(exact))]
    clock = Clock()
    lane, logs = _lane(tmp_path, [session], api, clock)
    lane.trigger(session, "prompt", "one")
    lane.run_due()
    assert _waiting(session) == [] and lane.stats["too_long"] == 1
    assert any(f"; {hints.Skip.TOO_LONG}" in m for m in logs)
    clock.now += hints.SESSION_GAP_S
    lane.trigger(session, "prompt", "two")
    lane.run_due()
    assert [m.text for m in _waiting(session)] == [exact]


def test_a_shadow_answer_or_one_that_did_not_fire_posts_nothing(tmp_path, state):
    session = _session(tmp_path, state)
    api = Api()
    api.script = [(200, {**_on(), "mode": "shadow", "hint": None}), (200, {**_on(), "fire": False})]
    clock = Clock()
    lane, _ = _lane(tmp_path, [session], api, clock)
    lane.trigger(session, "prompt", "one")
    lane.run_due()
    clock.now += hints.SESSION_GAP_S
    lane.trigger(session, "prompt", "two")
    lane.run_due()
    assert len(api.bodies) == 2 and _waiting(session) == []


def test_records_already_delivered_are_not_hinted_again_unless_they_changed(tmp_path, state):
    session = _session(tmp_path, state)
    api = Api(default=(200, _on()))
    clock = Clock()
    lane, _ = _lane(tmp_path, [session], api, clock)
    lane.trigger(session, "prompt", "one")
    lane.run_due()
    assert json.loads(_hook("UserPromptSubmit", tmp_path).stdout), "delivered"
    clock.now += hints.SESSION_GAP_S
    lane.trigger(session, "prompt", "two")
    lane.run_due()
    assert _waiting(session) == [] and lane.stats["repeat"] == 1
    # The next service (no memory of this one's posts) reads the claim log and the ledger.
    later, _ = _lane(tmp_path, [session], Api(default=(200, _on())))
    later.trigger(session, "prompt", "three")
    later.run_due()
    assert _waiting(session) == [] and later.stats["repeat"] == 1
    # The same record, changed: hinted again.
    changed = Api(default=(200, _on("[Probe] changed", {"doc_id": "doc-1", "date": "10-23"})))
    again, _ = _lane(tmp_path, [session], changed)
    again.trigger(session, "prompt", "four")
    again.run_due()
    assert [m.text for m in _waiting(session)] == ["[Probe] changed"]


def test_a_hint_waiting_with_the_same_records_is_not_posted_twice(tmp_path, state):
    session = _session(tmp_path, state)
    api = Api(default=(200, _on()))
    clock = Clock()
    lane, _ = _lane(tmp_path, [session], api, clock)
    lane.trigger(session, "search", "one")
    lane.run_due()
    clock.now += hints.SESSION_GAP_S
    lane.trigger(session, "search", "two")
    lane.run_due()
    assert len(_waiting(session)) == 1 and lane.stats["repeat"] == 1


def test_a_newer_prompt_withdraws_a_hint_still_waiting_and_nothing_else(tmp_path, state):
    session = _session(tmp_path, state)
    api = Api(default=(200, _on()))
    clock = Clock()
    lane, _ = _lane(tmp_path, [session], api, clock)
    with mailbox.rooted(session.state):
        mailbox.publish_here(mailbox.Message(id=mailbox.new_message_id(), session=SID, kind=mailbox.Kind.MESSAGE,
                                             text="the reader's note"))
    lane.trigger(session, "search", "one")
    lane.run_due()
    assert sorted(m.origin or "" for m in _waiting(session)) == ["", mailbox.ORIGIN_HINT], "a slot each"
    _seen(lane, session)
    _append(session, _user("a newer prompt", session.cwd))
    lane.read_once()
    assert [m.text for m in _waiting(session)] == ["the reader's note"]
    assert lane.stats["withdrawn"] == 1


def test_a_hint_replaced_in_its_slot_never_counts_as_shown(tmp_path, state):
    session = _session(tmp_path, state)
    first, second = {"doc_id": "doc-1", "date": "10-21"}, {"doc_id": "doc-2", "date": "10-22"}
    api = Api()
    api.script = [(200, _on("[Probe] first", first)), (200, _on("[Probe] second", second)),
                  (200, _on("[Probe] first again", first))]
    clock = Clock()
    lane, _ = _lane(tmp_path, [session], api, clock)
    for text in ("one", "two", "three"):
        lane.trigger(session, "search", text)
        lane.run_due()
        clock.now += hints.SESSION_GAP_S
    assert [m.text for m in _waiting(session)] == ["[Probe] first again"]
    assert lane.stats["posted"] == 3 and lane.stats["repeat"] == 0


def test_a_hint_gone_from_the_mailbox_unshown_never_counts_as_waiting(tmp_path, state):
    """What waits is read from the mailbox's files, not remembered: a hint
    another deliverer's rules removed unshown (an older worker's reader note
    replaces any unasked message) leaves its records free to be hinted."""
    session = _session(tmp_path, state)
    api = Api(default=(200, _on()))
    clock = Clock()
    lane, _ = _lane(tmp_path, [session], api, clock)
    lane.trigger(session, "search", "one")
    lane.run_due()
    with mailbox.rooted(session.state):
        for path, _msg in mailbox.waiting(SID):
            path.unlink()
    clock.now += hints.SESSION_GAP_S
    lane.trigger(session, "search", "two")
    lane.run_due()
    assert [m.origin for m in _waiting(session)] == [mailbox.ORIGIN_HINT] and lane.stats["repeat"] == 0


def test_a_hint_the_last_service_posted_still_waiting_is_not_posted_again(tmp_path, state):
    session = _session(tmp_path, state)
    before, _ = _lane(tmp_path, [session], Api(default=(200, _on())))
    before.trigger(session, "search", "one")
    before.run_due()
    after, _ = _lane(tmp_path, [session], Api(default=(200, _on())))
    after.trigger(session, "search", "two")
    after.run_due()
    assert len(_waiting(session)) == 1 and after.stats["repeat"] == 1


def test_old_ledgers_are_swept_again_while_the_service_runs(tmp_path, state):
    ledger = tmp_path / "ledger"
    ledger.mkdir()
    old = time.time() - hints.KEEP_LEDGER_S - 60

    def ended(name: str) -> Path:
        path = ledger / f"{name}.jsonl"
        path.write_text("{}\n")
        os.utime(path, (old, old))
        return path

    first = ended("ended-1")
    session = _session(tmp_path, state)
    api = Api()
    api.script = [(200, _on("[Probe] first", {"doc_id": "doc-1", "date": "10-21"})),
                  (200, _on("[Probe] second", {"doc_id": "doc-2", "date": "10-22"}))]
    clock = Clock()
    lane, _ = _lane(tmp_path, [session], api, clock)
    lane.trigger(session, "search", "one")
    lane.run_due()
    assert not first.exists()
    second = ended("ended-2")
    clock.now += hints.SWEEP_EVERY_S
    lane.trigger(session, "search", "two")
    lane.run_due()
    assert not second.exists() and (ledger / f"{SID}.jsonl").exists()


def test_a_newer_prompt_in_an_excluded_folder_still_withdraws_but_is_never_sent(tmp_path, state):
    session = _session(tmp_path, state)
    secret = Path(session.cwd) / "secret"
    secret.mkdir()
    (Path(session.cwd) / ".probe.config").write_text("secret/\n")
    api = Api(default=(200, _on()))
    lane, _ = _lane(tmp_path, [session], api)
    lane.trigger(session, "search", "one")
    lane.run_due()
    _seen(lane, session)
    _append(session, _user("a prompt about the secret folder", str(secret)))
    lane.read_once()
    assert _waiting(session) == [] and lane.stats["withdrawn"] == 1
    assert [b["text"] for b in api.bodies] == ["one"]


def test_a_first_look_never_withdraws_a_hint_the_last_service_posted(tmp_path, state):
    session = _session(tmp_path, state)
    before, _ = _lane(tmp_path, [session], Api(default=(200, _on())))
    before.trigger(session, "prompt", "the prompt just before a restart")
    before.run_due()
    _append(session, _user("the prompt just before a restart", session.cwd))
    after, _ = _lane(tmp_path, [session], Api(default=(200, _on())))
    after.read_once()  # the next service's first look reads that prompt again
    assert [m.origin for m in _waiting(session)] == [mailbox.ORIGIN_HINT]
    assert after.stats["withdrawn"] == 0


def _turn_end(cwd: str) -> dict:
    """Claude Code's end of a main-agent turn (the adapter's TURN_END)."""
    return {"type": "system", "subtype": "turn_duration", "durationMs": 4200, "timestamp": _stamp(), "cwd": cwd,
            "isSidechain": False}


def test_a_turn_that_ends_withdraws_its_hint_still_waiting(tmp_path, state):
    """A hint still waiting when the agent's turn ends was for that turn: the
    next prompt's hook would hand it over stale (R5), so it goes."""
    session = _session(tmp_path, state)
    api = Api(default=(200, _on()))
    lane, _ = _lane(tmp_path, [session], api)
    _seen(lane, session)
    _append(session, _user("benchmark RFD4-Proteina", session.cwd))
    lane.read_once()
    lane.run_due()
    assert [m.origin for m in _waiting(session)] == [mailbox.ORIGIN_HINT]
    _append(session, _turn_end(session.cwd))
    lane.read_once()
    assert _waiting(session) == [] and lane.stats["withdrawn"] == 1


def test_a_turn_that_ends_makes_its_lookups_stale(tmp_path, state):
    """A lookup in flight when the turn ends is never posted, and one still
    waiting out the session's gap is never sent."""
    session = _session(tmp_path, state)
    api = Api(default=(200, _on()))
    clock = Clock()
    lane, _ = _lane(tmp_path, [session], api, clock)
    _seen(lane, session)
    lane.trigger(session, "search", "in flight")
    with lane._cv:
        job, _wait = lane.take_due(False)
    clock.now += 1
    lane.trigger(session, "search", "waiting out the gap")
    _append(session, _turn_end(session.cwd))
    lane.read_once()
    lane.lookup(job)
    clock.now += hints.SESSION_GAP_S
    assert lane.run_due() == 0
    assert _waiting(session) == [] and lane.stats["stale"] == 1
    assert [b["text"] for b in api.bodies] == ["in flight"]


def test_a_first_look_at_a_turn_end_withdraws_nothing(tmp_path, state):
    session = _session(tmp_path, state)
    before, _ = _lane(tmp_path, [session], Api(default=(200, _on())))
    before.trigger(session, "prompt", "the prompt just before a restart")
    before.run_due()
    _append(session, _turn_end(session.cwd))
    after, _ = _lane(tmp_path, [session], Api(default=(200, _on())))
    after.read_once()
    assert [m.origin for m in _waiting(session)] == [mailbox.ORIGIN_HINT] and after.stats["withdrawn"] == 0


def test_the_records_the_session_was_shown_or_has_waiting_are_named_to_the_server(tmp_path, state):
    """`exclude_doc_ids` (most recent first): the server leaves them out before it
    renders (a partial repeat); the all-repeated rule stays for a server that does not."""
    session = _session(tmp_path, state)
    api = Api()
    api.script = [(200, _on("[Probe] a", {"doc_id": "doc-2", "date": "10-21"}, {"doc_id": "doc-1", "date": "10-21"})),
                  (200, _on("[Probe] b", {"doc_id": "doc-3", "date": "10-22"})), (200, SHADOW)]
    clock = Clock()
    lane, _ = _lane(tmp_path, [session], api, clock)
    lane.trigger(session, "search", "one")
    lane.run_due()
    assert json.loads(_hook("UserPromptSubmit", tmp_path).stdout), "delivered"
    clock.now += hints.SESSION_GAP_S
    lane.trigger(session, "search", "two")
    lane.run_due()  # doc-3 waits
    clock.now += hints.SESSION_GAP_S
    lane.trigger(session, "search", "three")
    lane.run_due()
    assert [b["exclude_doc_ids"] for b in api.bodies] == [[], ["doc-1", "doc-2"], ["doc-3", "doc-1", "doc-2"]]


def test_exclude_doc_ids_names_each_record_once_newest_first_and_at_most_its_cap():
    shown = [frozenset({"doc-9 10-23", "doc-8 "}), frozenset({"doc-9 10-20"}),
             frozenset({f"old-{i:03d} 10-01" for i in range(hints.MAX_EXCLUDE_DOC_IDS * 2)})]
    out = hints.exclude_doc_ids(shown)
    assert out[:2] == ["doc-8", "doc-9"] and out.count("doc-9") == 1
    assert len(out) == hints.MAX_EXCLUDE_DOC_IDS


def test_a_hint_looked_up_before_a_newer_prompt_is_never_posted(tmp_path, state):
    session = _session(tmp_path, state)
    api = Api(default=(200, _on()))
    lane, _ = _lane(tmp_path, [session], api)
    lane.trigger(session, "search", "one")
    with lane._cv:
        job, _wait = lane.take_due(False)
    lane.trigger(session, "prompt", "a newer prompt")  # arrives while the lookup is in flight
    lane.lookup(job)
    assert _waiting(session) == [] and lane.stats["stale"] == 1


# ---------------------------------------------------------------------------
# The ML state (R1).
# ---------------------------------------------------------------------------


def _store(state: Path, sid: str, facts: dict) -> Path:
    path = state / "daemon" / f"{sid}.sqlite"
    path.parent.mkdir(parents=True, exist_ok=True)
    db = sqlite3.connect(path)
    db.execute("PRAGMA journal_mode=WAL")
    db.execute("CREATE TABLE IF NOT EXISTS facts (key TEXT PRIMARY KEY, value TEXT NOT NULL)")
    for key, value in facts.items():
        db.execute("INSERT OR REPLACE INTO facts (key, value) VALUES (?, ?)", (key, json.dumps(value)))
    db.commit()
    db.close()
    return path


def test_the_ml_state_is_read_from_the_daemon_workers_store(tmp_path, state):
    assert hints.ml_state(str(state), SID) is None, "no store"
    _store(state, SID, {"gate_seq": 4})
    assert hints.ml_state(str(state), SID) is None, "the gate never answered"
    _store(state, SID, {"gate_answers": [0.1, 0.83, None]})
    assert hints.ml_state(str(state), SID) == {"signal": False, "p_ml": 0.83}
    _store(state, SID, {"gate_signal": "ran `probe exec`"})
    assert hints.ml_state(str(state), SID) == {"signal": True, "p_ml": 0.83}
    (state / "daemon" / f"{OTHER}.sqlite").write_text("not a database")
    assert hints.ml_state(str(state), OTHER) is None


def test_a_daemon_session_sends_its_ml_state_and_an_inline_one_sends_null(tmp_path, state):
    _store(state, SID, {"gate_answers": [0.9]})
    _store(state, OTHER, {"gate_answers": [0.9]})
    daemon, inline = _session(tmp_path, state, mode=Mode.DAEMON), _session(tmp_path, state, sid=OTHER)
    api = Api()
    lane, _ = _lane(tmp_path, [daemon, inline], api)
    lane.trigger(daemon, "prompt", "one")
    lane.trigger(inline, "prompt", "two")
    lane.run_due()
    assert {b["session_id"]: (b["ml"], b["client"]["mode"]) for b in api.bodies} == {
        SID: ({"signal": False, "p_ml": 0.9}, "daemon"), OTHER: (None, "inline")}


def test_a_store_locked_by_its_worker_still_reads_or_reads_as_unknown(tmp_path, state):
    path = _store(state, SID, {"gate_answers": [0.7]})
    holder = sqlite3.connect(path, isolation_level=None)
    holder.execute("BEGIN EXCLUSIVE")
    try:
        assert hints.ml_state(str(state), SID) in (None, {"signal": False, "p_ml": 0.7})
    finally:
        holder.execute("ROLLBACK")
        holder.close()


# ---------------------------------------------------------------------------
# Off, the guard, failing open.
# ---------------------------------------------------------------------------


def test_probe_hints_off_turns_the_lane_off(tmp_path, state):
    lane = hints.HintLane(sessions=lambda: [], log=lambda m: None, environ={"PROBE_HINTS": "off"}, transport=Api())
    lane.changed()
    assert lane.enabled is False and lane._threads == []
    assert hints.HintLane(sessions=lambda: [], log=lambda m: None, environ={}, transport=Api()).enabled


def _recording(sid: str, *, claimed: object = "/journal", env: dict | None = None, stopped: bool = False):
    controls = SimpleNamespace(stop=threading.Event(), pause=threading.Event())
    if claimed != "absent":  # "absent": a tap from before 0.10.6 publishes no claim
        controls.claimed = claimed
    if stopped:
        controls.stop.set()
    alive = threading.Event()
    thread = threading.Thread(target=alive.wait, daemon=True)
    thread.start()
    params = {"sid": sid, "harness": "claude_code", "cwd": "/work", "transcript": f"/t/{sid}.jsonl",
              "transcript_dir": None, "env": env or {}, "state_dir": "/state/probe"}
    return recorders.Recording(sid, params, controls, thread=thread), alive


def _registered(sid: str, mode: str = Mode.INLINE, unconfined: bool = True, owner_live: bool = True) -> Session:
    return Session(sid=sid, harness="claude_code", mode=mode, owner={"pid": 1, "start_time": "x"}, generation=1,
                   registered_at=0.0, heartbeat_at=0.0, owner_live=owner_live, state_dir="/state/probe",
                   unconfined=unconfined)


def test_only_live_sessions_whose_recorder_holds_them_and_tracking_is_on_are_read():
    sids = [f"{i:08d}-aaaa-bbbb-cccc-dddddddddddd" for i in range(9)]
    made = [
        _recording(sids[0]),  # read
        _recording(sids[1], claimed="absent"),  # a tap that publishes no claim: read
        _recording(sids[2]),  # registered off
        _recording(sids[3]),  # its owner exited
        _recording(sids[4]),  # registered from a sandbox
        _recording(sids[5], claimed=None),  # its recorder does not hold it (capture off, another recorder)
        _recording(sids[6], stopped=True),  # finishing
        _recording(sids[7], env={"PROBE_HINTS": "off"}),  # the session's own kill switch
        _recording(sids[8]),  # not registered
    ]
    registered = [_registered(sids[0]), _registered(sids[1], mode=Mode.DAEMON), _registered(sids[2], mode=Mode.OFF),
                  _registered(sids[3], owner_live=False), _registered(sids[4], unconfined=False),
                  _registered(sids[5]), _registered(sids[6]), _registered(sids[7])]
    try:
        out = hints.followed([r for r, _ in made], registered, now=time.time(), ttl=60.0, default_state="/default")
    finally:
        for _, alive in made:
            alive.set()
    assert [(f.sid, f.mode, f.state) for f in out] == [(sids[0], Mode.INLINE, "/state/probe"),
                                                       (sids[1], Mode.DAEMON, "/state/probe")]


@pytest.mark.parametrize("answer", [
    RuntimeError("boom"), (None, None), (500, {"detail": "engine down"}), (200, None), (200, ["not", "a", "dict"]),
    (200, {"mode": "on", "fire": True, "hint": 7, "records": "x"}),
])
def test_an_api_error_fails_open(tmp_path, state, answer):
    session = _session(tmp_path, state)
    api = Api()
    api.script = [answer]
    lane, logs = _lane(tmp_path, [session], api)
    lane.trigger(session, "prompt", "one")
    lane.run_due()
    assert len(api.bodies) == 1 and _waiting(session) == [] and logs


def test_no_key_means_no_request(tmp_path, state):
    session = _session(tmp_path, state)
    api = Api()
    lane, logs = _lane(tmp_path, [session], api)
    lane.endpoint_of = lambda env: None
    lane.trigger(session, "prompt", "one")
    lane.run_due()
    assert api.bodies == [] and lane.stats["no_key"] == 1 and len(logs) == 1


def test_the_key_is_the_read_only_one_of_the_sessions_config(tmp_path, monkeypatch):
    config = tmp_path / "cfg" / "config.json"
    config.parent.mkdir()
    row = {"base_url": "https://api.example.test/", "token": "pk_user", "mcp_token": "pk_read",
           "companion_token": "pk_daemon"}
    config.write_text(json.dumps({"version": 2, "current_context": "default", "contexts": {"default": row}}))
    assert hints.credentials({"PROBE_CONFIG_PATH": str(config)}) == Endpoint("https://api.example.test", "pk_read")
    del row["mcp_token"]
    config.write_text(json.dumps({"version": 2, "current_context": "default", "contexts": {"default": row}}))
    assert hints.credentials({"PROBE_CONFIG_PATH": str(config)}).key == "pk_user"
    assert hints.credentials({"PROBE_CONFIG_PATH": str(tmp_path / "missing.json")}) is None


@pytest.mark.parametrize("override", ["PROBE_BASE_URL", "PROBE_MCP_TOKEN", "PROBE_TOKEN", "PROBE_DAEMON_KEY"])
def test_a_session_whose_key_or_endpoint_comes_from_its_environment_is_never_asked_for(tmp_path, override):
    """Its own processes would talk to another deployment or as another key than
    the CLI config's (`sdk.config.resolve`): the lane never sends its text to the
    config's (as `alertpoll` never polls for such a worker)."""
    config = tmp_path / "cfg" / "config.json"
    config.parent.mkdir()
    row = {"base_url": "https://api.example.test/", "mcp_token": "pk_read"}
    config.write_text(json.dumps({"version": 2, "current_context": "default", "contexts": {"default": row}}))
    assert hints.credentials({"PROBE_CONFIG_PATH": str(config)}) is not None
    assert hints.credentials({"PROBE_CONFIG_PATH": str(config), override: "https://staging.example.test"}) is None


def test_a_transcript_that_is_no_regular_file_never_blocks_the_tail(tmp_path, state):
    """A FIFO named as one session's transcript (or anything not a regular
    file) is skipped without a blocking open: the other sessions are read."""
    fifo = tmp_path / "fifo.jsonl"
    os.mkfifo(fifo)
    stuck = hints.Followed(sid=OTHER, harness="claude_code", mode=Mode.INLINE, state=str(state),
                           cwd=str(tmp_path), transcript=str(fifo), transcript_dir=None)
    session = _session(tmp_path, state)
    api = Api()
    lane, _ = _lane(tmp_path, [stuck, session], api)
    Path(session.transcript).touch()
    done = threading.Event()

    def read() -> None:
        lane.read_once()
        _append(session, _user("benchmark RFD4-Proteina", session.cwd))
        lane.read_once()
        done.set()

    threading.Thread(target=read, daemon=True).start()
    try:
        assert done.wait(5), "the tail blocked on the FIFO"
    finally:
        with contextlib.suppress(OSError):  # a blocked open() returns once a writer opens it
            os.close(os.open(fifo, os.O_WRONLY | os.O_NONBLOCK))
    lane.run_due()
    assert [b["text"] for b in api.bodies] == ["benchmark RFD4-Proteina"]


def test_a_lookup_that_outlives_its_session_leaves_no_state(tmp_path, state):
    session = _session(tmp_path, state)
    sessions = [session]
    lane, _ = _lane(tmp_path, sessions, Api())
    _seen(lane, session)
    lane.trigger(session, "prompt", "one")
    with lane._cv:
        job, _wait = lane.take_due(False)
    sessions.clear()
    lane.read_once()  # the session ended while its lookup was in flight
    lane.lookup(job)
    lane.read_once()
    assert lane._states == {} and lane._tails == {}


def test_the_lane_never_raises_into_its_caller(tmp_path, state):
    def broken():
        raise RuntimeError("registry gone")

    logs: list = []
    lane = hints.HintLane(sessions=broken, log=logs.append, environ={}, transport=Api())
    assert lane.read_once() is False and logs
    session = _session(tmp_path, state)
    lane, _ = _lane(tmp_path, [session], Api())
    _seen(lane, session)
    with open(session.transcript, "ab") as out:
        out.write(b"\x00\xffnot json\n[1, 2]\n{\"type\": \"user\", \"message\": 7}\n")
        out.write(b"[" * 100_000 + b"]" * 100_000 + b"\n")  # too deep for the parser: skipped alone
    _append(session, _user("the next line is still read", session.cwd))
    assert lane.read_once() is True
    assert lane.stats["trigger_prompt"] == 1
    unknown = hints.Followed(sid=OTHER, harness="no-such-agent", mode=Mode.INLINE, state=str(state), cwd="/",
                             transcript=str(tmp_path / "x.jsonl"), transcript_dir=None)
    lane, _ = _lane(tmp_path, [unknown], Api())
    assert lane.read_once() is True


def test_the_lanes_threads_read_ask_and_post_and_stop(tmp_path, state):
    session = _session(tmp_path, state)
    Path(session.transcript).touch()
    api = Api(default=(200, _on()))
    lane = hints.HintLane(sessions=lambda: [session], log=lambda m: None, version=VERSION, environ={},
                          transport=api, endpoint_of=lambda env: Endpoint("https://api.example.test", "pk_read"),
                          ledger_dir=tmp_path / "ledger", poll_s=0.05)
    lane.changed()
    try:
        deadline = time.monotonic() + 5
        while getattr(lane._tails.get(SID), "offset", None) is None and time.monotonic() < deadline:
            time.sleep(0.02)  # its first look: the transcript empty
        _append(session, _user("benchmark RFD4-Proteina", session.cwd))
        while not _waiting(session) and time.monotonic() < deadline:
            time.sleep(0.02)
        assert [m.origin for m in _waiting(session)] == [mailbox.ORIGIN_HINT]
    finally:
        lane.close()
    for thread in lane._threads:
        thread.join(2)
        assert not thread.is_alive()


def test_the_service_builds_its_lane_and_lists_no_session_before_any_recording(tmp_path):
    from probe.service import server
    from probe.service.registry import Registry

    service = server.Service(registry=Registry(tmp_path / "sessions.json"))
    assert isinstance(service.hints, hints.HintLane)
    assert service._hint_sessions() == []
    service._hint_posted(SID)  # no loop yet: nothing to tell, nothing raised


# ---------------------------------------------------------------------------
# The window trigger (plan hints-window-trigger W1, W3).
# ---------------------------------------------------------------------------

T0 = time.time()


@pytest.fixture(autouse=True)
def _window_epoch(monkeypatch):
    """Each test's window stamps (`_at`) count from its own start: the lane
    compares them with the wall clock (WINDOW_COVERS_S), and a long run would
    otherwise age them past it."""
    monkeypatch.setattr(sys.modules[__name__], "T0", time.time())


WINDOW_SHADOW = {"mode": "on", "fire": False, "trigger_class": "window", "reason": "below_cutoff",
                 "top_score": 0.6, "records": []}
WINDOW_ERROR = {**WINDOW_SHADOW, "reason": "engine_error", "top_score": None}


def _at(seconds: float) -> str:
    return datetime.fromtimestamp(T0 + seconds, tz=timezone.utc).isoformat().replace("+00:00", "Z")


def _said(text: str, cwd: str, at: float) -> dict:
    return {"type": "assistant", "timestamp": _at(at), "cwd": cwd, "sessionId": SID,
            "message": {"role": "assistant", "content": [{"type": "text", "text": text}]}}


def _called(name: str, tool_input: dict, cwd: str, at: float) -> dict:
    return {**_tool(name, tool_input, cwd), "timestamp": _at(at)}


def _output(text: str, cwd: str, at: float) -> dict:
    return {"type": "user", "timestamp": _at(at), "cwd": cwd, "sessionId": SID,
            "message": {"role": "user", "content": [{"type": "tool_result", "tool_use_id": "toolu_1",
                                                      "content": text}]}}


def _thought(text: str, cwd: str, at: float) -> dict:
    return {"type": "assistant", "timestamp": _at(at), "cwd": cwd, "sessionId": SID,
            "message": {"role": "assistant", "content": [{"type": "thinking", "thinking": text}]}}


def _step(cwd: str, at: float) -> dict:
    return _called("Bash", {"command": "ls"}, cwd, at)


@pytest.mark.parametrize("on_clock, messages, due", [
    (hints.WINDOW_GAP_S - 1, ["a"], False),
    (hints.WINDOW_GAP_S, [], False),  # tool calls alone
    (hints.WINDOW_GAP_S, ["a"], True),
    (3 * hints.WINDOW_GAP_S, ["a", "b"], True),
])
def test_a_window_is_due_after_window_gap_s_with_a_new_agent_message(on_clock, messages, due):
    assert hints.window_due(5000.0 + on_clock, 5000.0, messages) is due
    assert hints.window_due(5000.0 + on_clock, None, messages) is False, "no clock before the first step"


def test_a_windows_segments_are_its_newest_messages_first_each_bounded():
    segments = hints.window_segments([f"m{i}" for i in range(40)] + ["  ", "x" * 10000])
    assert len(segments) == hints.WINDOW_MAX_SEGMENTS
    assert segments[0] == "x" * (hints.WINDOW_SEGMENT_CHARS + hints.SCAN_MARGIN_CHARS)
    assert segments[1:3] == ["m39", "m38"] and segments[-1] == "m9"
    assert hints.window_text(["b", "a"]) == "b\n\na"
    assert len(hints.window_text(["y" * 9000, "z" * 9000])) == hints.MAX_TEXT_CHARS


def test_a_window_look_sends_each_agent_message_since_and_never_a_tool_or_reasoning(tmp_path, state):
    session = _session(tmp_path, state)
    api = Api()
    clock = Clock()
    lane, logs = _lane(tmp_path, [session], api, clock)
    _seen(lane, session)
    cwd = session.cwd
    _append(session, _said("first: sweep lr on digits-mlp", cwd, 0),
            _called("Bash", {"command": "python train.py --lr 0.1"}, cwd, 60),
            _output("epoch 1 loss 0.9 OUTPUT-ONLY", cwd, 61),
            _thought("maybe the scaler matters", cwd, 120),
            _said("second: standardizing inputs next", cwd, 300))
    lane.read_once()
    assert lane.run_due() == 0, "under WINDOW_GAP_S on the clock"
    _append(session, _step(cwd, hints.WINDOW_GAP_S))
    lane.read_once()
    assert lane.run_due() == 1
    [body] = api.bodies
    assert body["trigger"] == "window" and body["session_id"] == SID
    assert body["segments"] == ["second: standardizing inputs next", "first: sweep lr on digits-mlp"]
    assert body["text"] == "second: standardizing inputs next\n\nfirst: sweep lr on digits-mlp"
    sent = json.dumps(body)
    assert "train.py" not in sent and "OUTPUT-ONLY" not in sent and "scaler" not in sent
    assert any(m.startswith(f"hints: session {SID} window (2 messages)") for m in logs)
    # The clock starts again at the step that made it due.
    clock.now += hints.SESSION_GAP_S
    _append(session, _said("third", cwd, hints.WINDOW_GAP_S + 60), _step(cwd, 2 * hints.WINDOW_GAP_S - 1))
    lane.read_once()
    assert lane.run_due() == 0
    _append(session, _step(cwd, 2 * hints.WINDOW_GAP_S))
    lane.read_once()
    assert lane.run_due() == 1 and api.bodies[1]["segments"] == ["third"]


def test_a_prompt_starts_the_window_clock_again_and_a_search_does_not(tmp_path, state):
    session = _session(tmp_path, state)
    api = Api()
    clock = Clock()
    lane, _ = _lane(tmp_path, [session], api, clock)
    _seen(lane, session)
    cwd = session.cwd
    _append(session, _said("before the prompt", cwd, 0), {**_user("now try the svm", cwd), "timestamp": _at(400)})
    lane.read_once()
    lane.run_due()
    clock.now += hints.SESSION_GAP_S
    _append(session, _called("WebSearch", {"query": "svm digits benchmark"}, cwd, 500))
    lane.read_once()
    lane.run_due()
    clock.now += hints.SESSION_GAP_S
    _append(session, _said("after the prompt", cwd, 700), _step(cwd, 400 + hints.WINDOW_GAP_S - 1))
    lane.read_once()
    assert lane.run_due() == 0, "WINDOW_GAP_S from the prompt, not from the first message"
    _append(session, _step(cwd, 400 + hints.WINDOW_GAP_S))
    lane.read_once()
    assert lane.run_due() == 1
    assert [b["trigger"] for b in api.bodies] == ["prompt", "search", "window"]
    assert api.bodies[-1]["segments"] == ["after the prompt"]


def test_tool_calls_alone_never_make_a_window_look(tmp_path, state):
    session = _session(tmp_path, state)
    api = Api()
    lane, _ = _lane(tmp_path, [session], api)
    _seen(lane, session)
    _append(session, _step(session.cwd, 0), _step(session.cwd, 2 * hints.WINDOW_GAP_S))
    lane.read_once()
    assert lane.run_due() == 0
    _append(session, _said("now a message", session.cwd, 2 * hints.WINDOW_GAP_S + 1))
    lane.read_once()
    assert lane.run_due() == 1 and api.bodies[0]["segments"] == ["now a message"]


def test_a_window_waits_behind_another_lookup_and_loses_no_message(tmp_path, state):
    session = _session(tmp_path, state)
    api = Api()
    clock = Clock()
    lane, _ = _lane(tmp_path, [session], api, clock)
    _seen(lane, session)
    cwd = session.cwd
    _append(session, _said("one", cwd, 0))
    lane.read_once()
    lane.trigger(session, "search", "first search")
    lane.run_due()
    lane.trigger(session, "search", "second search")  # waits out the session's gap
    _append(session, _said("two", cwd, hints.WINDOW_GAP_S))
    lane.read_once()
    assert lane.run_due() == 0
    clock.now += hints.SESSION_GAP_S
    assert lane.run_due() == 1 and api.bodies[-1]["text"] == "second search"
    clock.now += hints.SESSION_GAP_S
    _append(session, _step(cwd, hints.WINDOW_GAP_S + 10))
    lane.read_once()
    assert lane.run_due() == 1 and api.bodies[-1]["segments"] == ["two", "one"]


def test_a_turn_that_ends_drops_a_waiting_window_look(tmp_path, state):
    session = _session(tmp_path, state)
    api = Api()
    clock = Clock()
    lane, _ = _lane(tmp_path, [session], api, clock)
    _seen(lane, session)
    lane.trigger(session, "search", "a search")
    lane.run_due()
    _append(session, _said("one", session.cwd, 0), _said("two", session.cwd, hints.WINDOW_GAP_S),
            _turn_end(session.cwd))
    lane.read_once()
    clock.now += hints.SESSION_GAP_S
    assert lane.run_due() == 0 and lane.stats["ended"] == 1


def test_prompts_go_before_a_window_and_a_window_never_takes_the_last_tokens(tmp_path, state):
    looking, asking = _session(tmp_path, state), _session(tmp_path, state, sid=OTHER)
    api = Api()
    clock = Clock()
    lane, _ = _lane(tmp_path, [looking, asking], api, clock)
    _seen(lane, looking)
    _append(looking, _said("one", looking.cwd, 0), _said("two", looking.cwd, hints.WINDOW_GAP_S))
    lane.read_once()
    lane.trigger(asking, "prompt", "the researcher asks")
    assert lane.run_due() == 2
    assert [b["trigger"] for b in api.bodies] == ["prompt", "window"], "of the lookups due, a window goes last"
    clock.now += hints.SESSION_GAP_S
    with lane._cv:
        lane._tokens, lane._filled_at = 1.0, clock.now
    _append(looking, _said("three", looking.cwd, 2 * hints.WINDOW_GAP_S + 20))
    lane.read_once()
    with lane._cv:
        job, wait = lane.take_due(True)
    assert job is None and wait == pytest.approx((hints.WINDOW_TOKEN_RESERVE - 1.0) * 60.0 / hints.BUCKET_PER_MIN)
    lane.trigger(asking, "prompt", "a prompt takes the last token")
    assert lane.run_due() == 1 and api.bodies[-1]["trigger"] == "prompt"
    clock.now += hints.WINDOW_TOKEN_RESERVE * 60.0 / hints.BUCKET_PER_MIN
    assert lane.run_due() == 1 and api.bodies[-1]["segments"] == ["three"]


def test_a_message_in_a_folder_probe_config_turns_off_never_leaves(tmp_path, state):
    session = _session(tmp_path, state)
    secret = Path(session.cwd) / "secret"
    secret.mkdir()
    (Path(session.cwd) / ".probe.config").write_text("secret/\n")
    api = Api()
    lane, _ = _lane(tmp_path, [session], api)
    _seen(lane, session)
    _append(session, _said("work in the secret folder", str(secret), 0), _said("work in the project", session.cwd, 60),
            _step(str(secret), hints.WINDOW_GAP_S + 60), _step(session.cwd, hints.WINDOW_GAP_S + 61))
    lane.read_once()
    assert lane.run_due() == 1, "the clock starts at the first step kept"
    assert api.bodies[0]["segments"] == ["work in the project"]


def test_a_credential_in_a_window_message_never_leaves_the_machine(tmp_path, state):
    session = _session(tmp_path, state)
    api = Api()
    lane, _ = _lane(tmp_path, [session], api)
    _seen(lane, session)
    key = "x" * (hints.WINDOW_SEGMENT_CHARS - 10) + " sk-ant-api03-" + "a" * 80
    _append(session, _said(key, session.cwd, 0), _step(session.cwd, hints.WINDOW_GAP_S))
    lane.read_once()
    lane.run_due()
    [segment] = api.bodies[0]["segments"]
    assert "sk-ant" not in segment and len(segment) <= hints.WINDOW_SEGMENT_CHARS
    assert "sk-ant" not in api.bodies[0]["text"]


def _window_marker(session: hints.Followed) -> Path:
    with mailbox.rooted(session.state):
        return mailbox.hints_window_path(session.sid)


def _look(lane: hints.HintLane, session: hints.Followed, clock: Clock, sent: bool = True) -> None:
    """One window look for `session` from its transcript: a message, then a step
    WINDOW_GAP_S on the window clock; sent now (or held, `sent` False)."""
    state = lane._state(session.sid)
    at = state.window_since - T0 + 1 if state.window_since is not None else 0.0
    lane.stats["test_looks"] += 1
    _append(session, _said(f"message {lane.stats['test_looks']}", session.cwd, at),
            _step(session.cwd, at + hints.WINDOW_GAP_S))
    lane.read_once()
    assert lane.run_due() == (1 if sent else 0)
    clock.now += hints.SESSION_GAP_S


NO_WINDOW = {"detail": [{"type": "enum", "loc": ["body", "trigger"], "msg": "Input should be 'prompt', 'peer', "
                         "'search' or 'command'"}]}


@pytest.mark.parametrize("answers, marked", [
    ([], False),  # no window lookup answered yet
    ([(200, WINDOW_SHADOW)], True),
    ([(200, {**WINDOW_SHADOW, "trigger_class": "prompt"})], False),  # answered, but not as a window
    ([(200, WINDOW_SHADOW), (422, NO_WINDOW)], False),  # an older server
    ([(200, WINDOW_SHADOW), (404, {"detail": "no route"})], False),
    ([(200, WINDOW_SHADOW), (200, WINDOW_ERROR)], True),  # one failure
    ([(200, WINDOW_SHADOW), (429, {"detail": "slow down"})], True),  # one failure, and held a while
    ([(200, WINDOW_SHADOW), (401, {"detail": "no"})], False),  # a refused key: no marker at all
    ([(200, WINDOW_SHADOW), (200, WINDOW_ERROR), None], False),  # two in a row
    ([(200, WINDOW_SHADOW), (500, {}), (200, {**WINDOW_SHADOW, "reason": "rate_limited"})], False),
    ([(200, WINDOW_SHADOW), (200, WINDOW_ERROR), (200, WINDOW_ERROR), (200, WINDOW_SHADOW)], True),  # works again
])
def test_the_window_marker_is_touched_only_while_window_lookups_work(tmp_path, state, answers, marked):
    """W3: the session's reader stops its check-ins only on proof that window
    hints work for it; any failure lets the marker go stale and they resume."""
    session = _session(tmp_path, state)
    api = Api(default=(200, WINDOW_SHADOW))
    clock = Clock()
    lane, _ = _lane(tmp_path, [session], api, clock)
    _seen(lane, session)
    api.script = [TimeoutError("no answer") if a is None else a for a in answers]
    for _answer in answers:
        _look(lane, session, clock)
    marker = _window_marker(session)
    with contextlib.suppress(FileNotFoundError):
        marker.unlink()
    clock.now += hints.HINTS_LIVE_BEAT_S
    lane.read_once()
    assert _live(session).is_file()
    assert marker.is_file() is marked


def test_a_transcript_not_read_lately_stops_the_window_marker(tmp_path, state):
    session = _session(tmp_path, state)
    clock = Clock()
    lane, _ = _lane(tmp_path, [session], Api(default=(200, WINDOW_SHADOW)), clock)
    _seen(lane, session)
    _look(lane, session, clock)
    clock.now += hints.HINTS_LIVE_BEAT_S
    lane.read_once()
    marker = _window_marker(session)
    assert marker.is_file()
    marker.unlink()
    os.unlink(session.transcript)
    clock.now += hints.WINDOW_READ_FRESH_S + 1
    lane.read_once()
    assert not marker.is_file() and _live(session).is_file()


@pytest.mark.parametrize("answer", [(404, {"detail": "Not Found"}), (422, NO_WINDOW)])
def test_a_server_without_window_lookups_holds_them_never_its_prompts(tmp_path, state, answer):
    session = _session(tmp_path, state)
    api = Api(default=(200, WINDOW_SHADOW))
    api.script = [answer]
    clock = Clock()
    lane, logs = _lane(tmp_path, [session], api, clock)
    _seen(lane, session)
    _look(lane, session, clock)
    lane.trigger(session, "prompt", "the prompt still asks")
    assert lane.run_due() == 1
    clock.now += hints.SESSION_GAP_S
    _look(lane, session, clock, sent=False)
    clock.now += hints.MISSING_S
    assert lane.run_due() == 1
    assert [b["trigger"] for b in api.bodies] == ["window", "prompt", "window"]
    assert any(f"answered {answer[0]}; window lookups on this server are not asked" in m for m in logs)


def test_a_422_about_one_requests_content_holds_no_window_lookup(tmp_path, state):
    """Only a 422 naming `trigger` says the server has no window lookups."""
    session = _session(tmp_path, state)
    api = Api(default=(200, WINDOW_SHADOW))
    api.script = [(200, WINDOW_SHADOW), (422, {"detail": [{"type": "string_too_long", "loc": ["body", "segments", 0]}]})]
    clock = Clock()
    lane, _ = _lane(tmp_path, [session], api, clock)
    _seen(lane, session)
    _look(lane, session, clock)
    _look(lane, session, clock)
    _look(lane, session, clock)  # not held
    assert lane._window_ok and lane._state(session.sid).window_failures == 0


@pytest.mark.parametrize("answer", [(429, {"detail": "slow down"}), (200, {**WINDOW_SHADOW, "reason": "rate_limited"})])
def test_a_window_past_its_teams_rate_holds_only_that_keys_windows(tmp_path, state, answer):
    session = _session(tmp_path, state, KEY="pk_a")
    other_key = _session(tmp_path, state, sid=OTHER, KEY="pk_b")
    api = Api(default=(200, WINDOW_SHADOW))
    api.script = [answer]
    clock = Clock()
    lane, logs = _lane(tmp_path, [session, other_key], api, clock)
    lane.endpoint_of = _keyed
    _seen(lane, session)
    _seen(lane, other_key)
    _look(lane, session, clock)
    lane.trigger(session, "search", "a search still asks")
    assert lane.run_due() == 1
    clock.now += hints.SESSION_GAP_S
    _look(lane, other_key, clock)  # another key's windows on the same server still go
    _look(lane, session, clock, sent=False)
    clock.now += hints.LIMITED_S
    assert lane.run_due() == 1
    assert api.bodies[-1]["segments"] == ["message 3", "message 1"], "the failed look's messages went into the next"
    assert any("window lookups of this key on this server are not asked for 60 s" in m for m in logs)


def test_a_window_with_no_answer_holds_window_lookups_a_while(tmp_path, state):
    """A window waits WINDOW_TIMEOUT_S on its thread: a server not answering
    is not asked another for LIMITED_S, and prompts still go."""
    session, other = _session(tmp_path, state), _session(tmp_path, state, sid=OTHER)
    asking = _session(tmp_path, state, sid=PEER)
    api = Api(default=(200, WINDOW_SHADOW))
    api.script = [TimeoutError("no answer")]
    clock = Clock()
    lane, _ = _lane(tmp_path, [session, other, asking], api, clock)
    _seen(lane, session)
    _seen(lane, other)
    _look(lane, session, clock)
    _look(lane, other, clock, sent=False)
    lane.trigger(asking, "prompt", "a prompt goes")
    assert lane.run_due() == 1 and api.bodies[-1]["trigger"] == "prompt"
    clock.now += hints.LIMITED_S
    assert lane.run_due() == 1 and api.bodies[-1]["trigger"] == "window"


def test_a_window_request_waits_window_timeout_s_and_any_other_timeout_s(monkeypatch):
    from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

    class Slow(BaseHTTPRequestHandler):
        protocol_version = "HTTP/1.1"

        def log_message(self, *args) -> None:
            pass

        def handle_error(self, *args) -> None:
            pass

        def do_POST(self) -> None:
            body = json.loads(self.rfile.read(int(self.headers.get("Content-Length") or 0)))
            if body.get("text") != "fast":
                time.sleep(0.6)
            out = json.dumps(WINDOW_SHADOW).encode()
            with contextlib.suppress(OSError):
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", str(len(out)))
                self.end_headers()
                self.wfile.write(out)

    server = ThreadingHTTPServer(("127.0.0.1", 0), Slow)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    monkeypatch.setattr(hints, "TIMEOUT_S", 0.3)
    monkeypatch.setattr(hints.HintFetcher, "timeout", 0.3)  # as in production: the socket's own, TIMEOUT_S
    monkeypatch.setattr(hints, "WINDOW_TIMEOUT_S", 3.0)
    try:
        fetch = hints.HintFetcher(VERSION)
        ep = Endpoint(f"http://127.0.0.1:{server.server_address[1]}", "pk_read")
        prompt = fetch(ep, {"trigger": "prompt", "text": "slow"})
        window = fetch(ep, {"trigger": "window", "text": "slow", "segments": ["slow"]})
        fast = fetch(ep, {"trigger": "prompt", "text": "fast"})  # a kept connection, its socket at 0.3 s
        kept = fetch(ep, {"trigger": "window", "text": "slow", "segments": ["slow"]})
    finally:
        server.shutdown()
        server.server_close()
    assert prompt == (None, None)
    assert window == (200, WINDOW_SHADOW)
    assert fast == (200, WINDOW_SHADOW) and kept == (200, WINDOW_SHADOW)


def test_a_window_request_outwaits_the_servers_window_lookup():
    """The server spends its window budget on the engine, then at most five
    database statements under its statement timeout, before it answers."""
    source = AGENT_ROOT.parent / "app" / "hints" / "service.py"
    if not source.is_file():
        pytest.skip("the server's code is not beside this package")
    text = source.read_text(encoding="utf-8")
    engine = float(re.search(r"^ENGINE_BUDGET_SECONDS = ([\d.]+)", text, re.M).group(1))
    window = re.search(r"^WINDOW_BUDGET_SECONDS = (.+)$", text, re.M).group(1).strip()
    budget = engine if window == "ENGINE_BUDGET_SECONDS" else float(window)
    statement = float(re.search(r"statement_timeout = '(\d+)ms'", text).group(1)) / 1000.0
    assert hints.WINDOW_TIMEOUT_S >= budget + 5 * statement


def test_a_window_request_fits_the_servers_accepted_bounds():
    """Past one of them the server answers 422, and a 422 naming no `trigger` is
    one more failure: every window would fail."""
    source = AGENT_ROOT.parent / "app" / "hints" / "schemas.py"
    if not source.is_file():
        pytest.skip("the server's code is not beside this package")
    text = source.read_text(encoding="utf-8")

    def bound(name: str) -> int:
        return int(re.search(rf"^{name} = ([\d_]+)", text, re.M).group(1).replace("_", ""))

    assert hints.MAX_EXCLUDE_DOC_IDS <= bound("MAX_EXCLUDED_DOCS")
    assert hints.WINDOW_MAX_SEGMENTS <= bound("MAX_SEGMENTS_ACCEPTED")
    assert hints.WINDOW_SEGMENT_CHARS <= bound("MAX_SEGMENT_CHARS_ACCEPTED")


def test_only_a_server_that_answered_a_window_is_named_more_than_50_records(tmp_path, state):
    """A server before window lookups (#3402) refuses more than 50 `exclude_doc_ids`."""
    session = _session(tmp_path, state)
    api = Api(default=(200, WINDOW_SHADOW))
    clock = Clock()
    lane, _ = _lane(tmp_path, [session], api, clock)
    lane._shown = lambda session, state: [frozenset(f"doc-{i} 10-21" for i in range(150))]
    _seen(lane, session)
    lane.trigger(session, "prompt", "before any window")
    lane.run_due()
    clock.now += hints.SESSION_GAP_S
    _look(lane, session, clock)
    lane.trigger(session, "prompt", "after a window answered as one")
    lane.run_due()
    assert [len(b["exclude_doc_ids"]) for b in api.bodies] == [hints.LEGACY_EXCLUDE_DOC_IDS,
                                                               hints.LEGACY_EXCLUDE_DOC_IDS, hints.MAX_EXCLUDE_DOC_IDS]


def test_a_first_look_counts_no_old_agent_message_for_the_window(tmp_path, state):
    session = _session(tmp_path, state)
    api = Api()
    lane, _ = _lane(tmp_path, [session], api)
    _append(session, {**_said("old work", session.cwd, 0), "timestamp": _stamp(hints.FRESH_S + 60)},
            {**_said("new work", session.cwd, 0), "timestamp": _stamp(0)})
    lane.read_once()  # the first look: only lines younger than FRESH_S
    _append(session, {**_step(session.cwd, 0), "timestamp": _stamp(-(hints.WINDOW_GAP_S + 5))})
    lane.read_once()
    assert lane.run_due() == 1 and api.bodies[0]["segments"] == ["new work"]


def test_a_window_replaced_by_a_search_while_it_waits_loses_no_message(tmp_path, state):
    session = _session(tmp_path, state)
    api = Api()
    clock = Clock()
    lane, _ = _lane(tmp_path, [session], api, clock)
    _seen(lane, session)
    lane.trigger(session, "search", "first")
    lane.run_due()  # the session's gap runs from now
    _append(session, _said("one", session.cwd, 0), _said("two", session.cwd, hints.WINDOW_GAP_S))
    lane.read_once()
    assert lane._pending[SID].trigger == "window"
    _append(session, _said("three", session.cwd, hints.WINDOW_GAP_S + 1))
    lane.read_once()
    assert len(lane._pending) == 1, "one window waits; a later step queues no second"
    lane.trigger(session, "search", "second")  # replaces the waiting window
    clock.now += hints.SESSION_GAP_S
    assert lane.run_due() == 1 and api.bodies[-1]["text"] == "second"
    clock.now += hints.SESSION_GAP_S
    _append(session, _step(session.cwd, hints.WINDOW_GAP_S + 5))
    lane.read_once()
    assert lane.run_due() == 1 and api.bodies[-1]["segments"] == ["three", "two", "one"]


def test_a_prompt_drops_a_waiting_window_and_its_messages(tmp_path, state):
    session = _session(tmp_path, state)
    api = Api()
    clock = Clock()
    lane, _ = _lane(tmp_path, [session], api, clock)
    _seen(lane, session)
    lane.trigger(session, "search", "first")
    lane.run_due()
    _append(session, _said("before", session.cwd, 0), _said("due", session.cwd, hints.WINDOW_GAP_S))
    lane.read_once()
    assert lane._pending[SID].trigger == "window"
    _append(session, {**_user("now the svm", session.cwd), "timestamp": _at(hints.WINDOW_GAP_S + 2)})
    lane.read_once()
    clock.now += hints.SESSION_GAP_S
    assert lane.run_due() == 1 and [b["trigger"] for b in api.bodies] == ["search", "prompt"]
    assert not lane._state(SID).window_messages


def test_a_turn_end_ends_its_window(tmp_path, state):
    """The finished turn's messages are not looked at again, and the next turn's
    window clock starts at its first step, not at the turn end."""
    session = _session(tmp_path, state)
    api = Api()
    clock = Clock()
    lane, _ = _lane(tmp_path, [session], api, clock)
    _seen(lane, session)
    _append(session, _said("old turn work", session.cwd, 0), _turn_end(session.cwd))
    lane.read_once()
    later = 3 * 3600
    _append(session, _said("a background job finished", session.cwd, later), _step(session.cwd, later + 60))
    lane.read_once()
    assert lane.run_due() == 0, "a new turn's first minute: nothing due"
    _append(session, _step(session.cwd, later + hints.WINDOW_GAP_S))
    lane.read_once()
    assert lane.run_due() == 1 and api.bodies[0]["segments"] == ["a background job finished"]


def _pi(text: str, at: float, *, stop: bool) -> dict:
    message = {"role": "assistant", "content": [{"type": "text", "text": text}]}
    if stop:
        message["stopReason"] = "stop"
    return {"type": "message", "timestamp": _at(at), "message": message}


def test_a_turns_last_message_on_its_end_line_queues_no_window(tmp_path, state):
    """pi writes a turn's last message and its end on one line: no window is
    looked up for a turn that is over (its hint would wait for the next prompt)."""
    session = dataclasses.replace(_session(tmp_path, state), harness="pi")
    api = Api(default=(200, _on()))
    lane, _ = _lane(tmp_path, [session], api)
    _seen(lane, session)
    _append(session, _pi("working", 0, stop=False))
    lane.read_once()
    _append(session, _pi("done", hints.WINDOW_GAP_S + 5, stop=True))
    lane.read_once()
    assert lane.run_due() == 0 and _waiting(session) == [] and lane.stats["trigger_window"] == 1
    assert not lane._state(SID).window_messages


def test_a_window_taken_before_its_turn_ended_is_not_sent(tmp_path, state):
    session = _session(tmp_path, state)
    api = Api()
    lane, _ = _lane(tmp_path, [session], api)
    _seen(lane, session)
    _append(session, _said("one", session.cwd, 0), _step(session.cwd, hints.WINDOW_GAP_S))
    lane.read_once()
    with lane._cv:
        job, _wait = lane.take_due(True)
    _append(session, _turn_end(session.cwd))
    lane.read_once()
    lane.lookup(job)
    assert api.bodies == [] and lane.stats["stale"] == 1


def test_a_harness_that_shows_hints_only_at_a_prompt_gets_no_window(tmp_path, state):
    """Kimi Code hands a message over only at the next prompt, after the turn's
    end has withdrawn it: no window lookup, and no marker to stop its check-ins."""
    session, other = _session(tmp_path, state), _session(tmp_path, state, sid=OTHER)
    api = Api(default=(200, WINDOW_SHADOW))
    clock = Clock()
    lane, _ = _lane(tmp_path, [session, other], api, clock)
    _seen(lane, other)
    _look(lane, other, clock)  # the key's window lookups work
    _seen(lane, session)
    tail = lane._tails[SID]
    tail.adapter.capabilities = dataclasses.replace(tail.adapter.capabilities, inject_tool=False)
    _append(session, _said("one", session.cwd, 0), _step(session.cwd, hints.WINDOW_GAP_S))
    lane.read_once()
    assert lane.run_due() == 0
    clock.now += hints.HINTS_LIVE_BEAT_S
    lane.read_once()
    assert _live(session).is_file() and not _window_marker(session).exists()
    assert hints.shows_mid_turn(tail.adapter) is False
    for harness in ("claude_code", "codex", "pi"):
        from probe.daemon import adapters

        assert hints.shows_mid_turn(adapters.for_source(harness)), harness


def test_a_key_whose_window_lookups_fail_stops_every_sessions_marker(tmp_path, state):
    a, b = _session(tmp_path, state), _session(tmp_path, state, sid=OTHER)
    api = Api(default=(200, WINDOW_SHADOW))
    clock = Clock()
    lane, _ = _lane(tmp_path, [a, b], api, clock)
    _seen(lane, a)
    _seen(lane, b)
    _look(lane, a, clock)
    api.script = [(200, WINDOW_ERROR), (200, WINDOW_ERROR)]
    _look(lane, a, clock)
    _look(lane, a, clock)
    with contextlib.suppress(FileNotFoundError):
        _window_marker(b).unlink()
    clock.now += hints.HINTS_LIVE_BEAT_S
    lane.read_once()
    assert not _window_marker(b).exists(), "b sent none, but its key's window lookups fail"


def test_a_turn_looked_at_by_no_window_for_a_check_ins_length_stops_the_marker(tmp_path, state):
    """A turn of tool calls only (no message, so no window): the reader's
    check-in comes back after WINDOW_COVERS_S."""
    session = _session(tmp_path, state)
    clock = Clock()
    lane, _ = _lane(tmp_path, [session], Api(default=(200, WINDOW_SHADOW)), clock)
    _seen(lane, session)
    _look(lane, session, clock)
    with lane._cv:
        lane._state(SID).window_since = time.time() - hints.WINDOW_COVERS_S - 1
    marker = _window_marker(session)
    with contextlib.suppress(FileNotFoundError):
        marker.unlink()
    clock.now += hints.HINTS_LIVE_BEAT_S
    lane.read_once()
    assert not marker.exists()


def test_a_counted_tool_call_never_runs_the_filters_per_call_reads(tmp_path, state, monkeypatch):
    """The window only counts a tool call: its folder's verdict, never the
    filter's reads of what it touches (they walk trees, ~1 s each)."""
    from probe.daemon import exclusions

    called: list = []
    monkeypatch.setattr(exclusions.Filter, "_call_excluded", lambda self, event, where: called.append(1) or False)
    session = _session(tmp_path, state)
    secret = Path(session.cwd) / "secret"
    secret.mkdir()
    (Path(session.cwd) / ".probe.config").write_text("secret/\n")
    api = Api()
    lane, _ = _lane(tmp_path, [session], api)
    _seen(lane, session)
    _append(session, _said("one", session.cwd, 0), _called("Bash", {"command": "git status"}, session.cwd, 60),
            _called("Bash", {"command": "ls"}, str(secret), hints.WINDOW_GAP_S))
    lane.read_once()
    assert called == [] and lane.run_due() == 0, "a step in an `off` folder is not counted"
    _append(session, _called("Bash", {"command": "rg x ."}, session.cwd, hints.WINDOW_GAP_S + 1))
    lane.read_once()
    assert called == [] and lane.run_due() == 1


def test_past_max_pending_a_window_goes_before_any_other_lookup(tmp_path, state, monkeypatch):
    monkeypatch.setattr(hints, "MAX_PENDING", 3)
    sessions = [_session(tmp_path, state, sid=f"{i:08d}-0000-0000-0000-000000000000") for i in range(5)]
    lane, _ = _lane(tmp_path, sessions, Api())
    looking = sessions[0]
    state0 = lane._state(looking.sid)
    with lane._cv:
        state0.window_messages.append("a message")
    lane._queue_window(looking, state0, T0)
    for s in sessions[1:4]:
        lane.trigger(s, "prompt", f"prompt of {s.sid}")
    assert [j.trigger for j in lane._pending.values()] == ["prompt"] * 3
    lane._queue_window(looking, state0, T0)
    assert [j.trigger for j in lane._pending.values()] == ["prompt"] * 3, "a window never evicts a prompt"


def test_a_window_short_of_its_reserve_never_delays_a_lookup_that_needs_one_token(tmp_path, state):
    looking, asking = _session(tmp_path, state), _session(tmp_path, state, sid=OTHER)
    clock = Clock()
    lane, _ = _lane(tmp_path, [looking, asking], Api(), clock)
    lane.trigger(asking, "search", "first")
    lane.run_due()
    clock.now += hints.SESSION_GAP_S - 1
    lane.trigger(asking, "search", "due in a second")
    state0 = lane._state(looking.sid)
    with lane._cv:
        state0.window_messages.append("a message")
    lane._queue_window(looking, state0, T0)
    with lane._cv:
        lane._tokens, lane._filled_at = 1.0, clock.now
        window, window_wait = lane.take_due(True)
        job, wait = lane.take_due(False)
    assert window is None and window_wait == pytest.approx(
        (hints.WINDOW_TOKEN_RESERVE - 1.0) * 60.0 / hints.BUCKET_PER_MIN)
    assert job is None and wait == pytest.approx(1.0), "the search waits only its own gap"
    clock.now += 1.0
    with lane._cv:
        job, _wait = lane.take_due(False)
    assert job is not None and job.text == "due in a second"


def test_a_failed_window_whose_turn_ended_puts_no_message_back(tmp_path, state):
    session = _session(tmp_path, state)
    api = Api(default=(200, WINDOW_SHADOW))
    api.script = [TimeoutError("no answer")]
    lane, _ = _lane(tmp_path, [session], api)
    _seen(lane, session)
    _append(session, _said("the old turn", session.cwd, 0), _step(session.cwd, hints.WINDOW_GAP_S))
    lane.read_once()
    with lane._cv:
        job, _wait = lane.take_due(True)
    state_ = lane._state(SID)
    lane.lookup(job)  # sent, no answer: its messages are back
    assert list(state_.window_messages) == ["the old turn"]
    with lane._cv:
        state_.window_messages.clear()
    lane.turn_ended(session)
    api.script = [TimeoutError("no answer")]
    job.epoch = state_.epoch - 1
    lane._window_answered(job, state_, None, None)
    assert not state_.window_messages, "its turn is over: nothing back"


@pytest.mark.parametrize("answer", [(404, {"detail": "Not Found"}), (422, NO_WINDOW),
                                    (422, {"detail": [{"loc": ["body", "segments", 0]}]}), (400, {"detail": "bad"})])
def test_a_window_refused_for_its_content_or_route_puts_no_message_back(tmp_path, state, answer):
    session = _session(tmp_path, state)
    api = Api(default=(200, WINDOW_SHADOW))
    api.script = [answer]
    clock = Clock()
    lane, _ = _lane(tmp_path, [session], api, clock)
    _seen(lane, session)
    _look(lane, session, clock)
    assert not lane._state(SID).window_messages


# ---------------------------------------------------------------------------
# Latency (plan hints-latency L3, L4, R7, R9).
# ---------------------------------------------------------------------------


def test_a_window_just_sent_never_delays_its_sessions_prompt(tmp_path, state):
    """Each kind waits SESSION_GAP_S after its own lookup only (R7): a prompt
    right behind its session's window goes at once; a second prompt still waits."""
    session = _session(tmp_path, state)
    api = Api(default=(200, WINDOW_SHADOW))
    clock = Clock()
    lane, _ = _lane(tmp_path, [session], api, clock)
    _seen(lane, session)
    _append(session, _said("one", session.cwd, 0), _said("two", session.cwd, hints.WINDOW_GAP_S))
    lane.read_once()
    with lane._cv:
        window, _wait = lane.take_due(True)
    assert window is not None and window.trigger == "window"
    lane.trigger(session, "prompt", "the researcher asks right after")
    with lane._cv:
        prompt, wait = lane.take_due(False)
    assert prompt is not None and prompt.trigger == "prompt" and wait is None
    lane.trigger(session, "prompt", "and again")
    with lane._cv:
        job, wait = lane.take_due(False)
    assert job is None and wait == pytest.approx(hints.SESSION_GAP_S)


def test_each_lookup_thread_takes_only_its_own_kind(tmp_path, state):
    session, other = _session(tmp_path, state), _session(tmp_path, state, sid=OTHER)
    lane, _ = _lane(tmp_path, [session, other], Api())
    _seen(lane, session)
    _append(session, _said("one", session.cwd, 0), _said("two", session.cwd, hints.WINDOW_GAP_S))
    lane.read_once()
    lane.trigger(other, "prompt", "a prompt")
    with lane._cv:
        windows = [lane.take_due(True)[0] for _ in range(2)]
        others = [lane.take_due(False)[0] for _ in range(2)]
    assert [j and j.trigger for j in windows] == ["window", None]
    assert [j and j.trigger for j in others] == ["prompt", None]


class _SlowWindows(Api):
    """`/v1/hints` answering a window only once released, anything else at once."""

    def __init__(self) -> None:
        super().__init__()
        self.window_in = threading.Event()
        self.release = threading.Event()

    def __call__(self, ep: Endpoint, body: dict):
        if body["trigger"] == "window":
            self.window_in.set()
            self.release.wait(5)
            return 200, WINDOW_SHADOW
        return super().__call__(ep, body)


def test_a_prompt_is_never_held_up_by_a_window_in_flight(tmp_path, state):
    """The lane's own threads (R5): a window waiting on the server holds its own
    thread only; the prompt that comes meanwhile is asked and answered, and
    `close` stops all three."""
    session = _session(tmp_path, state)
    api = _SlowWindows()
    lane, _ = _lane(tmp_path, [session], api)
    _seen(lane, session)
    _append(session, _said("one", session.cwd, 0), _said("two", session.cwd, hints.WINDOW_GAP_S))
    lane.read_once()  # the window is queued
    lane.changed()
    try:
        assert api.window_in.wait(5), "the window thread asks"
        lane.trigger(session, "prompt", "the researcher asks meanwhile")
        deadline = time.monotonic() + 5
        while not api.bodies and time.monotonic() < deadline:
            time.sleep(0.01)
        assert [b["trigger"] for b in api.bodies] == ["prompt"] and not api.release.is_set()
    finally:
        api.release.set()
        lane.close()
    assert sorted(t.name for t in lane._threads) == ["hints-lookup", "hints-tail", "hints-window"]
    for thread in lane._threads:
        thread.join(2)
        assert not thread.is_alive()


def test_the_window_thread_asks_on_a_fetcher_of_its_own():
    """A fetcher's kept connections are not shared across threads."""
    lane = hints.HintLane(sessions=lambda: [], log=lambda m: None, environ={})
    assert isinstance(lane.window_transport, hints.HintFetcher) and lane.window_transport is not lane.transport


@pytest.mark.parametrize("answer", [(200, SHADOW), (429, {"detail": "slow down"}), (500, {"detail": "boom"})])
def test_every_answered_lookup_says_how_long_after_its_trigger(tmp_path, state, answer):
    """R9: the delay from the trigger to the answer, for every answer, not only
    a hint posted (the latency measure; `posted ... after the trigger` stays)."""
    session = _session(tmp_path, state)
    lane, logs = _lane(tmp_path, [session], Api(default=answer), wall=lambda: 5000.0)
    lane.trigger(session, "prompt", "benchmark RFD4-Proteina", happened=4998.5)
    lane.run_due()
    assert any(m.endswith("; answered 1500 ms after the trigger") for m in logs), logs


# ---------------------------------------------------------------------------
# Two lookup threads answering out of order (review of plan hints-latency L4).
# ---------------------------------------------------------------------------


def _window_due(lane: hints.HintLane, session: hints.Followed) -> hints.Lookup:
    _seen(lane, session)
    _append(session, _said("one", session.cwd, 0), _step(session.cwd, hints.WINDOW_GAP_S))
    lane.read_once()
    with lane._cv:
        window, _wait = lane.take_due(True)
    assert window is not None
    return window


def _record(doc: str) -> dict:
    return {"doc_id": doc, "date": "10-21", "kind": "page"}


def test_a_window_answered_after_a_newer_hint_never_replaces_it(tmp_path, state):
    """The window asked first, a search after it; the search's hint posts
    first. The window's, from the older trigger, would replace it in the
    session's one hint slot: it is not posted."""
    session = _session(tmp_path, state)
    api = Api()
    lane, logs = _lane(tmp_path, [session], api)
    window = _window_due(lane, session)
    lane.trigger(session, "search", "RFD4-Proteina benchmark", happened=window.happened + 1)
    with lane._cv:
        search, _wait = lane.take_due(False)
    api.default = (200, _on("[Probe] search hint", _record("doc-s")))
    lane.lookup(search)
    api.default = (200, {**_on("[Probe] window hint", _record("doc-w")), "trigger_class": "window"})
    lane.lookup(window)
    assert [m.text for m in _waiting(session)] == ["[Probe] search hint"]
    assert lane.stats["superseded"] == 1 and any(f"; {hints.Skip.SUPERSEDED}; answered" in m for m in logs)


@pytest.mark.parametrize("delivered", [True, False])
def test_a_hint_sharing_a_record_with_one_delivered_while_it_was_asked_is_not_posted(tmp_path, state, delivered):
    """A newer search's request was built before the window's hint posted, so
    it could not leave that hint's records out. Delivered meanwhile, a shared
    record would be shown twice: not posted. Still waiting, it is replaced by
    the search's hint: no record is shown twice, and the newer hint goes."""
    session = _session(tmp_path, state)
    claimed: set = set()
    api = Api(default=(200, {**_on("[Probe] window hint", _record("doc-a"), _record("doc-w")),
                             "trigger_class": "window"}))
    lane, _ = _lane(tmp_path, [session], api, delivered=lambda sid, st: set(claimed))
    window = _window_due(lane, session)
    lane.trigger(session, "search", "a newer search", happened=window.happened + 1)
    with lane._cv:
        search, _wait = lane.take_due(False)
    search.posted_before = lane._state(SID).posted  # its request built now, before the window posts
    lane.lookup(window)
    [window_id] = list(lane._state(SID).ledger)
    if delivered:
        claimed.add(window_id)
    posted, why = lane._deliver(search, lane._state(SID), "[Probe] search hint",
                                [_record("doc-a"), _record("doc-s")])
    assert (posted, why) == ((False, hints.Skip.REPEAT) if delivered else (True, "posted"))


def test_a_window_leaves_the_tokens_to_the_lookups_due_now(tmp_path, state):
    """With three tokens, two prompts due and a window due, the window waits:
    the prompts take theirs first, and the reserve stays."""
    looking = _session(tmp_path, state)
    asking = [_session(tmp_path, state, sid=OTHER), _session(tmp_path, state, sid=PEER)]
    clock = Clock()
    lane, _ = _lane(tmp_path, [looking, *asking], Api(), clock)
    _seen(lane, looking)
    _append(looking, _said("one", looking.cwd, 0), _step(looking.cwd, hints.WINDOW_GAP_S))
    lane.read_once()
    for s in asking:
        lane.trigger(s, "prompt", f"prompt of {s.sid}")
    with lane._cv:
        lane._tokens, lane._filled_at = 3.0, clock.now
        window, wait = lane.take_due(True)
        assert window is None and wait > 0
        taken = [lane.take_due(False)[0] for _ in range(2)]
        window, _wait = lane.take_due(True)
    assert [j.trigger for j in taken] == ["prompt", "prompt"]
    assert window is None, "one token left, under the reserve"


def test_a_hint_whose_teams_hints_went_off_meanwhile_is_not_posted(tmp_path, state):
    session = _session(tmp_path, state)
    api = Api(default=(200, _on()))
    lane, logs = _lane(tmp_path, [session], api)
    lane.trigger(session, "prompt", "benchmark RFD4-Proteina")
    with lane._cv:
        job, _wait = lane.take_due(False)
        lane._off[(job.ep.base_url, job.ep.key)] = lane.clock() + hints.OFF_RECHECK_S  # the other thread's answer
    lane.lookup(job)
    assert _waiting(session) == [] and lane.stats["off"] == 1
    assert any(f"; {hints.Skip.OFF}; answered" in m for m in logs)


def test_a_lane_that_closed_while_asking_posts_nothing(tmp_path, state):
    session = _session(tmp_path, state)
    lane, _ = _lane(tmp_path, [session], Api(default=(200, _on())))
    lane.trigger(session, "prompt", "benchmark RFD4-Proteina")
    with lane._cv:
        job, _wait = lane.take_due(False)
    lane.close()
    lane.lookup(job)
    assert _waiting(session) == []


def test_close_aborts_both_fetchers_and_a_request_in_flight_is_never_sent_again(monkeypatch):
    """`close` ends the window thread's request too, and the shut socket is
    no kept connection the server closed: no second try (it would ask again
    and wait on it while the service shuts down)."""
    from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

    seen: list = []
    release = threading.Event()

    class Slow(BaseHTTPRequestHandler):
        protocol_version = "HTTP/1.1"

        def log_message(self, *args) -> None:
            pass

        def do_POST(self) -> None:
            self.rfile.read(int(self.headers.get("Content-Length") or 0))
            seen.append(self.path)
            release.wait(5)

    server = ThreadingHTTPServer(("127.0.0.1", 0), Slow)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    lane = hints.HintLane(sessions=lambda: [], log=lambda m: None, version=VERSION, environ={})
    ep = Endpoint(f"http://127.0.0.1:{server.server_address[1]}", "pk_read")
    answers: list = []
    asking = threading.Thread(target=lambda: answers.append(lane.window_transport(ep, {"trigger": "window"})))
    try:
        asking.start()
        deadline = time.monotonic() + 5
        while not seen and time.monotonic() < deadline:
            time.sleep(0.01)
        started = time.monotonic()
        lane.close()
        asking.join(3)
        took = time.monotonic() - started
    finally:
        release.set()
        server.shutdown()
        server.server_close()
    assert answers == [(None, None)] and seen == ["/v1/hints"] and took < 2
    assert lane.transport.closing and lane.window_transport.closing


def test_an_unfinished_last_line_is_not_read_again_until_the_file_grows(tmp_path, state, monkeypatch):
    session = _session(tmp_path, state)
    lane, _ = _lane(tmp_path, [session], Api())
    _seen(lane, session)
    with open(session.transcript, "a", encoding="utf-8") as out:
        out.write('{"type": "assistant", "partial": "')
    reads: list = []
    real_fdopen = os.fdopen

    def counted(fd, *args, **kwargs):
        handle = real_fdopen(fd, *args, **kwargs)
        real_read = handle.read
        handle.read = lambda *a: reads.append(1) or real_read(*a)
        return handle

    monkeypatch.setattr(hints.os, "fdopen", counted)
    for _ in range(4):
        lane.read_once()
    assert len(reads) == 1, "read once, then left until it grows"
    _append(session, _user("benchmark RFD4-Proteina", session.cwd))
    lane.read_once()
    assert len(reads) == 2
