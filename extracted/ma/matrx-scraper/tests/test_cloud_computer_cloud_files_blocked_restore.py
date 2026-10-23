"""A restore that does not put the exact file back never becomes a cloud delete
(live, 2026-10-22, image f9b5a9e7d1: FIX-DELETE-SAFETY-SERVER-2026-10-22).

Live scenario: 30 files in ``~/Cloud/cc-held-test`` were held; an agent made
directories at ``f03.txt`` and ``f04.txt``; the person's restore answered
``restored: 28`` and the hold cleared. The two blocked files were treated as
"skipped", left the hold, and once the directories were removed the next push
deleted them from the cloud (404). Before this fix the tests below fail.
Class: every "skipped / not a file / could not read" outcome during a hold is
"not restored" (stays held, retried), never "absent → delete".
"""

from __future__ import annotations

import shutil
from pathlib import Path

from matrx_scraper.cloud_browser.worker.cloud_files_sync import CloudFilesSync

from test_cloud_computer_cloud_files_sync import FakeBridge, _sync, mirror, run

FOLDER = "cc-held-test"
NAMES = [f"{FOLDER}/f{i:02d}.txt" for i in range(30)]


def _push(sync: CloudFilesSync, times: int = 1) -> None:
    for _ in range(times):
        run(sync.push_once())


def _held_folder(tmp_path: Path, bridge: FakeBridge) -> CloudFilesSync:
    for rel in NAMES:
        bridge.cloud_write(rel, rel.encode())
    sync = _sync(tmp_path, bridge)
    mirror(sync)
    shutil.rmtree(tmp_path / "Cloud" / FOLDER)
    _push(sync, times=3)
    assert sync.halt and sync.halt["held"] == 30 and len(bridge.files) == 30
    return sync


def _block(tmp_path: Path, *names: str) -> None:
    for n in names:
        (tmp_path / "Cloud" / FOLDER / n).mkdir(parents=True)


def _unblock(tmp_path: Path, *names: str) -> None:
    for n in names:
        (tmp_path / "Cloud" / FOLDER / n).rmdir()


def test_the_live_scenario_blocked_targets_stay_held_and_are_never_deleted(tmp_path: Path) -> None:
    bridge = FakeBridge()
    sync = _held_folder(tmp_path, bridge)
    _block(tmp_path, "f03.txt", "f04.txt")
    answer = run(sync.resolve_held(sync.halt["hold_id"], "restore"))
    assert answer["restored"] == 28
    assert sync.halt and sync.halt["reason"] == "restore_failed"
    assert sorted(sync.halt["paths"]) == [f"{FOLDER}/f03.txt", f"{FOLDER}/f04.txt"]
    _push(sync, times=4)  # still blocked: held, retried, nothing sent
    assert sync.halt and sync.halt["held"] == 2 and len(bridge.files) == 30
    _unblock(tmp_path, "f03.txt", "f04.txt")
    _push(sync, times=6)  # before the fix: these passes deleted f03/f04 in the cloud
    assert len(bridge.files) == 30, "a blocked restore turned into a cloud delete"
    assert (tmp_path / "Cloud" / FOLDER / "f03.txt").read_bytes() == f"{FOLDER}/f03.txt".encode()
    assert sync.halt is None


def test_blocked_targets_stay_held_across_a_worker_restart(tmp_path: Path) -> None:
    bridge = FakeBridge()
    sync = _held_folder(tmp_path, bridge)
    _block(tmp_path, "f03.txt", "f04.txt")
    run(sync.resolve_held(sync.halt["hold_id"], "restore"))
    again = _sync(tmp_path, bridge)
    _push(again, times=2)
    _unblock(tmp_path, "f03.txt", "f04.txt")
    _push(again, times=6)
    assert len(bridge.files) == 30


def test_a_symlink_at_the_target_is_not_a_restore(tmp_path: Path) -> None:
    bridge = FakeBridge()
    sync = _held_folder(tmp_path, bridge)
    (tmp_path / "Cloud" / FOLDER).mkdir()
    (tmp_path / "elsewhere").write_text("x")
    (tmp_path / "Cloud" / FOLDER / "f07.txt").symlink_to(tmp_path / "elsewhere")
    answer = run(sync.resolve_held(sync.halt["hold_id"], "restore"))
    assert answer["restored"] == 29 and sync.halt["paths"] == [f"{FOLDER}/f07.txt"]
    (tmp_path / "Cloud" / FOLDER / "f07.txt").unlink()
    _push(sync, times=6)
    assert len(bridge.files) == 30


class OddBridge(FakeBridge):
    """A download that fails with an error the sync has no name for."""

    def __init__(self) -> None:
        super().__init__()
        self.odd: set[str] = set()

    async def get(self, path: str) -> bytes:
        if path in self.odd:
            raise RuntimeError("unexpected")
        return await super().get(path)


def test_any_error_during_restore_keeps_the_file_held(tmp_path: Path) -> None:
    bridge = OddBridge()
    sync = _held_folder(tmp_path, bridge)
    sync.knobs.mirror_max_file_bytes = 10**9  # copies, so the bridge is called
    bridge.odd = {f"{FOLDER}/f09.txt"}
    for e in sync.entries.values():
        e.stub = False
    answer = run(sync.resolve_held(sync.halt["hold_id"], "restore"))
    assert answer["restored"] == 29 and sync.halt["paths"] == [f"{FOLDER}/f09.txt"]
    _push(sync, times=6)
    assert len(bridge.files) == 30
