"""A held delete is resolvable by the person, one bad entry never stalls the
sync, and an edit during a transfer is never lost (review 2 N2, N3, N4, N8).

Every test drives the real ``CloudFilesSync`` against the in-memory bridge of
``test_cloud_computer_cloud_files_sync`` and fails on the module at ``bb8bd53f2f``:
it had no ``resolve_held``, held for ever, recorded an edit made during an upload
as synced, and a symlink out of ``~/Cloud`` raised on every pass.
"""

from __future__ import annotations

import os
from datetime import timedelta
from pathlib import Path

import pytest

from matrx_scraper.cloud_browser.worker.cloud_files_sync import (
    STUB_MAGIC,
    BridgeError,
    CloudFilesSync,
    HoldChanged,
    SyncKnobs,
)

from test_cloud_computer_cloud_files_sync import NOW, FakeBridge, _sync, mirror, run


def _push(sync: CloudFilesSync, times: int = 1) -> None:
    for _ in range(times):
        run(sync.push_once())


def _held_mass_delete(tmp_path: Path, bridge: FakeBridge, **knobs: int) -> CloudFilesSync:
    for i in range(10):
        bridge.cloud_write(f"docs/{i}.txt", f"doc {i}".encode())
    sync = _sync(tmp_path, bridge, max_deletes_per_pass=3, **knobs)
    mirror(sync)
    for i in range(5):
        (tmp_path / f"Cloud/docs/{i}.txt").unlink()
    _push(sync, times=3)
    assert sync.halt and sync.halt["reason"] == "mass_delete" and len(bridge.files) == 10
    return sync


def test_the_person_sees_the_hold_without_the_full_path_list(tmp_path: Path) -> None:
    sync = _held_mass_delete(tmp_path, FakeBridge())
    view = sync.status()["halt"]
    assert view["held"] == 5 and view["hold_id"] and "paths" not in view
    assert view["restores_at"] > view["since"]
    work = sync.work_signals()
    assert work["hold_id"] == view["hold_id"] and work["deletes_held"] == 5


def test_restore_brings_the_held_files_back_and_clears_the_hold(tmp_path: Path) -> None:
    bridge = FakeBridge()
    sync = _held_mass_delete(tmp_path, bridge)
    answer = run(sync.resolve_held(sync.halt["hold_id"], "restore"))
    assert answer == {"resolved": True, "action": "restore", "restored": 5}
    for i in range(5):
        assert (tmp_path / f"Cloud/docs/{i}.txt").read_bytes() == f"doc {i}".encode()
    assert sync.halt is None
    _push(sync, times=3)
    assert len(bridge.files) == 10 and sync.halt is None


def test_delete_sends_exactly_the_held_set_and_nothing_new(tmp_path: Path) -> None:
    bridge = FakeBridge()
    sync = _held_mass_delete(tmp_path, bridge)
    hold_id = sync.halt["hold_id"]
    # A file deleted AFTER the person saw the hold is not part of their answer.
    (tmp_path / "Cloud/docs/9.txt").unlink()
    answer = run(sync.resolve_held(hold_id, "delete"))
    assert answer["deleted"] == 5
    assert sorted(bridge.files) == [f"docs/{i}.txt" for i in range(5, 10)]


def test_an_answer_to_a_different_hold_is_refused(tmp_path: Path) -> None:
    sync = _held_mass_delete(tmp_path, FakeBridge())
    with pytest.raises(HoldChanged):
        run(sync.resolve_held("not-this-hold", "delete"))


def test_a_legitimately_emptied_folder_can_be_deleted_by_the_person(tmp_path: Path) -> None:
    bridge = FakeBridge()
    for name in ("old/a.txt", "old/b.txt", "old/c.txt", "keep.txt"):
        bridge.cloud_write(name, name.encode())
    sync = _sync(tmp_path, bridge)
    mirror(sync)
    for name in ("a", "b", "c"):
        (tmp_path / f"Cloud/old/{name}.txt").unlink()  # the folder is empty now, on purpose
    _push(sync, times=3)
    assert sync.halt and sync.halt["reason"] == "folder_unhealthy" and len(bridge.files) == 4
    run(sync.resolve_held(sync.halt["hold_id"], "delete"))
    assert sorted(bridge.files) == ["keep.txt"] and sync.halt is None


def test_an_unanswered_hold_restores_itself_after_the_window(tmp_path: Path) -> None:
    bridge = FakeBridge()
    clock = {"now": NOW}
    for i in range(10):
        bridge.cloud_write(f"docs/{i}.txt", f"doc {i}".encode())
    sync = CloudFilesSync(tmp_path / "Cloud", bridge, state_dir=tmp_path / ".matrx/cloud-sync",
                          knobs=SyncKnobs(max_deletes_per_pass=3, held_delete_restore_after_seconds=3600),
                          now=lambda: clock["now"])
    mirror(sync)
    for i in range(5):
        (tmp_path / f"Cloud/docs/{i}.txt").unlink()
    _push(sync, times=3)
    assert sync.halt is not None
    clock["now"] = NOW + timedelta(minutes=59)
    _push(sync)
    assert sync.halt is not None, "restored before the window"
    clock["now"] = NOW + timedelta(hours=1, seconds=1)
    _push(sync)
    assert sync.halt is None and sync.stats.auto_restored == 5
    assert all((tmp_path / f"Cloud/docs/{i}.txt").exists() for i in range(5))
    _push(sync, times=3)
    assert len(bridge.files) == 10, "the restore turned into a delete"


def test_deletes_dripped_a_few_per_pass_are_still_held(tmp_path: Path) -> None:
    bridge = FakeBridge()
    for i in range(10):
        bridge.cloud_write(f"docs/{i}.txt", f"doc {i}".encode())
    sync = _sync(tmp_path, bridge, max_deletes_per_pass=3, delete_window_seconds=600)
    mirror(sync)
    for i in range(2):
        (tmp_path / f"Cloud/docs/{i}.txt").unlink()
    _push(sync, times=2)
    assert len(bridge.files) == 8  # two individual deletes: fine
    for i in range(2, 4):
        (tmp_path / f"Cloud/docs/{i}.txt").unlink()
    _push(sync, times=2)
    assert len(bridge.files) == 8, "a slow drip passed the cap"
    assert sync.halt and sync.halt["reason"] == "mass_delete"


def test_an_edit_made_during_the_upload_is_uploaded_too(tmp_path: Path) -> None:
    bridge = FakeBridge()
    bridge.cloud_write("notes.txt", b"v0")
    sync = _sync(tmp_path, bridge)
    mirror(sync)
    target = tmp_path / "Cloud/notes.txt"
    target.write_bytes(b"v1")
    real_put = bridge.put

    async def racing_put(path, content, expected):
        answer = await real_put(path, content, expected)
        if content == b"v1":
            target.write_bytes(b"v2 written while v1 uploaded")
            st = target.stat()
            os.utime(target, ns=(st.st_atime_ns, st.st_mtime_ns + 1_000_000))
        return answer

    bridge.put = racing_put
    _push(sync)
    assert bridge.files["notes.txt"]["data"] == b"v1"
    _push(sync)
    assert bridge.files["notes.txt"]["data"] == b"v2 written while v1 uploaded", "the edit was lost"


def test_a_write_during_a_download_is_never_overwritten(tmp_path: Path) -> None:
    bridge = FakeBridge()
    bridge.cloud_write("big.bin", b"x" * 100)
    sync = _sync(tmp_path, bridge, mirror_max_file_bytes=10)
    mirror(sync)
    stub = tmp_path / "Cloud/big.bin"
    assert stub.read_text().startswith(STUB_MAGIC)
    real_get = bridge.get

    async def racing_get(path):
        data = await real_get(path)
        stub.write_bytes(b"the person's own words")
        return data

    bridge.get = racing_get
    run(sync.hydrate("big.bin"))
    assert stub.read_bytes() == b"the person's own words"
    bridge.get = real_get
    _push(sync)
    assert bridge.files["big.bin"]["data"] == b"the person's own words"


def test_a_symlink_out_of_the_folder_is_skipped_and_the_rest_keeps_syncing(tmp_path: Path) -> None:
    bridge = FakeBridge()
    bridge.cloud_write("docs/a.txt", b"a")
    sync = _sync(tmp_path, bridge)
    mirror(sync)
    outside = tmp_path / "Downloads"
    outside.mkdir()
    (outside / "secret.txt").write_text("not cloud")
    (tmp_path / "Cloud/dl").symlink_to(outside, target_is_directory=True)
    (tmp_path / "Cloud/link.txt").symlink_to(outside / "secret.txt")
    (tmp_path / "Cloud/new.txt").write_text("new")
    _push(sync, times=2)
    assert bridge.files["new.txt"]["data"] == b"new", "one symlink stalled every upload"
    assert "link.txt" not in bridge.files and not any(p.startswith("dl/") for p in bridge.files)
    skipped = {i["path"] for i in sync.status()["skipped"]["items"]}
    assert {"dl", "link.txt"} <= skipped


def test_a_folder_replaced_by_a_symlink_never_stalls_the_pull_or_reads_as_deleted(tmp_path: Path) -> None:
    bridge = FakeBridge()
    bridge.cloud_write("proj/a.txt", b"a")
    bridge.cloud_write("proj/b.txt", b"b")
    bridge.cloud_write("other.txt", b"o")
    sync = _sync(tmp_path, bridge)
    mirror(sync)
    outside = tmp_path / "elsewhere"
    os.replace(tmp_path / "Cloud/proj", outside)
    (tmp_path / "Cloud/proj").symlink_to(outside, target_is_directory=True)
    bridge.cloud_write("proj/c.txt", b"c")  # a cloud change under the link
    bridge.cloud_write("other.txt", b"o2")  # and one elsewhere
    run(sync.pull_once())
    assert (tmp_path / "Cloud/other.txt").read_bytes() == b"o2", "the pull stalled on the link"
    _push(sync, times=3)
    assert {"proj/a.txt", "proj/b.txt"} <= set(bridge.files), "files under a link read as deleted"


def test_one_file_the_cloud_refuses_never_stalls_the_others(tmp_path: Path) -> None:
    bridge = FakeBridge()
    sync = _sync(tmp_path, bridge)
    mirror(sync)
    (tmp_path / "Cloud").mkdir(exist_ok=True)
    (tmp_path / "Cloud/huge.bin").write_bytes(b"too big")
    (tmp_path / "Cloud/fine.txt").write_text("fine")
    real_put = bridge.put
    calls: list[str] = []

    async def picky_put(path, content, expected):
        calls.append(path)
        if path == "huge.bin":
            raise BridgeError(413, {"error": "too_large"})
        return await real_put(path, content, expected)

    bridge.put = picky_put
    _push(sync, times=3)
    assert bridge.files["fine.txt"]["data"] == b"fine"
    assert calls.count("huge.bin") == 1, "a refused file was re-sent every pass"
    assert sync.skipped["huge.bin"].startswith("cloud refused")
