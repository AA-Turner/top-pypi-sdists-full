"""Only the person's answer path records an answer through the Probe service (#3355).

The Probe daemon holds a risky action until the researcher says yes, and the
coding agent's question tool asks them; the answer hook records their pick. The
service's `mailbox.answer` writes the same answer, and any process of this user
reaches its socket: the agent's own shell among them. So the service takes an
answer only with the held question's answer key (`approvals.Board.mint_key`),
which lives in the approvals folder beside the request: the answer hook reads
it, the agent's shell (which the guard keeps out of that folder) cannot. And
where an answer came from is the service's to say, never the caller's.

These run the real pieces: the service as a process in its own HOME
(`service_harness`), the approvals hook as Claude Code runs it (a subprocess
with the harness's payload on stdin), and the call the agent's shell would make
(`python -I -m probe.service.client call mailbox.answer ...`). Older pieces on
either side stay safe: a hook from before keys is refused and writes the answer
file itself (`fixtures/old_hooks/approvals_hook_before_answer_key.py`, the hook
as plugin 0.170.0 shipped it), and a question filed before keys has none, so
the service refuses every answer to it and the hook writes it.
"""

from __future__ import annotations

import json
import os
import shutil
import stat
import subprocess
import sys
import time
from pathlib import Path

import pytest

from probe.daemon import approvals as appr
from probe.service import client, protocol
from probe.service.mailhost import ANSWER_CHANNEL, MailHost
from probe.service.protocol import ErrorCode, Method
from tests.service_harness import service_home  # noqa: F401 -- a fixture

pytestmark = pytest.mark.skipif(sys.platform == "win32", reason="the service is POSIX-only (plan S8)")

AGENT_ROOT = Path(__file__).resolve().parents[1]
HOOKS = AGENT_ROOT / "plugins" / "probe-research" / "hooks"
OLD_HOOK = Path(__file__).parent / "fixtures" / "old_hooks" / "approvals_hook_before_answer_key.py"
SID = "11111111-2222-3333-4444-555555555555"
COMMAND = "rm -rf ~/scratch-data"


def _state() -> Path:
    return Path(os.environ["XDG_STATE_HOME"]) / "probe"


def _key_file(rid: str) -> Path:
    return _state() / "approvals" / appr.KEYS_DIRNAME / rid


@pytest.fixture
def home(service_home, monkeypatch):  # noqa: F811 -- the harness's fixture, wrapped
    """A running service in its own HOME, with every Probe and agent folder inside it."""
    monkeypatch.setenv("XDG_STATE_HOME", str(service_home.home / "state"))
    monkeypatch.setenv("CLAUDE_CONFIG_DIR", str(service_home.home / ".claude"))
    monkeypatch.setenv("PROBE_OUTBOX_DIR", str(service_home.home / "outbox"))
    monkeypatch.delenv("PROBE_AGENT", raising=False)
    service_home.start()
    return service_home


def _held() -> appr.Request:
    """A shell command the daemon holds for a yes, filed as the daemon files it."""
    return appr.Board().hold(policy="shell.unsafe_command", session_id=SID,
                             facts={"command": COMMAND, "cwd": "/w"},
                             held={"kind": "shell", "command": COMMAND, "cwd": "/w"}, bypass=False)


def _request(rid: str = "a1b2c3d4", command: str = COMMAND) -> appr.Request:
    """A waiting question, built and not filed."""
    facts = {"command": command, "cwd": "/w"}
    return appr.Request(id=rid, policy="shell.unsafe_command", session_id=SID,
                        question=appr.POLICIES["shell.unsafe_command"].render(facts, f"Probe {rid}"),
                        facts=facts, fingerprint="f", held={"kind": "shell", "command": command, "cwd": "/w"},
                        asked_at=time.time(), expires_at=time.time() + 3600, action="a")


def _unkeyed(rid: str = "a1b2c3d4") -> appr.Request:
    """A question as a daemon from before keys filed it: the request alone."""
    req = _request(rid)
    appr.Board().save(req)
    return req


def _hook_env() -> dict:
    return {"PATH": os.environ.get("PATH", "/usr/bin:/bin"), "HOME": os.environ["HOME"],
            "XDG_STATE_HOME": os.environ["XDG_STATE_HOME"]}


def _ask(req: appr.Request, choice: str, hook: Path = HOOKS / "approvals_hook.py") -> None:
    """The person answers through the question tool: PreToolUse, then PostToolUse
    with their pick, each run by the harness as a subprocess."""
    q = req.question
    tool_input = {"questions": [{"header": q.header, "question": q.question, "multiSelect": False,
                                 "options": [{"label": q.yes_label, "description": ""},
                                             {"label": q.no_label, "description": ""}]}]}
    base = {"session_id": SID, "cwd": "/tmp", "tool_name": "AskUserQuestion", "tool_input": tool_input,
            "tool_use_id": f"toolu_{req.id}"}
    for payload in ({**base, "hook_event_name": "PreToolUse"},
                    {**base, "hook_event_name": "PostToolUse", "tool_response": {"answers": {q.question: choice}}}):
        done = subprocess.run([sys.executable, str(hook)], input=json.dumps(payload), capture_output=True,
                              text=True, env=_hook_env(), timeout=30)
        assert (done.returncode, done.stdout) == (0, ""), done.stderr


def _written_by_the_service(rid: str) -> bool:
    """`Board.answer` (the service's step) writes indented JSON; the hook's own write is one line."""
    return "\n" in (_state() / "approvals" / "answers" / f"{rid}.json").read_text(encoding="utf-8").strip()


# ---------------------------------------------------------------------------
# The agent's shell is refused.
# ---------------------------------------------------------------------------


def test_the_agents_shell_cannot_say_yes_through_the_service(home):
    """The report's call, as the agent's shell makes it: one RPC, no file named.
    Before the key it came back `{"answered": true}` and the daemon ran the command."""
    req = _held()
    params = {"state_dir": str(_state()), "id": req.id, "choice": req.question.yes_label,
              "channel": "question-tool"}
    out = subprocess.run([sys.executable, "-I", "-m", "probe.service.client", "call", Method.MAILBOX_ANSWER,
                          json.dumps(params)], capture_output=True, text=True, env=dict(os.environ), timeout=30)
    answer = json.loads(out.stdout)
    assert answer.get("answered") is not True
    assert out.returncode == 3 and answer["error"]["code"] == ErrorCode.REFUSED, out.stdout
    board = appr.Board()
    assert board.take_answer(req.id) is None, "no answer was written"
    assert board.get(req.id).state == appr.WAITING, "the action stays held"


@pytest.mark.parametrize("key", ["", "0" * appr.KEY_HEX_CHARS, "not a key", "other"])
def test_a_wrong_key_is_refused_and_never_echoed(home, key):
    req = _held()
    if key == "other":  # another question's key: each question has its own
        key = _key_file(_held_other().id).read_text(encoding="ascii")
    with home.connect() as conn:
        with pytest.raises(client.ServiceError) as refused:
            conn.call(Method.MAILBOX_ANSWER, {"state_dir": str(_state()), "id": req.id,
                                              "choice": req.question.yes_label, "channel": "question-tool",
                                              "key": key})
    assert refused.value.code == ErrorCode.REFUSED
    real = _key_file(req.id).read_text(encoding="ascii")
    assert real not in str(refused.value) and (not key or key not in str(refused.value))
    assert appr.Board().take_answer(req.id) is None


def _held_other() -> appr.Request:
    """Another question the daemon holds in the same session, with a key of its own."""
    return appr.Board().hold(policy="shell.unsafe_command", session_id=SID, facts={"command": "make", "cwd": "/w"},
                             held={"kind": "shell", "command": "make", "cwd": "/w"}, bypass=False)


def test_a_question_any_caller_posts_gets_a_key_it_is_never_sent(home):
    """`mailbox.post` is open to the same callers: a question posted there gets a
    key written beside it, and nothing sends it back, so its poster cannot then
    answer it through the service either."""
    question = _request("feedfeed")
    with home.connect() as conn:
        posted = conn.call(Method.MAILBOX_POST, {"sid": SID, "state_dir": str(_state()),
                                                 "question": question.to_json()})
        assert posted == {"posted": "feedfeed", "kind": "question", "late": False}
        key = _key_file("feedfeed").read_text(encoding="ascii")
        assert appr.is_answer_key(key) and key not in json.dumps(posted)
        with pytest.raises(client.ServiceError) as refused:
            conn.call(Method.MAILBOX_ANSWER, {"state_dir": str(_state()), "id": "feedfeed",
                                              "choice": question.question.yes_label, "channel": "question-tool"})
    assert refused.value.code == ErrorCode.REFUSED
    assert stat.S_IMODE(_key_file("feedfeed").stat().st_mode) == 0o600
    assert stat.S_IMODE(_key_file("feedfeed").parent.stat().st_mode) == 0o700


# ---------------------------------------------------------------------------
# The person's answer path keeps working, old pieces included.
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("pick", ["yes", "no"])
def test_the_persons_pick_goes_through_the_service_with_its_key(home, pick):
    req = _held()
    q = req.question
    _ask(req, q.yes_label if pick == "yes" else q.no_label)
    answer = appr.Board().take_answer(req.id)
    assert answer["answer"] == (appr.YES if pick == "yes" else appr.NO)
    assert answer["channel"] == "question-tool"
    assert _written_by_the_service(req.id)


def test_the_service_names_where_an_answer_came_from(home):
    """The caller's `channel` is checked (an older service requires one) and
    never recorded: a caller holding the key still cannot say it answered in
    a terminal."""
    req = _held()
    key = _key_file(req.id).read_text(encoding="ascii")
    with home.connect() as conn:
        got = conn.call(Method.MAILBOX_ANSWER, {"state_dir": str(_state()), "id": req.id,
                                                "choice": req.question.no_label, "channel": "terminal",
                                                "key": key})
    assert got == {"answered": True, "sid": SID, "late": False}
    assert appr.Board().take_answer(req.id)["channel"] == ANSWER_CHANNEL == "question-tool"


def test_a_question_filed_before_keys_is_answered_by_the_hook_itself(home):
    """An older daemon's question has no key: the service refuses every answer
    to it, and the hook writes the answer file, as with no service at all."""
    req = _unkeyed()
    assert not _key_file(req.id).exists()
    _ask(req, req.question.yes_label)
    assert appr.Board().take_answer(req.id)["answer"] == appr.YES
    assert not _written_by_the_service(req.id)


def test_an_older_hook_is_refused_and_writes_the_answer_itself(home, tmp_path):
    """A session on a plugin from before keys sends no key: refused, it writes
    the answer file itself (it has the folder), so the person's pick lands."""
    folder = tmp_path / "plugin" / "hooks"
    shutil.copytree(HOOKS, folder)
    shutil.copy(OLD_HOOK, folder / "approvals_hook.py")
    req = _held()
    _ask(req, req.question.yes_label, hook=folder / "approvals_hook.py")
    assert appr.Board().take_answer(req.id)["answer"] == appr.YES
    assert not _written_by_the_service(req.id)


def test_the_hooks_call_still_passes_an_older_services_check():
    """A newer hook talking to an older service: `protocol.need_mailbox_answer`
    is unchanged by the key (an older service runs this same check), so the
    hook's call, `channel` included, is still accepted there."""
    source = (HOOKS / "approvals_hook.py").read_text(encoding="utf-8")
    assert '"channel": "question-tool"' in source
    params = {"state_dir": "/s/probe", "id": "a1b2c3d4", "choice": "Run it", "channel": "question-tool",
              "deadline": time.time() + 1, "budget": 0.8, "key": "0" * appr.KEY_HEX_CHARS}
    checked = protocol.need_mailbox_answer(params)
    assert (checked["id"], checked["choice"], checked["channel"]) == ("a1b2c3d4", "Run it", "question-tool")


# ---------------------------------------------------------------------------
# The key itself.
# ---------------------------------------------------------------------------


def test_each_request_has_one_private_key_kept_until_it_is_pruned(tmp_path):
    clock = [1_000_000.0]
    board = appr.Board(tmp_path / "board", clock=lambda: clock[0])  # not `approvals`: filed here, no service
    req = board.hold(policy="shell.unsafe_command", session_id=SID, facts={"command": "make", "cwd": "/w"},
                     held={"kind": "shell", "command": "make", "cwd": "/w"}, bypass=False)
    path = board.root / appr.KEYS_DIRNAME / req.id
    key = path.read_text(encoding="ascii")
    assert appr.is_answer_key(key)
    assert stat.S_IMODE(path.stat().st_mode) == 0o600
    board.mint_key(req.id)
    assert path.read_text(encoding="ascii") == key, "a key is written once"
    assert board.key_matches(req.id, key)
    for wrong in (None, "", key.upper(), key[:-1], key + "0", "0" * appr.KEY_HEX_CHARS, 7):
        assert not board.key_matches(req.id, wrong)
    assert not board.key_matches("../" + req.id, key) and not board.key_matches("nope", key)
    # Never in the request (an older reader takes no unknown field), and never in the question shown.
    assert key not in json.dumps(req.to_json()) and key not in (board.root / "requests" / f"{req.id}.json").read_text()
    board.resolve(req, state=appr.DENIED, outcome="no")
    clock[0] += appr.KEEP_RESOLVED_S + 1
    board.prune()
    assert not path.exists(), "pruned with its request"


def test_a_key_that_is_not_a_plain_file_matches_nothing(tmp_path):
    board = appr.Board(tmp_path / "board")
    (board.root / appr.KEYS_DIRNAME).mkdir()
    target = tmp_path / "planted"
    target.write_text("0" * appr.KEY_HEX_CHARS)
    os.symlink(target, board.root / appr.KEYS_DIRNAME / "q1")
    assert not board.key_matches("q1", "0" * appr.KEY_HEX_CHARS)
    os.mkfifo(board.root / appr.KEYS_DIRNAME / "q2")
    assert not board.key_matches("q2", "0" * appr.KEY_HEX_CHARS), "and a FIFO never blocks the service"


def test_the_service_step_refuses_before_it_writes(tmp_path):
    """`MailHost.answer` on the mailbox thread: no key, no answer file."""
    board = appr.Board(tmp_path / "probe" / "approvals")
    req = _request(command="make")
    board.create(req)
    request = protocol.need_mailbox_answer({"state_dir": str(tmp_path / "probe"), "id": req.id,
                                            "choice": req.question.yes_label, "channel": "question-tool"})
    request["state"], request["key"] = request["state_dir"], None
    assert "refused" in MailHost.answer(request)
    assert board.take_answer(req.id) is None
    request["key"] = (board.root / appr.KEYS_DIRNAME / req.id).read_text(encoding="ascii")
    assert MailHost.answer(request) == {"answered": True, "sid": SID, "late": False}
    assert board.take_answer(req.id)["channel"] == ANSWER_CHANNEL


def test_prune_never_follows_an_id_written_inside_a_request(tmp_path):
    """A request file's own `id` is its contents' word, not its name: pruning a
    settled one removes `answers/<name>` and `keys/<name>`, never a path the
    contents spell (`../`)."""
    clock = [1_000_000.0]
    board = appr.Board(tmp_path / "board", clock=lambda: clock[0])
    victim = tmp_path / "board" / "victim"
    victim.write_text("keep me")
    (tmp_path / "board" / "victim.json").write_text("keep me too")
    req = _request("a1b2c3d4")
    req.state, req.answered_at = appr.DENIED, clock[0]
    data = req.to_json()
    data["id"] = "../victim"
    (board.root / "requests" / "a1b2c3d4.json").write_text(json.dumps(data))
    board.mint_key("a1b2c3d4")
    clock[0] += appr.KEEP_RESOLVED_S + 1
    board.prune()
    assert victim.read_text() == "keep me" and (tmp_path / "board" / "victim.json").read_text() == "keep me too"
    assert not (board.root / "requests" / "a1b2c3d4.json").exists()
    assert not (board.root / appr.KEYS_DIRNAME / "a1b2c3d4").exists(), "its key went with it"
