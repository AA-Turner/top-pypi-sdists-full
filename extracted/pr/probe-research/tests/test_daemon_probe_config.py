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
    # `grep -rn` reads the whole tree, which holds an excluded folder: dropped whole,
    # since an output cannot be trusted to name every file it read (`grep -h`).
    assert "grep -rn token" not in stored and "token = None" not in stored
    assert "ls src" in stored and "tidy the repo" in stored


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


# ---------------------------------------------------------------------------
# Levels: `read` paths enter the store tagged; globs are expanded
# ---------------------------------------------------------------------------


@pytest.fixture
def levels(tmp_path):
    work = tmp_path / "home" / "work"
    for rel in ("notebooks/a.ipynb", "notebooks/b.ipynb", "secret/keys.txt", "src/a.py"):
        (work / rel).parent.mkdir(parents=True, exist_ok=True)
        (work / rel).write_text("CONTENT-" + rel)
    (work / ".probe.config").write_text("notebooks/ @probe read\nsecret/*\n")
    return work


def _notes(w) -> list[tuple[str, str | None]]:
    return [(r[0], r[1]) for r in w.store.db.execute("SELECT kind, note FROM events ORDER BY seq").fetchall()]


def test_a_read_path_is_kept_and_tagged_with_its_output(tmp_path, levels):
    transcript = tmp_path / f"{SID}.jsonl"
    transcript.write_text(
        _line(_use("t1", "Read", {"file_path": str(levels / "notebooks" / "a.ipynb")}, levels))
        + _line(_use("t2", "Bash", {"command": "ls src"}, levels))
        + _line(_result("t2", "a.py", levels))
        + _line(_result("t1", "CELL-OUTPUT", levels))  # the output comes later
    )
    w = _worker(tmp_path, transcript, levels)
    w.read_new()
    stored = _stored(w)
    assert "CELL-OUTPUT" in stored  # read: the daemon may look
    notes = _notes(w)
    tagged = [n for _, n in notes if n]
    assert len(tagged) == 2 and all("to read: Probe may look, records nothing about it" in n for n in tagged)
    assert "notebooks/a.ipynb" in tagged[0]
    rows = w.store.db.execute("SELECT * FROM events WHERE note IS NOT NULL ORDER BY seq").fetchall()
    from probe.daemon import bite as bite_mod
    from probe.daemon.store import StoredEvent

    shown = bite_mod.render(StoredEvent.from_row(rows[0]))
    assert shown.endswith(f"({tagged[0]})")


def test_a_glob_into_off_files_is_dropped(tmp_path, levels):
    transcript = tmp_path / f"{SID}.jsonl"
    transcript.write_text(
        _line(_use("t1", "Bash", {"command": "cat secret/*"}, levels))
        + _line(_result("t1", "CONTENT-secret/keys.txt", levels))
        + _line(_use("t2", "Bash", {"command": "head notebooks/*.ipynb"}, levels))
        + _line(_result("t2", "CONTENT-notebooks", levels))
    )
    w = _worker(tmp_path, transcript, levels)
    w.read_new()
    stored = _stored(w)
    assert "secret" not in stored
    assert "head notebooks/*.ipynb" in stored and "CONTENT-notebooks" in stored
    assert any(n and "notebooks/*.ipynb" in n for _, n in _notes(w))


def test_an_output_listing_read_files_is_tagged_and_off_lines_go(tmp_path, levels):
    transcript = tmp_path / f"{SID}.jsonl"
    transcript.write_text(
        _line(_use("t1", "Bash", {"command": "python report.py"}, levels))
        + _line(_result(
            "t1",
            "./notebooks/a.ipynb:1:CONTENT-a\n./secret/keys.txt:1:CONTENT-key\n./src/a.py:1:CONTENT-src",
            levels,
        ))
        + _line(_use("t2", "Bash", {"command": "grep -rn CONTENT ."}, levels))
        + _line(_result("t2", "./src/a.py:1:CONTENT-tree", levels))
    )
    w = _worker(tmp_path, transcript, levels)
    w.read_new()
    stored = _stored(w)
    assert "CONTENT-key" not in stored and "CONTENT-a" in stored and "CONTENT-src" in stored
    assert "CONTENT-tree" not in stored  # a tree read over a folder holding an off path: dropped
    out_notes = [n for k, n in _notes(w) if k == "tool_output"]
    assert out_notes and "./notebooks/a.ipynb" in out_notes[0]


def test_a_session_in_a_read_folder_is_kept_and_tagged(tmp_path, levels):
    transcript = tmp_path / f"{SID}.jsonl"
    nb = levels / "notebooks"
    transcript.write_text(_line(_use("t1", "Bash", {"command": "ls"}, nb)) + _line(_result("t1", "a.ipynb", nb)))
    w = _worker(tmp_path, transcript, nb)
    w.read_new()
    notes = [n for _, n in _notes(w)]
    assert len(notes) == 2 and all(n and "to read: Probe may look" in n for n in notes)
    assert "the folder it ran in" in notes[0]


def test_folder_check_skips_read_files_too(tmp_path, levels):
    f = exclusions_mod.Filter(None, SID, levels)
    seen = folders.scan([levels], {}, is_secret=lambda p: False, text_room=10_000, excluded=f.path_excluded)
    names = {Path(s.path).name for s in seen}
    assert "a.py" in names and "a.ipynb" not in names and "keys.txt" not in names


def test_an_old_store_gains_the_note_column(tmp_path):
    import sqlite3

    from probe.daemon.store import Store

    path = tmp_path / "old.sqlite"
    db = sqlite3.connect(str(path))
    db.executescript(
        "CREATE TABLE events (seq INTEGER PRIMARY KEY AUTOINCREMENT, event_id TEXT UNIQUE NOT NULL, "
        "stream TEXT NOT NULL, offset INTEGER NOT NULL, idx INTEGER NOT NULL, kind TEXT NOT NULL, "
        "turn INTEGER NOT NULL, ts TEXT, noticed REAL NOT NULL, text TEXT NOT NULL DEFAULT '', tool TEXT, "
        "call_id TEXT, command TEXT, tool_input TEXT, is_error INTEGER NOT NULL DEFAULT 0, side_file TEXT, "
        "parent TEXT, cwd TEXT, chars INTEGER NOT NULL DEFAULT 0, bite INTEGER);"
    )
    db.close()
    store = Store(path)
    store.add([Event(Kind.TOOL_CALL, "main", 1, tool="Bash", tool_input={"command": "ls"}, note="tag")])
    assert store.db.execute("SELECT note FROM events").fetchone()[0] == "tag"


# ---------------------------------------------------------------------------
# The daemon records nothing about a `read` or `off` path
# ---------------------------------------------------------------------------


def _config_check(argv, levels, document=None):
    from probe.daemon import precheck

    checker = pc.Checker(cwd=str(levels), legacy=True)
    return precheck.check_config(precheck.parse(argv), cwd=levels, checker=checker, document=document)


def test_a_write_naming_a_read_path_is_refused_with_no_override(levels):
    block = _config_check(["artifact", "add", "r1", "notebooks/a.ipynb"], levels)
    assert block is not None and not block.overridable and block.check == "probe_config"
    message = block.message()
    assert "`" + str(levels / "notebooks" / "a.ipynb") + "` is set to read by" in message
    assert "Probe records nothing about it. Do not retry" in message and "This check has no override" in message


def test_text_naming_a_path_is_refused_and_plain_text_is_not(levels):
    assert _config_check(["run", "set", "r1", "--description", "trained on secret/keys.txt"], levels) is not None
    assert _config_check(["run", "set", "r1", "--description", "see notebooks/a.ipynb."], levels) is not None
    assert _config_check(["run", "set", "r1", "--description", "trained on src/a.py and/or more"], levels) is None


def test_a_note_document_naming_a_path_is_refused(levels, tmp_path):
    note = tmp_path / "note.md"
    note.write_text("# Results\nThe cells in notebooks/b.ipynb show it.\n")
    assert _config_check(["notes", "push", "--project", "p"], levels, document=note) is not None
    note.write_text("# Results\nsrc/a.py does it.\n")
    assert _config_check(["notes", "push", "--project", "p"], levels, document=note) is None


def test_a_manifest_row_naming_a_read_path_is_refused(levels, tmp_path):
    manifest = tmp_path / "rows.jsonl"
    manifest.write_text(json.dumps({"path": str(levels / "notebooks" / "a.ipynb")}) + "\n")
    assert _config_check(["artifact", "add", "--from-manifest", str(manifest), "--run", "r1"], levels) is not None


# ---------------------------------------------------------------------------
# The daemon's own shell never reads an `off` path
# ---------------------------------------------------------------------------


def _shell_classify(command, levels):
    from probe.daemon import shell as sh

    checker = pc.Checker(cwd=str(levels), legacy=True)
    return sh.classify(command, workdirs=[levels], home=levels.parent, cwd=levels,
                       hidden=lambda p: checker.check(p).hidden)


def test_the_daemon_shell_never_reads_an_off_path(levels):
    verdict = _shell_classify("cat secret/keys.txt", levels)
    assert not verdict.safe and verdict.refused and "sets it to off" in verdict.reason
    assert _shell_classify("cat notebooks/a.ipynb", levels).safe  # read: the daemon may look
    assert _shell_classify("cat src/a.py", levels).safe


def test_the_daemon_file_reader_never_reads_an_off_path(levels):
    from probe.daemon import shell as sh

    checker = pc.Checker(cwd=str(levels), legacy=True)
    refused = sh.read_refusal("secret/keys.txt", workdirs=[levels], home=levels.parent, cwd=levels,
                              hidden=lambda p: checker.check(p).hidden)
    assert refused is not None and refused[1] is True


def test_a_listing_from_the_daemon_shell_loses_off_lines(levels):
    checker = pc.Checker(cwd=str(levels), legacy=True)
    text, read = exclusions_mod.scrub_listing(
        "./notebooks/a.ipynb\n./secret/keys.txt\n./src/a.py", checker
    )
    assert "secret" not in text.split("[")[0] and "./src/a.py" in text and read == ["`./notebooks/a.ipynb`"]


def test_off_files_leave_git_diffs_json_and_nul_listings(levels):
    checker = pc.Checker(cwd=str(levels), legacy=True)
    diff = (
        "diff --git a/src/a.py b/src/a.py\n+ok = 1\n"
        "diff --git a/secret/keys.txt b/secret/keys.txt\n+PRIVATE-DIFF\n"
        "diff --git a/notebooks/a.ipynb b/notebooks/a.ipynb\n+cell"
    )
    text, read = exclusions_mod.scrub_listing(diff, checker)
    assert "PRIVATE-DIFF" not in text and "ok = 1" in text and "+cell" in text
    assert read == ["`notebooks/a.ipynb`"] or any("notebooks/a.ipynb" in r for r in read)
    rg = '{"type":"match","data":{"path":{"text":"./secret/keys.txt"},"lines":{"text":"PRIVATE-JSON"}}}\n' \
         '{"type":"match","data":{"path":{"text":"./src/a.py"},"lines":{"text":"ok"}}}'
    text, _ = exclusions_mod.scrub_listing(rg, checker)
    assert "PRIVATE-JSON" not in text and '"ok"' in text
    text, _ = exclusions_mod.scrub_listing("./src/a.py\0./secret/keys.txt\0", checker)
    assert "secret" not in text.split("[")[0] and "./src/a.py" in text


def test_the_daemon_shell_never_shows_an_off_file_from_git_history(levels):
    verdict = _shell_classify("git show --no-textconv --no-ext-diff HEAD:secret/keys.txt", levels)
    assert verdict.refused and "sets it to off" in verdict.reason


def test_a_glob_expansion_is_bounded(levels, monkeypatch):
    monkeypatch.setattr(exclusions_mod, "GLOB_BUDGET_S", 0.0)
    found, finished = exclusions_mod._bounded_glob(str(levels / "**" / "*.txt"), 0.0, 10)
    assert (found, finished) == ([], False)  # past the deadline at once: unknown, never "none"
    found, finished = exclusions_mod._bounded_glob(str(levels / "**" / "*.txt"), 1e18, 10)
    assert finished and str(levels / "secret" / "keys.txt") in found
    found, finished = exclusions_mod._bounded_glob(str(levels / "**" / "*"), 1e18, 1)
    assert not finished  # cut at the cap: unknown


# ---------------------------------------------------------------------------
# Review round: output shapes, tree reads, fail closed
# ---------------------------------------------------------------------------


def test_the_scrub_handles_headings_prefixes_colours_heads_and_nul_lines(levels):
    checker = pc.Checker(cwd=str(levels), legacy=True)
    cases = {
        "heading": "secret/keys.txt\n1:LEAK-HEADING\n\nsrc/a.py\n2:ok",
        "no-prefix": "diff --git secret/keys.txt secret/keys.txt\n+LEAK-NOPREFIX\ndiff --git src/a.py src/a.py\n+ok",
        "mnemonic": "diff --git i/secret/keys.txt w/secret/keys.txt\n+LEAK-MNEMONIC",
        "colour": "\x1b[1mdiff --git a/secret/keys.txt b/secret/keys.txt\x1b[m\n+LEAK-COLOUR",
        "unified": "--- secret/keys.txt\n+++ secret/keys.txt\n@@ -1 +1 @@\n+LEAK-UNIFIED",
        "head": "==> secret/keys.txt <==\nLEAK-HEAD\n\n==> src/a.py <==\nok",
        "nul": "secret/keys.txt\x001:LEAK-NUL\nsrc/a.py\x002:ok",
        "spaced": "secret/my keys.txt:1:LEAK-SPACED",
    }
    for name, text in cases.items():
        out, _ = exclusions_mod.scrub_listing(text, checker)
        assert "LEAK" not in out, (name, out)
    out, _ = exclusions_mod.scrub_listing(cases["heading"], checker)
    assert "2:ok" in out


def test_a_bare_file_name_and_a_cd_are_followed(tmp_path, levels):
    (levels / "secret" / "plain.txt").write_text("LEAK-BARE")
    transcript = tmp_path / f"{SID}.jsonl"
    transcript.write_text(
        _line(_use("t1", "Bash", {"command": "cd secret && cat plain.txt"}, levels))
        + _line(_result("t1", "LEAK-BARE", levels))
        + _line(_use("t2", "Bash", {"command": "python train.py --out model.ckpt"}, levels))
        + _line(_result("t2", "loss 0.1", levels))
    )
    w = _worker(tmp_path, transcript, levels)
    w.read_new()
    stored = _stored(w)
    assert "LEAK-BARE" not in stored and "loss 0.1" in stored


def test_a_truncated_glob_drops_the_call(tmp_path, levels, monkeypatch):
    monkeypatch.setattr(exclusions_mod, "MAX_GLOB_MATCHES", 1)
    for k in range(3):
        (levels / "src" / f"f{k}.txt").write_text("x")
    transcript = tmp_path / f"{SID}.jsonl"
    transcript.write_text(_line(_use("t1", "Bash", {"command": "head */*.txt"}, levels))
                          + _line(_result("t1", "PARTIAL", levels))
                          + _line(_use("t2", "Bash", {"command": "head src/*.txt"}, levels))
                          + _line(_result("t2", "CLEAN-PARTIAL", levels)))
    w = _worker(tmp_path, transcript, levels)
    w.read_new()
    stored = _stored(w)
    assert "PARTIAL" not in stored.replace("CLEAN-PARTIAL", "")  # cut short over a tree holding an off path
    assert "CLEAN-PARTIAL" in stored  # cut short where nothing is off: unknown files can't be off


def test_a_broken_filter_drops_the_tool_events(tmp_path, levels, monkeypatch):
    f = exclusions_mod.Filter(type("S", (), {"fact": lambda s, k, d=None: d, "set_fact": lambda s, k, v: None})(),
                              SID, levels)
    monkeypatch.setattr(f, "_keep", lambda *a, **k: 1 / 0)
    events = [Event(Kind.PROMPT, "main", 1, text="hi"),
              Event(Kind.TOOL_CALL, "main", 2, tool="Bash", call_id="x", tool_input={"command": "ls"}),
              Event(Kind.TOOL_OUTPUT, "main", 3, call_id="x", text="out")]
    assert [e.kind for e in f.keep(events, stream="main")] == [Kind.PROMPT]


def test_the_daemon_shell_refuses_a_tree_read_holding_an_off_path(levels):
    from probe.daemon import shell as sh

    checker = pc.Checker(cwd=str(levels), legacy=True)
    kw = dict(workdirs=[levels], home=levels.parent, cwd=levels, hidden=lambda p: checker.check(p).hidden,
              off_inside=lambda folder: pc.off_inside(folder, legacy=True))
    for command in ("rg -I PRIVATE .", "rg --heading -n PRIVATE", "find . -name x", "ls -R"):
        verdict = sh.classify(command, **kw)
        assert verdict.refused and "sets to off or is too big to check" in verdict.reason, command
    assert sh.classify("rg -n ok src", **kw).safe
    nested = levels / "repo"
    (nested / "sub").mkdir(parents=True)
    (nested / ".git").mkdir()
    (nested / "secret.txt").write_text("x")
    (nested / ".probe.config").write_text("/secret.txt\n")
    kw["cwd"] = nested / "sub"
    kw["workdirs"] = [levels]
    verdict = sh.classify("git show --no-textconv --no-ext-diff HEAD:secret.txt", **kw)
    assert verdict.refused  # REV:path is the repository root's, not the folder's


def test_write_text_checks_unwrap_markdown_and_have_no_cap(levels, tmp_path):
    assert _config_check(["run", "set", "r1", "--description", "see **secret/keys.txt**"], levels) is not None
    assert _config_check(["run", "set", "r1", "--description", "[notebooks/a.ipynb](x)"], levels) is not None
    many = " ".join(f"src/f{k}" for k in range(600)) + " secret/keys.txt"
    assert _config_check(["run", "set", "r1", "--description", many], levels) is not None
    body = tmp_path / "body.md"
    body.write_text("trained on notebooks/b.ipynb\n")
    assert _config_check(["run", "set", "r1", "--description", f"@{body}"], levels) is not None


# ---------------------------------------------------------------------------
# Second review round
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("command", [
    "rg -I -e '^'", "rg --regexp CONTENT", "rg -m 1 CONTENT", 'cat "|" secret/keys.txt',
    "(cd src); cat ../secret/keys.txt", "xargs cat <<< secret/keys.txt", "env -i cat secret/keys.txt",
    "/usr/bin/env cat secret/keys.txt", "timeout 3 cat secret/keys.txt", "cd secret && cat *.txt",
    "echo `cat secret/keys.txt`",
])
def test_intake_drops_reads_of_off_files_in_any_shape(tmp_path, levels, command):
    transcript = tmp_path / f"{SID}.jsonl"
    transcript.write_text(_line(_use("t1", "Bash", {"command": command}, levels))
                          + _line(_result("t1", "LEAKED", levels)))
    w = _worker(tmp_path, transcript, levels)
    w.read_new()
    assert "LEAKED" not in _stored(w), command


def test_intake_keeps_runs_writing_off_files_and_clean_trees(tmp_path, levels):
    runs = tmp_path / "home" / "runs"
    runs.mkdir(parents=True)
    (runs / ".probe.config").write_text("*.ckpt\n")
    (runs / "model.ckpt").write_text("x")
    clean = tmp_path / "home" / "clean"
    (clean / "src").mkdir(parents=True)
    (clean / "src" / "a.py").write_text("x")
    transcript = tmp_path / f"{SID}.jsonl"
    transcript.write_text(
        _line(_use("t1", "Bash", {"command": "python train.py --out model.ckpt > log.txt"}, runs))
        + _line(_result("t1", "KEPT-RUN", runs))
        + _line(_use("t2", "Bash", {"command": "rg -I -e x"}, clean))
        + _line(_result("t2", "KEPT-CLEAN", clean))
    )
    w = _worker(tmp_path, transcript, levels)
    w.read_new()
    stored = _stored(w)
    assert "KEPT-RUN" in stored and "KEPT-CLEAN" in stored


def test_bare_name_headings_are_scrubbed(levels):
    (levels / "secret.txt").write_text("x")
    (levels / ".probe.config").write_text("notebooks/ @probe read\nsecret/*\nsecret.txt\n")
    pc._CACHE.clear()
    checker = pc.Checker(cwd=str(levels), legacy=True)
    for text in ("==> secret.txt <==\nOFF-CONTENT", "secret.txt\n1:OFF-CONTENT"):
        out, _ = exclusions_mod.scrub_listing(text, checker)
        assert "OFF-CONTENT" not in out, text


def test_markdown_unwrap_keeps_relative_spellings(levels):
    for text in ("see ./secret/keys.txt", "see ../work/secret/keys.txt", "see **./secret/keys.txt**"):
        assert _config_check(["run", "set", "r1", "--description", text], levels) is not None, text


def test_off_inside_follows_a_symlinked_folder_and_hidden_ones(tmp_path):
    data = tmp_path / "data"
    data.mkdir()
    (data / "secret.txt").write_text("x")
    (data / ".probe.config").write_text("secret.txt\n")
    (tmp_path / "link").symlink_to(data)
    assert pc.off_inside(tmp_path / "link")
    repo = tmp_path / "repo"
    (repo / "wandb").mkdir(parents=True)
    (repo / "wandb" / "data.txt").write_text("x")
    (repo / ".probe.config").write_text("wandb/ @probe off\n")
    assert pc.off_inside(repo)


def test_a_printed_off_path_hides_only_its_own_line(levels):
    # Found live (0.231.0): `cat .probe.config` printed `secret/`, and the
    # heading rule hid the rest of the output, the `read` plan and code included.
    checker = pc.Checker(cwd=str(levels), legacy=True)
    text = "secret/keys.txt\nnotebooks/ @probe read\n---\nREAD-PLAN tune lr\n---\nacc = 0.91"
    out, _ = exclusions_mod.scrub_listing(text, checker)
    assert "READ-PLAN tune lr" in out and "acc = 0.91" in out
    assert "secret/keys.txt" not in out
    heading, _ = exclusions_mod.scrub_listing("secret/keys.txt\n1:LEAK\n2:LEAK\n\nsrc/a.py\n3:ok", checker)
    assert "LEAK" not in heading and "3:ok" in heading


@pytest.mark.parametrize("program", ["md5sum", "sha224sum", "sha384sum", "b2sum", "cksum", "shasum -a 256"])
def test_every_digest_program_reads_the_file_it_names(levels, program):
    # The daemon's shell runs these at once (F3); the file they hash is a file read, for the
    # `read` note and the off check alike. md5sum was listed already: the control.
    files, trees = exclusions_mod.command_reads(f"{program} a.py", str(levels / "src"))
    assert files == [str(levels / "src" / "a.py")] and trees == [], program
