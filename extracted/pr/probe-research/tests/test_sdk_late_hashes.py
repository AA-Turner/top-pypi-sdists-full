"""Hashes that arrive late, under one observation id (lineage plan 3, F7).

A close that runs out of time sends reads unhashed, and an unhashed read never
matches. Server 0290 keys a read on (run, path, host, observation_id), so a
LATER report of the same observation with its hash replaces the unhashed row.
These tests pin the SDK half: every read row carries a derived observation id
(only to a server that understands it); the owner's hasher tails its workers'
spools during the run so fewer reads are left for the close; and what the
close ran out of time for is kept, hashed by the next process (or the next
run of this one) and re-sent under the same id, with no coverage -- and never
with bytes the file got since.
"""

from __future__ import annotations

import hashlib
import json
import os
import queue
import threading
import time
from pathlib import Path

import pytest

from probe.sdk import fluent, inputs
from tests.conftest import run_outputs_problems


@pytest.fixture(autouse=True)
def _recorder(monkeypatch, tmp_path):
    monkeypatch.setenv(inputs.READS_ENV, "1")
    for name in (inputs.CHILD_DIR_ENV, inputs.OWNER_PID_ENV, inputs.BIND_ENV, inputs.WRITES_ENV,
                 inputs.OUTPUTS_ENV, "PROBE_RUN_ID"):
        monkeypatch.delenv(name, raising=False)
    monkeypatch.setenv("XDG_STATE_HOME", str(tmp_path / "state"))
    monkeypatch.setenv("PROBE_OUTBOX_DIR", str(tmp_path / "outbox"))
    inputs._active.clear()
    inputs._hash_results.clear()
    fluent._current.set(None)
    fluent._process_default = None
    yield
    inputs._active.clear()


class _Journal:
    def __init__(self) -> None:
        self.ops: list[tuple] = []

    def append_http(self, method, path, body, *, run_ref=None, blocking=True, **_):
        self.ops.append((method, path, body, run_ref, blocking))
        return "op"


class _Client:
    def __init__(self, *features: str) -> None:
        self.features = set(features)
        self.journal = _Journal()

    def supports_feature(self, name: str) -> bool:
        return name in self.features


BOTH = (inputs.FEATURE, inputs.OUTPUTS_FEATURE)


def _sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _file(tmp_path: Path, name: str, data: bytes) -> Path:
    path = tmp_path / "work" / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)
    return path


class _Unhashed(queue.Queue):
    """The background hasher never gets the reads: the close is left to
    hash them, and has no time to."""

    def put(self, item, block=True, timeout=None):  # noqa: ARG002
        return None


def _bodies(client: _Client, route: str) -> list[dict]:
    return [op[2] for op in client.journal.ops if op[1].endswith("/" + route)]


# -- the observation id ----------------------------------------------------------


def test_each_read_carries_a_derived_observation_id(tmp_path) -> None:
    data = _file(tmp_path, "train.bin", b"t" * 300)
    assert inputs.start("run-obs")
    data.read_bytes()
    (row,) = inputs.collect_all("run-obs", wait_s=5).inputs
    ident = inputs._ident(os.stat(data))
    assert row["observation_id"] == inputs._read_observation("run-obs", row["host"], str(data), ident)
    assert len(row["observation_id"]) == 32 and int(row["observation_id"], 16) >= 0
    # The same read, recorded again (a replay, a recovery): the same id.
    assert inputs.start("run-obs")
    data.read_bytes()
    (again,) = inputs.collect_all("run-obs", wait_s=5).inputs
    assert again["observation_id"] == row["observation_id"]
    # Another version of the file is another observation.
    data.write_bytes(b"u" * 300)
    assert inputs._read_observation("run-obs", row["host"], str(data), inputs._ident(os.stat(data))) != row[
        "observation_id"
    ]


@pytest.mark.parametrize(("features", "carried"), [(BOTH, True), ((inputs.FEATURE,), False)])
def test_the_id_goes_only_to_a_server_that_keys_on_it(tmp_path, features, carried) -> None:
    """An older server ignores the field but would keep a late hash as a
    second row: it gets neither the id nor a late re-send."""
    data = _file(tmp_path, "keyed.bin", b"k" * 300)
    assert inputs.start("run-keyed")
    data.read_bytes()
    client = _Client(*features)
    inputs.finalize(client, "run-keyed", wait_s=5)
    (body,) = _bodies(client, "inputs")
    assert ("observation_id" in body["inputs"][0]) is carried


def test_a_host_too_long_to_key_on_sends_no_id() -> None:
    row = inputs._typed_row("/d/x", None, None, 1, "h" * 300, True, "2026-09-28T00:00:00+00:00", "a" * 32)
    assert row is not None and "observation_id" not in row
    row = inputs._typed_row("/d/x", None, None, 1, "host", True, "2026-09-28T00:00:00+00:00", "not-hex")
    assert row is not None and "observation_id" not in row


def test_an_observed_read_row_is_lifted_past_the_journal_scrubber() -> None:
    from probe.sdk import stamp_scrub

    row = inputs._typed_row("/d/x", "a" * 64, None, 1, "host", True, "2026-09-28T00:00:00+00:00", "b" * 32)
    fields = stamp_scrub._checked_fields(row)
    assert fields is not None and fields[-1] == "b" * 32
    assert stamp_scrub._restore_reads([{"path": "/d/x", "host": "host"}], [fields]) == [row]


# -- the hasher tails its workers ----------------------------------------------------


def _worker_spool(run_id: str, owner: int, data: Path) -> Path:
    """A live worker's spool (pid: this process's parent, alive and not this
    one) with one read, its header naming ``owner``."""
    st = os.stat(data)
    spool = inputs.run_dir(run_id) / f"{inputs._host()}.{os.getppid()}.jsonl"
    line = {"p": str(data), "d": st.st_dev, "i": st.st_ino, "s": st.st_size, "m": st.st_mtime_ns,
            "c": st.st_ctime_ns, "t": "2026-09-28T00:00:00+00:00"}
    spool.write_text(json.dumps({"run": run_id, "owner": owner}) + "\n" + json.dumps(line) + "\n")
    return spool


def test_the_hasher_tails_its_workers_spools_during_the_run(tmp_path, monkeypatch) -> None:
    """A worker's reads used to be hashed only at the close, whatever time it
    had. The owner's hasher now reads its workers' spools as they grow."""
    monkeypatch.setattr(inputs, "TAIL_S", 0.05)
    monkeypatch.setattr(inputs, "_hash_queue", queue.Queue())
    mine = _file(tmp_path, "worker_read.bin", b"w" * 500)
    theirs = _file(tmp_path, "rank_read.bin", b"r" * 500)
    assert inputs.start("run-tail")
    _worker_spool("run-tail", os.getpid(), mine)
    rank_run = "run-tail-rank"
    assert inputs.start(rank_run)
    _worker_spool(rank_run, os.getppid(), theirs)  # a rank's: its header names itself
    loop = threading.Thread(target=inputs._hash_loop, daemon=True)
    loop.start()
    ident = inputs._ident(os.stat(mine))
    deadline = time.monotonic() + 5
    while ident not in inputs._hash_results and time.monotonic() < deadline:
        time.sleep(0.02)
    for _ in range(2):
        inputs._hash_queue.put(None)
    loop.join(5)
    assert inputs._hash_results.get(ident, (None,))[0] == _sha(b"w" * 500)
    assert inputs._ident(os.stat(theirs)) not in inputs._hash_results, "a rank hashes its own"
    inputs.abandon("run-tail")
    inputs.abandon(rank_run)


# -- late hashes ---------------------------------------------------------------------


def _close_out_of_time(run_id: str, tmp_path: Path, monkeypatch, *, features=BOTH) -> tuple[Path, Path, _Client]:
    monkeypatch.setattr(inputs, "_hash_queue", _Unhashed())
    read = _file(tmp_path, "slow_read.bin", b"s" * 400)
    wrote = tmp_path / "work" / "slow_write.bin"
    assert inputs.start(run_id)
    read.read_bytes()
    wrote.write_bytes(b"o" * 400)
    client = _Client(*features)
    with monkeypatch.context() as close:
        # The close looks at its writes, then its time is up before any hash.
        close.setattr(inputs, "_hash_within", lambda todo, budget, deadline, own, **k: None)
        inputs.finalize(client, run_id, wait_s=5)
    return read, wrote, client


def test_what_the_close_had_no_time_for_is_re_sent_hashed_under_the_same_id(tmp_path, monkeypatch) -> None:
    read, wrote, first = _close_out_of_time("run-late", tmp_path, monkeypatch)
    (in_body,) = _bodies(first, "inputs")
    (out_body,) = _bodies(first, "outputs")
    (unhashed,) = in_body["inputs"]
    (unhashed_out,) = out_body["outputs"]
    assert unhashed["content_hash"] is None and unhashed_out["content_hash"] == ""
    assert in_body["coverage"]["hash_cut"] == {inputs.CUT_DEADLINE: 1}
    assert inputs._late_files(inputs.run_dir("run-late")), "kept for later"
    later = _Client(*BOTH)
    assert inputs.recover_orphans(later, late_only=True) == 1
    (again,) = _bodies(later, "inputs")
    (again_out,) = _bodies(later, "outputs")
    assert "coverage" not in again and "coverage" not in again_out, "the run's own coverage stays"
    (hashed,) = again["inputs"]
    assert hashed["observation_id"] == unhashed["observation_id"]
    assert hashed["content_hash"] == _sha(b"s" * 400)
    assert {k: v for k, v in hashed.items() if k not in ("content_hash", "fingerprint")} == {
        k: v for k, v in unhashed.items() if k not in ("content_hash", "fingerprint")
    }
    (hashed_out,) = again_out["outputs"]
    assert hashed_out["observation_id"] == unhashed_out["observation_id"]
    assert hashed_out["content_hash"] == _sha(b"o" * 400)
    assert hashed_out["last_modified_at"] == unhashed_out["last_modified_at"]
    assert run_outputs_problems(again_out) == []
    assert not inputs._late_files(inputs.run_dir("run-late")), "tried once, then gone"
    assert inputs.recover_orphans(_Client(*BOTH), late_only=True) == 0


def test_a_file_changed_since_is_never_re_sent_with_its_new_bytes(tmp_path, monkeypatch) -> None:
    read, wrote, _ = _close_out_of_time("run-late-changed", tmp_path, monkeypatch)
    time.sleep(0.01)
    read.write_bytes(b"another run's bytes")
    wrote.write_bytes(b"rewritten since")
    later = _Client(*BOTH)
    assert inputs.recover_orphans(later, late_only=True) == 0
    assert later.journal.ops == []
    assert not inputs._late_files(inputs.run_dir("run-late-changed"))


def test_no_late_hashes_for_a_server_that_does_not_key_on_the_id(tmp_path, monkeypatch) -> None:
    _close_out_of_time("run-late-old", tmp_path, monkeypatch, features=(inputs.FEATURE,))
    assert not inputs._late_files(inputs.run_dir("run-late-old"))


def test_a_late_file_for_a_server_that_stopped_keying_on_the_id_is_dropped(tmp_path, monkeypatch) -> None:
    _close_out_of_time("run-late-drop", tmp_path, monkeypatch)
    old = _Client(inputs.FEATURE)
    inputs.recover_orphans(old, late_only=True)
    assert old.journal.ops == [] and not inputs._late_files(inputs.run_dir("run-late-drop"))


def test_what_the_budget_cut_is_not_retried(tmp_path, monkeypatch) -> None:
    """The run's budget said no: a later process does not spend another."""
    monkeypatch.setattr(inputs, "_hash_queue", _Unhashed())
    monkeypatch.setattr(inputs, "RUN_HASH_BUDGET_BYTES", 10)
    data = _file(tmp_path, "big.bin", b"b" * 400)
    assert inputs.start("run-late-budget")
    data.read_bytes()
    client = _Client(*BOTH)
    inputs.finalize(client, "run-late-budget", wait_s=5)
    (body,) = _bodies(client, "inputs")
    assert body["coverage"]["hash_cut"] == {inputs.CUT_BUDGET: 1}
    assert not inputs._late_files(inputs.run_dir("run-late-budget"))


def test_each_later_run_of_a_process_re_sends_the_late_hashes(monkeypatch) -> None:
    """The first run a process opens recovers everything; each later one (a
    sweep's runs close within a short budget) re-sends the late hashes."""
    calls: list[dict] = []
    monkeypatch.setattr(inputs, "recover_orphans", lambda client, **k: calls.append(k))
    monkeypatch.setattr(inputs, "_recovery_started", False)
    for _ in range(2):
        inputs.start_recovery(object())
    deadline = time.monotonic() + 5
    while len(calls) < 2 and time.monotonic() < deadline:
        time.sleep(0.01)
    assert sorted(c["late_only"] for c in calls) == [False, True]


def test_the_run_folder_is_kept_while_late_hashes_wait(tmp_path, monkeypatch) -> None:
    _close_out_of_time("run-late-keep", tmp_path, monkeypatch)
    directory = inputs.run_dir("run-late-keep")
    assert (directory / "owner.json").exists(), "which server and credential they are for"
    assert not list(directory.glob("*.jsonl")), "the spools themselves were sent"


def test_an_offline_runs_late_hashes_go_into_its_queue(tmp_path, monkeypatch) -> None:
    """`probe sync` (`recover_offline`) queues them before it delivers."""
    from probe.sdk.journal import Journal

    queue_dir = tmp_path / "offline-queue"
    Journal(queue_dir)._ensure()
    run_id = "local:late"
    monkeypatch.setattr(inputs, "_hash_queue", _Unhashed())
    data = _file(tmp_path, "offline_read.bin", b"f" * 300)
    assert inputs.start(run_id, offline_dir=queue_dir)
    data.read_bytes()
    with monkeypatch.context() as close:
        close.setattr(inputs, "_hash_within", lambda todo, budget, deadline, own, **k: None)
        inputs.finalize(inputs._OfflineQueue(str(queue_dir)), run_id, wait_s=5)
    queued = [op for _, op in Journal(queue_dir).pending()]
    (first,) = [op for op in queued if op["path"].endswith("/inputs")]
    assert first["body"]["inputs"][0]["content_hash"] is None
    assert inputs.recover_offline(run_id, queue_dir) is True
    again = [op for _, op in Journal(queue_dir).pending() if op["path"].endswith("/inputs")][1:]
    (row,) = again[0]["body"]["inputs"]
    assert row["content_hash"] == _sha(b"f" * 300)
    assert row["observation_id"] == first["body"]["inputs"][0]["observation_id"]


def test_a_late_read_is_re_sent_only_with_a_full_hash(tmp_path, monkeypatch) -> None:
    """The server takes a report WITHOUT a hash under an id it knows as a
    retry: it widens the first sighting and keeps nothing else (gaps-server
    4562ad828). A read whose late look gets only a fingerprint (over the full
    -hash size) is therefore not re-sent; a write's is (its merge keeps a
    fingerprint at the same modification time)."""
    monkeypatch.setattr(inputs, "FULL_HASH_MAX_BYTES", 100)
    read, wrote, _ = _close_out_of_time("run-late-fp", tmp_path, monkeypatch)
    later = _Client(*BOTH)
    assert inputs.recover_orphans(later, late_only=True) == 1
    assert _bodies(later, "inputs") == [], "a fingerprint alone would not reach the read's row"
    (out,) = _bodies(later, "outputs")
    assert out["outputs"][0]["fingerprint"] and out["outputs"][0]["content_hash"] == ""
