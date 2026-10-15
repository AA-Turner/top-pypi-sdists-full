"""`.probe.config` level `hash` (data catalog C9, R26/R34): the SDK records a
file's IDENTITY (path, sha256 or fingerprint, size, rows) and nothing else; the
run is still opened; the daemon treats the path exactly as `off`; `read` and
`hash` never combine into something looser than either."""

from __future__ import annotations

import json
import os

import pytest

import probe
from probe.cli import write_gate
from probe.sdk import disabled, exclusions, fluent, inputs, outputs, probe_config as pc, snapshot
from probe.sdk.run import Run
from tests.conftest import make_client


@pytest.fixture(autouse=True)
def _fresh(tmp_path, monkeypatch):
    monkeypatch.setenv("HOME", str(tmp_path / "home"))
    monkeypatch.setenv("XDG_STATE_HOME", str(tmp_path / "state"))
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path / "config"))
    monkeypatch.setenv("PROBE_OUTBOX_DIR", str(tmp_path / "outbox"))
    for name in ("CLAUDE_CODE_SESSION_ID", "CODEX_THREAD_ID", "PI_SESSION_ID", "PROBE_MODE", "PROBE_RUN_ID",
                 "PROBE_CAPTURE_LOG"):
        monkeypatch.delenv(name, raising=False)
    pc._CACHE.clear()
    pc._CHECKED.clear()
    exclusions._view_at = -1.0e9
    yield
    pc._CACHE.clear()
    pc._CHECKED.clear()


@pytest.fixture
def tree(tmp_path):
    repo = tmp_path / "repo"
    for sub in ("data", "src", "secret", "notes"):
        (repo / sub).mkdir(parents=True)
    (repo / "data" / "rows.jsonl").write_text('{"a": 1}\n' * 20)
    (repo / "data" / "tiny.txt").write_text("label\n")
    (repo / "src" / "train.py").write_text("print('x')\n")
    (repo / "secret" / "k.txt").write_text("PRIVATE\n")
    (repo / "notes" / "n.md").write_text("n\n")
    (repo / pc.CONFIG_NAME).write_text("data/ @probe hash\nsecret/\nnotes/ @probe read\n")
    return repo


# -- the parser ----------------------------------------------------------------


def test_hash_is_a_level_word_in_both_spellings(tmp_path):
    assert pc.HASH == "hash" and pc.level_of("HASH") == "hash" and pc.HASH in pc.LEVELS
    (tmp_path / pc.CONFIG_NAME).write_text("@probe hash\n*.jsonl\n*.ckpt @probe off\n")
    assert pc.check(tmp_path / "a.jsonl", is_dir=False).level == pc.HASH
    assert pc.check(tmp_path / "m.ckpt", is_dir=False).level == pc.OFF


def test_an_unknown_level_still_counts_as_off_and_its_warning_names_hash(tmp_path, capsys):
    (tmp_path / pc.CONFIG_NAME).write_text("x.bin @probe hush\n")
    assert pc.check(tmp_path / "x.bin", is_dir=False).level == pc.OFF
    assert "(on, read, hash, off)" in capsys.readouterr().err


def test_a_hash_verdict_is_excluded_identity_only_and_not_hidden(tree):
    verdict = pc.check(tree / "data" / "rows.jsonl", is_dir=False)
    assert verdict.excluded and verdict.identity_only and not verdict.hidden
    assert verdict.daemon_hidden
    assert not pc.check(tree / "notes" / "n.md", is_dir=False).identity_only
    assert pc.check(tree / "secret" / "k.txt", is_dir=False).hidden


def test_a_hash_folder_stays_open_and_a_deeper_file_may_only_narrow_it(tree):
    (tree / "data" / pc.CONFIG_NAME).write_text("open.jsonl @probe on\nshut.jsonl\nlooked.jsonl @probe read\n")
    pc._CACHE.clear()
    assert pc.check(tree / "data" / "open.jsonl", is_dir=False).level == pc.HASH  # never loosened to `on`
    assert pc.check(tree / "data" / "looked.jsonl", is_dir=False).level == pc.HASH  # nor to `read`
    assert pc.check(tree / "data" / "shut.jsonl", is_dir=False).level == pc.OFF  # narrowed
    assert pc.check(tree / "data" / "deep" / "x.csv", is_dir=False).level == pc.HASH  # inherited


def test_a_read_folder_never_becomes_hash_from_a_deeper_file(tree):
    (tree / "notes" / pc.CONFIG_NAME).write_text("n.md @probe hash\n")
    pc._CACHE.clear()
    assert pc.check(tree / "notes" / "n.md", is_dir=False).level == pc.READ


def test_lines_of_the_same_file_may_loosen_inside_a_hash_folder(tmp_path):
    (tmp_path / pc.CONFIG_NAME).write_text("data/ @probe hash\ndata/public.jsonl @probe on\n")
    assert pc.check(tmp_path / "data" / "public.jsonl", is_dir=False).level == pc.ON


def test_read_and_hash_meet_as_off_and_stricter_is_never_looser():
    read = pc.Verdict(True, None, "/a", pc.READ)
    hashed = pc.Verdict(True, None, "/b", pc.HASH)
    off = pc.Verdict(True, None, "/c", pc.OFF)
    assert pc.stricter(read, hashed).level == pc.OFF and pc.stricter(hashed, read).level == pc.OFF
    assert pc.stricter(pc.NOT_EXCLUDED, hashed) is hashed
    assert pc.stricter(hashed, off) is off
    assert pc.stricter(hashed, hashed) is hashed


def test_a_symlink_into_a_hash_folder_is_hash_and_one_into_off_is_off(tree, tmp_path):
    link = tmp_path / "elsewhere"
    link.mkdir()
    os.symlink(tree / "data" / "rows.jsonl", link / "rows.jsonl")
    os.symlink(tree / "secret" / "k.txt", link / "k.txt")
    assert pc.check(link / "rows.jsonl", is_dir=False).level == pc.HASH
    assert pc.check(link / "k.txt", is_dir=False).level == pc.OFF


def test_the_daemon_reads_hash_as_off(tree):
    plain = pc.Checker()
    daemon = pc.Checker(daemon=True)
    path = tree / "data" / "rows.jsonl"
    assert plain.check(path).level == pc.HASH
    assert daemon.check(path).level == pc.OFF and daemon.check(path).hidden
    assert daemon.closed(tree / "data")
    assert pc.daemon_view(pc.check(tree / "notes" / "n.md", is_dir=False)).level == pc.READ
    # A tree holding a hash folder is a tree holding an `off` one, to the daemon.
    assert pc.off_inside(tree)
    assert not pc.off_inside(tree / "src")


def test_the_session_summary_names_hash_places_as_hash_only(tree):
    summary = pc.summarize(tree)
    hashed = [e for e in summary.entries if "data" in e]
    assert hashed and hashed[0].endswith(pc.HASH_ONLY_SUFFIX)
    assert not any(e.endswith(pc.HASH_ONLY_SUFFIX) for e in summary.entries if "secret" in e)


# -- the SDK: identity only, never bytes (C9a) -------------------------------------


def test_the_recorder_records_hash_paths_and_skips_read_and_off(tree):
    assert not inputs._config_excluded(str(tree / "data" / "rows.jsonl"))
    assert inputs._config_excluded(str(tree / "notes" / "n.md"))
    assert inputs._config_excluded(str(tree / "secret" / "k.txt"))


def test_a_hash_file_is_never_uploaded_captured_or_snapshotted(tree, capsys):
    assert Run.log_artifact(object(), "rows", path=str(tree / "data" / "rows.jsonl")) is None
    assert "was not uploaded" in capsys.readouterr().err
    found, _cut = outputs._walk(str(tree), set(), 1000)
    assert "src/train.py" in found and not any(p.startswith("data/") for p in found)
    ignored = snapshot._Ignored(None, str(tree))
    # A hash folder stays open (like `read`); every file in it is excluded.
    assert ignored.path("data/rows.jsonl") and ignored.config_excluded("data/rows.jsonl")


def test_a_read_and_hash_symlink_pair_is_not_recorded(tree, tmp_path):
    os.symlink(tree / "notes" / "n.md", tree / "data" / "n-link.md")
    pc._CACHE.clear()
    path = str(tree / "data" / "n-link.md")
    assert inputs._write_config_excluded(path, os.path.realpath(path))


# -- probe.init() (C9i, V9) ----------------------------------------------------------


@pytest.fixture
def wired(app, tmp_path, monkeypatch):
    built = []

    def factory(*_a, **_kw):
        client = make_client(app, tmp_spool=tmp_path / "spool")
        built.append(client)
        return client

    monkeypatch.setattr(fluent, "Client", factory)
    app.seed_experiment("e1")
    fluent._current.set(None)
    fluent._process_default = None
    yield built
    fluent._current.set(None)
    fluent._process_default = None


def test_init_in_a_hash_folder_opens_the_run_without_its_console_log(tree, wired, app, monkeypatch, capsys):
    monkeypatch.chdir(tree / "data")
    monkeypatch.setattr("sys.argv", [str(tree / "src" / "train.py")])
    assert exclusions.run_identity_only()
    assert not outputs.log_enabled()
    run = probe.init(experiment="e1", name="relabel", capture_outputs=False)
    try:
        assert not isinstance(run, disabled.DisabledRun)
        assert run.id in app.runs
        assert "is at `hash`" in capsys.readouterr().err
    finally:
        run.finish()


def test_init_in_an_off_folder_still_opens_none(tree, wired, monkeypatch):
    monkeypatch.chdir(tree / "secret")
    run = probe.init(experiment="e1", name="r")
    try:
        assert isinstance(run, disabled.DisabledRun)
    finally:
        run.finish()


def test_a_hash_folder_running_an_off_script_is_off(tree, monkeypatch):
    script = tree / "secret" / "go.py"
    script.write_text("x")
    monkeypatch.chdir(tree / "data")
    monkeypatch.setattr("sys.argv", [str(script)])
    hit = exclusions.run_excluded()
    assert hit is not None and hit[1].hidden


def test_a_hash_folder_running_a_read_script_is_off(tree, monkeypatch):
    script = tree / "notes" / "go.py"
    script.write_text("x")
    monkeypatch.chdir(tree / "data")
    monkeypatch.setattr("sys.argv", [str(script)])
    hit = exclusions.run_excluded()
    assert hit is not None and hit[1].level == pc.OFF


def test_the_log_stays_on_elsewhere(tree, monkeypatch):
    monkeypatch.chdir(tree / "src")
    monkeypatch.setattr("sys.argv", [str(tree / "src" / "train.py")])
    assert outputs.log_enabled()


# -- the CLI write gate --------------------------------------------------------------


def test_the_write_gate_lets_hash_through_where_only_identity_is_recorded(tree, monkeypatch):
    from probe.sdk import session_marker

    # `dataset` is a write group (the catalog CLI); said here so this test does
    # not hang on the order the classifier learns it in.
    monkeypatch.setattr(session_marker, "WRITE_GROUPS", session_marker.WRITE_GROUPS | {"dataset"})
    monkeypatch.chdir(tree)
    data = "data/rows.jsonl"
    assert write_gate.excluded_refusal(["exec", "--input", data, "--", "head", data]) is None
    assert write_gate.excluded_refusal(["dataset", "add", data, "--name", "rows"]) is None
    refused = write_gate.excluded_refusal(["dataset", "add", data, "--name", "rows", "--upload"])
    assert refused is not None and refused[1] is None
    assert write_gate.excluded_refusal(["artifact", "add", "r1", data]) is not None
    # `off` keeps its meaning for every command.
    assert write_gate.excluded_refusal(["exec", "--", "cat", "secret/k.txt"])[1] == ["cat", "secret/k.txt"]
    assert "dataset add" in write_gate.HASH_LEVEL_WRITES and "--upload" in write_gate.HASH_LEVEL_REFUSED_FLAGS


def test_a_hash_working_directory_refuses_no_write(tree, monkeypatch):
    monkeypatch.chdir(tree / "data")
    assert write_gate.excluded_refusal(["log", "r1", "loss=1"]) is None
    assert write_gate.excluded_refusal(["exec", "--", "true"]) is None
    monkeypatch.chdir(tree / "secret")
    assert write_gate.excluded_refusal(["log", "r1", "loss=1"]) is not None


# -- the daemon (C9b) ------------------------------------------------------------------


def test_the_daemon_drops_hash_events_as_it_drops_off(tmp_path, monkeypatch):
    pytest.importorskip("pydantic_ai")
    from probe.daemon import worker as worker_mod

    sid = "11111111-2222-3333-4444-555555555556"
    monkeypatch.setenv("PROBE_CONFIG_PATH", str(tmp_path / "no-config.json"))
    monkeypatch.delenv("PROBE_DAEMON_KEY", raising=False)
    monkeypatch.setenv("PROBE_DAEMON_MCP", "0")
    sessions = tmp_path / "state" / "probe" / "sessions"
    sessions.mkdir(parents=True)
    (sessions / f"{sid}.state").write_text("daemon")
    work = tmp_path / "home" / "work"
    (work / "data").mkdir(parents=True)
    (work / "src").mkdir()
    (work / "data" / "rows.jsonl").write_text('{"text": "PRIVATE-ROW"}\n')
    (work / ".probe.config").write_text("data/ @probe hash\n")

    def line(obj):
        return json.dumps(obj) + "\n"

    def use(call_id, name, tool_input):
        return {"type": "assistant", "cwd": str(work),
                "message": {"content": [{"type": "tool_use", "id": call_id, "name": name, "input": tool_input}]}}

    def result(call_id, text):
        return {"type": "user", "cwd": str(work),
                "message": {"content": [{"type": "tool_result", "tool_use_id": call_id, "content": text}]}}

    transcript = tmp_path / f"{sid}.jsonl"
    transcript.write_text(
        line({"type": "user", "message": {"content": "relabel the rows"}, "cwd": str(work)})
        + line(use("t1", "Read", {"file_path": str(work / "data" / "rows.jsonl")}))
        + line(result("t1", "PRIVATE-ROW-ONE"))
        + line(use("t2", "Bash", {"command": "head -n 1 data/rows.jsonl"}))
        + line(result("t2", "PRIVATE-ROW-TWO"))
        + line(use("t3", "Bash", {"command": "ls src"}))
        + line(result("t3", "a.py"))
    )
    w = worker_mod.Worker(worker_mod.Session(sid, transcript, work, "claude_code", home=tmp_path / "home"))
    assert w.read_new() > 0
    rows = w.store.db.execute("SELECT kind, text, tool_input FROM events ORDER BY seq").fetchall()
    stored = json.dumps([tuple(r) for r in rows])
    for leaked in ("PRIVATE-ROW-ONE", "PRIVATE-ROW-TWO", "head -n 1 data/rows.jsonl"):
        assert leaked not in stored
    assert "ls src" in stored and "relabel the rows" in stored
