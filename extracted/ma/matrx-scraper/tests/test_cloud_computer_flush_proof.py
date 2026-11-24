"""The worker's proof that a stop's Cloud files are saved: ``clean_since_flush_request``.

A pass that STARTED before the flush request and finished after it scanned before the person's
last write, so it proves nothing about that write (review 2026-11-10: it read clean and hid a lost
file). Only a pass that started after the request, with nothing left, no failures and no held
delete, sets the proof, on this machine's own clock.
"""

from __future__ import annotations

import asyncio
import time
from pathlib import Path

from test_cloud_computer_cloud_files_sync import FakeBridge, _sync, mirror, run


def _ready(tmp_path: Path):  # noqa: ANN202
    bridge = FakeBridge()
    bridge.cloud_write("a.md", b"v1")
    sync = _sync(tmp_path, bridge)
    mirror(sync)
    sync.initial_done = True
    return bridge, sync


def test_a_pass_that_started_before_the_request_is_never_proof(tmp_path: Path) -> None:
    bridge, sync = _ready(tmp_path)
    real_put = bridge.put

    async def put_while_the_request_arrives(path, content, expected):  # noqa: ANN001, ANN202
        sync.flush_requested_mono = time.monotonic()  # the stop asks while this pass is mid-flight
        return await real_put(path, content, expected)

    bridge.put = put_while_the_request_arrives  # type: ignore[method-assign]
    (tmp_path / "Cloud/a.md").write_bytes(b"v2")
    run(sync.push_once())
    assert sync.unsent_after_push == [] and sync.pending_uploads == 0
    assert sync.work_signals()["clean_since_flush_request"] is False


def test_a_pass_that_started_after_the_request_with_nothing_left_is_proof(tmp_path: Path) -> None:
    _, sync = _ready(tmp_path)
    (tmp_path / "Cloud/a.md").write_bytes(b"v2")
    sync.flush_requested_mono = time.monotonic()
    run(asyncio.sleep(0.01))
    run(sync.push_once())
    assert sync.work_signals()["clean_since_flush_request"] is True


def test_no_request_no_proof_and_failures_or_holds_void_it(tmp_path: Path) -> None:
    _, sync = _ready(tmp_path)
    run(sync.push_once())
    assert sync.work_signals()["clean_since_flush_request"] is False  # nobody asked
    sync.flush_requested_mono = time.monotonic()
    sync.stats.consecutive_failures = 1
    run(asyncio.sleep(0.01))
    run(sync.push_once())
    assert sync.work_signals()["clean_since_flush_request"] is False


def _qualified(tmp_path: Path):  # noqa: ANN202
    _, sync = _ready(tmp_path)
    sync.flush_requested_mono = time.monotonic()
    run(asyncio.sleep(0.01))
    run(sync.push_once())
    assert sync.clean_since_flush_request is True
    return sync


def test_a_write_after_the_qualifying_scan_is_not_clean_at_the_status_read(tmp_path: Path) -> None:
    sync = _qualified(tmp_path)
    (tmp_path / "Cloud/late.md").write_bytes(b"written after the pass scanned")
    assert run(sync.clean_now()) is False


def test_an_edit_of_a_known_file_after_the_scan_is_not_clean(tmp_path: Path) -> None:
    sync = _qualified(tmp_path)
    time.sleep(0.05)
    (tmp_path / "Cloud/a.md").write_bytes(b"edited late")
    sync._clean_scan_wall = time.time() - 10  # the scan was 10 s ago; the edit is newer
    assert run(sync.clean_now()) is False


def test_nothing_new_since_the_scan_stays_clean(tmp_path: Path) -> None:
    sync = _qualified(tmp_path)
    sync._clean_scan_wall = time.time() + 10  # nothing on disk is newer than this
    assert run(sync.clean_now()) is True


def test_a_recheck_that_cannot_finish_is_not_clean(tmp_path: Path) -> None:
    sync = _qualified(tmp_path)
    sync._clean_scan_wall = time.time() + 10
    sync._anything_newer_than = lambda wall: (time.sleep(1), False)[1]  # type: ignore[method-assign]
    assert run(sync.clean_now(0.1)) is False
