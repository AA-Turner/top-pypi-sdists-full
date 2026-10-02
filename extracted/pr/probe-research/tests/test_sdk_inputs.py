"""The read recorder (lineage): what a run READS, observed from inside the run.

`probe.init()` records every file the process opens for reading, hashes it and
sends the list at `finish()`; the server matches each hash to the run that
wrote those bytes. These tests pin what is recorded (reads, not writes; the
run's reads, not Probe's own), how a read is identified (unstable when the file
moved), the bounds (budget, fingerprint), the processes that record (forked
workers, `probe exec`'s Python child) and the delivery (non-blocking, only to a
server that accepts it, recovered after a crash).
"""

from __future__ import annotations

import hashlib
import json
import multiprocessing
import os
import subprocess
import sys
import time
from pathlib import Path

import pytest

import probe
from probe.sdk import fluent, inputs
from tests.conftest import make_client


@pytest.fixture(autouse=True)
def _recorder(monkeypatch, tmp_path):
    """Read capture ON, its state under tmp, and no run left recording."""
    monkeypatch.setenv(inputs.READS_ENV, "1")
    monkeypatch.delenv(inputs.CHILD_DIR_ENV, raising=False)
    # A launcher's hand-off, possibly left in os.environ by another test file:
    # probe.init(experiment=...) refuses to run under one.
    for name in ("PROBE_RUN_ID", "PROBE_RUN_EPOCH"):
        monkeypatch.delenv(name, raising=False)
    monkeypatch.setenv("XDG_STATE_HOME", str(tmp_path / "state"))
    inputs._active.clear()
    inputs._hash_results.clear()
    fluent._current.set(None)
    fluent._process_default = None
    yield
    inputs._active.clear()
    fluent._current.set(None)
    fluent._process_default = None


def _sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _data_file(tmp_path: Path, name: str, data: bytes) -> Path:
    path = tmp_path / "work" / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)
    return path


def _dead_pid() -> int:
    return int(
        subprocess.run(
            [sys.executable, "-c", "import os; print(os.getpid())"],
            capture_output=True,
            text=True,
            check=True,
        ).stdout.strip()
    )


def _spool_line(path: Path, t: str = "2026-09-26T00:00:00+00:00") -> str:
    st = os.stat(path)
    return (
        json.dumps(
            {
                "p": str(path),
                "d": st.st_dev,
                "i": st.st_ino,
                "s": st.st_size,
                "m": st.st_mtime_ns,
                "c": st.st_ctime_ns,
                "t": t,
            }
        )
        + "\n"
    )


# -- what counts as a read ------------------------------------------------------


@pytest.mark.parametrize(
    ("mode", "flags", "expected"),
    [
        ("r", 0, True),
        ("rb", 0, True),
        ("w", 0, False),
        ("a", 0, False),
        ("r+", 0, False),
        ("xb", 0, False),
        (None, os.O_RDONLY, True),
        (None, os.O_WRONLY, False),
        (None, os.O_RDWR, False),
        (None, os.O_RDONLY | os.O_CREAT, False),
        (None, None, False),
    ],
)
def test_reads_are_told_from_writes(mode, flags, expected) -> None:
    assert inputs._is_read(mode, flags) is expected


def test_what_is_never_an_input(tmp_path) -> None:
    home = str(Path.home())
    site = next(p for p in sys.path if p.endswith("site-packages"))
    never = [
        f"{site}/numpy/core/data.bin",
        "/proc/self/status",
        "/etc/resolv.conf",
        f"{tmp_path}/train.py",
        f"{tmp_path}/mod.cpython-312.pyc",
        f"{home}/.cache/pip/http/x",
        f"{home}/.ssh/config",
        f"{tmp_path}/.env",
        f"{tmp_path}/credentials.json",
        f"{home}/.local/state/probe/outbox/op.json",
        f"{home}/.cache/huggingface/token",
        f"{home}/.kube/config",
        f"{home}/.docker/config.json",
        "/usr/lib/python3/dist-packages/x.txt",
        "/run/secrets/db_password",
        "relative/path.csv",
    ]
    kept = [
        f"{home}/.cache/huggingface/hub/models--x/snapshots/1/config.json",
        f"{tmp_path}/data/train.parquet",
        "/tmp/shards/000.tar",
        "/usr/src/app/data/train.csv",
        "/run/media/me/disk/shard.tar",
    ]
    for path in never:
        assert inputs.excluded(path), path
    for path in kept:
        assert not inputs.excluded(path), path


# -- recording in process ------------------------------------------------------


def test_a_run_records_what_it_reads_not_what_it_writes(tmp_path) -> None:
    data = _data_file(tmp_path, "train.csv", b"x,y\n" * 100)
    assert inputs.start("run-a")
    with open(data, "rb") as handle:
        handle.read()
    (tmp_path / "work" / "out.json").write_text("{}")
    rows, coverage = inputs.collect("run-a", wait_s=5)
    by_path = {r["path"]: r for r in rows}
    assert str(data) in by_path
    assert by_path[str(data)]["content_hash"] == _sha(b"x,y\n" * 100)
    assert by_path[str(data)]["stable"] is True
    assert str(tmp_path / "work" / "out.json") not in by_path
    assert coverage["recorder"] == inputs.RECORDER
    assert coverage["unseen"] == list(inputs.UNSEEN_READERS)
    assert not inputs.is_recording("run-a")


def test_probes_own_file_work_is_never_a_read(tmp_path) -> None:
    """A `log_artifact` fingerprint, a snapshot or upload staging opens the
    file too; those are Probe's reads, not the run's."""
    from probe.sdk.hashing import fingerprint

    data = _data_file(tmp_path, "model.bin", b"w" * 500)
    other = _data_file(tmp_path, "notes.bin", b"n" * 500)
    assert inputs.start("run-b")
    fingerprint(str(data))  # Probe code opens it
    with inputs.internal():
        other.read_bytes()
    rows, _ = inputs.collect("run-b", wait_s=5)
    assert rows == []


def test_several_unbound_runs_in_one_process_record_nothing(tmp_path) -> None:
    data = _data_file(tmp_path, "shared.bin", b"s" * 500)
    assert inputs.start("run-1") and inputs.start("run-2")
    data.read_bytes()  # nobody bound: ambiguous, recorded for neither
    rows1, coverage1 = inputs.collect("run-1", wait_s=5)
    rows2, _ = inputs.collect("run-2", wait_s=5)
    assert rows1 == [] and rows2 == []
    assert coverage1["ambiguous_opens"] >= 1


def test_a_read_goes_to_the_run_bound_to_this_thread(tmp_path) -> None:
    from types import SimpleNamespace

    data = _data_file(tmp_path, "mine.bin", b"m" * 500)
    assert inputs.start("run-1") and inputs.start("run-2")
    fluent._current.set(SimpleNamespace(run=SimpleNamespace(id="run-2")))
    data.read_bytes()
    rows1, _ = inputs.collect("run-1", wait_s=5)
    rows2, _ = inputs.collect("run-2", wait_s=5)
    assert rows1 == [] and [r["path"] for r in rows2] == [str(data)]


def test_a_forked_worker_records_into_its_own_spool(tmp_path) -> None:
    data = _data_file(tmp_path, "shard.bin", b"f" * 1000)
    assert inputs.start("run-f")

    def worker(path: str) -> None:
        with open(path, "rb") as handle:
            handle.read()

    ctx = multiprocessing.get_context("fork")
    proc = ctx.Process(target=worker, args=(str(data),))
    proc.start()
    proc.join(10)
    assert proc.exitcode == 0
    rows, _ = inputs.collect("run-f", wait_s=5)
    assert [r["path"] for r in rows] == [str(data)]
    assert rows[0]["content_hash"] == _sha(b"f" * 1000)


# -- identity and bounds -------------------------------------------------------


def test_a_file_that_moved_since_the_read_is_unstable(tmp_path) -> None:
    data = _data_file(tmp_path, "moving.bin", b"a" * 100)
    st = os.stat(data)
    ident = inputs._ident(st)
    data.write_bytes(b"b" * 200)
    assert inputs.hash_file(str(data), ident, cache=None, budget=[1 << 40]) == (None, None)


def test_big_files_and_an_exhausted_budget_get_a_fingerprint(tmp_path, monkeypatch) -> None:
    data = _data_file(tmp_path, "big.bin", os.urandom(3000))
    st = os.stat(data)
    ident = inputs._ident(st)
    monkeypatch.setattr(inputs, "FULL_HASH_MAX_BYTES", 1000)
    sha, fp = inputs.hash_file(str(data), ident, cache=None, budget=[1 << 40])
    assert sha is None and fp.startswith("3000:")
    monkeypatch.setattr(inputs, "FULL_HASH_MAX_BYTES", 1 << 30)
    # Past the budget a fingerprint is taken only if the budget can pay for
    # the edges it reads (F2c: every byte counts)...
    monkeypatch.setattr(inputs, "EDGE_BYTES", 100)
    budget = [500]
    sha, fp = inputs.hash_file(str(data), ident, cache=None, budget=budget)
    assert sha is None and fp is not None and budget == [300]
    # ...and when it cannot, nothing is read at all.
    budget = [10]
    assert inputs.hash_file(str(data), ident, cache=None, budget=budget) is None
    assert budget == [10]


def test_the_machine_cache_hashes_a_file_once(tmp_path, monkeypatch) -> None:
    data = _data_file(tmp_path, "dataset.bin", b"d" * 2000)
    st = os.stat(data)
    ident = inputs._ident(st)
    cache = inputs._HashCache()
    first = inputs.hash_file(str(data), ident, cache=cache, budget=[1 << 40])
    opened = []
    real_open = open
    monkeypatch.setattr("builtins.open", lambda *a, **k: opened.append(a) or real_open(*a, **k))
    second = inputs.hash_file(str(data), ident, cache=inputs._HashCache(), budget=[1 << 40])
    assert first == second == (_sha(b"d" * 2000), None)
    assert not any(str(data) in str(a[0]) for a in opened)


def test_a_rewritten_file_is_read_again(tmp_path) -> None:
    """Read checkpoint A, replace it at the same path with B, read again: both
    are the run's inputs."""
    data = _data_file(tmp_path, "ckpt.bin", b"A" * 300)
    assert inputs.start("run-rewrite")
    data.read_bytes()
    deadline = time.monotonic() + 5  # A hashed before it is gone (else: unstable)
    while inputs._hash_queue.unfinished_tasks and time.monotonic() < deadline:
        time.sleep(0.02)
    data.unlink()
    data.write_bytes(b"B" * 300)
    data.read_bytes()
    rows, _ = inputs.collect("run-rewrite", wait_s=5)
    assert sorted(r["content_hash"] for r in rows) == sorted([_sha(b"A" * 300), _sha(b"B" * 300)])


def test_a_failed_open_does_not_hide_the_later_read(tmp_path) -> None:
    """A job polling for a file another job has not written yet."""
    later = tmp_path / "work" / "best_eval.json"
    later.parent.mkdir(parents=True, exist_ok=True)
    assert inputs.start("run-poll")
    with pytest.raises(FileNotFoundError):
        later.read_bytes()
    later.write_bytes(b"e" * 300)
    later.read_bytes()
    rows, _ = inputs.collect("run-poll", wait_s=5)
    assert [r["path"] for r in rows] == [str(later)]


def test_the_path_cap_bounds_what_is_held(tmp_path, monkeypatch) -> None:
    monkeypatch.setattr(inputs, "MAX_PATHS", 3)
    files = [_data_file(tmp_path, f"f{i}.bin", bytes([65 + i]) * 100) for i in range(5)]
    assert inputs.start("run-cap")
    for f in files:
        f.read_bytes()
    reads = inputs._active["run-cap"]
    assert len(reads.seen) == 3 and reads.truncated
    rows, coverage = inputs.collect("run-cap", wait_s=5)
    assert len(rows) == 3 and coverage["truncated"] is True


def test_finishing_never_waits_past_its_budget_on_a_stalled_file(tmp_path, monkeypatch) -> None:
    """A dataset mount that hangs after training must cost the read its hash,
    never the run its close."""
    data = _data_file(tmp_path, "stalled.bin", b"s" * 300)
    assert inputs.start("run-stall")
    data.read_bytes()
    time.sleep(0.3)
    inputs._hash_results.clear()
    monkeypatch.setattr(inputs, "hash_file", lambda *a, **k: time.sleep(2) or ("x", None))
    began = time.monotonic()
    rows, coverage = inputs.collect("run-stall", wait_s=0.2)
    assert time.monotonic() - began < 2
    assert rows[0]["content_hash"] is None and rows[0]["stable"] is True
    assert coverage["unhashed"] == 1
    # While that worker is stuck, a second close hashes nothing more rather
    # than pile another thread onto the same mount.
    assert inputs.start("run-stall-2")
    data.read_bytes()
    rows2, coverage2 = inputs.collect("run-stall-2", wait_s=0.2)
    assert coverage2["unhashed"] == 1
    inputs._finish_worker.join(10)


def test_a_budget_fingerprint_is_not_cached_as_the_files_answer(tmp_path, monkeypatch) -> None:
    monkeypatch.setattr(inputs, "EDGE_BYTES", 100)
    data = _data_file(tmp_path, "small.bin", b"q" * 3000)
    ident = inputs._ident(os.stat(data))
    cache = inputs._HashCache()
    sha, fp = inputs.hash_file(str(data), ident, cache=cache, budget=[500])
    assert sha is None and fp is not None
    assert inputs.hash_file(str(data), ident, cache=cache, budget=[1 << 40]) == (
        _sha(b"q" * 3000),
        None,
    )


def test_unsendable_paths_are_counted_not_sent() -> None:
    assert inputs._sendable("/data/ok.bin")
    assert not inputs._sendable("/data/" + "x" * 3000)
    assert not inputs._sendable("/data/\udcff.bin")


def test_a_fork_while_the_lock_is_held_does_not_deadlock_the_child(monkeypatch) -> None:
    import threading

    for name in ("_lock", "_hash_queue", "_hasher", "_hasher_pid"):
        monkeypatch.setattr(inputs, name, getattr(inputs, name))
    held, release = threading.Event(), threading.Event()

    def holder() -> None:
        with inputs._lock:
            held.set()
            release.wait(5)

    thread = threading.Thread(target=holder)
    thread.start()
    held.wait(5)
    assert inputs.start("run-forked")
    reads = inputs._active["run-forked"]
    reads.seen["/x"] = (1,)
    reads.count, reads.truncated = inputs.MAX_PATHS, True
    try:
        inputs._after_fork_in_child()  # what os.fork runs in the child
        assert inputs._lock.acquire(timeout=1)
        inputs._lock.release()
        # The child records its own reads from zero, not under the parent's cap.
        assert reads.seen == {} and reads.count == 0 and reads.truncated is False
    finally:
        release.set()
        thread.join()


def test_a_capped_spool_says_so(tmp_path) -> None:
    """A forked worker or a probe exec child knows it hit the cap; the closing
    process learns it only from the spool."""
    data = _data_file(tmp_path, "one.bin", b"1" * 100)
    spool = tmp_path / "x.1.jsonl"
    spool.write_text(_spool_line(data) + json.dumps({"truncated": True}) + "\n")
    observed, truncated = inputs._read_spools([spool])
    assert len(observed) == 1 and truncated is True


def test_a_rank_that_has_not_read_yet_keeps_the_folder(tmp_path) -> None:
    """Spools appear at the first read. Another live process's marker keeps the
    first rank to close from deleting the folder (and a probe exec child's
    hook) under it."""
    data = _data_file(tmp_path, "r.bin", b"r" * 100)
    assert inputs.start("run-two-ranks")
    data.read_bytes()
    directory = inputs.run_dir("run-two-ranks")
    (directory / f"{inputs._host()}.{os.getppid()}.live").touch()  # a live peer
    inputs.collect("run-two-ranks", wait_s=5)
    inputs.discard("run-two-ranks")
    assert directory.exists()
    assert not list(directory.glob("*.jsonl"))


def test_a_system_python_does_not_hide_usr_src(monkeypatch) -> None:
    """Debian/Ubuntu Python has base_prefix /usr; /usr/src/app is where the
    official images keep the job."""
    monkeypatch.setattr(sys, "base_prefix", "/usr")
    inputs._interpreter_prefixes.cache_clear()
    try:
        assert not inputs.excluded("/usr/src/app/data/train.csv")
        assert inputs.excluded("/usr/lib/python3.12/json/decoder.txt")
    finally:
        inputs._interpreter_prefixes.cache_clear()


def test_a_budget_fingerprint_stays_with_its_run() -> None:
    own: dict = {}
    small, big = (1, 2, 100, 3, 4), (1, 3, inputs.FULL_HASH_MAX_BYTES + 1, 3, 4)
    inputs._keep((None, "fp"), small, own)
    inputs._keep((None, "fp"), big, own)
    inputs._keep(("sha", None), (1, 4, 100, 3, 4), own)
    assert small in own and small not in inputs._hash_results
    assert big in inputs._hash_results and (1, 4, 100, 3, 4) in inputs._hash_results


# -- delivery ------------------------------------------------------------------


class _Journal:
    def __init__(self) -> None:
        self.ops: list[tuple] = []

    def append_http(self, method, path, body, *, run_ref=None, blocking=True, **_):
        self.ops.append((method, path, body, run_ref, blocking))
        return "op"


class _Client:
    def __init__(self, supported: bool) -> None:
        self.supported = supported
        self.journal = _Journal()

    def supports_feature(self, name: str) -> bool:
        return self.supported and name == inputs.FEATURE


def test_reads_are_sent_in_chunks_as_non_blocking_ops() -> None:
    rows = [
        {
            "path": f"/d/{i}",
            "content_hash": None,
            "stable": True,
            "first_seen_at": "2026-09-26T00:00:00+00:00",
        }
        for i in range(4500)
    ]
    client = _Client(True)
    assert inputs.send(client, "run-s", rows, {"recorder": "x"})
    ops = client.journal.ops
    assert [len(o[2]["inputs"]) for o in ops] == [2000, 2000, 500]
    assert all(o[0] == "POST" and o[1] == "/v1/runs/run-s/inputs" for o in ops)
    assert all(o[4] is False for o in ops)  # never holds the run's close
    # Every batch carries the coverage: only a late re-send has none (F7).
    assert all(o[2]["coverage"] == {"recorder": "x"} for o in ops)


def test_an_older_server_drops_the_reads_without_hashing(tmp_path, monkeypatch) -> None:
    """A server that does not declare run_inputs never will for this build:
    hashing for it is wasted work and keeping the spools grows the disk forever."""
    _data_file(tmp_path, "old.bin", b"o" * 100)
    assert inputs.start("run-old")
    (tmp_path / "work" / "old.bin").read_bytes()
    collected: list[str] = []
    monkeypatch.setattr(inputs, "collect_all", lambda run_id, **k: collected.append(run_id))
    client = _Client(False)
    inputs.finalize(client, "run-old", wait_s=0)
    assert client.journal.ops == [] and collected == []  # no finish-time hashing
    assert not inputs.is_recording("run-old")
    assert not inputs.run_dir("run-old").exists()


def test_an_unreachable_server_keeps_the_reads_for_recovery(tmp_path) -> None:
    _data_file(tmp_path, "keep.bin", b"k" * 100)
    assert inputs.start("run-away")
    (tmp_path / "work" / "keep.bin").read_bytes()

    class _Down(_Client):
        def supports_feature(self, name: str) -> bool:
            raise ConnectionError("no route to host")

    client = _Down(True)
    inputs.finalize(client, "run-away", wait_s=0)
    assert client.journal.ops == []
    assert not inputs.is_recording("run-away")
    assert list(inputs.run_dir("run-away").glob("*.jsonl"))
    assert inputs.recover_orphans(client, now=time.time() + 3600) == 0


def test_recovery_clears_a_dead_run_that_read_nothing(tmp_path) -> None:
    directory = inputs.run_dir("run-empty")
    directory.mkdir(parents=True)
    (directory / "owner.json").write_text(
        json.dumps({"run_id": "run-empty", "pid": _dead_pid(), "host": inputs._host()})
    )
    client = _Client(True)
    assert inputs.recover_orphans(client, now=time.time() + 3600) == 0
    assert client.journal.ops == []
    assert not directory.exists()


def test_a_dead_runs_reads_are_recovered(tmp_path) -> None:
    data = _data_file(tmp_path, "left.bin", b"l" * 300)
    directory = inputs.run_dir("run-dead")
    directory.mkdir(parents=True)
    dead = _dead_pid()
    (directory / "owner.json").write_text(json.dumps({"run_id": "run-dead", "pid": dead}))
    (directory / f"{inputs._host()}.{dead}.jsonl").write_text(_spool_line(data))
    client = _Client(True)
    assert inputs.recover_orphans(client, now=time.time()) == 0  # too fresh
    assert inputs.recover_orphans(client, now=time.time() + 3600) == 1
    body = client.journal.ops[0][2]
    assert body["coverage"]["recovered"] is True
    assert body["inputs"][0]["content_hash"] == _sha(b"l" * 300)
    assert not directory.exists()


def test_another_hosts_spools_are_never_taken(tmp_path) -> None:
    """A home directory shared across a cluster holds every node's spools: a
    pid dead HERE says nothing about a process on another node."""
    data = _data_file(tmp_path, "remote.bin", b"r" * 300)
    directory = inputs.run_dir("run-remote")
    directory.mkdir(parents=True)
    (directory / "owner.json").write_text(json.dumps({"run_id": "run-remote", "pid": 1}))
    (directory / f"other-node.{_dead_pid()}.jsonl").write_text(_spool_line(data))
    client = _Client(True)
    assert inputs.recover_orphans(client, now=time.time() + 3600) == 0
    assert client.journal.ops == []
    assert list(directory.glob("*.jsonl"))


def test_another_tenants_leftovers_are_not_sent(tmp_path) -> None:
    data = _data_file(tmp_path, "theirs.bin", b"t" * 300)
    directory = inputs.run_dir("run-theirs")
    directory.mkdir(parents=True)
    dead = _dead_pid()
    (directory / "owner.json").write_text(
        json.dumps({"run_id": "run-theirs", "pid": dead, "token_id": "someone-else"})
    )
    (directory / f"{inputs._host()}.{dead}.jsonl").write_text(_spool_line(data))
    client = _Client(True)
    client.settings = type("S", (), {"base_url": None, "token": "mine"})()
    assert inputs.recover_orphans(client, now=time.time() + 3600) == 0
    assert list(directory.glob("*.jsonl"))


def test_a_live_ranks_spool_is_left_for_it(tmp_path) -> None:
    """Several ranks on one run each send their own reads: the first to close
    must not read and delete a spool another live process still writes."""
    mine = _data_file(tmp_path, "mine.bin", b"m" * 300)
    theirs = _data_file(tmp_path, "theirs.bin", b"o" * 300)
    assert inputs.start("run-ranks")
    mine.read_bytes()
    live = inputs.run_dir("run-ranks") / f"{inputs._host()}.{os.getppid()}.jsonl"
    live.write_text(_spool_line(theirs))
    rows, _ = inputs.collect("run-ranks", wait_s=5)
    assert [r["path"] for r in rows] == [str(mine)]
    inputs.discard("run-ranks")
    assert live.exists()


# -- probe exec's Python child ---------------------------------------------------


def test_an_exec_child_records_through_the_injected_hook(tmp_path) -> None:
    data = _data_file(tmp_path, "input.bin", b"c" * 400)
    user_site = tmp_path / "user_site"
    user_site.mkdir()
    marker = tmp_path / "chained"
    (user_site / "sitecustomize.py").write_text(f"open({str(marker)!r}, 'w').write('yes')\n")
    env = {**os.environ, "PYTHONPATH": str(user_site)}
    assert inputs.prepare_child("run-x", env)
    assert env["PYTHONPATH"].endswith(str(user_site))
    code = f"open({str(data)!r}, 'rb').read(); open({str(tmp_path / 'w.txt')!r}, 'w').write('x')"
    subprocess.run([sys.executable, "-c", code], env=env, check=True)
    assert marker.read_text() == "yes"  # the environment's own sitecustomize still ran
    rows, _ = inputs.collect("run-x", wait_s=5)
    assert [r["path"] for r in rows] == [str(data)]
    assert rows[0]["content_hash"] == _sha(b"c" * 400)


def test_the_child_hook_lets_the_main_script_open(tmp_path) -> None:
    """The interpreter opens `python train.py`'s script with no Python frame
    on the stack; the hook asking for its caller's frame raised there, and an
    audit hook's exception fails the open ("can't open file ... [Errno 22]")."""
    data = _data_file(tmp_path, "script_input.bin", b"s" * 300)
    script = tmp_path / "train.py"
    script.write_text(f"open({str(data)!r}, 'rb').read()\n")
    env = {**os.environ}
    assert inputs.prepare_child("run-script", env)
    subprocess.run([sys.executable, str(script)], env=env, check=True)
    rows, _ = inputs.collect("run-script", wait_s=5)
    assert [r["path"] for r in rows] == [str(data)]


def test_an_open_with_no_python_frame_never_raises_into_it(tmp_path, monkeypatch) -> None:
    data = _data_file(tmp_path, "from_c.bin", b"c" * 300)
    assert inputs.start("run-no-frame")

    def no_frame(depth=0):
        raise ValueError("call stack is not deep enough")

    with monkeypatch.context() as patched:
        patched.setattr(sys, "_getframe", no_frame)
        inputs._on_audit("open", (str(data), "r", 0))  # no raise: the open goes on
    rows, _ = inputs.collect("run-no-frame", wait_s=5)
    assert [r["path"] for r in rows] == [str(data)], "no Python code on the stack is not Probe's"


def test_a_nested_exec_installs_one_hook(tmp_path) -> None:
    """`probe exec` inside `probe exec`: the inner child gets the inner hook
    only. Chaining to the outer one used to recurse, a hook per level."""
    data = _data_file(tmp_path, "nested.bin", b"n" * 400)
    outer = {**os.environ}
    assert inputs.prepare_child("run-outer", outer)
    inner = dict(outer)
    assert inputs.prepare_child("run-inner", inner)
    assert str(inputs.run_dir("run-outer")) not in inner["PYTHONPATH"]
    code = (
        f"open({str(data)!r}, 'rb').read(); import sys; "
        "print(len(getattr(sys, '_probe_reads_state', {}).get('seen', {})))"
    )
    out = subprocess.run([sys.executable, "-c", code], env=inner, check=True, capture_output=True)
    assert out.stdout.strip() == b"1"
    spools = list(inputs.run_dir("run-inner").glob("*.jsonl"))
    lines = spools[0].read_text().splitlines()
    assert len(spools) == 1 and json.loads(lines[0]) == {"run": "run-inner", "owner": None, "follows": False}
    assert len(lines) == 2, "the header and ONE read"


def test_a_worker_forked_by_the_exec_child_records_its_own_reads(tmp_path) -> None:
    before = _data_file(tmp_path, "before_fork.bin", b"a" * 200)
    after = _data_file(tmp_path, "in_worker.bin", b"b" * 200)
    env = {**os.environ}
    assert inputs.prepare_child("run-fork-child", env)
    code = (
        f"import os\nopen({str(before)!r}, 'rb').read()\npid = os.fork()\n"
        f"if pid == 0:\n    open({str(after)!r}, 'rb').read()\n    os._exit(0)\n"
        "os.waitpid(pid, 0)\n"
    )
    subprocess.run([sys.executable, "-c", code], env=env, check=True)
    rows, _ = inputs.collect("run-fork-child", wait_s=5)
    assert sorted(r["path"] for r in rows) == sorted([str(before), str(after)])
    assert len(list(inputs.run_dir("run-fork-child").glob("*.jsonl"))) == 2


def test_the_childs_own_environment_can_opt_out(tmp_path) -> None:
    env = {**os.environ, inputs.READS_ENV: "0"}
    assert inputs.prepare_child("run-quiet", env) is False
    assert inputs.CHILD_DIR_ENV not in env


def test_probes_own_opens_in_an_exec_child_are_not_reads(tmp_path) -> None:
    data = _data_file(tmp_path, "logged.bin", b"g" * 400)
    env = {**os.environ}
    assert inputs.prepare_child("run-own", env)
    code = f"from probe.sdk import hashing; hashing.fingerprint({str(data)!r})"
    subprocess.run([sys.executable, "-c", code], env=env, check=True)
    rows, _ = inputs.collect("run-own", wait_s=5)
    assert rows == []


def test_a_process_under_the_exec_hook_does_not_record_twice(monkeypatch, tmp_path) -> None:
    monkeypatch.setenv(inputs.CHILD_DIR_ENV, str(tmp_path / "spool"))
    assert inputs.start("run-y") is False


def test_opting_out(monkeypatch) -> None:
    monkeypatch.setenv(inputs.READS_ENV, "0")
    assert inputs.start("run-z") is False
    env: dict[str, str] = {}
    assert inputs.prepare_child("run-z", env) is False and env == {}
    assert inputs.start("run-z", capture_reads=True)


# -- through the public API -------------------------------------------------------


def test_init_records_and_finish_sends(app, tmp_path, monkeypatch) -> None:
    data = _data_file(tmp_path, "features.npy", b"F" * 700)
    monkeypatch.setattr(
        fluent, "Client", lambda *a, **k: make_client(app, tmp_spool=tmp_path / "spool")
    )
    app.seed_experiment("e1")
    run = probe.init(experiment="e1", name="reader")
    data.read_bytes()
    probe.finish()
    batches = app.__dict__.get("run_inputs", {}).get(run.id, [])
    paths = [row["path"] for batch in batches for row in batch["inputs"]]
    assert str(data) in paths
    assert batches[0]["coverage"]["recorder"] == inputs.RECORDER
    assert app.runs[run.id]["status"] == "completed"


def test_init_capture_reads_false_records_nothing(app, tmp_path, monkeypatch) -> None:
    monkeypatch.setattr(
        fluent, "Client", lambda *a, **k: make_client(app, tmp_spool=tmp_path / "spool")
    )
    app.seed_experiment("e1")
    run = probe.init(experiment="e1", name="quiet", capture_reads=False)
    _data_file(tmp_path, "x.bin", b"x" * 100).read_bytes()
    probe.finish()
    assert run.id not in app.__dict__.get("run_inputs", {})


def test_log_artifact_marks_what_the_run_wrote(app, tmp_path, monkeypatch) -> None:
    monkeypatch.setattr(
        fluent, "Client", lambda *a, **k: make_client(app, tmp_spool=tmp_path / "spool")
    )
    app.seed_experiment("e1")
    old = _data_file(tmp_path, "old.bin", b"o" * 100)
    past = time.time() - 3600
    os.utime(old, (past, past))
    run = probe.init(experiment="e1", name="writer", capture_reads=False)
    # The fake backend stamps every run with one fixed old time; a real server
    # stamps the start, which is what the rule compares against.
    from datetime import datetime
    from probe._compat import UTC

    run._data["started_at"] = datetime.now(UTC).isoformat()
    new = _data_file(tmp_path, "new.bin", b"n" * 100)
    assert run._write_marks(new)["written_during_run"] is True
    assert run._write_marks(old)["written_during_run"] is False
    assert run._write_marks(tmp_path / "missing") == {}
    probe.finish()


def test_the_sdk_says_when_it_derived_a_parent() -> None:
    from probe.sdk.client import Client

    body = Client._run_create_body(
        None,
        description=None,
        notes=None,
        source="api",
        external_id=None,
        parent_run_id="p",
        parent_relation="retry",
        group_id=None,
        config=None,
        tags=None,
        metadata=None,
        labeled_point_budget=None,
        parent_provenance="observed_call",
    )
    assert body["parent_provenance"] == "observed_call"
    declared = Client._run_create_body(
        None,
        description=None,
        notes=None,
        source="api",
        external_id=None,
        parent_run_id="p",
        parent_relation="retry",
        group_id=None,
        config=None,
        tags=None,
        metadata=None,
        labeled_point_budget=None,
    )
    assert "parent_provenance" not in declared


def test_probe_exec_sends_what_its_python_child_read(client, app, tmp_path) -> None:
    """The launcher side of `probe exec`: the child's hook spools, the launcher
    hashes and sends once the child exits."""
    from tests.conftest import open_run

    data = _data_file(tmp_path, "exec_input.bin", b"x" * 500)
    run = open_run(client, experiment="exp-reads")
    run.execute([sys.executable, "-c", f"open({str(data)!r}, 'rb').read()"], cwd=str(tmp_path))
    client.flush(run_ref=run.id)
    rows = [row for batch in app.run_inputs.get(run.id, []) for row in batch["inputs"]]
    assert [(r["path"], r["content_hash"]) for r in rows] == [(str(data), _sha(b"x" * 500))]
    assert not inputs.run_dir(run.id).exists()


def test_a_submitted_job_gets_no_hook(client, app, tmp_path) -> None:
    """finalize=False: the launcher only submitted the work, which reads on
    another machine where its own probe.init() records."""
    from tests.conftest import open_run

    out = tmp_path / "child_env.txt"
    run = open_run(client, experiment="exp-submit")
    code = f"import os; open({str(out)!r}, 'w').write(os.environ.get('PROBE_READS_DIR', ''))"
    run.execute([sys.executable, "-c", code], cwd=str(tmp_path), finalize=False)
    assert out.read_text() == ""
    assert not inputs.run_dir(run.id).exists()


# -- the typed sanitizer (plan (k)) ------------------------------------------------
#
# A read list reached the wire through the journal's generic `default_scrub`,
# which walked every key and value of every row several times: ~200k
# `scrub_string` calls and ~3.9 s at `finish()` for 10k reads (6.8 s on the
# plan's box). `collect()` now builds each row by type -- the path scrubbed
# once, hashes and times validated -- and the scrubber caches repeats.

PATH_TOKEN = "ghp_" + "A1b2C3d4E5f6G7h8I9j0K1l2M3n4O5p6Q7r8"


def _dead_run_spool(run_id: str, lines: list[str]) -> None:
    directory = inputs.run_dir(run_id)
    directory.mkdir(parents=True)
    dead = _dead_pid()
    (directory / "owner.json").write_text(
        json.dumps({"run_id": run_id, "pid": dead, "host": inputs._host()})
    )
    (directory / f"{inputs._host()}.{dead}.jsonl").write_text("".join(lines))


def _raw_line(path: str, i: int, t: str = "2026-09-26T00:00:00+00:00", s=100) -> str:
    return json.dumps({"p": path, "d": 1, "i": i, "s": s, "m": i, "c": i, "t": t}) + "\n"


def test_a_token_in_a_read_path_is_redacted_and_never_sent(tmp_path) -> None:
    _dead_run_spool("run-tok", [_raw_line(f"/data/{PATH_TOKEN}/train.bin", 1),
                                _raw_line("/home/someone/data/val.bin", 2)])
    rows, coverage = inputs.collect("run-tok", wait_s=0)
    paths = [r["path"] for r in rows]
    assert PATH_TOKEN not in json.dumps(rows)
    assert paths[0].startswith("/data/<redacted") and paths[0].endswith("/train.bin")
    # An ordinary home path is kept as it is: the server keys reads on it.
    assert paths[1] == "/home/someone/data/val.bin"
    client = _Client(True)
    assert inputs.send(client, "run-tok", rows, coverage)
    assert PATH_TOKEN not in json.dumps(client.journal.ops)


def test_only_well_formed_hashes_sizes_and_times_are_sent() -> None:
    good_sha, good_fp = "a" * 64, "5000:1727300000000000000:" + "b" * 64
    t = "2026-09-26T00:00:00.5+00:00"
    row = inputs._typed_row("/d/x", good_sha, good_fp, 5000, "h", True, t)
    assert (row["content_hash"], row["fingerprint"], row["size_bytes"]) == (good_sha, good_fp, 5000)
    assert row["first_seen_at"] == t
    for bad in ("A" * 64, "a" * 63, "g" * 64, "sha256:" + "a" * 64, 7, None, "password=hunter2"):
        assert inputs._typed_row("/d/x", bad, None, 1, "h", True, t)["content_hash"] is None
    for bad in ("1:2:" + "z" * 64, "x:2:" + "a" * 64, "token=" + "a" * 64):
        assert inputs._typed_row("/d/x", None, bad, 1, "h", True, t)["fingerprint"] is None
    for bad in (-1, True, "12", 1.5):
        assert inputs._typed_row("/d/x", None, None, bad, "h", True, t)["size_bytes"] is None
    # A timestamp this module did not write drops the row: never re-dated.
    for bad in ("yesterday api_key=abc", None, 1727300000, "2026-09-26 00:00:00"):
        assert inputs._typed_row("/d/x", None, None, 1, "h", True, bad) is None


def test_a_row_with_a_malformed_timestamp_is_dropped_and_counted(tmp_path) -> None:
    """(k) review LOW: a corrupt or edited spool line's timestamp used to be
    replaced with the collect time, recording a read at a moment it did not
    happen. Control: the well-formed line beside it is sent unchanged."""
    _dead_run_spool("run-badt", [_raw_line("/data/a.bin", 1, t="not a time"),
                                 _raw_line("/data/b.bin", 2)])
    rows, coverage = inputs.collect("run-badt", wait_s=0)
    assert [(r["path"], r["first_seen_at"]) for r in rows] == [("/data/b.bin", "2026-09-26T00:00:00+00:00")]
    assert coverage["malformed_rows"] == 1 and coverage["count"] == 1
    clean_rows, clean = inputs.collect("run-none-malformed", wait_s=0)
    assert "malformed_rows" not in clean


def test_collect_scrubs_each_row_once(tmp_path, monkeypatch) -> None:
    from probe.sdk import redaction

    n = 300
    _dead_run_spool("run-once", [_raw_line(f"/data/part-{i}.bin", i) for i in range(n)])
    calls: list[str] = []
    real = redaction.scrub_string
    monkeypatch.setattr(redaction, "scrub_string", lambda v, **k: calls.append(v) or real(v, **k))
    rows, _ = inputs.collect("run-once", wait_s=0)
    assert len(rows) == n
    assert len(calls) == n + 1, "one per row's path, plus the host once"


def test_ten_thousand_reads_collect_and_journal_quickly(tmp_path, monkeypatch) -> None:
    """The finish-time cost, through the REAL journal (whose own scrubs re-read
    every row): it was ~3.9 s here and 6.8 s on the plan's box.

    Realistic rows (the (k) review): every read has its own path, timestamp,
    content hash and fingerprint, as real spools and hashed files do. With one
    shared timestamp and no hashes the cache hid ~24k full scans (1.38-1.42 s
    against this limit). The count of UNCACHED scrubs is the deterministic
    check: one per row's path (and a few constants), not one per field. The
    time bound is CPU time, not wall time: the cost this guards is the scan,
    and on a shared box at load 20 the same run took 2.8 s of wall clock."""
    from probe.sdk import redaction
    from probe.sdk.journal import Journal

    monkeypatch.setenv("PROBE_OUTBOX_MIN_FREE_BYTES", "0")
    assert redaction.enable_scrub_cache(), "the SDK run path turns the cache on"
    n = 10_000
    _dead_run_spool(
        "run-10k",
        [
            _raw_line(
                f"/data/shards/part-{i // 100:03d}/train-{i}.parquet", i,
                t=f"2026-09-26T{i // 3600 % 24:02d}:{i // 60 % 60:02d}:{i % 60:02d}.{i:06d}+00:00",
                s=1000 + i,
            )
            for i in range(n)
        ],
    )

    def fake_hash(todo, budget, deadline, own, **_writes):
        # Every read hashed, as a real finish with small files would be,
        # without paying for 10k files on disk.
        for path, ident in todo:
            digest = hashlib.sha256(path.encode()).hexdigest()
            own[ident] = (digest, f"{1000 + len(own)}:{1727300000000000000 + len(own)}:{digest}")

    monkeypatch.setattr(inputs, "_hash_within", fake_hash)
    uncached = [0]
    real = redaction._scrub_string
    monkeypatch.setattr(redaction, "_scrub_string", lambda v, **k: (uncached.__setitem__(0, uncached[0] + 1), real(v, **k))[1])

    class _RealJournalClient:
        journal = Journal(tmp_path / "outbox", context={"base_url": "http://x"})

        def supports_feature(self, name: str) -> bool:
            return True

    started = time.process_time()
    rows, coverage = inputs.collect("run-10k", wait_s=0)
    assert inputs.send(_RealJournalClient(), "run-10k", rows, coverage)
    elapsed = time.process_time() - started
    assert len(rows) == n and all(r["content_hash"] and r["fingerprint"] for r in rows)
    assert len({r["first_seen_at"] for r in rows}) == n
    assert uncached[0] < n + 200, f"{uncached[0]} uncached scrubs for {n} rows"
    assert elapsed < 1.5, f"{elapsed:.2f}s of CPU for {n} reads"


# -- .probeignore (plan (n)) ------------------------------------------------------


def test_an_ignored_read_is_never_recorded_or_hashed(tmp_path, monkeypatch) -> None:
    from probe.sdk import ignore

    keep = _data_file(tmp_path, "train.bin", b"k" * 300)
    skip = _data_file(tmp_path, "cache/big.bin", b"s" * 300)
    rules = ignore.load(str(tmp_path / "work"), extra=["cache/"])
    hashed: list[str] = []
    real_hash = inputs.hash_file

    def spy(path, *a, **k):
        hashed.append(path)
        return real_hash(path, *a, **k)

    monkeypatch.setattr(inputs, "hash_file", spy)
    assert inputs.start("run-ign", ignore=rules)
    for path in (keep, skip):
        with open(path, "rb") as handle:
            handle.read()
    rows, coverage = inputs.collect("run-ign", wait_s=5)
    assert [r["path"] for r in rows] == [str(keep)]
    assert str(skip) not in hashed, "excluded before hashing"
    spooled = "".join(p.read_text() for p in inputs.run_dir("run-ign").glob("*.jsonl")) if inputs.run_dir("run-ign").exists() else ""
    assert str(skip) not in spooled, "never even spooled"


def test_collect_drops_ignored_child_reads_before_hashing(tmp_path, monkeypatch) -> None:
    """The `probe exec` child's hook is stdlib-only and spools every read; the
    launcher filters with the run's rules before it hashes anything."""
    from probe.sdk import ignore

    keep = _data_file(tmp_path, "val.bin", b"v" * 200)
    skip = _data_file(tmp_path, "scratch/tmp.bin", b"t" * 200)
    directory = inputs.run_dir("run-child")
    directory.mkdir(parents=True)
    (directory / f"{inputs._host()}.{_dead_pid()}.jsonl").write_text(_spool_line(keep) + _spool_line(skip))
    hashed: list[str] = []
    real_hash = inputs.hash_file
    monkeypatch.setattr(inputs, "hash_file", lambda p, *a, **k: (hashed.append(p), real_hash(p, *a, **k))[1])
    rules = ignore.load(str(tmp_path / "work"), extra=["scratch/"])
    rows, coverage = inputs.collect("run-child", wait_s=5, ignore=rules)
    assert [r["path"] for r in rows] == [str(keep)]
    assert str(skip) not in hashed
    assert coverage["probeignore"] == 1


@pytest.mark.parametrize("with_rules", [True, False])
def test_a_recovered_childs_reads_honour_the_runs_rules(tmp_path, with_rules) -> None:
    """A Ctrl-C'd `probe exec` (or a launcher that died) never collects its
    child's spool, and the child's stdlib hook spooled every read: the next run
    on this host sends it. The rules ride in `owner.json`, so that send drops
    what the run's own close would have dropped. Control: no rules, both go."""
    from probe.sdk import ignore

    keep = _data_file(tmp_path, "val.bin", b"v" * 200)
    skip = _data_file(tmp_path, "scratch/tmp.bin", b"t" * 200)
    rules = ignore.load(str(tmp_path / "work"), extra=["scratch/"]) if with_rules else None
    env: dict[str, str] = {}
    assert inputs.prepare_child("run-orph", env, ignore=rules)
    directory = inputs.run_dir("run-orph")
    (directory / f"{inputs._host()}.{_dead_pid()}.jsonl").write_text(_spool_line(keep) + _spool_line(skip))
    inputs.abandon("run-orph")  # what an interrupted launcher does
    client = _Client(True)
    assert inputs.recover_orphans(client, now=time.time() + 3600) == 1
    body = client.journal.ops[0][2]
    sent = sorted(row["path"] for row in body["inputs"])
    if with_rules:
        assert sent == [str(keep)]
        assert body["coverage"]["probeignore"] == 1 and body["coverage"]["recovered"] is True
    else:
        assert sent == sorted([str(keep), str(skip)]) and "probeignore" not in body["coverage"]


def test_no_rules_changes_nothing(tmp_path) -> None:
    keep = _data_file(tmp_path, "a.bin", b"a" * 10)
    assert inputs.start("run-none")
    with open(keep, "rb") as handle:
        handle.read()
    rows, coverage = inputs.collect("run-none", wait_s=5)
    assert [r["path"] for r in rows] == [str(keep)] and "probeignore" not in coverage


def test_probe_exec_exports_the_ignore_file_and_filters_the_childs_reads(client, app, tmp_path) -> None:
    from tests.conftest import open_run

    work = tmp_path / "work"
    keep = _data_file(tmp_path, "input.bin", b"i" * 100)
    skip = _data_file(tmp_path, "ckpt/model.bin", b"m" * 100)
    (work / ".probeignore").write_text("ckpt/\n")
    seen = tmp_path / "child_env.txt"
    code = (
        "import os\n"
        f"open({str(keep)!r}, 'rb').read(); open({str(skip)!r}, 'rb').read()\n"
        f"open({str(seen)!r}, 'w').write(os.environ.get('PROBE_IGNORE_FILE', '') + '|' + os.environ.get('PROBE_IGNORE_EXPORTED', ''))\n"
    )
    run = open_run(client, experiment="exp-ign-exec")
    run._set_ignore(["*.never", "a,b.bin"])
    run.execute([sys.executable, "-c", code], cwd=str(work))
    client.flush(run_ref=run.id)
    rows = [row for batch in app.run_inputs.get(run.id, []) for row in batch["inputs"]]
    assert [r["path"] for r in rows] == [str(keep)]
    exported_file, exported_patterns = seen.read_text().split("|")
    assert exported_file == str(work / ".probeignore")
    # One per line in their own variable: the comma survives (review LOW-7).
    assert exported_patterns == "*.never\na,b.bin"


def test_a_negated_read_under_an_excluded_folder_stays_out(tmp_path) -> None:
    """#2045 review LOW-5: `drafts/` then `!drafts/notes.md` sent notes.md's
    path and hash; as in git, a file under an excluded folder stays out. (Not
    `secrets/`: read capture never records a credential folder at all.)"""
    from probe.sdk import ignore

    work = tmp_path / "work"
    keep = _data_file(tmp_path, "train.bin", b"k" * 100)
    notes = _data_file(tmp_path, "drafts/notes.md", b"n" * 100)
    (work / ".probeignore").write_text("drafts/\n!drafts/notes.md\n")
    assert inputs.start("run-neg", ignore=ignore.load(str(work)))
    for path in (keep, notes):
        with open(path, "rb") as handle:
            handle.read()
    rows, _ = inputs.collect("run-neg", wait_s=5)
    assert [r["path"] for r in rows] == [str(keep)]


def test_a_read_outside_the_root_meets_the_unanchored_patterns(tmp_path) -> None:
    """#2045 review MED-1: a checkpoint read from $SCRATCH is out of the repo;
    `*.ckpt` still applies there, an anchored `/data` cannot."""
    from probe.sdk import ignore

    work = tmp_path / "work"
    work.mkdir()
    (work / ".probeignore").write_text("*.ckpt\n/data\n")
    far = tmp_path / "scratch"
    far.mkdir()
    ckpt = far / "model.ckpt"
    ckpt.write_bytes(b"w" * 100)
    (far / "data").mkdir()
    shard = far / "data" / "shard.bin"
    shard.write_bytes(b"s" * 100)
    assert inputs.start("run-far", ignore=ignore.load(str(work)))
    for path in (ckpt, shard):
        with open(path, "rb") as handle:
            handle.read()
    rows, _ = inputs.collect("run-far", wait_s=5)
    assert [r["path"] for r in rows] == [str(shard)]


# -- the #2045 re-review ------------------------------------------------------------


@pytest.mark.parametrize("handed", [True, False])
def test_an_exec_childs_own_ignore_reaches_the_launchers_collect(tmp_path, handed) -> None:
    """MED: `probe.init(ignore=[...])` in a `probe exec` child did nothing for
    reads -- the launcher collected the child's spool with ITS rules (none
    here) and sent every `.ckpt` with its hash. The child now hands its rules
    over in its spool, and from then on its hook skips what they exclude, a
    forked worker's too. Control: nothing handed, everything is sent."""
    work = tmp_path / "work"
    early = _data_file(tmp_path, "early.ckpt", b"e" * 100)
    late = _data_file(tmp_path, "late.ckpt", b"l" * 100)
    forked = _data_file(tmp_path, "forked.ckpt", b"f" * 100)
    keep = _data_file(tmp_path, "keep.csv", b"k" * 100)
    env = {**os.environ}
    assert inputs.prepare_child("run-hand", env)
    hand = (
        "from probe.sdk import ignore, inputs\n"
        "assert inputs.hand_to_launcher('run-hand', ignore.load(os.getcwd(), extra=['*.ckpt']))\n"
        if handed
        else ""
    )
    code = (
        f"import os\nopen({str(early)!r}, 'rb').read()\n"
        + hand
        + f"open({str(late)!r}, 'rb').read(); open({str(keep)!r}, 'rb').read()\n"
        "pid = os.fork()\n"
        f"if pid == 0:\n    open({str(forked)!r}, 'rb').read()\n    os._exit(0)\n"
        "os.waitpid(pid, 0)\n"
    )
    subprocess.run([sys.executable, "-c", code], env=env, cwd=str(work), check=True)
    spooled = "".join(p.read_text() for p in inputs.run_dir("run-hand").glob("*.jsonl"))
    rows, coverage = inputs.collect("run-hand", wait_s=5)
    sent = sorted(r["path"] for r in rows)
    if handed:
        assert sent == [str(keep)]
        assert str(late) not in spooled and str(forked) not in spooled, "the hook skipped them"
        assert str(early) in spooled, "spooled before the rules arrived..."
        assert coverage["probeignore"] == 1, "...and dropped by the launcher's collect"
    else:
        assert sent == sorted(map(str, (early, late, forked, keep)))
        assert "probeignore" not in coverage


def test_rules_are_handed_only_into_the_runs_own_spool(tmp_path, monkeypatch) -> None:
    from probe.sdk import ignore

    rules = ignore.load(str(tmp_path), extra=["*.ckpt"])
    monkeypatch.delenv(inputs.CHILD_DIR_ENV, raising=False)
    assert not inputs.hand_to_launcher("run-a", rules), "no launcher hook: nothing to hand"
    monkeypatch.setenv(inputs.CHILD_DIR_ENV, str(inputs.run_dir("run-b")))
    assert not inputs.hand_to_launcher("run-a", rules), "another run's spool"
    assert not inputs.hand_to_launcher("run-b", None)


def test_a_read_through_a_symlink_is_matched_both_ways(tmp_path) -> None:
    """LOW: `data/` excluded + `datalink -> data` recorded `datalink/rows.csv`;
    `bigdata/` excluded + `bigdata -> <elsewhere>` recorded a read of the
    resolved path. Control: a read nothing names is still recorded."""
    from probe.sdk import ignore

    work = tmp_path / "work"
    _data_file(tmp_path, "data/rows.csv", b"r" * 100)
    (work / "datalink").symlink_to("data", target_is_directory=True)
    ext = tmp_path / "elsewhere"
    ext.mkdir()
    shard = ext / "shard.bin"
    shard.write_bytes(b"s" * 100)
    (work / "bigdata").symlink_to(ext, target_is_directory=True)
    keep = _data_file(tmp_path, "keep.bin", b"k" * 100)
    (work / ".probeignore").write_text("data/\nbigdata/\n")
    assert inputs.start("run-links", ignore=ignore.load(str(work)))
    for path in (work / "datalink" / "rows.csv", shard, work / "bigdata" / "shard.bin", keep):
        with open(path, "rb") as handle:
            handle.read()
    rows, _ = inputs.collect("run-links", wait_s=5)
    assert [r["path"] for r in rows] == [str(keep)]


def test_a_handed_rule_line_past_the_read_cap_still_counts(tmp_path, monkeypatch) -> None:
    from probe.sdk import ignore

    a = _data_file(tmp_path, "a.bin", b"a" * 10)
    b = _data_file(tmp_path, "b.bin", b"b" * 10)
    rules = ignore.load(str(tmp_path), extra=["*.ckpt"])
    spool = tmp_path / "x.1.jsonl"
    spool.write_text(_spool_line(a) + _spool_line(b) + json.dumps({"ignore": ignore.to_record(rules)}) + "\n")
    monkeypatch.setattr(inputs, "MAX_PATHS", 1)
    handed: list = []
    observed, truncated = inputs._read_spools([spool], handed)
    assert len(observed) == 1 and truncated is True
    assert handed == [rules]
