"""Process crashes and concurrent retries retain terminal artifact identities."""

from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
import json
import multiprocessing
import os
from pathlib import Path
import sqlite3

import pytest

from probe.sdk import journal as jm
from probe.sdk.durable import file_lock, write_text_atomic

CTX = multiprocessing.get_context("fork")


def _result(op):
    return {**op["body"], "id": "artifact-" + op["correlation"], "status": "complete"}


def _append(queue, correlation="one"):
    return queue.append_http(
        "POST",
        "/v1/projects/p/artifacts",
        {"name": "report", "uri": "file:///source", "is_reference": True},
        correlation=correlation,
    )


@pytest.fixture
def queue(tmp_path, monkeypatch):
    monkeypatch.setattr(jm, "MIN_FREE_BYTES", 0)
    return jm.Journal.for_receipts(tmp_path / "outbox", context={"base_url": "http://test"})


def legacy_receipt(queue, correlation="one"):
    """Use the real producer and receipt validator with the previous JSON sink."""
    _append(queue, correlation)
    path, op = next((path, op) for path, op in queue.pending() if op["correlation"] == correlation)
    original = queue._index_receipts

    def legacy_sink(receipts):
        for receipt in receipts:
            key = queue._correlation_key(receipt["correlation"])
            write_text_atomic(queue.receipts_dir / f"{key}.json", json.dumps(receipt), mode=0o600)

    queue._index_receipts = legacy_sink
    try:
        queue._save_delivery_receipt(op, _result(op))
    finally:
        queue._index_receipts = original
    path.unlink()
    key = queue._correlation_key(correlation)
    (queue.dir / "correlations" / f"{key}.lock").touch()
    return queue.receipt(correlation)


def _crash_compaction(directory, stage):
    queue = jm.Journal(directory)
    original_commit = jm.Journal._commit_receipt_index
    if stage in ("before_commit", "after_commit"):

        def crash(conn):
            if stage == "after_commit":
                original_commit(conn)
            os._exit(81)

        jm.Journal._commit_receipt_index = staticmethod(crash)
    else:
        original_unlink = Path.unlink

        def crash_unlink(path, *args, **kwargs):
            original_unlink(path, *args, **kwargs)
            if path.parent == queue.receipts_dir:
                os._exit(81)

        Path.unlink = crash_unlink
    queue.compact_receipts()


@pytest.mark.parametrize("stage", ["before_commit", "after_commit", "after_json_unlink"])
def test_process_exit_at_each_compaction_boundary_preserves_exact_receipt(queue, stage):
    expected = legacy_receipt(queue)
    process = CTX.Process(target=_crash_compaction, args=(queue.dir, stage))
    process.start()
    process.join(5)
    assert not process.is_alive() and process.exitcode == 81
    restarted = jm.Journal(queue.dir, context=queue.context, attribution=queue.attribution)
    assert restarted.receipt("one") == expected
    restarted.compact_receipts()
    assert restarted.receipt("one") == expected
    assert not list(restarted.receipts_dir.iterdir())
    assert not list((restarted.dir / "correlations").iterdir())
    assert _append(restarted) == expected["op_id"] and not restarted.pending()


def _commit_then_exit(directory, op):
    jm.Journal(directory)._save_delivery_receipt(op, _result(op))
    os._exit(82)  # the queue operation deliberately remains on disk


def test_process_exit_after_index_commit_before_operation_delete_never_resends(queue):
    _append(queue)
    _, op = queue.pending()[0]
    process = CTX.Process(target=_commit_then_exit, args=(queue.dir, op))
    process.start()
    process.join(5)
    assert process.exitcode == 82 and len(queue.pending()) == 1
    assert queue.receipt("one")["artifact_id"] == "artifact-one"

    def no_network(*args):
        raise AssertionError("terminal receipt must prevent a second remote request")

    assert jm.drain(queue, client_factory=no_network).delivered == 1
    assert not queue.pending()


def test_concurrent_compaction_and_exact_replays_return_one_identity(queue):
    expected = legacy_receipt(queue)

    def replay():
        restarted = jm.Journal(queue.dir, context=queue.context, attribution=queue.attribution)
        for _ in range(30):
            assert _append(restarted) == expected["op_id"]
            assert restarted.receipt("one") == expected

    def compact():
        for _ in range(10):
            jm.Journal(queue.dir).compact_receipts()

    with ThreadPoolExecutor(max_workers=3) as executor:
        jobs = [executor.submit(replay), executor.submit(replay), executor.submit(compact)]
        for job in jobs:
            job.result(timeout=10)
    assert not queue.pending() and queue.receipt("one") == expected
    with pytest.raises(ValueError, match="different immutable request"):
        queue.append_http(
            "POST",
            "/v1/projects/p/artifacts",
            {"name": "different", "uri": "file:///source", "is_reference": True},
            correlation="one",
        )


def _hold_legacy_lock(path, ready, release):
    with file_lock(path):
        ready.set()
        release.wait(5)


def test_active_legacy_lock_is_retained_and_retried_later(queue):
    expected = legacy_receipt(queue)
    key = queue._correlation_key("one")
    path = queue.dir / "correlations" / f"{key}.lock"
    ready, release = CTX.Event(), CTX.Event()
    process = CTX.Process(target=_hold_legacy_lock, args=(path, ready, release))
    process.start()
    try:
        assert ready.wait(3)
        result = queue.compact_receipts()
        assert result["deferred"] == 1 and path.exists()
        assert queue.receipt("one") == expected
    finally:
        release.set()
        process.join(5)
    assert process.exitcode == 0
    assert queue.compact_receipts()["locks_removed"] == 1
    assert not path.exists() and queue.receipt("one") == expected


def test_stable_stripe_survives_cleanup_and_legacy_inode_is_never_recreated(queue):
    expected = legacy_receipt(queue)
    key = queue._correlation_key("one")
    stripe = queue.correlation_locks / f"{key[:2]}.lock"
    original_inode = stripe.stat().st_ino
    assert queue.compact_receipts()["locks_removed"] == 1
    assert _append(queue) == expected["op_id"]
    assert stripe.stat().st_ino == original_inode
    assert not list((queue.dir / "correlations").iterdir())


def test_compaction_is_bounded_and_does_not_delete_identity_history(queue):
    expected = {str(index): legacy_receipt(queue, str(index)) for index in range(5)}
    result = queue.compact_receipts(max_records=2)
    assert result["indexed"] == result["json_removed"] == result["locks_removed"] == 2
    assert len(list(queue.receipts_dir.iterdir())) == 3
    for _ in range(3):
        queue.compact_receipts(max_records=2)
    assert not list(queue.receipts_dir.iterdir())
    assert {correlation: queue.receipt(correlation) for correlation in expected} == expected
    assert not jm.Journal(queue.dir.parent).pending()  # old production enumeration


def test_new_receipts_use_index_without_per_receipt_files_or_locks(queue):
    for index in range(20):
        _append(queue, str(index))
        path, op = queue.pending()[0]
        queue._save_delivery_receipt(op, _result(op))
        path.unlink()
    assert not list(queue.receipts_dir.iterdir())
    assert not list((queue.dir / "correlations").iterdir())
    assert len(list(queue.correlation_locks.iterdir())) <= 20
    assert queue.receipt_index.stat().st_mode & 0o777 == 0o600
    with sqlite3.connect(queue.receipt_index) as conn:
        assert conn.execute("SELECT count(*) FROM receipts").fetchone()[0] == 20
    assert queue.receipt("19")["artifact_id"] == "artifact-19"


def test_unknown_index_version_fails_closed_without_requeueing(queue):
    _append(queue)
    path, op = queue.pending()[0]
    queue._save_delivery_receipt(op, _result(op))
    path.unlink()
    with sqlite3.connect(queue.receipt_index) as conn:
        conn.execute("PRAGMA user_version=999")
    with pytest.raises(ValueError, match="unsupported terminal receipt"):
        _append(queue)
    assert not queue.pending() and queue.receipt_index.exists()


def test_terminal_read_and_replay_do_not_scan_receipt_history(queue, monkeypatch):
    expected = legacy_receipt(queue)
    queue.compact_receipts()

    def forbidden_scan(*args, **kwargs):
        raise AssertionError("indexed terminal lookup must not scan history")

    monkeypatch.setattr(jm.os, "scandir", forbidden_scan)
    assert queue.receipt("one") == expected
    assert _append(queue) == expected["op_id"]
