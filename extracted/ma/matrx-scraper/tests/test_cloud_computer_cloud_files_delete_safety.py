"""The Cloud folder sync never destroys a person's cloud files (review D6, 2026-10-18).

Break (code-read): ``_local_files`` returned an empty set for a missing root and
skipped unreadable folders silently; ``push_once`` then deleted every cloud file
it could not see, with no ceiling, in one 5 s scan. A network-drive hiccup, a
mount not ready at wake, or a restore in progress would empty the person's cloud.

Every test drives the real ``CloudFilesSync`` against the in-memory bridge of
``test_cloud_computer_cloud_files_sync`` and fails on the pre-fix module.
"""

from __future__ import annotations

import asyncio
import json
import os
import shutil
from pathlib import Path

import pytest

from matrx_scraper.cloud_browser.worker.cloud_files_sync import STUB_MAGIC, CloudFilesSync

from test_cloud_computer_cloud_files_sync import FakeBridge, _sync, mirror, run


def _tree(bridge: FakeBridge, n: int = 6) -> list[str]:
    paths = [f"projects/p{i}/notes.txt" for i in range(n)] + ["top.txt"]
    for p in paths:
        bridge.cloud_write(p, f"real {p}".encode())
    return paths


def _push(sync: CloudFilesSync, times: int = 1) -> None:
    for _ in range(times):
        try:
            run(sync.push_once())
        except Exception:  # noqa: BLE001 - a refusing pass is fine; what matters is the cloud
            pass


def test_ghost_empty_folder_replay_deletes_nothing_and_holds(tmp_path: Path) -> None:
    """Replay: the Cloud folder reads empty for a while (drive hiccup, restore in
    progress), then the files are back. Nothing may be deleted in the cloud."""
    bridge = FakeBridge()
    paths = _tree(bridge)
    sync = _sync(tmp_path, bridge)
    mirror(sync)
    root = tmp_path / "Cloud"
    aside = tmp_path / "aside"
    os.replace(root, aside)
    root.mkdir()  # the folder is there but reads empty
    _push(sync, times=3)
    assert sorted(bridge.files) == sorted(paths), "a ghost empty folder deleted cloud files"
    assert sync.halt and sync.halt["reason"] == "folder_unhealthy"
    assert sync.status()["work"]["deletes_held"] == len(paths)
    root.rmdir()
    os.replace(aside, root)  # the drive is back
    _push(sync, times=2)
    assert sorted(bridge.files) == sorted(paths)
    assert sync.halt is None


def test_a_missing_cloud_folder_deletes_nothing(tmp_path: Path) -> None:
    bridge = FakeBridge()
    paths = _tree(bridge)
    sync = _sync(tmp_path, bridge)
    mirror(sync)
    shutil.rmtree(tmp_path / "Cloud")
    _push(sync, times=3)
    assert sorted(bridge.files) == sorted(paths)


@pytest.mark.skipif(os.geteuid() == 0, reason="root reads any folder")
def test_an_unreadable_folder_deletes_nothing(tmp_path: Path) -> None:
    bridge = FakeBridge()
    paths = _tree(bridge)
    sync = _sync(tmp_path, bridge)
    mirror(sync)
    locked = tmp_path / "Cloud/projects/p3"
    locked.chmod(0)
    try:
        _push(sync, times=3)
    finally:
        locked.chmod(0o755)
    assert sorted(bridge.files) == sorted(paths)


def test_a_mass_delete_is_held_until_the_person_confirms_it(tmp_path: Path) -> None:
    bridge = FakeBridge()
    for i in range(10):
        bridge.cloud_write(f"docs/{i}.txt", f"doc {i}".encode())
    sync = _sync(tmp_path, bridge, max_deletes_per_pass=3)
    mirror(sync)
    for i in range(5):  # rm of five files; the folder still holds five
        (tmp_path / f"Cloud/docs/{i}.txt").unlink()
    _push(sync, times=3)
    assert len(bridge.files) == 10, "a delete over the cap reached the cloud"
    assert sync.halt and sync.halt["reason"] == "mass_delete" and sync.halt["held"] == 5
    answer = run(sync.resolve_held(sync.halt["hold_id"], "delete"))
    assert answer["resolved"] and answer["deleted"] == 5
    assert sorted(bridge.files) == [f"docs/{i}.txt" for i in range(5, 10)]
    lines = [json.loads(x) for x in (tmp_path / ".matrx/cloud-sync/deleted.jsonl").read_text().splitlines()]
    assert sorted(x["path"] for x in lines) == [f"docs/{i}.txt" for i in range(5)]
    assert all(x["checksum"] for x in lines)
    assert sync.halt is None


def test_a_held_delete_stays_held_in_a_new_process(tmp_path: Path) -> None:
    bridge = FakeBridge()
    for i in range(10):
        bridge.cloud_write(f"docs/{i}.txt", f"doc {i}".encode())
    sync = _sync(tmp_path, bridge, max_deletes_per_pass=3)
    mirror(sync)
    for i in range(5):
        (tmp_path / f"Cloud/docs/{i}.txt").unlink()
    _push(sync, times=2)
    fresh = _sync(tmp_path, bridge, max_deletes_per_pass=3)  # a new task
    _push(fresh, times=3)
    assert len(bridge.files) == 10
    assert fresh.halt and fresh.halt["reason"] == "mass_delete"


def test_one_real_delete_reaches_the_cloud_and_is_written_down(tmp_path: Path) -> None:
    bridge = FakeBridge()
    paths = _tree(bridge)
    sync = _sync(tmp_path, bridge)
    mirror(sync)
    (tmp_path / "Cloud/projects/p1/notes.txt").unlink()  # its folder is now empty: one file, fine
    (tmp_path / "Cloud/top.txt").unlink()
    _push(sync, times=2)
    assert sorted(bridge.files) == sorted(set(paths) - {"projects/p1/notes.txt", "top.txt"})
    assert sync.halt is None
    log = (tmp_path / ".matrx/cloud-sync/deleted.jsonl").read_text()
    assert "projects/p1/notes.txt" in log and "top.txt" in log


def test_a_file_the_walk_skips_is_never_deleted_from_the_cloud(tmp_path: Path) -> None:
    bridge = FakeBridge()
    for name in (".env", "draft.tmp", "notes.txt~", "keep.txt"):
        bridge.cloud_write(name, f"real {name}".encode())
    sync = _sync(tmp_path, bridge)
    mirror(sync)
    _push(sync, times=3)
    assert sorted(bridge.files) == [".env", "draft.tmp", "keep.txt", "notes.txt~"]


def test_a_newer_cloud_version_is_never_erased_by_a_local_delete(tmp_path: Path) -> None:
    bridge = FakeBridge()
    bridge.cloud_write("plan.txt", b"v1")
    bridge.cloud_write("other.txt", b"other")
    sync = _sync(tmp_path, bridge)
    mirror(sync)
    (tmp_path / "Cloud/plan.txt").unlink()
    bridge.cloud_write("plan.txt", b"v2 written in the web app")
    try:
        mirror(sync)
    except Exception:  # noqa: BLE001
        pass
    _push(sync, times=2)
    assert bridge.files["plan.txt"]["data"] == b"v2 written in the web app"
    assert (tmp_path / "Cloud/plan.txt").read_bytes() == b"v2 written in the web app"


def test_a_placeholder_is_never_uploaded_over_the_real_file(tmp_path: Path) -> None:
    bridge = FakeBridge()
    real = b"R" * 5000
    bridge.cloud_write("video/big.bin", real)
    sync = _sync(tmp_path, bridge, mirror_max_file_bytes=1000)
    mirror(sync)
    stub = tmp_path / "Cloud/video/big.bin"
    assert stub.read_text().startswith(STUB_MAGIC)
    with stub.open("a") as fh:
        fh.write("a line a script appended to the placeholder\n")
    _push(sync, times=2)
    assert bridge.files["video/big.bin"]["data"] == real


def test_a_lost_sync_state_never_overwrites_a_local_edit(tmp_path: Path) -> None:
    bridge = FakeBridge()
    bridge.cloud_write("report.txt", b"cloud copy")
    sync = _sync(tmp_path, bridge)
    mirror(sync)
    (tmp_path / "Cloud/report.txt").write_bytes(b"edit made on the machine, not yet uploaded")
    shutil.rmtree(tmp_path / ".matrx/cloud-sync")  # the state is gone (new home, restore)
    fresh = _sync(tmp_path, bridge)
    mirror(fresh)
    root = tmp_path / "Cloud"
    kept = [p.read_bytes() for p in root.rglob("*") if p.is_file()]
    assert b"edit made on the machine, not yet uploaded" in kept
    assert any(f["data"] == b"edit made on the machine, not yet uploaded" for f in bridge.files.values())


def test_an_unknown_local_file_matching_the_cloud_is_adopted_not_rewritten(tmp_path: Path) -> None:
    bridge = FakeBridge()
    bridge.cloud_write("same.txt", b"identical")
    (tmp_path / "Cloud").mkdir()
    (tmp_path / "Cloud/same.txt").write_bytes(b"identical")
    sync = _sync(tmp_path, bridge)
    mirror(sync)
    _push(sync, times=2)
    assert bridge.puts == [] and not any("conflict" in p for p in bridge.files)


def test_two_conflicts_in_the_same_second_keep_both_copies(tmp_path: Path) -> None:
    bridge = FakeBridge()
    bridge.cloud_write("plan.txt", b"base")
    sync = _sync(tmp_path, bridge)  # the clock is frozen: both conflicts share one stamp
    mirror(sync)
    root = tmp_path / "Cloud"
    (root / "plan.txt").write_bytes(b"machine edit 1")
    bridge.cloud_write("plan.txt", b"cloud edit 1")
    mirror(sync)
    (root / "plan.txt").write_bytes(b"machine edit 2")
    bridge.cloud_write("plan.txt", b"cloud edit 2")
    mirror(sync)
    copies = sorted(p.read_bytes() for p in root.glob("plan (conflict from Cloud Computer *).txt"))
    assert copies == [b"machine edit 1", b"machine edit 2"]
    cloud = {f["data"] for f in bridge.files.values()}
    assert {b"machine edit 1", b"machine edit 2"} <= cloud


def test_an_upload_in_flight_is_reported_as_work(tmp_path: Path) -> None:
    """D7 needs this: the build move asks the sync whether a transfer is running."""
    bridge = FakeBridge()
    gate = asyncio.Event()
    started = asyncio.Event()
    seen: list[dict] = []
    sync = _sync(tmp_path, bridge)
    mirror(sync)
    real_put = bridge.put

    async def slow_put(path, content, expected):
        seen.append(dict(sync.work_signals()))
        started.set()
        await gate.wait()
        return await real_put(path, content, expected)

    bridge.put = slow_put  # type: ignore[method-assign]
    (tmp_path / "Cloud").mkdir(exist_ok=True)
    (tmp_path / "Cloud/new.txt").write_bytes(b"uploading")

    async def scenario() -> None:
        task = asyncio.create_task(sync.push_once())
        await asyncio.wait_for(started.wait(), 5)
        gate.set()
        await task

    run(scenario())
    assert seen[0]["transfers"] == 1 and seen[0]["pending_uploads"] == 1
    assert sync.work_signals()["transfers"] == 0 and sync.work_signals()["pending_uploads"] == 0
