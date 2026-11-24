"""A stop's final Cloud flush uploads its waiting files side by side, inside its budget.

Live evidence (2026-11-20, machine 488ce713, system_error 971c0173 / dd2fe7c7 / 534a0e50):
three stops in six minutes each filed "8-27 Cloud file(s) had not finished uploading (timed
out)". The pass sent one file at a time — every changed file a full round trip to the bridge
behind the one before — after a first walk of the folder that the flush had just made itself.
With a bridge that takes a moment per upload, a few dozen files outran the 90-second budget.

These tests drive the real ``CloudFilesSync`` with a bridge whose ``put`` takes 0.2 s.
"""

from __future__ import annotations

import asyncio
from pathlib import Path

import pytest

from matrx_scraper.cloud_browser.worker.cloud_files_sync import BridgeError, CloudFilesSync, SyncKnobs

from test_cloud_computer_cloud_files_sync import NOW, FakeBridge, mirror, run

PUT_SECONDS = 0.2
FILES = 20


class SlowBridge(FakeBridge):
    def __init__(self) -> None:
        super().__init__()
        self.in_flight = 0
        self.most_in_flight = 0
        self.fail_with: BridgeError | None = None

    async def put(self, path: str, content: bytes, expected_checksum: str | None) -> dict:
        self.in_flight += 1
        self.most_in_flight = max(self.most_in_flight, self.in_flight)
        try:
            await asyncio.sleep(PUT_SECONDS)
            if self.fail_with is not None:
                raise self.fail_with
            return await super().put(path, content, expected_checksum)
        finally:
            self.in_flight -= 1


def _sync(home: Path, bridge: FakeBridge) -> CloudFilesSync:
    return CloudFilesSync(home / "Cloud", bridge, state_dir=home / ".matrx/cloud-sync",
                          knobs=SyncKnobs(), now=lambda: NOW)


def _edits(home: Path) -> None:
    for i in range(FILES):
        (home / "Cloud" / f"note-{i:02d}.md").write_text(f"edit {i}")


def test_the_final_flush_uploads_a_few_dozen_files_inside_a_short_budget(tmp_path: Path) -> None:
    bridge = SlowBridge()
    bridge.cloud_write("seed.txt", b"seed")
    sync = _sync(tmp_path, bridge)
    mirror(sync)
    _edits(tmp_path)
    # One at a time this is FILES * PUT_SECONDS = 4 s of round trips: past a 2 s budget.
    answer = run(sync.flush(2.0))
    assert answer["flushed"] is True, answer
    assert answer["uploaded"] == FILES
    assert all(bridge.files[f"note-{i:02d}.md"]["data"] == f"edit {i}".encode() for i in range(FILES))
    assert 1 < bridge.most_in_flight <= SyncKnobs().upload_concurrency


def test_a_bridge_outage_still_stops_the_pass_as_itself(tmp_path: Path) -> None:
    bridge = SlowBridge()
    bridge.cloud_write("seed.txt", b"seed")
    sync = _sync(tmp_path, bridge)
    mirror(sync)
    _edits(tmp_path)
    bridge.fail_with = BridgeError(503, {"error": "down"})
    with pytest.raises(BridgeError) as caught:
        run(sync.push_once())
    assert caught.value.status == 503
    assert bridge.in_flight == 0  # the other uploads were stopped, none left running
    # Nothing was recorded as sent: every edit is still waiting for the next pass.
    assert len(run(asyncio.to_thread(sync._unsent))) == FILES
