"""One cloud file the bridge cannot give (404 since the feed listed it) never pauses the sync.

Live 2026-11-14: a Cloud Computer reported "Cloud folder sync has been paused" for hours —
``fill_copies`` (run inside the push pass) fetched a placeholder whose ``/cloud-files/get``
answered 404, the BridgeError escaped the pass, and every pass after failed the same way.
"""

from __future__ import annotations

import asyncio
from pathlib import Path

import pytest

from matrx_scraper.cloud_browser.worker.cloud_files_sync import BridgeError

from test_cloud_computer_cloud_files_sync import FakeBridge, _sync, run


class GoneOnGetBridge(FakeBridge):
    def __init__(self, gone: set[str], status: int = 404) -> None:
        super().__init__()
        self.gone = gone
        self.status = status

    async def get(self, path: str) -> bytes:
        if path in self.gone:
            self.gets.append(path)
            raise BridgeError(self.status, {"error": "not_found", "message": f"File '{path}' not found"})
        return await super().get(path)


def test_one_unreadable_copy_is_skipped_and_the_others_fill(tmp_path: Path) -> None:
    bridge = GoneOnGetBridge({"library/gone.pdf"})
    bridge.cloud_write("library/gone.pdf", b"pdf bytes")
    bridge.cloud_write("notes/ok.txt", b"fine")
    sync = _sync(tmp_path, bridge)
    run(sync.pull_once())

    filled = run(sync.fill_copies(limit=10))  # used to raise BridgeError(404)

    assert filled == 1
    assert (tmp_path / "Cloud/notes/ok.txt").read_bytes() == b"fine"
    assert sync.entries["library/gone.pdf"].stub and not sync.entries["library/gone.pdf"].want_copy
    assert "library/gone.pdf" in str(sync.skipped_view())
    # Not asked again every pass.
    bridge.gets.clear()
    run(sync.fill_copies(limit=10))
    assert "library/gone.pdf" not in bridge.gets


@pytest.mark.parametrize("status", [401, 429, 503])
def test_a_bridge_outage_still_fails_the_pass(tmp_path: Path, status: int) -> None:
    bridge = GoneOnGetBridge({"library/gone.pdf"}, status=status)
    bridge.cloud_write("library/gone.pdf", b"pdf bytes")
    sync = _sync(tmp_path, bridge)
    run(sync.pull_once())
    with pytest.raises(BridgeError):
        run(sync.fill_copies(limit=10))


def _synced(tmp_path: Path, bridge: GoneOnGetBridge):
    bridge.cloud_write("notes/a.txt", b"original")
    for i in range(5):  # a healthy folder: one file going missing is a delete, not an outage
        bridge.cloud_write(f"notes/other{i}.txt", b"x")
    sync = _sync(tmp_path, bridge)
    run(sync.pull_once())
    run(sync.fill_copies(limit=10))
    assert (tmp_path / "Cloud/notes/a.txt").read_bytes() == b"original"
    return sync


def test_conflict_refetch_404_keeps_local_copy_and_a_placeholder(tmp_path: Path) -> None:
    """After a 412 the cloud copy is re-fetched; a 404 there used to fail the push pass."""
    bridge = GoneOnGetBridge(set())
    sync = _synced(tmp_path, bridge)
    bridge.cloud_write("notes/a.txt", b"moved on in the cloud")  # checksum moves: 412
    bridge.gone.add("notes/a.txt")
    (tmp_path / "Cloud/notes/a.txt").write_bytes(b"my edit")

    run(sync.push_once())  # used to raise BridgeError(404)

    root = tmp_path / "Cloud/notes"
    assert [p.read_bytes() for p in root.glob("a (conflict*")] == [b"my edit"]
    assert (root / "a.txt").exists(), "a hole at the path reads as a delete"
    assert "notes/a.txt" in str(sync.skipped_view())
    assert "notes/a.txt" in bridge.files, "must never turn into a cloud delete"
    run(sync.push_once())  # and the next pass is clean


def test_conflict_refetch_outage_still_fails_the_pass(tmp_path: Path) -> None:
    bridge = GoneOnGetBridge(set(), status=503)
    sync = _synced(tmp_path, bridge)
    bridge.cloud_write("notes/a.txt", b"moved on in the cloud")
    bridge.gone.add("notes/a.txt")
    (tmp_path / "Cloud/notes/a.txt").write_bytes(b"my edit")
    with pytest.raises(BridgeError):
        run(sync.push_once())


def _refuse_delete(bridge: GoneOnGetBridge) -> None:
    async def delete(path: str) -> None:
        raise BridgeError(409, {"error": "kept"})

    bridge.delete = delete  # type: ignore[method-assign]


def test_restore_after_a_kept_delete_404_leaves_a_placeholder(tmp_path: Path) -> None:
    """The cloud kept a deleted file (409) and the restore fetch 404s: the pass must survive."""
    bridge = GoneOnGetBridge(set())
    sync = _synced(tmp_path, bridge)
    _refuse_delete(bridge)
    bridge.gone.add("notes/a.txt")
    (tmp_path / "Cloud/notes/a.txt").unlink()

    run(sync.push_once())  # a delete is confirmed on the second sighting
    run(sync.push_once())  # used to raise BridgeError(404)

    assert (tmp_path / "Cloud/notes/a.txt").exists()
    assert "notes/a.txt" in str(sync.skipped_view())
    assert "notes/a.txt" in bridge.files


def test_restore_after_a_kept_delete_outage_still_fails_the_pass(tmp_path: Path) -> None:
    bridge = GoneOnGetBridge(set(), status=503)
    sync = _synced(tmp_path, bridge)
    _refuse_delete(bridge)
    bridge.gone.add("notes/a.txt")
    (tmp_path / "Cloud/notes/a.txt").unlink()
    run(sync.push_once())
    with pytest.raises(BridgeError):
        run(sync.push_once())


def test_a_404_that_escapes_a_pass_names_its_file_and_does_not_pause_the_loop(tmp_path: Path) -> None:
    """Safety net for any call site that lets a per-file 404 out of the push pass."""
    bridge = FakeBridge()
    sync = _sync(tmp_path, bridge)
    run(sync.pull_once())
    sync.initial_done = True
    calls = {"n": 0}

    async def push_once() -> None:
        calls["n"] += 1
        if calls["n"] == 1:
            raise BridgeError(404, {"error": "not_found"}, path="library/guideline/gone.pdf")
        raise asyncio.CancelledError  # stop the loop after the second pass

    sync.push_once = push_once  # type: ignore[method-assign]
    sync.knobs.local_scan_seconds = 0

    async def go() -> None:
        with pytest.raises(asyncio.CancelledError):
            await sync.run_forever()

    run(go())
    assert sync.stats.last_push_error is None and not sync.stats.consecutive_failures
    assert "library/guideline/gone.pdf" in str(sync.skipped_view())
