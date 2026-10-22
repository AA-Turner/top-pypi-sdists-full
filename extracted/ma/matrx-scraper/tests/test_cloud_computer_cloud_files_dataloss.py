"""A restore that partly fails never turns into a cloud delete, and the delete-rate
window survives a worker restart (adversarial review 3, 2026-10-21: D1, D4).

Each test drives the real ``CloudFilesSync`` against the in-memory bridge of
``test_cloud_computer_cloud_files_sync``. On the module before this fix
(origin/main at 5603dca18d) the D1 tests fail: ``_restore`` cleared the hold even
for the files it could not bring back, so the next scans sent them to the cloud
trash with no person click; the D4 test fails because the window lived in memory.
"""

from __future__ import annotations

from datetime import timedelta
from pathlib import Path

from matrx_scraper.cloud_browser.worker.cloud_files_sync import BridgeError, CloudFilesSync, SyncKnobs

from test_cloud_computer_cloud_files_sync import NOW, FakeBridge, _sync, mirror, run


class FlakyBridge(FakeBridge):
    """Downloads of the paths in ``broken`` fail like a cloud 5xx."""

    def __init__(self) -> None:
        super().__init__()
        self.broken: set[str] = set()

    async def get(self, path: str) -> bytes:
        if path in self.broken:
            raise BridgeError(503, {"error": "unavailable"})
        return await super().get(path)


def _push(sync: CloudFilesSync, times: int = 1) -> None:
    for _ in range(times):
        run(sync.push_once())


def _hold_five(tmp_path: Path, bridge: FakeBridge, **kw) -> CloudFilesSync:
    for i in range(10):
        bridge.cloud_write(f"docs/{i}.txt", f"doc {i}".encode())
    sync = kw.pop("sync", None) or _sync(tmp_path, bridge, max_deletes_per_pass=3)
    mirror(sync)
    for i in range(5):
        (tmp_path / f"Cloud/docs/{i}.txt").unlink()
    _push(sync, times=3)
    assert sync.halt and sync.halt["reason"] == "mass_delete" and len(bridge.files) == 10
    return sync


def test_files_a_restore_could_not_bring_back_stay_held_and_are_never_deleted(tmp_path: Path) -> None:
    bridge = FlakyBridge()
    sync = _hold_five(tmp_path, bridge)
    bridge.broken = {"docs/0.txt", "docs/1.txt"}
    answer = run(sync.resolve_held(sync.halt["hold_id"], "restore"))
    assert answer["restored"] == 3
    assert sync.halt and sync.halt["reason"] == "restore_failed" and sync.halt["held"] == 2
    _push(sync, times=6)  # fewer than the cap: before the fix these went to the cloud trash
    assert len(bridge.files) == 10, "a failed restore turned into a cloud delete"
    assert sync.halt and sync.halt["held"] == 2
    bridge.broken = set()  # the cloud answers again: the retry brings them back
    _push(sync)
    assert sync.halt is None
    assert all((tmp_path / f"Cloud/docs/{i}.txt").exists() for i in range(5))
    _push(sync, times=3)
    assert len(bridge.files) == 10


def test_the_automatic_restore_takes_the_same_safe_path(tmp_path: Path) -> None:
    bridge = FlakyBridge()
    clock = {"now": NOW}
    sync = CloudFilesSync(tmp_path / "Cloud", bridge, state_dir=tmp_path / ".matrx/cloud-sync",
                          knobs=SyncKnobs(max_deletes_per_pass=3, held_delete_restore_after_seconds=3600),
                          now=lambda: clock["now"])
    _hold_five(tmp_path, bridge, sync=sync)
    bridge.broken = {"docs/4.txt"}
    clock["now"] = NOW + timedelta(hours=1, seconds=1)
    _push(sync)
    assert sync.stats.auto_restored == 4 and sync.halt and sync.halt["paths"] == ["docs/4.txt"]
    _push(sync, times=6)
    assert "docs/4.txt" in bridge.files, "the automatic restore deleted a file it could not restore"


def test_the_unrestored_hold_survives_a_worker_restart(tmp_path: Path) -> None:
    bridge = FlakyBridge()
    sync = _hold_five(tmp_path, bridge)
    bridge.broken = {"docs/0.txt", "docs/1.txt"}
    run(sync.resolve_held(sync.halt["hold_id"], "restore"))
    again = _sync(tmp_path, bridge, max_deletes_per_pass=3)  # a new process, same home
    _push(again, times=6)
    assert len(bridge.files) == 10 and again.halt and again.halt["held"] == 2


def test_the_person_can_still_delete_what_could_not_be_restored(tmp_path: Path) -> None:
    bridge = FlakyBridge()
    sync = _hold_five(tmp_path, bridge)
    bridge.broken = {"docs/0.txt", "docs/1.txt"}
    run(sync.resolve_held(sync.halt["hold_id"], "restore"))
    answer = run(sync.resolve_held(sync.halt["hold_id"], "delete"))
    assert answer["deleted"] == 2 and sync.halt is None
    assert sorted(bridge.files) == [f"docs/{i}.txt" for i in range(2, 10)]


def test_the_delete_window_survives_a_worker_restart(tmp_path: Path) -> None:
    bridge = FakeBridge()
    for i in range(10):
        bridge.cloud_write(f"docs/{i}.txt", f"doc {i}".encode())
    sync = _sync(tmp_path, bridge, max_deletes_per_pass=3, delete_window_seconds=600)
    mirror(sync)
    for i in range(2):
        (tmp_path / f"Cloud/docs/{i}.txt").unlink()
    _push(sync, times=2)
    assert len(bridge.files) == 8
    again = _sync(tmp_path, bridge, max_deletes_per_pass=3, delete_window_seconds=600)
    for i in range(2, 4):
        (tmp_path / f"Cloud/docs/{i}.txt").unlink()
    _push(again, times=2)
    assert len(bridge.files) == 8, "a restart reset the delete window"
    assert again.halt and again.halt["reason"] == "mass_delete"
