"""The Cloud folder on a Cloud Computer: mirror + stubs, upload-back, conflicts (P2).

Every test drives the real ``CloudFilesSync`` against an in-memory bridge that
behaves like ``/api/cloud-files/*`` (checksums are sha256, ``put`` honors
``expected_checksum`` with 412, ``changes`` pages by ``updated_at``).
"""

from __future__ import annotations

import asyncio
import hashlib
from datetime import datetime, timedelta, UTC
from pathlib import Path

import pytest

from matrx_scraper.cloud_browser.worker.cloud_files_sync import (
    STUB_MAGIC,
    BridgeError,
    CloudFilesSync,
    SyncKnobs,
)
from matrx_scraper.cloud_browser.worker.machine_agent import hydrate_for_request

NOW = datetime(2026, 10, 18, 12, 0, tzinfo=UTC)


class FakeBridge:
    def __init__(self) -> None:
        self.files: dict[str, dict] = {}
        self.deleted: list[dict] = []
        self.clock = 0
        self.gets: list[str] = []
        self.puts: list[tuple[str, str | None]] = []

    def _stamp(self) -> str:
        self.clock += 1
        return (NOW - timedelta(days=1) + timedelta(seconds=self.clock)).isoformat()

    def cloud_write(self, path: str, data: bytes, *, updated: str | None = None) -> None:
        self.files[path] = {
            "file_path": path, "data": data, "size_bytes": len(data),
            "checksum": hashlib.sha256(data).hexdigest(), "updated_at": updated or self._stamp(),
        }

    async def changes(self, since: str, limit: int) -> dict:
        rows = [
            {k: v for k, v in f.items() if k != "data"} for f in self.files.values()
        ] + self.deleted
        rows = sorted((r for r in rows if r["updated_at"] > since), key=lambda r: r["updated_at"])[:limit]
        return {"files": rows, "next_cursor": rows[-1]["updated_at"] if rows else since,
                "deletions_supported": True, "poll_after_seconds": 30}

    async def get(self, path: str) -> bytes:
        self.gets.append(path)
        return self.files[path]["data"]

    async def put(self, path: str, content: bytes, expected_checksum: str | None) -> dict:
        self.puts.append((path, expected_checksum))
        current = self.files.get(path)
        if expected_checksum and current and current["checksum"] != expected_checksum:
            raise BridgeError(412, {"error": "checksum_mismatch"})
        self.cloud_write(path, content)
        return {"file_path": path, "version": 1, "size_bytes": len(content)}

    async def delete(self, path: str) -> None:
        row = self.files.pop(path)
        self.deleted.append({"file_path": path, "deleted": True, "updated_at": self._stamp(),
                             "checksum": row["checksum"]})

    async def session(self) -> dict:
        return {}


def _sync(home: Path, bridge: FakeBridge, **knobs: int) -> CloudFilesSync:
    return CloudFilesSync(home / "Cloud", bridge, state_dir=home / ".matrx/cloud-sync",
                          knobs=SyncKnobs(**knobs), now=lambda: NOW)


def run(coro):
    return asyncio.run(coro)


def mirror(sync: CloudFilesSync) -> None:
    run(sync.pull_once())
    run(sync.fill_copies(limit=1000))


def test_the_first_mirror_shows_the_whole_tree_before_copying_anything(tmp_path: Path) -> None:
    bridge = FakeBridge()
    for i in range(5):
        bridge.cloud_write(f"docs/{i}.txt", f"doc {i}".encode())
    sync = _sync(tmp_path, bridge)
    run(sync.pull_once())
    assert bridge.gets == [] and sync.status()["copies_pending"] == 5
    assert all((tmp_path / f"Cloud/docs/{i}.txt").read_text().startswith(STUB_MAGIC) for i in range(5))
    run(sync.fill_copies(limit=2))
    assert bridge.gets == ["docs/4.txt", "docs/3.txt"]  # newest first
    run(sync.fill_copies(limit=10))
    assert (tmp_path / "Cloud/docs/0.txt").read_bytes() == b"doc 0" and sync.status()["copies_pending"] == 0
    run(sync.push_once())
    assert bridge.puts == []  # filling copies is never an edit


def test_small_recent_files_are_copied_and_big_or_cold_files_are_stubs(tmp_path: Path) -> None:
    bridge = FakeBridge()
    bridge.cloud_write("notes/todo.txt", b"buy milk")
    bridge.cloud_write("video/big.bin", b"x" * 5000)
    bridge.cloud_write("old/report.txt", b"ancient", updated=(NOW - timedelta(days=400)).isoformat())
    sync = _sync(tmp_path, bridge, mirror_max_file_bytes=1000, mirror_recent_days=90)
    mirror(sync)
    root = tmp_path / "Cloud"
    assert (root / "notes/todo.txt").read_bytes() == b"buy milk"
    big = (root / "video/big.bin").read_text()
    assert big.startswith(STUB_MAGIC) and "5000 bytes" in big and "cloud-files fetch" in big
    assert (root / "old/report.txt").read_text().startswith(STUB_MAGIC)
    assert sorted(bridge.gets) == ["notes/todo.txt"]
    assert sync.is_stub("video/big.bin") and not sync.is_stub("notes/todo.txt")


def test_a_stub_opens_as_the_real_file(tmp_path: Path) -> None:
    bridge = FakeBridge()
    bridge.cloud_write("video/big.bin", b"y" * 5000)
    sync = _sync(tmp_path, bridge, mirror_max_file_bytes=1000)
    mirror(sync)
    assert run(sync.hydrate("video/big.bin")) is True
    assert (tmp_path / "Cloud/video/big.bin").read_bytes() == b"y" * 5000
    assert not sync.is_stub("video/big.bin")
    run(sync.push_once())
    assert bridge.puts == []  # fetching a file is not an edit


def test_the_agent_open_hook_fetches_stubs_a_read_or_command_names(tmp_path: Path) -> None:
    bridge = FakeBridge()
    bridge.cloud_write("a/big1.bin", b"1" * 5000)
    bridge.cloud_write("b/big2.bin", b"2" * 5000)
    bridge.cloud_write("c/big3.bin", b"3" * 5000)
    sync = _sync(tmp_path, bridge, mirror_max_file_bytes=1000)
    mirror(sync)
    run(hydrate_for_request("GET", "fs/read", {"path": str(tmp_path / "Cloud/a/big1.bin")}, None, sync))
    run(hydrate_for_request("POST", "exec", {}, {"command": "wc -c Cloud/b/big2.bin"}, sync))
    assert not sync.is_stub("a/big1.bin") and not sync.is_stub("b/big2.bin")
    assert sync.is_stub("c/big3.bin")


def test_a_machine_edit_uploads_with_the_last_synced_checksum(tmp_path: Path) -> None:
    bridge = FakeBridge()
    bridge.cloud_write("doc.txt", b"v1")
    sync = _sync(tmp_path, bridge)
    mirror(sync)
    (tmp_path / "Cloud/doc.txt").write_bytes(b"v2 from the machine")
    (tmp_path / "Cloud/new.txt").write_bytes(b"brand new")
    run(sync.push_once())
    assert bridge.files["doc.txt"]["data"] == b"v2 from the machine"
    assert bridge.files["new.txt"]["data"] == b"brand new"
    assert ("doc.txt", hashlib.sha256(b"v1").hexdigest()) in bridge.puts
    gets = len(bridge.gets)
    mirror(sync)  # our own uploads echo back on the change feed
    assert len(bridge.gets) == gets
    run(sync.push_once())
    assert len(bridge.puts) == 2


def test_both_sides_changed_keeps_both_never_loses_either(tmp_path: Path) -> None:
    bridge = FakeBridge()
    bridge.cloud_write("plan.txt", b"base")
    sync = _sync(tmp_path, bridge)
    mirror(sync)
    (tmp_path / "Cloud/plan.txt").write_bytes(b"machine edit")
    bridge.cloud_write("plan.txt", b"cloud edit")
    mirror(sync)
    root = tmp_path / "Cloud"
    assert (root / "plan.txt").read_bytes() == b"cloud edit"
    copies = list(root.glob("plan (conflict from Cloud Computer *).txt"))
    assert len(copies) == 1 and copies[0].read_bytes() == b"machine edit"
    assert any(f["data"] == b"machine edit" for f in bridge.files.values())


def test_an_upload_refused_because_the_cloud_moved_keeps_both(tmp_path: Path) -> None:
    bridge = FakeBridge()
    bridge.cloud_write("plan.txt", b"base")
    sync = _sync(tmp_path, bridge)
    mirror(sync)
    bridge.cloud_write("plan.txt", b"cloud edit")  # not yet pulled
    (tmp_path / "Cloud/plan.txt").write_bytes(b"machine edit")
    run(sync.push_once())
    root = tmp_path / "Cloud"
    assert (root / "plan.txt").read_bytes() == b"cloud edit"
    assert bridge.files["plan.txt"]["data"] == b"cloud edit"
    copies = list(root.glob("plan (conflict from Cloud Computer *).txt"))
    assert copies and copies[0].read_bytes() == b"machine edit"
    assert any(f["data"] == b"machine edit" for p, f in bridge.files.items() if p != "plan.txt")


def test_deletes_travel_both_ways_and_a_local_edit_survives_a_cloud_delete(tmp_path: Path) -> None:
    bridge = FakeBridge()
    for name in ("gone-in-cloud.txt", "gone-on-machine.txt", "edited.txt"):
        bridge.cloud_write(name, name.encode())
    sync = _sync(tmp_path, bridge)
    mirror(sync)
    root = tmp_path / "Cloud"
    run(bridge.delete("gone-in-cloud.txt"))
    (root / "edited.txt").write_bytes(b"kept")
    run(bridge.delete("edited.txt"))
    mirror(sync)
    assert not (root / "gone-in-cloud.txt").exists()
    assert (root / "edited.txt").read_bytes() == b"kept"
    (root / "gone-on-machine.txt").unlink()
    run(sync.push_once())
    assert "gone-on-machine.txt" in bridge.files  # one scan is never proof of a delete
    run(sync.push_once())
    assert "gone-on-machine.txt" not in bridge.files
    assert bridge.files["edited.txt"]["data"] == b"kept"


def test_over_the_disk_budget_the_coldest_clean_files_become_stubs(tmp_path: Path) -> None:
    bridge = FakeBridge()
    for i in range(4):
        bridge.cloud_write(f"f{i}.bin", bytes([i]) * 100)
    sync = _sync(tmp_path, bridge, disk_budget_bytes=1000)
    mirror(sync)
    assert sync.status()["stubs"] == 0
    sync.knobs.disk_budget_bytes = 250
    assert sync.evict() == 2
    assert sync.is_stub("f0.bin") and sync.is_stub("f1.bin") and not sync.is_stub("f3.bin")


def test_state_survives_a_new_task_and_build(tmp_path: Path) -> None:
    bridge = FakeBridge()
    bridge.cloud_write("keep.txt", b"hello")
    bridge.cloud_write("big.bin", b"z" * 5000)
    mirror(_sync(tmp_path, bridge, mirror_max_file_bytes=1000))
    gets = list(bridge.gets)
    fresh = _sync(tmp_path, bridge, mirror_max_file_bytes=1000)  # a new process on a new build
    assert fresh.initial_done and fresh.is_stub("big.bin")
    run(fresh.pull_once())
    run(fresh.push_once())
    assert bridge.gets == gets and bridge.puts == []


def test_a_path_cannot_escape_the_cloud_folder(tmp_path: Path) -> None:
    sync = _sync(tmp_path, FakeBridge())
    with pytest.raises(ValueError):
        sync._path("../.ssh/authorized_keys")
    assert sync.rel_for("/etc/passwd") is None


class SlowDriveSync(CloudFilesSync):
    """The home's network drive cold: every walk and stat is slow (blocking I/O)."""

    def _scan(self):
        import time
        time.sleep(0.6)
        return super()._scan()

    def _local_changed(self, rel, entry) -> bool:
        import time
        time.sleep(0.05)
        return super()._local_changed(rel, entry)


def test_a_slow_drive_never_blocks_the_workers_event_loop(tmp_path: Path) -> None:
    """Break (live 2026-10-18): a wake with a 12.5k-file Cloud folder answered its
    first /health at 170 s — the sync walked and stat'ed the folder ON the event
    loop that also serves /health, so readiness waited for the sync."""
    bridge = FakeBridge()
    for i in range(8):
        bridge.cloud_write(f"docs/{i}.txt", f"doc {i}".encode())
    sync = SlowDriveSync(tmp_path / "Cloud", bridge, state_dir=tmp_path / ".matrx/cloud-sync",
                         knobs=SyncKnobs(), now=lambda: NOW)

    async def scenario() -> float:
        import time
        worst = 0.0
        done = asyncio.Event()

        async def health() -> None:  # what /health needs: the loop answering
            nonlocal worst
            while not done.is_set():
                t = time.monotonic()
                await asyncio.sleep(0.01)
                worst = max(worst, time.monotonic() - t)

        ticker = asyncio.create_task(health())
        await asyncio.sleep(0.02)  # the ticker is waiting on the loop, like /health
        await sync.pull_once()
        await sync.fill_copies(limit=100)
        await sync.push_once()
        await asyncio.to_thread(sync.evict)
        done.set()
        await ticker
        return worst

    worst = run(scenario())
    assert worst < 0.3, f"the event loop stalled {worst:.2f} s behind the sync"
