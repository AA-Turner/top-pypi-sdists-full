"""`.probe.config` in the Probe daemon (v2): what it excludes never enters the
session store, so no bite, reader or tool can see it."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

pytest.importorskip("pydantic_ai")

from probe.daemon import exclusions as exclusions_mod  # noqa: E402
from probe.daemon import folders  # noqa: E402
from probe.daemon import worker as worker_mod  # noqa: E402
from probe.daemon.events import Event, Kind  # noqa: E402
from probe.sdk import probe_config as pc  # noqa: E402

SID = "11111111-2222-3333-4444-555555555555"


@pytest.fixture(autouse=True)
def _isolated(tmp_path, monkeypatch):
    monkeypatch.setenv("PROBE_CONFIG_PATH", str(tmp_path / "no-config.json"))
    monkeypatch.delenv("PROBE_DAEMON_KEY", raising=False)
    monkeypatch.setenv("PROBE_DAEMON_MCP", "0")
    state = tmp_path / "state"
    monkeypatch.setenv("XDG_STATE_HOME", str(state))
    (state / "probe" / "sessions").mkdir(parents=True)
    (state / "probe" / "sessions" / f"{SID}.state").write_text("daemon")
    pc._CACHE.clear()
    pc._CHECKED.clear()


def _line(obj: dict) -> str:
    return json.dumps(obj) + "\n"


def _use(call_id, name, tool_input, cwd):
    return {"type": "assistant", "cwd": str(cwd),
            "message": {"content": [{"type": "tool_use", "id": call_id, "name": name, "input": tool_input}]}}


def _result(call_id, text, cwd):
    return {"type": "user", "cwd": str(cwd),
            "message": {"content": [{"type": "tool_result", "tool_use_id": call_id, "content": text}]}}


def _worker(tmp_path, transcript, work):
    return worker_mod.Worker(worker_mod.Session(SID, transcript, work, "claude_code", home=tmp_path / "home"))


def _stored(w) -> str:
    rows = w.store.db.execute("SELECT kind, text, tool_input FROM events ORDER BY seq").fetchall()
    return json.dumps([tuple(r) for r in rows])


@pytest.fixture
def repo(tmp_path):
    work = tmp_path / "home" / "work"
    (work / "secret").mkdir(parents=True)
    (work / "src").mkdir()
    (work / "secret" / "keys.txt").write_text("PRIVATE")
    (work / ".probe.config").write_text("secret/\n")
    return work


def test_excluded_calls_outputs_and_listed_lines_never_enter_the_store(tmp_path, repo):
    transcript = tmp_path / f"{SID}.jsonl"
    transcript.write_text(
        _line({"type": "user", "message": {"content": "tidy the repo"}, "cwd": str(repo)})
        + _line(_use("t1", "Read", {"file_path": str(repo / "secret" / "keys.txt")}, repo))
        + _line(_result("t1", "SECRET-ONE", repo))
        + _line(_use("t2", "Bash", {"command": "cat secret/notes.md"}, repo))
        + _line(_result("t2", "SECRET-TWO", repo))
        + _line(_use("t3", "Bash", {"command": "grep -rn token ."}, repo))
        + _line(_result("t3", "./secret/keys.txt:1:token=SECRET-THREE\n./src/a.py:2:token = None", repo))
        + _line(_use("t4", "Bash", {"command": "ls src"}, repo))
        + _line(_result("t4", "a.py", repo))
    )
    w = _worker(tmp_path, transcript, repo)
    assert w.read_new() > 0
    stored = _stored(w)
    for leaked in ("SECRET-ONE", "SECRET-TWO", "SECRET-THREE", "cat secret/notes.md"):
        assert leaked not in stored
    assert "ls src" in stored and "src/a.py:2:token = None" in stored and "tidy the repo" in stored
    assert "1 line(s) about paths a .probe.config excludes were removed" in stored


def test_an_output_read_later_or_after_a_restart_is_dropped(tmp_path, repo):
    transcript = tmp_path / f"{SID}.jsonl"
    transcript.write_text(_line(_use("t9", "Read", {"file_path": str(repo / "secret" / "k")}, repo)))
    w = _worker(tmp_path, transcript, repo)
    w.read_new()
    w.store.close()
    with transcript.open("a") as handle:
        handle.write(_line(_result("t9", "LATE-SECRET", repo)))
    w2 = _worker(tmp_path, transcript, repo)  # a restart: same store
    w2.read_new()
    assert "LATE-SECRET" not in _stored(w2)


def test_a_session_in_an_excluded_folder_stores_nothing(tmp_path):
    private = tmp_path / "home" / "private"
    private.mkdir(parents=True)
    (private / ".probe.config").write_text("*\n")
    transcript = tmp_path / f"{SID}.jsonl"
    transcript.write_text(
        _line({"type": "user", "message": {"content": "hello"}, "cwd": str(private)})
        + _line(_use("t1", "Bash", {"command": "ls"}, private))
        + _line(_result("t1", "x", private))
    )
    w = _worker(tmp_path, transcript, private)
    w.read_new()
    assert w.store.db.execute("SELECT count(*) FROM events").fetchone()[0] == 0


def test_kept_event_ids_do_not_move(tmp_path, repo):
    line = {"type": "assistant", "cwd": str(repo), "message": {"content": [
        {"type": "tool_use", "id": "a", "name": "Read", "input": {"file_path": str(repo / "secret" / "x")}},
        {"type": "tool_use", "id": "b", "name": "Bash", "input": {"command": "ls"}}]}}
    transcript = tmp_path / f"{SID}.jsonl"
    transcript.write_text(_line(line))
    w = _worker(tmp_path, transcript, repo)
    w.read_new()
    ids = [r[0] for r in w.store.db.execute("SELECT event_id FROM events").fetchall()]
    assert len(ids) == 1 and ids[0].endswith(":1")  # the kept call keeps index 1


def test_parent_file_set_aside_only_on_the_answer(tmp_path):
    code = tmp_path / "home" / "code"
    launch = code / "repo-a"
    launch.mkdir(parents=True)
    (code / ".probe.config").write_text("/*\n")
    from probe.sdk import session_marker

    pc.record_launch_dir(session_marker.sessions_dir(), SID, str(launch))
    transcript = tmp_path / f"{SID}.jsonl"
    transcript.write_text(_line({"type": "user", "message": {"content": "train it"}, "cwd": str(launch)}))
    w = _worker(tmp_path, transcript, launch)
    w.read_new()
    assert "train it" not in _stored(w)  # unanswered: followed

    pc.record_answer(session_marker.sessions_dir(), SID, pc.IGNORE)
    w.store.close()
    (tmp_path / f"{SID}.jsonl").write_text(_line({"type": "user", "message": {"content": "train it"}, "cwd": str(launch)}))
    w2 = _worker(tmp_path, transcript, launch)
    w2.store.set_cursor("main", str(transcript), 0)
    w2.read_new()
    assert "train it" in _stored(w2)


def test_codex_workdir_counts(tmp_path, repo):
    class _Store:
        def __init__(self):
            self.facts = {}

        def fact(self, key, default=None):
            return self.facts.get(key, default)

        def set_fact(self, key, value):
            self.facts[key] = value

    f = exclusions_mod.Filter(_Store(), SID, repo)
    call = Event(Kind.TOOL_CALL, "main", 10, tool="shell", call_id="c1",
                 tool_input={"command": ["bash", "-lc", "cat keys.txt"], "workdir": str(repo / "secret")})
    out = Event(Kind.TOOL_OUTPUT, "main", 20, call_id="c1", text="PRIVATE")
    ok = Event(Kind.TOOL_CALL, "main", 30, tool="shell", call_id="c2",
               tool_input={"command": ["bash", "-lc", "ls"], "workdir": str(repo / "src")})
    assert f.keep([call, out, ok], stream="main") == [ok]


def test_folder_check_skips_excluded_files(tmp_path, repo):
    (repo / "src" / "a.py").write_text("x = 1")
    f = exclusions_mod.Filter(None, SID, repo)
    seen = folders.scan([repo], {}, is_secret=lambda p: False, text_room=10_000, excluded=f.path_excluded)
    names = {Path(s.path).name for s in seen}
    assert "a.py" in names and "keys.txt" not in names


def test_no_config_changes_nothing(tmp_path):
    plain = tmp_path / "home" / "plain"
    plain.mkdir(parents=True)
    events = [Event(Kind.PROMPT, "main", 1, text="hi", cwd=str(plain)),
              Event(Kind.TOOL_CALL, "main", 2, tool="Bash", call_id="x", tool_input={"command": "cat a/b"}),
              Event(Kind.TOOL_OUTPUT, "main", 3, call_id="x", text="a/b:1:ok")]
    f = exclusions_mod.Filter(type("S", (), {"fact": lambda s, k, d=None: d, "set_fact": lambda s, k, v: None})(), SID, plain)
    before = [(e.kind, e.text) for e in events]
    assert [(e.kind, e.text) for e in f.keep(events, stream="main")] == before
