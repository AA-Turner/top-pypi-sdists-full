"""Row counts from the hashing read, the per-machine cache table `h3`, and the
64-byte floor for `.probe.config` `hash` paths (data catalog C9: F30, F38,
V10, R27)."""

from __future__ import annotations

import hashlib
import os
import sqlite3
import sys
from pathlib import Path

import pytest

from probe.sdk import exclusions, fluent, inputs, probe_config as pc


@pytest.fixture(autouse=True)
def _recorder(monkeypatch, tmp_path):
    monkeypatch.setenv(inputs.READS_ENV, "1")
    monkeypatch.delenv(inputs.CHILD_DIR_ENV, raising=False)
    for name in ("PROBE_RUN_ID", "PROBE_RUN_EPOCH", "CLAUDE_CODE_SESSION_ID", "CODEX_THREAD_ID"):
        monkeypatch.delenv(name, raising=False)
    monkeypatch.setenv("XDG_STATE_HOME", str(tmp_path / "state"))
    monkeypatch.setenv("HOME", str(tmp_path / "home"))
    inputs._active.clear()
    inputs._hash_results.clear()
    fluent._current.set(None)
    fluent._process_default = None
    pc._CACHE.clear()
    pc._CHECKED.clear()
    exclusions._view_at = -1.0e9
    yield
    inputs._active.clear()
    inputs._hash_results.clear()
    pc._CACHE.clear()
    pc._CHECKED.clear()


def _file(tmp_path: Path, name: str, data: bytes) -> Path:
    path = tmp_path / "work" / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)
    return path


def _hash(path: Path, *, cache=None, budget=None):
    return inputs.hash_file(str(path), inputs._ident(os.stat(path)), cache=cache, budget=budget or [1 << 40])


# -- C9e: counted in the same read ------------------------------------------------


@pytest.mark.parametrize(
    "name, data, rows",
    [
        ("a.jsonl", b'{"x": 1}\n{"x": 2}\n{"x": 3}\n', 3),
        ("b.jsonl", b'{"x": 1}\n{"x": 2}', 2),  # a final unterminated line counts
        ("c.ndjson", b"{}\n" * 7, 7),
        ("d.csv", b"id,label\n1,a\n2,b\n", 2),  # the header is not a row
        ("e.tsv", b"id\tlabel\n1\ta", 1),
        ("f.txt", b"one\ntwo\n\nfour\n", 4),
        ("g.csv", b"id,label\n", 0),
        ("h.jsonl", b"", 0),
        ("i.bin", b"\n" * 10, None),  # not a line format
        ("J.JSONL", b"{}\n{}\n", 2),
    ],
)
def test_rows_are_counted_in_the_hashing_read(tmp_path, name, data, rows):
    path = _file(tmp_path, name, data)
    sha, fp, counted = _hash(path)
    assert sha == hashlib.sha256(data).hexdigest() and fp is None
    assert counted == rows


def test_rows_span_read_chunks(tmp_path, monkeypatch):
    monkeypatch.setattr(inputs, "_CHUNK", 7)
    data = b"".join(b"row-%d\n" % i for i in range(50)) + b"last"
    assert _hash(_file(tmp_path, "big.txt", data))[2] == 51


def test_a_fingerprinted_file_has_no_row_count(tmp_path, monkeypatch):
    monkeypatch.setattr(inputs, "FULL_HASH_MAX_BYTES", 100)
    sha, fp, rows = _hash(_file(tmp_path, "huge.jsonl", b'{"x": 1}\n' * 50))
    assert sha is None and fp is not None and rows is None


def test_a_file_past_the_budget_has_no_row_count(tmp_path, monkeypatch):
    monkeypatch.setattr(inputs, "EDGE_BYTES", 10)
    sha, fp, rows = _hash(_file(tmp_path, "over.jsonl", b"{}\n" * 200), budget=[50])
    assert sha is None and fp is not None and rows is None


def test_parquet_rows_come_from_the_footer_only_when_pyarrow_is_imported(tmp_path, monkeypatch):
    pa = pytest.importorskip("pyarrow")
    pq = pytest.importorskip("pyarrow.parquet")
    path = tmp_path / "work" / "t.parquet"
    path.parent.mkdir(parents=True)
    with inputs.internal():
        pq.write_table(pa.table({"x": list(range(42))}), str(path))
    assert _hash(path)[2] == 42
    # A fingerprinted parquet still has its footer count (a small extra read).
    monkeypatch.setattr(inputs, "FULL_HASH_MAX_BYTES", 10)
    assert _hash(path)[2] == 42
    monkeypatch.setattr(inputs, "FULL_HASH_MAX_BYTES", 1 << 30)
    # Never an import: with pyarrow not loaded, no count.
    monkeypatch.delitem(sys.modules, "pyarrow")
    assert _hash(path)[2] is None


# -- C9e2: the cache keeps rows (h3), an h2 answer is re-hashed once ------------------


def test_an_h3_hit_keeps_its_rows_without_reading_the_file(tmp_path, monkeypatch):
    path = _file(tmp_path, "cached.jsonl", b"{}\n" * 9)
    first = _hash(path, cache=inputs._HashCache())
    assert first[2] == 9
    opened = []
    real_open = open
    monkeypatch.setattr("builtins.open", lambda *a, **k: opened.append(a) or real_open(*a, **k))
    assert _hash(path, cache=inputs._HashCache()) == first
    assert not any(str(path) in str(a[0]) for a in opened)


def test_an_old_h2_answer_is_re_hashed_once_for_its_rows(tmp_path, monkeypatch):
    data = b"a\nb\nc\n"
    path = _file(tmp_path, "old.txt", data)
    ident = inputs._ident(os.stat(path))
    cache = inputs._HashCache()
    # What a release before row counts left: the hash, in h2, no rows.
    with sqlite3.connect(str(inputs.state_dir().parent / "hashcache.sqlite3")) as db:
        db.execute("INSERT INTO h2 (d, i, s, m, c, sha, fp) VALUES (?, ?, ?, ?, ?, ?, NULL)",
                   (*ident, hashlib.sha256(data).hexdigest()))
    read: list[str] = []
    real_open = open

    def spy(*a, **k):
        if str(a[0]) == str(path):
            read.append(str(a[0]))
        return real_open(*a, **k)

    monkeypatch.setattr("builtins.open", spy)
    assert inputs.hash_file(str(path), ident, cache=cache, budget=[1 << 40]) == (
        hashlib.sha256(data).hexdigest(), None, 3,
    )
    assert inputs.hash_file(str(path), ident, cache=inputs._HashCache(), budget=[1 << 40])[2] == 3
    assert len(read) == 1, "re-hashed once, then answered from h3"


def test_an_old_h2_answer_past_the_budget_comes_back_without_rows(tmp_path):
    data = b"a\nb\n"
    path = _file(tmp_path, "old2.txt", data)
    ident = inputs._ident(os.stat(path))
    cache = inputs._HashCache()
    with sqlite3.connect(str(inputs.state_dir().parent / "hashcache.sqlite3")) as db:
        db.execute("INSERT INTO h2 (d, i, s, m, c, sha, fp) VALUES (?, ?, ?, ?, ?, ?, NULL)",
                   (*ident, "f" * 64))
    budget = [1]
    assert inputs.hash_file(str(path), ident, cache=cache, budget=budget) == ("f" * 64, None, None)
    assert budget == [1]


def test_an_old_h2_answer_for_an_uncounted_file_moves_without_a_read(tmp_path, monkeypatch):
    path = _file(tmp_path, "weights.bin", b"w" * 100)
    ident = inputs._ident(os.stat(path))
    cache = inputs._HashCache()
    with sqlite3.connect(str(inputs.state_dir().parent / "hashcache.sqlite3")) as db:
        db.execute("INSERT INTO h2 (d, i, s, m, c, sha, fp) VALUES (?, ?, ?, ?, ?, ?, NULL)", (*ident, "e" * 64))
    budget = [0]
    assert inputs.hash_file(str(path), ident, cache=cache, budget=budget) == ("e" * 64, None, None)
    assert cache.get(ident) == ("e" * 64, None, None)


# -- rows on the wire --------------------------------------------------------------------


def test_rows_ride_read_and_write_rows_and_are_left_out_when_unknown():
    seen = "2026-10-13T00:00:00+00:00"
    with_rows = inputs._typed_row("/d/a.jsonl", "a" * 64, None, 10, "h", True, seen, rows=3)
    without = inputs._typed_row("/d/a.bin", "a" * 64, None, 10, "h", True, seen)
    assert with_rows["rows"] == 3 and "rows" not in without
    out = inputs._typed_output_row("/d/b.jsonl", "b" * 64, None, 10, "h", seen, seen, "c" * 32, rows=0)
    assert out["rows"] == 0
    assert "rows" not in inputs._typed_output_row("/d/b", "b" * 64, None, 10, "h", seen, seen, "c" * 32, rows=-1)


def test_a_run_sends_rows_for_what_it_read(tmp_path):
    data = b'{"x": 1}\n' * 12
    path = _file(tmp_path, "train.jsonl", data)
    assert inputs.start("run-rows")
    path.read_bytes()
    rows, _coverage = inputs.collect("run-rows", wait_s=5)
    assert rows[0]["content_hash"] == hashlib.sha256(data).hexdigest() and rows[0]["rows"] == 12


# -- C9d: the 64-byte floor at `hash` ------------------------------------------------------


@pytest.fixture
def hashed(tmp_path):
    folder = tmp_path / "work" / "labels"
    folder.mkdir(parents=True)
    (tmp_path / "work" / pc.CONFIG_NAME).write_text("labels/ @probe hash\n")
    return folder


def test_a_tiny_hash_file_is_sent_with_path_and_size_only(tmp_path, hashed):
    tiny = hashed / "label.txt"
    tiny.write_bytes(b"positive\n")
    big = hashed / "rows.jsonl"
    big.write_bytes(b'{"text": "a long enough record"}\n' * 4)
    plain = _file(tmp_path, "plain.txt", b"x\n")
    assert inputs.start("run-floor")
    for p in (tiny, big, plain):
        p.read_bytes()
    rows, coverage = inputs.collect("run-floor", wait_s=5)
    by_name = {Path(r["path"]).name: r for r in rows}
    assert by_name["label.txt"]["content_hash"] is None and by_name["label.txt"]["fingerprint"] is None
    assert by_name["label.txt"]["size_bytes"] == 9 and by_name["label.txt"]["stable"] is True
    assert "rows" not in by_name["label.txt"]
    assert by_name["rows.jsonl"]["content_hash"] == hashlib.sha256(big.read_bytes()).hexdigest()
    assert by_name["rows.jsonl"]["rows"] == 4
    assert by_name["plain.txt"]["content_hash"] is not None  # not `hash`: no floor
    assert coverage["unhashed"] == 0


def test_file_identity_is_the_recorders_hasher_with_the_floor(tmp_path, hashed):
    tiny = hashed / "label.txt"
    tiny.write_bytes(b"positive\n")
    assert inputs.file_identity(str(tiny), budget=[1 << 40], hash_level=True) == {
        "content_hash": None, "fingerprint": None, "size_bytes": 9, "rows": None,
    }
    assert inputs.file_identity(str(tiny), budget=[1 << 40])["content_hash"] == hashlib.sha256(
        b"positive\n"
    ).hexdigest()
    assert inputs.file_identity(str(tiny), budget=[1 << 40])["rows"] == 1
    assert inputs.file_identity(str(tmp_path / "missing"), budget=[1 << 40]) is None
    assert inputs.file_identity(str(hashed), budget=[1 << 40]) is None  # a folder
    over = inputs.file_identity(str(tiny), budget=[0])
    assert over == {"content_hash": None, "fingerprint": None, "size_bytes": 9, "rows": None}


def test_an_old_h2_answer_keeps_its_hash_when_the_re_read_runs_out_of_time(tmp_path, monkeypatch):
    """Review of #2791 F7: re-hashing an h2 answer for its rows ran into the
    deadline mid-file and returned None, losing the full sha the cache held."""
    data = b"line\n" * (300_000)  # over one read chunk
    path = _file(tmp_path, "big.txt", data)
    ident = inputs._ident(os.stat(path))
    cache = inputs._HashCache()
    with sqlite3.connect(str(inputs.state_dir().parent / "hashcache.sqlite3")) as db:
        db.execute("INSERT INTO h2 (d, i, s, m, c, sha, fp) VALUES (?, ?, ?, ?, ?, ?, NULL)", (*ident, "a" * 64))
    import threading

    real, me, calls = inputs.time.monotonic, threading.get_ident(), {"n": 0}

    def clock() -> float:
        if threading.get_ident() != me:
            return real()
        calls["n"] += 1
        return 0.0 if calls["n"] == 1 else 1000.0  # past the deadline after the first chunk

    monkeypatch.setattr(inputs.time, "monotonic", clock)
    assert inputs.hash_file(str(path), ident, cache=cache, budget=[1 << 40], deadline=10.0) == ("a" * 64, None, None)
