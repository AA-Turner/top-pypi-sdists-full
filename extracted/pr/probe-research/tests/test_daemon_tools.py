"""Daemon v2 tuning (plan 2026-09-26): the daemon's tools.

Each test failed on the code before its change (the plan's task in brackets):

    [T1]  a command's Idempotency-Key covers the files it sends: a second push of
          one note with new text is a new key, the same text keeps its key
    [T11] printing a file in slices is a question in normal mode; bypass runs it
    [T7]  several commands per shell call: each probe part goes through the probe
          tool's checks, in order, in the folder the `cd` parts set, with bash's
          `&&` / `||` / `;`; `probe <read> | <filter>` feeds the filter
    [T8]  a file reader: line ranges, CSV/TSV/JSON/Parquet/NumPy previews; never a
          pickle or an image; the shell's safe-read rules; scrubbed and capped
"""

from __future__ import annotations

import asyncio
import json
import pickle
import re
import struct
import time
import zipfile

import pytest

from probe.daemon import approvals as appr, lease, probe_api, reader, tools
from probe.daemon.store import Store

SID = "11111111-2222-3333-4444-555555555555"
FAKE_KEY = "sk-proj-" + "Ab3dE5gH7jK9mN1pQ3sT5vX7zB9dF1hJ3lN5pR7tV9xZ"


@pytest.fixture(autouse=True)
def _state(tmp_path, monkeypatch):
    monkeypatch.setenv("XDG_STATE_HOME", str(tmp_path / "state"))
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path / "config"))
    monkeypatch.delenv("PROBE_AGENT", raising=False)
    monkeypatch.setattr(probe_api, "_features", None)


def _live(sid: str = SID) -> None:
    lease.sessions_dir().mkdir(parents=True, exist_ok=True)
    (lease.sessions_dir() / f"{sid}.state").write_text("daemon")
    assert lease.renew(sid)


def _deps(tmp_path, *, bypass: bool = False, seed: str | None = f"{SID}:41") -> tools.Deps:
    work = tmp_path / "work"
    work.mkdir(parents=True, exist_ok=True)
    deps = tools.Deps(store=Store(tmp_path / "s.sqlite", clock=time.time), board=appr.Board(tmp_path / "appr"),
                      session_id=SID, cwd=work, workdirs=[work], home=tmp_path, write_dirs=[], probe_env={},
                      bypass=bypass, mode_known=True, bite_id=1)
    deps.op_seed = seed
    _live()
    return deps


def _run(coro):
    return asyncio.run(coro)


class Probe:
    """Stands in for `tools.run_probe_process`, the function every probe command
    the daemon runs goes through: records what ran, with its key and folder."""

    def __init__(self, answers: dict[str, str] | None = None, codes: dict[str, int] | None = None) -> None:
        self.calls: list[tuple[list[str], str]] = []
        self.folders: list = []
        self.answers = answers or {}
        self.codes = codes or {}

    async def __call__(self, deps, argv, op_id, **kw):
        self.calls.append((list(argv), op_id))
        self.folders.append(kw.get("cwd", deps.cwd))
        head = " ".join(argv[:2])
        return tools.ProbeResult(self.codes.get(head, 0), self.answers.get(head, "{}"))

    def argvs(self) -> list[list[str]]:
        return [argv for argv, _ in self.calls]

    def keys(self, head: list[str]) -> list[str]:
        return [key for argv, key in self.calls if argv[:len(head)] == head]


# ---------------------------------------------------------------------------
# [T1] the Idempotency-Key covers the files a command sends
# ---------------------------------------------------------------------------


def _checked_out(tmp_path, monkeypatch) -> tuple[Probe, object]:
    note = tmp_path / "state" / "probe" / "notes" / "run-r1.md"
    note.parent.mkdir(parents=True, exist_ok=True)
    probe = Probe({"notes checkout": json.dumps({"target": "run", "path": str(note)})})
    monkeypatch.setattr(tools, "run_probe_process", probe)
    return probe, note


def test_two_pushes_of_one_note_with_new_text_send_new_keys(tmp_path, monkeypatch):
    """[T1] the server answers a key it has seen with another body with 422: the
    second push of a note in one bite failed. A, B, then A again are three keys
    (A's first key would replay A's receipt while the server keeps B)."""
    probe, note = _checked_out(tmp_path, monkeypatch)
    deps = _deps(tmp_path)
    _run(tools.run_probe_command(deps, ["notes", "checkout", "--run", "r1"]))
    push = ["notes", "push", "--run", "r1"]
    for text in ("first", "second", "first"):
        note.write_text(f"# Findings\n{text}\n")
        assert _run(tools.run_probe_command(deps, push)).startswith("[exit 0]")
    keys = probe.keys(push)
    assert len(set(keys)) == 3, keys
    assert _run(tools.run_probe_command(deps, push)).startswith("[exit 0]")
    assert probe.keys(push)[-1] == keys[-1]  # the same text again: the same key, so a landed push replays
    # A retried bite (same seed, fresh state) sending the same text in the same order sends the same keys.
    retry = _deps(tmp_path / "retry")
    note.write_text("# Findings\nfirst\n")
    _run(tools.run_probe_command(retry, ["notes", "checkout", "--run", "r1"]))
    _run(tools.run_probe_command(retry, push))
    assert probe.keys(push)[-1] == keys[0]


@pytest.mark.parametrize("argv, file", [
    (["run", "set", "r1", "--notes", "@summary.md"], "summary.md"),  # an @file the CLI reads as the text
    (["notes", "create", "--run", "r1", "--title", "Eval", "eval.md"], "eval.md"),
])
def test_a_file_a_command_sends_is_part_of_its_key(tmp_path, monkeypatch, argv, file):
    probe = Probe()
    monkeypatch.setattr(tools, "run_probe_process", probe)
    deps = _deps(tmp_path)
    for text in ("val F1 0.81\n", "val F1 0.84\n"):
        (deps.cwd / file).write_text(text)
        assert _run(tools.run_probe_command(deps, argv)).startswith("[exit 0]")
    first, second = probe.keys(argv)
    assert first != second


def test_a_manifest_rows_file_is_part_of_its_key(tmp_path, monkeypatch):
    probe = Probe()
    monkeypatch.setattr(tools, "run_probe_process", probe)
    deps = _deps(tmp_path)
    (deps.cwd / "rows.jsonl").write_text(json.dumps({"path": "results.csv"}) + "\n")
    argv = ["artifact", "add", "--from-manifest", "rows.jsonl", "--project", "p"]
    for text in ("acc\n0.91\n", "acc\n0.93\n"):
        (deps.cwd / "results.csv").write_text(text)
        _run(tools.run_probe_command(deps, argv))
    first, second = probe.keys(argv)
    assert first != second


def test_a_command_that_sends_no_file_keeps_its_key(tmp_path, monkeypatch):
    """The same words, nothing sent: the same key (R3-7's replay), as before."""
    probe = Probe()
    monkeypatch.setattr(tools, "run_probe_process", probe)
    deps = _deps(tmp_path)
    for _ in range(2):
        _run(tools.run_probe_command(deps, ["run", "tag", "r1", "abandoned"]))
    first, second = probe.keys(["run", "tag"])
    assert first == second


# ---------------------------------------------------------------------------
# [T11] slicing a file is a question in normal mode; bypass runs it
# ---------------------------------------------------------------------------


def test_slicing_a_file_is_asked_unless_bypass(tmp_path):
    deps = _deps(tmp_path)
    (deps.cwd / "file.txt").write_text("hello world\n")
    assert "held for the researcher" in _run(tools.shell(deps, "cut -c1-5 file.txt"))
    assert deps.board.all()[0].policy == "shell.unsafe_command"
    bypass = _deps(tmp_path / "b", bypass=True)
    (bypass.cwd / "file.txt").write_text("hello world\n")
    out = _run(tools.shell(bypass, "cut -c1-5 file.txt"))
    assert appr.AUTO in out and out.rstrip().endswith("hello"), out


# ---------------------------------------------------------------------------
# [T7] several commands per shell call
# ---------------------------------------------------------------------------


def _probe(monkeypatch, **kw) -> Probe:
    probe = Probe(**kw)
    monkeypatch.setattr(tools, "run_probe_process", probe)
    return probe


def test_write_tools_name_the_tools_that_write():
    assert tools.WRITE_TOOLS == frozenset({"shell"})


def test_each_probe_part_runs_through_the_probe_tool_in_order_in_the_cd_folder(tmp_path, monkeypatch):
    probe = _probe(monkeypatch)
    deps = _deps(tmp_path)
    sub = deps.cwd / "eval"
    sub.mkdir()
    (sub / "results.csv").write_text("acc\n0.91\n")
    out = _run(tools.shell(deps, "cd eval && probe artifact add results.csv --project p && probe run tag r1 done",
                           why="record the eval"))
    assert probe.argvs() == [["artifact", "add", "results.csv", "--project", "p"], ["run", "tag", "r1", "done"]]
    assert probe.folders == [sub, sub]
    rows = deps.store.db.execute("SELECT head, status, op_id FROM writes ORDER BY id").fetchall()
    assert [(r["head"], r["status"]) for r in rows] == [("artifact add", "ran"), ("run tag", "ran")]
    assert all(r["op_id"] for r in rows)  # each one its own Idempotency-Key
    assert "$ cd eval" in out and "$ probe run tag r1 done" in out


def test_every_probe_part_gets_the_checks_in_the_folder_it_runs_in(tmp_path, monkeypatch):
    probe = _probe(monkeypatch)
    deps = _deps(tmp_path)
    (deps.cwd / "eval").mkdir()
    (deps.cwd / "notes.md").write_text("val F1 0.81\n")  # clean here...
    (deps.cwd / "eval" / "notes.md").write_text(f"token = {FAKE_KEY}\n")  # ...a key in the one the cd reaches
    out = _run(tools.shell(deps, "cd eval && probe run set r1 --notes @notes.md; probe session toggle; "
                                 "probe run tag r1 x"))
    assert "credential" in out and "isn't the daemon's to run" in out, out
    assert probe.argvs() == [["run", "tag", "r1", "x"]]


@pytest.mark.parametrize("op, code, ran", [("&&", 1, False), ("&&", 0, True), ("||", 1, True), ("||", 0, False),
                                           (";", 1, True), ("\n", 1, True)])
def test_and_or_and_semicolon_run_the_next_part_as_bash_would(tmp_path, monkeypatch, op, code, ran):
    probe = _probe(monkeypatch, codes={"run get": code})
    deps = _deps(tmp_path)
    out = _run(tools.shell(deps, f"probe run get r1 {op} probe run tag r1 x"))
    assert (["run", "tag", "r1", "x"] in probe.argvs()) == ran, out
    if not ran:
        assert "[not run: the part before it" in out


def test_a_part_that_did_not_run_counts_as_a_failure(tmp_path, monkeypatch):
    probe = _probe(monkeypatch)
    deps = _deps(tmp_path)
    _run(tools.shell(deps, "probe session toggle && probe run tag r1 a"))  # blocked: the tag waits on it
    _run(tools.shell(deps, "probe session toggle || probe run tag r1 b"))
    assert probe.argvs() == [["run", "tag", "r1", "b"]]


def test_a_probe_read_piped_into_a_filter(tmp_path, monkeypatch):
    probe = _probe(monkeypatch, answers={"run list": "alpha\nbeta\ngamma\n"})
    deps = _deps(tmp_path)
    out = _run(tools.shell(deps, "probe run list | head -1"))
    assert "alpha" in out and "beta" not in out, out
    # A filter off the safe list (tr on text that may hold a key) cannot be held:
    # the output it would read is gone by the time a yes runs it. It is judged
    # BEFORE the probe command runs, so neither part runs.
    ran = len(probe.calls)
    out = _run(tools.shell(deps, "probe run list | tr a-z A-Z"))
    assert "neither part ran" in out and "ALPHA" not in out and deps.board.all() == []
    assert len(probe.calls) == ran
    bypass = _deps(tmp_path / "b", bypass=True)
    assert "ALPHA" in _run(tools.shell(bypass, "probe run list | tr a-z A-Z"))


def test_an_unsafe_part_is_asked_and_what_needs_it_waits(tmp_path, monkeypatch):
    probe = _probe(monkeypatch)
    deps = _deps(tmp_path)
    command = "probe run tag r1 a && touch done.txt && probe run tag r1 b"
    out = _run(tools.shell(deps, command))
    assert "held for the researcher" in out and probe.argvs() == [["run", "tag", "r1", "a"]]
    req = deps.board.all()[0]
    assert (req.held["command"], req.held["cwd"]) == ("touch done.txt", str(deps.cwd))
    bypass = _deps(tmp_path / "b", bypass=True)
    _run(tools.shell(bypass, command))
    assert (bypass.cwd / "done.txt").exists() and probe.argvs()[-1] == ["run", "tag", "r1", "b"]


def test_a_moved_switch_stops_the_rest_of_the_compound(tmp_path, monkeypatch):
    ran = []

    async def run_probe(deps, argv, op_id, **kw):
        ran.append(list(argv))
        (lease.sessions_dir() / f"{SID}.state").write_text("off")  # the researcher moves the switch
        return tools.ProbeResult(0, "{}")

    monkeypatch.setattr(tools, "run_probe_process", run_probe)
    deps = _deps(tmp_path)
    out = _run(tools.shell(deps, "probe run tag r1 a; probe run tag r1 b"))
    assert ran == [["run", "tag", "r1", "a"]] and tools.NO_LEASE in out and deps.stopped


def test_a_compound_with_a_redirected_probe_command_runs_nothing(tmp_path, monkeypatch):
    probe = _probe(monkeypatch)
    deps = _deps(tmp_path, bypass=True)
    out = _run(tools.shell(deps, "probe run tag r1 a && probe run list > runs.json"))
    assert out.startswith("not run") and "refused in every mode" in out and probe.calls == []


def test_an_override_of_a_block_from_another_folder_is_refused(tmp_path, monkeypatch):
    """A yes runs from the worker in the session's folder: a relative path would
    name another file there than the one the check read."""
    _probe(monkeypatch)
    deps = _deps(tmp_path)
    (deps.cwd / "eval").mkdir()
    (deps.cwd / "eval" / "notes.md").write_text(f"token = {FAKE_KEY}\n")
    out = _run(tools.shell(deps, "cd eval && probe run set r1 --notes @notes.md"))
    block_id = re.search(r"block (\w+)", out).group(1)
    out = _run(tools.shell(deps, f"probe daemon override {block_id} --why 'a test fixture'"))
    assert out.startswith("not run") and "came from a command run in" in out and deps.board.all() == []


def test_the_probe_process_starts_in_the_folder_the_cd_reached(tmp_path, monkeypatch):
    """Through the real process runner: a stand-in `probe` executable prints
    where it runs (no server is involved)."""
    fake = tmp_path / "probe"
    fake.write_text("#!/bin/sh\npwd\n")
    fake.chmod(0o755)
    monkeypatch.setattr(tools, "probe_executable", lambda: [str(fake)])
    deps = _deps(tmp_path)
    (deps.cwd / "eval").mkdir()
    out = _run(tools.shell(deps, "cd eval && probe run list && cd .. && probe run list"))
    printed = [line for line in out.splitlines() if line.startswith("/")]
    assert printed == [str(deps.cwd / "eval"), str(deps.cwd)], out


def test_a_long_compound_keeps_its_lease(tmp_path, monkeypatch):
    """The lease is renewed between tool calls; a compound's parts are progress
    inside one call, so it is renewed between them too (a lapsed one stays lost)."""
    seen = []

    async def run_probe(deps, argv, op_id, **kw):
        seen.append(lease.may_write(SID, now=time.time() + 60))  # would the lease still hold a minute on?
        data = json.loads(lease.lease_path(SID).read_text())
        lease.lease_path(SID).write_text(json.dumps({**data, "expires_at": time.time() + 30}))  # a slow command
        return tools.ProbeResult(0, "{}")

    monkeypatch.setattr(tools, "run_probe_process", run_probe)
    deps = _deps(tmp_path)
    _run(tools.shell(deps, "probe run tag r1 a && probe run tag r1 b && probe run tag r1 c"))
    assert seen == [None, None, None]
    lease.release(SID, lease.REASON_STOPPED)
    out = _run(tools.shell(deps, "probe run tag r1 d; probe run tag r1 e"))
    assert tools.NO_LEASE in out and len(seen) == 3  # a released lease is not renewed back to life


# ---------------------------------------------------------------------------
# [T8] the file reader
# ---------------------------------------------------------------------------


def _read(deps, path, **kw) -> str:
    return _run(tools.read_file(deps, path, **kw))


def _npy(descr: str, shape: tuple, fmt: str = "", values: tuple = ()) -> bytes:
    """A .npy file in NumPy's own format (version 1.0), without numpy."""
    header = repr({"descr": descr, "fortran_order": False, "shape": shape}).encode("latin1")
    header += b" " * ((64 - (11 + len(header)) % 64) % 64) + b"\n"
    return b"\x93NUMPY\x01\x00" + struct.pack("<H", len(header)) + header + struct.pack(f"<{fmt}", *values)


def test_read_numbers_lines_and_reads_a_range(tmp_path):
    deps = _deps(tmp_path)
    (deps.cwd / "log.txt").write_text("".join(f"line {n}\n" for n in range(1, 51)))
    out = _read(deps, "log.txt", offset=10, limit=5)
    assert "    10\tline 10" in out and "    14\tline 14" in out and "line 15" not in out and "offset=15" in out
    whole = _read(deps, "log.txt")
    assert "    50\tline 50" in whole and "more follows" not in whole
    (deps.cwd / "wide.txt").write_text("x" * 50_000 + "\nnext\n")
    wide = _read(deps, "wide.txt")
    assert "[... line cut]" in wide and "     2\tnext" in wide and len(wide) < 5_000
    big = deps.cwd / "big.txt"
    big.write_text("".join(f"{'y' * 100} {n}\n" for n in range(5_000)))
    assert len(_read(deps, "big.txt")) <= reader.MAX_CHARS + 200  # capped, with where to read on
    row = deps.store.db.execute("SELECT tool, query FROM lookups ORDER BY id DESC").fetchone()
    assert (row["tool"], row["query"]) == ("read", "big.txt")


def test_read_previews_tables_and_json(tmp_path):
    deps = _deps(tmp_path)
    (deps.cwd / "results.csv").write_text("model,acc\nsvm,0.9889\nlogreg,0.9603\n")
    out = _read(deps, "results.csv")
    assert "2 rows × 2 columns" in out and "svm" in out and "0.9603" in out
    (deps.cwd / "results.tsv").write_text("model\tacc\nsvm\t0.9889\n")
    assert "1 rows × 2 columns" in _read(deps, "results.tsv")
    (deps.cwd / "metrics.json").write_text(json.dumps({"acc": 0.91, "runs": [1, 2]}))
    out = _read(deps, "metrics.json")
    assert "an object with 2 keys: acc, runs" in out and '"acc": 0.91' in out
    assert "     1\tmodel,acc" in _read(deps, "results.csv", offset=1, limit=1)  # a range reads it as text


def test_read_previews_numpy_without_numpy(tmp_path):
    deps = _deps(tmp_path)
    (deps.cwd / "w.npy").write_bytes(_npy("<f8", (2, 3), "6d", (1, 2, 3, 4, 5, 6.5)))
    out = _read(deps, "w.npy")
    assert "dtype float64, shape (2, 3)" in out and "[1, 2, 3]" in out and "[4, 5, 6.5]" in out
    with zipfile.ZipFile(deps.cwd / "arrays.npz", "w") as archive:
        archive.writestr("a.npy", _npy("<i8", (4,), "4q", (0, 1, 2, 3)))
        archive.writestr("b.npy", _npy("|b1", (1,), "?", (True,)))
    out = _read(deps, "arrays.npz")
    assert "a: dtype int64, shape (4,)" in out and "[0, 1, 2, 3]" in out and "b: dtype bool" in out


@pytest.mark.parametrize("name, data", [
    ("model.pkl", pickle.dumps({"w": 1})),
    ("blob.bin", pickle.dumps({"w": 1})),  # a pickle by its bytes, whatever its name
    ("weights.pt", b"PK\x03\x04 a torch archive"),
    ("objects.npy", _npy("|O", (2,))),  # an object array: NumPy pickles it
], ids=["pkl", "pickle-bytes", "torch", "object-array"])
def test_read_never_loads_a_pickle(tmp_path, name, data):
    deps = _deps(tmp_path)
    (deps.cwd / name).write_bytes(data)
    out = _read(deps, name)
    assert out.startswith("not read") and "pickle" in out, out


def test_read_refuses_images_and_binaries_and_says_what_parquet_needs(tmp_path, monkeypatch):
    deps = _deps(tmp_path)
    (deps.cwd / "plot.png").write_bytes(b"\x89PNG\r\n\x1a\n")
    assert "image" in _read(deps, "plot.png")
    (deps.cwd / "data.bin").write_bytes(b"\x00\x01\x02" * 10)
    assert "binary file" in _read(deps, "data.bin")

    def missing():
        raise ImportError("No module named 'pyarrow'")

    monkeypatch.setattr(reader, "_import_parquet", missing)
    (deps.cwd / "rows.parquet").write_bytes(b"PAR1....PAR1")
    out = _read(deps, "rows.parquet")
    assert out.startswith("not previewed") and "pyarrow" in out


def test_read_previews_parquet_when_pyarrow_is_there(tmp_path):
    pa = pytest.importorskip("pyarrow")
    import pyarrow.parquet as pq

    deps = _deps(tmp_path)
    pq.write_table(pa.table({"model": ["svm", "logreg"], "acc": [0.9889, 0.9603]}), deps.cwd / "rows.parquet")
    out = _read(deps, "rows.parquet")
    assert "2 rows × 2 columns" in out and "svm" in out


def test_read_keeps_to_the_shells_safe_reads(tmp_path, monkeypatch):
    deps = _deps(tmp_path)
    (tmp_path / "outside.txt").write_text("elsewhere\n")
    (deps.cwd / ".venv").mkdir()
    (deps.cwd / ".venv" / "cfg.txt").write_text("x\n")
    config = tmp_path / "config" / "probe"
    config.mkdir(parents=True)
    (config / "config.json").write_text('{"token": "x"}\n')
    for path in (str(tmp_path / "outside.txt"), ".venv/cfg.txt", "../outside.txt"):
        assert _read(deps, path).startswith("not read"), path
    assert "every mode" in _read(deps, str(config / "config.json"))
    memory = tmp_path / ".claude" / "projects" / "-w" / "memory" / "MEMORY.md"
    memory.parent.mkdir(parents=True)
    memory.write_text("- prefer uv\n")
    assert "prefer uv" in _read(deps, "~/.claude/projects/-w/memory/MEMORY.md")  # the agent's memory
    notes = tmp_path / "state" / "probe" / "notes"
    notes.mkdir(parents=True)
    (notes / "run-r1.md").write_text("# Findings\n")
    deps.write_dirs = [notes]
    assert "# Findings" in _read(deps, str(notes / "run-r1.md"))  # a checked-out note
    bypass = _deps(tmp_path / "b", bypass=True)
    assert "elsewhere" in _read(bypass, str(tmp_path / "outside.txt"))  # bypass means bypass...
    assert "every mode" in _read(bypass, str(config / "config.json"))  # ...but never Probe's own key


def test_read_scrubs_and_stops_with_the_lease(tmp_path):
    deps = _deps(tmp_path)
    (deps.cwd / "run.log").write_text(f"key={FAKE_KEY}\nacc 0.91\n")
    out = _read(deps, "run.log")
    assert FAKE_KEY not in out and "acc 0.91" in out
    (lease.sessions_dir() / f"{SID}.state").write_text("off")
    assert _read(deps, "run.log").startswith(tools.NO_LEASE)



# ---------------------------------------------------------------------------
# review of daemon v2 tuning: compound folders, filters, keys, the reader
# ---------------------------------------------------------------------------


def test_a_cd_through_a_symlink_cannot_climb_out_of_the_working_folders(tmp_path, monkeypatch):
    """`cd latest && cd ../..`: the check reads `..` from the link's target, bash
    climbs the link itself -- out of the working folder, into its siblings."""
    probe = _probe(monkeypatch)
    deps = _deps(tmp_path)
    (deps.cwd / "runs" / "a" / "b").mkdir(parents=True)
    (deps.cwd / "latest").symlink_to("runs/a/b")
    (tmp_path / "other").mkdir()
    (tmp_path / "other" / "private.txt").write_text("SIBLING PROJECT PLAN\n")
    out = _run(tools.shell(deps, "cd latest && cd ../.. && probe run list && cat other/private.txt"))
    assert "SIBLING PROJECT PLAN" not in out and "outside the working folders" in out, out
    assert probe.calls == []  # `&&`: nothing after the failed cd ran
    inside = _run(tools.shell(deps, "cd latest && probe run list"))
    assert probe.folders[-1] is not None and "outside" not in inside


def test_a_probe_write_whose_filter_is_refused_does_not_run(tmp_path, monkeypatch):
    """The write would land while the model is told "not run"."""
    probe = _probe(monkeypatch)
    deps = _deps(tmp_path)
    out = _run(tools.shell(deps, "probe run tag r1 best | tee tag.log"))
    assert "not run" in out and "neither part ran" in out and probe.calls == []
    assert not (deps.cwd / "tag.log").exists()


def test_a_write_sent_again_after_a_different_one_gets_its_own_key(tmp_path, monkeypatch):
    """A, B, A of one command path: the third is a new write, not A's replay (the
    server would answer A's stored receipt and keep B)."""
    probe = _probe(monkeypatch)
    deps = _deps(tmp_path)
    for status in ("running", "finished", "running"):
        _run(tools.shell(deps, f"probe run set r1 --status {status}"))
    first, second, third = (key for _, key in probe.calls)
    assert len({first, second, third}) == 3
    _run(tools.shell(deps, "probe run set r1 --status running"))  # again, nothing between: replayed
    assert probe.calls[-1][1] == third
    # The same create twice is made once (a replay); a create after another stays itself.
    for title in ("a", "a", "b", "a"):
        _run(tools.shell(deps, f"probe notes create --project p --title {title}"))
    keys = [key for _, key in probe.calls[-4:]]
    assert keys[0] == keys[1] == keys[3] and keys[2] != keys[0]
    # And a retried bite that sends the same things in the same order sends the same keys.
    retry = _deps(tmp_path / "retry")
    replay = _probe(monkeypatch)
    for status in ("running", "finished", "running"):
        _run(tools.shell(retry, f"probe run set r1 --status {status}"))
    assert [key for _, key in replay.calls] == [first, second, third]


def test_a_blocked_command_reads_none_of_the_files_it_names(tmp_path, monkeypatch):
    _probe(monkeypatch)
    deps = _deps(tmp_path)
    read = []
    monkeypatch.setattr(tools, "_file_digest", lambda path: read.append(path) or "x")
    (deps.cwd / "notes.md").write_text(f"token = {FAKE_KEY}\n")
    out = _run(tools.shell(deps, "probe run set r1 --notes @notes.md"))
    assert "block" in out and read == [] and deps.sent == {}


def test_a_cut_never_shows_a_piece_of_a_key(tmp_path):
    deps = _deps(tmp_path)
    key = "sk-ant-api03-" + "x" * 80
    (deps.cwd / "keys.csv").write_text(f"name,value\nprod,{key}\n")
    out = _read(deps, "keys.csv")
    assert "sk-ant" not in out and "xxxxxxxxxx" not in out, out
    (deps.cwd / "wide.txt").write_text("a " * 999 + key + "\n")
    out = _read(deps, "wide.txt")
    assert "sk-ant" not in out and "[... line cut]" in out, out


@pytest.mark.parametrize("shape", [(2, 1_000_000_000), (-1,), "(3,)", (True,)])
def test_a_crafted_numpy_header_reads_a_bounded_amount(tmp_path, shape):
    deps = _deps(tmp_path)
    header = repr({"descr": "<i8", "fortran_order": False, "shape": shape}).encode("latin1")
    header += b" " * ((64 - (11 + len(header)) % 64) % 64) + b"\n"
    body = b"\x93NUMPY\x01\x00" + struct.pack("<H", len(header)) + header + b"\0" * 4096
    with zipfile.ZipFile(deps.cwd / "bomb.npz", "w", compression=zipfile.ZIP_DEFLATED) as archive:
        archive.writestr("a.npy", body + b"\0" * 50_000_000)
    reads: list[int] = []
    real_open = zipfile.ZipFile.open

    def counting_open(self, *args, **kwargs):
        member = real_open(self, *args, **kwargs)
        real_read = member.read
        member.read = lambda n=-1: reads.append(n) or real_read(n)
        return member

    zipfile.ZipFile.open = counting_open
    try:
        out = _read(deps, "bomb.npz")
    finally:
        zipfile.ZipFile.open = real_open
    assert all(0 <= n <= (1 << 20) for n in reads), reads
    assert out.startswith("[") or out.startswith("not read"), out


def test_the_reader_does_not_wait_on_a_fifo_or_trip_on_a_nul(tmp_path):
    import os

    deps = _deps(tmp_path)
    os.mkfifo(deps.cwd / "pipe")
    assert "isn't a regular file" in _read(deps, "pipe")
    assert _read(deps, "a\0b").startswith("not read")


# ---------------------------------------------------------------------------
# session(op=...): one tool for the chat log, the logbook and the state of the
# record. Its schema is the union of the ops' arguments, so an argument of
# another op is refused, never dropped (#735).
# ---------------------------------------------------------------------------


#: One value for every argument of `session` but `op`.
SESSION_ARGS = {"event_id": "main:1:0", "turn": 1, "page": 1, "query": "sweep", "kind": "prompt", "turn_from": 1,
                "turn_to": 2}


def test_the_session_arguments_walked_are_the_tools_whole_schema():
    pytest.importorskip("pydantic_ai")
    from pydantic_ai.models.function import FunctionModel

    from probe.daemon import agent as agent_mod

    agent = agent_mod.build_agent("instructions", model=FunctionModel(lambda m, i: None))
    schema = agent._function_toolset.tools["session"].tool_def.parameters_json_schema
    assert set(schema["properties"]) - {"op"} == set(SESSION_ARGS)
    assert schema["properties"]["op"]["enum"] == [op.value for op in tools.SessionOp]
    assert schema["required"] == ["op"]
    assert {name for opts in tools.SESSION_OPTIONS.values() for name in opts} == set(SESSION_ARGS)


@pytest.mark.parametrize("op", list(tools.SessionOp))
def test_session_refuses_every_argument_of_another_op(tmp_path, op):
    deps = _deps(tmp_path)
    read: list[int] = []
    options = tools.SESSION_OPTIONS[op]
    foreign = [name for name in SESSION_ARGS if name not in options]
    for name in foreign:
        out = tools.session(deps, op.value, status=lambda: read.append(1) or "state", **{name: SESSION_ARGS[name]})
        assert out == (f"not run: `{name}` is not an option of op={op.value}; its options are: "
                       f"{', '.join(options) or 'none'}"), out
    if len(foreign) > 1:
        out = tools.session(deps, op.value, **{name: SESSION_ARGS[name] for name in foreign[:2]})
        assert out.startswith(f"not run: `{foreign[0]}`, `{foreign[1]}` are not options of op={op.value}")
    assert read == [] and deps.store.db.execute("SELECT count(*) AS n FROM lookups").fetchone()["n"] == 0
    # Its own arguments are never refused.
    own = tools.session(deps, op.value, status=lambda: "state", **{name: SESSION_ARGS[name] for name in options})
    assert "is not an option" not in own and "are not options" not in own
