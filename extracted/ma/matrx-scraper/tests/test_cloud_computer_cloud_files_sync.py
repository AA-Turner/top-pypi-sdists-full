"""The Cloud folder on a Cloud Computer: mirror + stubs, upload-back, conflicts (P2).

Every test drives the real ``CloudFilesSync`` against an in-memory bridge that
behaves like ``/api/cloud-files/*`` (checksums are sha256, ``put`` honors
``expected_checksum`` with 412, ``changes`` pages by ``updated_at``).
"""

from __future__ import annotations

import asyncio
import hashlib
import json
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
    """Answers like BOTH real feeds over one dataset: the legacy ``/cloud-files/changes``
    (``updated_at > since``, newest seen as cursor) and THE device feed
    ``/cloud-files/sync/changes`` (``(updated_at, id)`` keyset, bootstrap alive-only, the
    relocation ledger re-sending a moved file at its new path by ``file_id``)."""

    def __init__(self) -> None:
        self.files: dict[str, dict] = {}
        self.deleted: list[dict] = []
        self.clock = 0
        self.ids = 0
        self.gets: list[str] = []
        self.puts: list[tuple[str, str | None]] = []
        #: The relocation ledger: (seq, file_id, feed_at).
        self.moves: list[tuple[int, str]] = []
        self.feed_calls = 0
        #: When set, every feed call raises this (a feed outage).
        self.feed_error: Exception | None = None
        #: True = the first server of THE feed, which served every relocation before any
        #: keyset row (review defect 1). The client must be correct under both orders.
        self.moves_first = False
        #: Paths THE device feed leaves out on purpose while the file stays a live, visible
        #: cloud file (a dot folder like ``.matrx-tmp/``, a crawl capture, a row stamped in the
        #: feed's last 10 s). The legacy feed and ``/get`` still serve them.
        self.feed_omits: set[str] = set()
        #: Rows no write may change (a crawl capture is ``system_immutable``): the bridge
        #: answers 409 ``file_write_conflict`` to a put at that path.
        self.immutable: set[str] = set()

    def _stamp(self) -> str:
        self.clock += 1
        return (NOW - timedelta(days=1) + timedelta(seconds=self.clock)).isoformat()

    def cloud_write(self, path: str, data: bytes, *, updated: str | None = None) -> None:
        current = self.files.get(path)
        if current is None:
            self.ids += 1
        fid = current["file_id"] if current else f"id-{self.ids:05d}"
        self.files[path] = {
            "file_id": fid, "file_path": path, "data": data, "size_bytes": len(data),
            "checksum": hashlib.sha256(data).hexdigest(), "updated_at": updated or self._stamp(),
        }

    def cloud_move(self, old: str, new: str) -> None:
        """The placement mover: the path changes, ``updated_at`` is kept, a ledger mark is written."""
        row = self.files.pop(old)
        row["file_path"] = new
        self.files[new] = row
        self.moves.append((len(self.moves) + 1, row["file_id"], self._stamp()))

    def cloud_hide(self, path: str) -> None:
        """The row stays in the cloud but its owner can no longer see it (organization archived,
        access lost): the feed states it gone with ``gone_reason: no_longer_visible``."""
        row = self.files.pop(path)
        self.hidden = {**getattr(self, "hidden", {}), path: row}
        self.deleted.append({"file_id": row["file_id"], "file_path": path, "deleted": True,
                             "gone_reason": "no_longer_visible", "updated_at": self._stamp(),
                             "checksum": row["checksum"]})

    def _rows(self) -> list[dict]:
        return [{k: v for k, v in f.items() if k != "data"} for f in self.files.values()] + self.deleted

    async def changes(self, since: str, limit: int) -> dict:
        if self.feed_error is not None:
            raise self.feed_error
        rows = sorted((r for r in self._rows() if r["updated_at"] > since), key=lambda r: r["updated_at"])[:limit]
        return {"files": rows, "next_cursor": rows[-1]["updated_at"] if rows else since,
                "deletions_supported": True, "poll_after_seconds": 30}

    async def sync_changes(self, cursor: str | None, limit: int) -> dict:
        self.feed_calls += 1
        if self.feed_error is not None:
            raise self.feed_error
        if cursor is None:
            ts, fid, aware, mpos = "", "", False, len(self.moves)
        else:
            c = json.loads(cursor)
            ts, fid, aware, mpos = c["ts"], c["id"], c["d"], c["m"]
        # Source 2 — ledger marks after ``mpos``, each the file's CURRENT row, keyed by feed_at.
        marks: list[tuple[tuple[str, int, str], int, dict]] = []
        if aware:
            for seq, mid, at in self.moves:
                if seq > mpos:
                    row = next((r for r in self._rows() if r.get("file_id") == mid), None)
                    if row is not None:
                        marks.append(((at, 1, str(seq)), seq, row))
        keyed = sorted(
            (((r["updated_at"], 0, r.get("file_id") or ""), r) for r in self._rows()
             if r["file_path"] not in self.feed_omits and (aware or not r.get("deleted")) and (r["updated_at"], r.get("file_id") or "") > (ts, fid)),
            key=lambda kr: kr[0],
        )
        if self.moves_first:
            merged = [("m", k, s, r) for k, s, r in marks] + [("k", k, None, r) for k, r in keyed]
        else:  # ONE causal stream: moves and keyset rows interleaved by time
            merged = sorted([("m", k, s, r) for k, s, r in marks] + [("k", k, None, r) for k, r in keyed],
                            key=lambda e: e[1])
        out, full = merged[:limit], len(merged) > limit
        for kind, key, seq, row in out:
            if kind == "m":
                mpos = seq
            else:
                ts, fid = row["updated_at"], row.get("file_id") or ""
        keyed_left = any(e[0] == "k" for e in merged[limit:])
        nxt = json.dumps({"ts": ts, "id": fid, "d": aware or not keyed_left, "m": mpos})
        return {"files": [e[3] for e in out], "next_cursor": nxt, "has_more": full, "poll_after_seconds": 30}

    async def get(self, path: str) -> bytes:
        self.gets.append(path)
        return self.files[path]["data"]

    async def put(self, path: str, content: bytes, expected_checksum: str | None) -> dict:
        self.puts.append((path, expected_checksum))
        current = self.files.get(path)
        if current is not None and path in self.immutable:
            raise BridgeError(409, {"error": "file_write_conflict"})
        if expected_checksum and current and current["checksum"] != expected_checksum:
            raise BridgeError(412, {"error": "checksum_mismatch"})
        self.cloud_write(path, content)
        return {"id": self.files[path]["file_id"], "file_path": path, "version": 1, "size_bytes": len(content)}

    async def delete(self, path: str) -> None:
        row = self.files.pop(path)
        self.deleted.append({"file_id": row["file_id"], "file_path": path, "deleted": True,
                             "updated_at": self._stamp(), "checksum": row["checksum"]})

    async def session(self) -> dict:
        return {}

    async def still_visible(self, path: str) -> bool | None:
        """The bridge's ``/get`` access gate by path: a live file here, or none (trashed, moved)."""
        return path in self.files


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


def test_a_file_the_person_may_not_write_is_refused_once_not_every_pass(tmp_path: Path) -> None:
    """A 403 on one file's PUT is that file's answer, not the bridge refusing everything:
    the file is listed, the other files still upload, and it is not re-sent until it changes
    (2026-10-31: a 403 aborted the pass and the same file was re-sent every ~5 s for ever)."""
    bridge = FakeBridge()
    bridge.cloud_write("capture.html", b"server made")
    bridge.cloud_write("notes.txt", b"mine")
    sync = _sync(tmp_path, bridge)
    mirror(sync)
    root = tmp_path / "Cloud"
    real_put = bridge.put

    async def put(path: str, content: bytes, expected: str | None) -> dict:
        if path == "capture.html":
            bridge.puts.append((path, expected))
            raise BridgeError(403, {"detail": "lacks 'write' access on file 'x'"})
        return await real_put(path, content, expected)

    bridge.put = put  # type: ignore[method-assign]
    (root / "capture.html").write_bytes(b"touched")
    (root / "notes.txt").write_bytes(b"edited")
    for _ in range(3):
        run(sync.push_once())
    assert [p for p, _ in bridge.puts].count("capture.html") == 1
    assert bridge.files["notes.txt"]["data"] == b"edited"
    assert "capture.html" in sync.status()["skipped"]["items"] or sync.skipped.get("capture.html")
    (root / "capture.html").write_bytes(b"touched again, longer")
    run(sync.push_once())
    assert [p for p, _ in bridge.puts].count("capture.html") == 2


def test_a_refused_file_costs_no_call_on_later_passes(tmp_path: Path) -> None:
    """A file the cloud refused as it is is skipped before the file service is asked about its
    path: a pass made one ``still_visible`` GET per refused file (319 crawl captures live,
    2026-11-02) and a new file waited behind them all (161 s machine -> cloud)."""
    bridge = FakeBridge()
    sync = _sync(tmp_path, bridge)
    mirror(sync)
    root = tmp_path / "Cloud"
    (root / "web-crawls-x").mkdir(parents=True)
    for i in range(5):
        (root / f"web-crawls-x/c{i}.html").write_bytes(b"capture %d" % i)
    asked: list[str] = []

    async def still_visible(path: str) -> bool | None:
        asked.append(path)
        return None  # the file service cannot say

    real_put = bridge.put

    async def put(path: str, content: bytes, expected: str | None) -> dict:
        if path.startswith("web-crawls-x/"):
            bridge.puts.append((path, expected))
            raise BridgeError(403, {"detail": "lacks 'write' access"})
        return await real_put(path, content, expected)

    bridge.still_visible = still_visible  # type: ignore[method-assign]
    bridge.put = put  # type: ignore[method-assign]
    run(sync.push_once())
    assert len(asked) == 5 and len(bridge.puts) == 5
    run(sync.push_once())
    run(sync.push_once())
    assert len(asked) == 5, "a refused file was asked about again"
    assert len(bridge.puts) == 5, "a refused file was sent again"
    (root / "new.txt").write_bytes(b"made on the machine")
    run(sync.push_once())
    assert bridge.files["new.txt"]["data"] == b"made on the machine"


def test_a_refused_file_is_not_sent_again_after_a_restart(tmp_path: Path) -> None:
    """Nothing on the machine changed the file, so nothing is pushed — across a worker restart
    too. The refusal used to live only in memory: every wake (a new task) re-sent each refused
    file once more (319 crawl captures, 2026-11-02). It is persisted with the file's signature;
    an edit after the restart still uploads."""
    bridge = FakeBridge()
    sync = _sync(tmp_path, bridge)
    mirror(sync)
    root = tmp_path / "Cloud"
    (root / "web-crawls-x").mkdir(parents=True)
    for i in range(3):
        (root / f"web-crawls-x/c{i}.html").write_bytes(b"capture %d" % i)

    async def put(path: str, content: bytes, expected: str | None) -> dict:
        bridge.puts.append((path, expected))
        raise BridgeError(403, {"detail": "lacks 'write' access"})

    async def still_visible(path: str) -> bool | None:
        return None

    bridge.put = put  # type: ignore[method-assign]
    bridge.still_visible = still_visible  # type: ignore[method-assign]
    run(sync.push_once())
    assert len(bridge.puts) == 3
    restarted = _sync(tmp_path, bridge)  # a new task: same home, same state, fresh process
    run(restarted.push_once())
    assert len(bridge.puts) == 3, "a refused, unchanged file was sent again after a restart"
    assert len(restarted.skipped) == 3, "a remembered refusal stays listed"
    (root / "web-crawls-x/c0.html").write_bytes(b"edited on the machine")
    run(restarted.push_once())
    assert [p for p, _ in bridge.puts].count("web-crawls-x/c0.html") == 2


# -- one unreadable cloud file never pauses the whole sync (2026-11-16) ------------------------


def _bridge_with_missing_get(status: int) -> tuple[FakeBridge, str]:
    """Three cloud files; the bridge answers ``status`` to the GET of the middle one only."""
    bridge = FakeBridge()
    for name in ("a.pdf", "b.pdf", "c.pdf"):
        bridge.cloud_write(f"library/guideline/{name}", name.encode())
    bad = "library/guideline/b.pdf"
    real_get = bridge.get

    async def get(path: str) -> bytes:
        if path == bad:
            raise BridgeError(status, {"error": "not_found", "message": f"File '{path}' not found"})
        return await real_get(path)

    bridge.get = get  # type: ignore[method-assign]
    return bridge, bad


def test_a_file_the_bridge_404s_stays_a_listed_placeholder_and_the_rest_copy_in(tmp_path: Path) -> None:
    bridge, bad = _bridge_with_missing_get(404)
    sync = _sync(tmp_path, bridge)
    run(sync.pull_once())
    run(sync.fill_copies(limit=10))  # must not raise
    root = tmp_path / "Cloud"
    assert (root / "library/guideline/a.pdf").read_bytes() == b"a.pdf"
    assert (root / "library/guideline/c.pdf").read_bytes() == b"c.pdf"
    assert (root / bad).read_text().startswith(STUB_MAGIC)
    assert bad in sync.skipped and "404" in sync.skipped[bad]
    assert sync.pending_copies() == 0  # not retried every pass


def test_a_404_file_does_not_pause_the_running_sync(tmp_path: Path) -> None:
    bridge, bad = _bridge_with_missing_get(404)
    sync = _sync(tmp_path, bridge, local_scan_seconds=1)

    async def drive() -> None:
        task = asyncio.create_task(sync.run_forever())
        await asyncio.sleep(1.5)
        task.cancel()

    run(drive())
    assert sync.stats.consecutive_failures == 0 and sync.stats.last_push_error is None
    assert sync.stats.failing_since is None


def test_a_bridge_outage_on_a_copy_still_pauses_loudly(tmp_path: Path) -> None:
    bridge, _ = _bridge_with_missing_get(503)
    sync = _sync(tmp_path, bridge)
    run(sync.pull_once())
    with pytest.raises(BridgeError):
        run(sync.fill_copies(limit=10))
