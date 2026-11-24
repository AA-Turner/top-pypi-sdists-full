"""The Cloud folder reads THE device feed: nothing is skipped, moves arrive, outages never stop uploads.

Drives the real ``CloudFilesSync`` against ``FakeBridge``, which answers like BOTH real feeds
over one dataset (the legacy ``/cloud-files/changes`` and ``/cloud-files/sync/changes``), so
every test here fails on the sync that read the legacy feed (sync audit 2026-11-02):

* proof A — 600 cloud files written in one transaction share one ``updated_at``; the old
  timestamp cursor delivered 500 and skipped the rest for good;
* proof B — the placement mover keeps ``updated_at``; the old feed never re-sent a moved
  file, so the old path lingered and the new path never appeared;
* a feed outage aborted the whole pass before the push, so the machine's edits stalled
  silently;
* a file its owner can no longer see (``gone_reason: no_longer_visible`` — organization
  archived, access lost) lingers, or takes an edit made here down with it, or the edit is
  pushed back onto the file the owner cannot see.
"""

from __future__ import annotations

import asyncio
import json
from pathlib import Path

from matrx_scraper.cloud_browser.worker.cloud_files_sync import BridgeError, CloudFilesSync, FEED_NAME

from test_cloud_computer_cloud_files_sync import FakeBridge, _sync, mirror, run


def test_proof_a_six_hundred_files_sharing_one_updated_at_all_reach_the_machine(tmp_path: Path) -> None:
    bridge = FakeBridge()
    same = "2026-10-31T19:00:00.000001+00:00"
    for i in range(600):
        bridge.cloud_write(f"bulk/f{i:04d}.txt", f"{i}".encode(), updated=same)
    sync = _sync(tmp_path, bridge)
    run(sync.pull_once())
    run(sync.pull_once())
    assert len(list((tmp_path / "Cloud/bulk").iterdir())) == 600


def test_proof_b_a_moved_file_appears_at_the_new_path_and_the_old_path_goes(tmp_path: Path) -> None:
    bridge = FakeBridge()
    bridge.cloud_write("Inbox/song.mp3", b"audio")
    sync = _sync(tmp_path, bridge)
    mirror(sync)
    gets_before = list(bridge.gets)
    bridge.cloud_move("Inbox/song.mp3", "Audio/song.mp3")
    run(sync.pull_once())
    root = tmp_path / "Cloud"
    assert (root / "Audio/song.mp3").read_bytes() == b"audio"
    assert not (root / "Inbox/song.mp3").exists()
    assert not (root / "Inbox").exists()  # the empty folder the move left goes too
    assert bridge.gets == gets_before  # renamed by file id, never downloaded again
    run(sync.push_once())
    assert bridge.puts == []  # a move is not an edit


def test_a_local_edit_travels_with_a_cloud_move_and_uploads_at_the_new_path(tmp_path: Path) -> None:
    bridge = FakeBridge()
    bridge.cloud_write("Inbox/notes.txt", b"v1")
    sync = _sync(tmp_path, bridge)
    mirror(sync)
    (tmp_path / "Cloud/Inbox/notes.txt").write_bytes(b"edited on the machine")
    bridge.cloud_move("Inbox/notes.txt", "Docs/notes.txt")
    run(sync.pull_once())
    run(sync.push_once())
    assert bridge.files["Docs/notes.txt"]["data"] == b"edited on the machine"
    assert "Inbox/notes.txt" not in bridge.files


def test_a_folder_left_by_the_old_feed_reconciles_once_and_keeps_local_edits(tmp_path: Path) -> None:
    """Upgrade: a state written against the old timestamp feed holds zombies (moved files at
    their old path). The first pull bootstraps THE feed: the moved files appear at their new
    path, a zombie edited on the machine stays and uploads, and a clean zombie STAYS too — an
    entry without a file id never proves the cloud held those bytes, so nothing removes it on
    an absence or a 404 (gate 2026-11-02, third run)."""
    bridge = FakeBridge()
    bridge.cloud_write("Inbox/a.txt", b"a")
    bridge.cloud_write("Inbox/b.txt", b"b")
    old = _sync(tmp_path, bridge)
    mirror(old)
    # What the old code left: no file ids, a timestamp cursor, then two moves it never saw.
    state = tmp_path / ".matrx/cloud-sync/state.json"
    data = json.loads(state.read_text())
    data.pop("feed", None)
    data["cursor"] = "2026-10-18T12:00:00+00:00"
    for entry in data["files"].values():
        entry["file_id"] = None
    state.write_text(json.dumps(data))
    bridge.cloud_move("Inbox/a.txt", "Audio/a.txt")
    bridge.cloud_move("Inbox/b.txt", "Audio/b.txt")
    (tmp_path / "Cloud/Inbox/b.txt").write_bytes(b"b edited here")

    upgraded = _sync(tmp_path, bridge)
    assert upgraded.cursor is None  # the old cursor is never trusted
    mirror(upgraded)
    run(upgraded.push_once())
    root = tmp_path / "Cloud"
    assert (root / "Audio/a.txt").read_bytes() == b"a"
    assert (root / "Inbox/a.txt").read_bytes() == b"a"  # kept: a duplicate, never a loss
    assert "Inbox/a.txt" not in bridge.files  # and never pushed back
    assert (root / "Inbox/b.txt").read_bytes() == b"b edited here"  # never lost
    assert bridge.files["Inbox/b.txt"]["data"] == b"b edited here"
    assert json.loads(state.read_text())["feed"] == FEED_NAME


def test_a_feed_outage_never_stops_uploads_and_the_server_sees_the_pause(tmp_path: Path) -> None:
    bridge = FakeBridge()
    bridge.cloud_write("notes.txt", b"v1")
    sync = _sync(tmp_path, bridge, local_scan_seconds=1)
    mirror(sync)
    bridge.feed_error = BridgeError(503, {"error": "cloud_file_change_feed_busy"})
    (tmp_path / "Cloud/notes.txt").write_bytes(b"written while the feed is down")

    async def passes(seconds: float) -> None:
        task = asyncio.create_task(sync.run_forever())
        await asyncio.sleep(seconds)
        task.cancel()
        try:
            await task
        except asyncio.CancelledError:
            pass

    run(passes(1.5))
    assert bridge.files["notes.txt"]["data"] == b"written while the feed is down"
    work = sync.work_signals()
    assert work["last_error"].startswith("pull:") and "503" in work["last_error"]
    assert work["consecutive_failures"] >= 1 and work["failing_since"]
    assert work["last_push_at"]

    bridge.feed_error = None
    run(passes(1.5))
    work = sync.work_signals()
    assert work["consecutive_failures"] == 0 and work["failing_since"] is None and work["last_error"] is None
    assert work["last_pull_at"]


def test_the_state_records_which_feed_its_cursor_belongs_to(tmp_path: Path) -> None:
    bridge = FakeBridge()
    bridge.cloud_write("x.txt", b"x")
    sync = _sync(tmp_path, bridge)
    run(sync.pull_once())
    again = CloudFilesSync(tmp_path / "Cloud", bridge, state_dir=tmp_path / ".matrx/cloud-sync")
    assert again.cursor == sync.cursor and again.cursor is not None


def test_files_of_every_organization_the_owner_sees_are_mirrored(tmp_path: Path) -> None:
    bridge = FakeBridge()
    bridge.cloud_write("Home org/a.txt", b"a")
    bridge.cloud_write("Other org/b.txt", b"b")
    for row in bridge.files.values():
        row["organization_id"] = "org-home" if row["file_path"].startswith("Home") else "org-other"
    sync = _sync(tmp_path, bridge)
    mirror(sync)
    assert (tmp_path / "Cloud/Home org/a.txt").read_bytes() == b"a"
    assert (tmp_path / "Cloud/Other org/b.txt").read_bytes() == b"b"


def test_a_file_no_longer_visible_leaves_the_machine(tmp_path: Path) -> None:
    bridge = FakeBridge()
    bridge.cloud_write("Closed/report.txt", b"r")
    bridge.cloud_write("Open/keep.txt", b"k")
    sync = _sync(tmp_path, bridge)
    mirror(sync)
    bridge.cloud_hide("Closed/report.txt")
    run(sync.pull_once())
    run(sync.push_once())
    assert not (tmp_path / "Cloud/Closed/report.txt").exists()
    assert (tmp_path / "Cloud/Open/keep.txt").read_bytes() == b"k"
    assert bridge.puts == []  # a removal the cloud announced is never pushed back


def test_an_edit_to_a_file_no_longer_visible_is_kept_as_its_own_new_file(tmp_path: Path) -> None:
    bridge = FakeBridge()
    bridge.cloud_write("Closed/notes.txt", b"v1")
    sync = _sync(tmp_path, bridge)
    mirror(sync)
    (tmp_path / "Cloud/Closed/notes.txt").write_bytes(b"edited on the machine")
    bridge.cloud_hide("Closed/notes.txt")
    run(sync.pull_once())
    run(sync.push_once())
    assert not (tmp_path / "Cloud/Closed/notes.txt").exists()
    assert "Closed/notes.txt" not in [p for p, _ in bridge.puts]  # never onto the unseen file
    kept = [p for p, _ in bridge.puts]
    assert len(kept) == 1 and bridge.files[kept[0]]["data"] == b"edited on the machine"
    assert (tmp_path / "Cloud" / kept[0]).read_bytes() == b"edited on the machine"
