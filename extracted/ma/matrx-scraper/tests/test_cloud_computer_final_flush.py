"""Final Cloud flush before a Cloud Computer stops (2026-11-01, item 1).

A stop (save-before-stop, or the ECS SIGTERM that follows) used to end the task
with whatever the 5 s loop had not yet uploaded still only on the machine. The
flush uploads every local change, writes every conflict copy, waits — bounded by
the ``final_flush_seconds`` knob — and says what was left. Never silent.
"""

from __future__ import annotations

import asyncio
from pathlib import Path

import pytest

from matrx_scraper.cloud_browser.worker import http_app
from matrx_scraper.cloud_browser.worker.cloud_files_sync import SyncKnobs
from matrx_scraper.cloud_browser.worker.http_app import create_worker_app
from matrx_scraper.cloud_browser.worker.runtime import BrowserWorker

from test_cloud_computer_cloud_files_sync import FakeBridge, _sync, mirror, run


def test_a_local_edit_reaches_the_cloud_before_the_stop(tmp_path: Path) -> None:
    bridge = FakeBridge()
    bridge.cloud_write("notes/plan.md", b"v1")
    sync = _sync(tmp_path, bridge)
    mirror(sync)
    sync.initial_done = True
    (tmp_path / "Cloud/notes/plan.md").write_bytes(b"v2 written by the agent")
    (tmp_path / "Cloud/notes/new.md").write_bytes(b"brand new")
    answer = run(sync.flush(5))
    assert answer["flushed"] is True and answer["pending"] == 0
    assert answer["uploaded"] == 2
    assert bridge.files["notes/plan.md"]["data"] == b"v2 written by the agent"
    assert bridge.files["notes/new.md"]["data"] == b"brand new"


def test_a_both_sides_edit_writes_its_conflict_copy_before_the_stop(tmp_path: Path) -> None:
    bridge = FakeBridge()
    bridge.cloud_write("doc.txt", b"base")
    sync = _sync(tmp_path, bridge)
    mirror(sync)
    sync.initial_done = True
    bridge.cloud_write("doc.txt", b"edited on another machine")
    (tmp_path / "Cloud/doc.txt").write_bytes(b"edited here")
    answer = run(sync.flush(5))
    assert answer["flushed"] is True and answer["conflict_copies"] == 1
    copies = [p for p in bridge.files if p != "doc.txt"]
    assert len(copies) == 1 and bridge.files[copies[0]]["data"] == b"edited here"


def test_a_flush_that_cannot_finish_in_time_says_so(tmp_path: Path) -> None:
    bridge = FakeBridge()
    sync = _sync(tmp_path, bridge)
    run(sync.pull_once())
    sync.initial_done = True
    real_put = bridge.put

    async def slow_put(path, content, expected):  # noqa: ANN001, ANN202
        await asyncio.sleep(5)
        return await real_put(path, content, expected)

    bridge.put = slow_put  # type: ignore[method-assign]
    (tmp_path / "Cloud").mkdir(exist_ok=True)
    (tmp_path / "Cloud/big.bin").write_bytes(b"x" * 100)
    answer = run(sync.flush(0.3))
    assert answer["flushed"] is False and answer["timed_out"] is True
    assert answer["pending"] == 1 and answer["reason"] == "timed out"


def test_the_knob_bounds_the_flush_when_no_timeout_is_given(tmp_path: Path) -> None:
    sync = _sync(tmp_path, FakeBridge())
    assert SyncKnobs().final_flush_seconds == 90
    assert SyncKnobs.from_mapping({"final_flush_seconds": 12}).final_flush_seconds == 12
    answer = run(sync.flush())
    assert answer["timeout_seconds"] == 90.0


def test_a_flush_before_the_first_sync_finished_is_honest(tmp_path: Path) -> None:
    sync = _sync(tmp_path, FakeBridge())
    answer = run(sync.flush(1))
    assert answer["flushed"] is False and answer["reason"] == "first sync not finished"


@pytest.mark.asyncio
async def test_sigterm_runs_the_final_flush_beside_chromes_close(monkeypatch) -> None:
    worker = BrowserWorker(worker_id="browser-worker-flush")
    events: list[str] = []

    async def close(*, reason: str) -> None:
        events.append("chrome closed")

    async def flush() -> dict:
        events.append("cloud flushed")
        return {"flushed": True}

    worker.terminate_gracefully = close  # type: ignore[method-assign]

    class Loop:
        callback = None

        def add_signal_handler(self, _signal, callback) -> None:  # noqa: ANN001
            self.callback = callback

        def create_task(self, coro, *, name=None):  # noqa: ANN001, ANN202
            return asyncio.create_task(coro, name=name)

        def remove_signal_handler(self, _signal) -> bool:  # noqa: ANN001
            return True

    loop = Loop()
    monkeypatch.setattr(http_app.asyncio, "get_running_loop", lambda: loop)
    monkeypatch.setattr(http_app.signal, "getsignal", lambda _s: lambda signum, _frame: None)
    app = create_worker_app(worker)
    app.state.background_flushers = [flush]
    async with http_app._termination_lifespan(worker, None)(app):
        loop.callback()
    assert sorted(events) == ["chrome closed", "cloud flushed"]


def test_a_flush_answers_inside_its_budget_even_when_counting_what_is_left_is_slow(tmp_path: Path) -> None:
    """2026-11-09: three stops in 24 h ended "no answer (ReadTimeout)". After the upload wait
    timed out, the flush counted what was left with a full folder walk, unbounded (minutes cold
    on a big folder over EFS), so the answer came after the stop had stopped listening. The
    answer is due inside the budget; a count that cannot finish says so (never a made-up 0)."""
    import time as _time

    bridge = FakeBridge()
    sync = _sync(tmp_path, bridge)
    run(sync.pull_once())
    sync.initial_done = True
    (tmp_path / "Cloud").mkdir(exist_ok=True)
    (tmp_path / "Cloud/big.bin").write_bytes(b"x" * 100)
    real_put = bridge.put

    async def slow_put(path, content, expected):  # noqa: ANN001, ANN202
        await asyncio.sleep(5)
        return await real_put(path, content, expected)

    bridge.put = slow_put  # type: ignore[method-assign]
    real_scan = sync._scan
    calls = {"n": 0}

    def slow_scan():  # noqa: ANN202 - the walk of a big folder on a cold network drive
        calls["n"] += 1
        if calls["n"] > 1:  # quick: only the "anything waiting?" walk (the first pass reuses its list)
            _time.sleep(2.0)
        return real_scan()

    sync._scan = slow_scan  # type: ignore[method-assign]
    async def timed():  # noqa: ANN202 - timed inside the loop (asyncio.run's exit joins the walk)
        started = _time.monotonic()
        answer = await sync.flush(1.0)
        return answer, _time.monotonic() - started

    answer, took = run(timed())
    assert took < 1.3, f"the flush answered after {took:.1f}s, past its 1.0s budget"
    assert answer["flushed"] is False and answer["timed_out"] is True
    assert answer["pending_counted"] is False
    assert answer["pending"] == 1  # the pass in flight had one file waiting: at least that many


def test_a_flush_with_nothing_to_send_walks_the_folder_twice_not_three_times(tmp_path: Path) -> None:
    """The final flush's budget went to folder walks over the network drive (2026-11-09: 27 stops of one
    machine ended 'timed out' with nothing counted waiting). The push pass already walks before and after
    its uploads; the flush reads that closing walk instead of making a third."""
    bridge = FakeBridge()
    sync = _sync(tmp_path, bridge)
    run(sync.pull_once())
    sync.initial_done = True
    (tmp_path / "Cloud").mkdir(exist_ok=True)
    walks = 0
    real_scan = sync._scan

    def counted():  # noqa: ANN202
        nonlocal walks
        walks += 1
        return real_scan()

    sync._scan = counted  # type: ignore[method-assign]
    answer = run(sync.flush(5))
    assert answer["flushed"] is True and answer["pending"] == 0
    assert walks == 1, walks  # 2026-11-10: nothing waiting answers after one walk, with no pass at all


def test_a_clean_folder_answers_at_once_even_while_the_background_pass_holds_the_lock(tmp_path: Path) -> None:
    """2026-11-09/10: 26 stops filed 'timed out, after 81s and no file known to be waiting'. With
    nothing to upload, the flush still ran full passes: each waits for the background pass's lock and
    walks a big network-drive folder twice, so a clean folder spent the whole budget proving it was
    clean. Nothing waiting must answer flushed at once, without waiting for the pass lock."""
    import time as _time

    bridge = FakeBridge()
    bridge.cloud_write("notes/plan.md", b"v1")
    sync = _sync(tmp_path, bridge)
    mirror(sync)
    sync.initial_done = True

    async def scenario():  # noqa: ANN202
        await sync._lock.acquire()  # the background pass, mid-walk, for far longer than the budget
        try:
            started = _time.monotonic()
            answer = await sync.flush(2.0)
            return answer, _time.monotonic() - started
        finally:
            sync._lock.release()

    answer, took = run(scenario())
    assert answer["flushed"] is True and answer["pending"] == 0, answer
    assert took < 1.0, f"a clean folder took {took:.1f}s to answer"


def test_a_pass_that_runs_long_but_leaves_nothing_waiting_is_flushed(tmp_path: Path) -> None:
    """The passes may run past the budget (a slow walk) and still have sent everything: the closing
    count finds nothing waiting, and the answer says flushed, never 'timed out' with zero files left."""
    import time as _time

    bridge = FakeBridge()
    sync = _sync(tmp_path, bridge)
    run(sync.pull_once())
    sync.initial_done = True
    (tmp_path / "Cloud").mkdir(exist_ok=True)
    (tmp_path / "Cloud/new.md").write_bytes(b"brand new")
    real_scan = sync._scan
    calls = {"n": 0}

    def scan():  # noqa: ANN202 - the pass's closing walk (the 2nd; the 1st is "anything waiting?") is slow
        calls["n"] += 1
        if calls["n"] == 2:
            _time.sleep(1.2)
        return real_scan()

    sync._scan = scan  # type: ignore[method-assign]
    answer = run(sync.flush(1.5))
    assert bridge.files["new.md"]["data"] == b"brand new"
    assert answer["flushed"] is True and answer["pending"] == 0, answer
    assert answer.get("timed_out") is True and answer["pending_counted"] is True
