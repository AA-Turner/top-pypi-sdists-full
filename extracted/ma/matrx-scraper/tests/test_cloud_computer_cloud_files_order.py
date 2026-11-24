"""The Cloud folder applies cloud changes by file id, in causal order, and never half-moves.

Reproductions from the independent review of the device-feed sync (2026-11-02). Each drove
the real ``CloudFilesSync`` against ``FakeBridge`` and failed on the first sync of THE feed:

1. while the machine slept, X at a path was deleted and Y moved onto that path: the feed
   served the move first, the sync turned X into a conflict copy (resurrecting it in the
   cloud), then X's tombstone deleted Y by path;
2. a swap through a temp name uploaded a spurious conflict copy;
3. a tombstone for a file the machine does not hold (another organization's row at the same
   path) deleted the machine's own file by path;
4. a relocation that failed midway dropped the old path's record, so the next push uploaded
   the moved file again at its old path.

Every ordering test runs against both servers: the causal stream (moves and keyset rows
interleaved by time) and the first server that served all moves first. The client must be
right under both.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from matrx_scraper.cloud_browser.worker.cloud_files_sync import STUB_MAGIC, BridgeError, CloudFilesSync

from test_cloud_computer_cloud_files_sync import FakeBridge, _sync, mirror, run

ORDERS = pytest.mark.parametrize("moves_first", [False, True], ids=["causal", "moves-first"])


def cloud_delete(bridge: FakeBridge, path: str) -> None:
    row = bridge.files.pop(path)
    bridge.deleted.append({"file_id": row["file_id"], "file_path": path, "deleted": True,
                           "updated_at": bridge._stamp(), "checksum": row["checksum"]})


def attempt(coro) -> None:
    """One pass that may meet a bridge failure (the loop retries it next pass)."""
    try:
        run(coro)
    except BridgeError:
        pass


def local_files(root: Path) -> list[str]:
    return sorted(str(p.relative_to(root)) for p in root.rglob("*") if p.is_file())


@ORDERS
def test_1_asleep_delete_then_move_into_the_same_path(tmp_path: Path, moves_first: bool) -> None:
    b = FakeBridge()
    b.moves_first = moves_first
    b.cloud_write("Docs/report.txt", b"X old report")
    b.cloud_write("Inbox/report.txt", b"Y new report")
    s = _sync(tmp_path, b)
    mirror(s)
    cloud_delete(b, "Docs/report.txt")
    b.cloud_move("Inbox/report.txt", "Docs/report.txt")
    run(s.pull_once())
    run(s.push_once())
    root = tmp_path / "Cloud"
    assert (root / "Docs/report.txt").read_bytes() == b"Y new report", local_files(root)
    assert [p for p in b.files if "conflict" in p] == [], "the deleted file came back as a conflict copy"
    assert sorted(b.files) == ["Docs/report.txt"]
    assert local_files(root) == ["Docs/report.txt"]
    run(s.pull_once())
    run(s.push_once())
    assert local_files(root) == ["Docs/report.txt"]


@ORDERS
def test_2_a_swap_through_a_temp_name_uploads_nothing(tmp_path: Path, moves_first: bool) -> None:
    b = FakeBridge()
    b.moves_first = moves_first
    b.cloud_write("a.txt", b"AAA")
    b.cloud_write("b.txt", b"BBB")
    s = _sync(tmp_path, b)
    mirror(s)
    gets = list(b.gets)
    b.cloud_move("a.txt", "tmp.txt")
    b.cloud_move("b.txt", "a.txt")
    b.cloud_move("tmp.txt", "b.txt")
    run(s.pull_once())
    run(s.push_once())
    root = tmp_path / "Cloud"
    assert (root / "a.txt").read_bytes() == b"BBB" and (root / "b.txt").read_bytes() == b"AAA"
    assert not [p for p in b.files if "conflict" in p], "a swap uploaded a spurious conflict copy"
    assert b.puts == [] and b.gets == gets  # renamed by file id: no upload, no download
    assert local_files(root) == ["a.txt", "b.txt"]


@ORDERS
def test_2b_an_edit_travels_through_a_swap(tmp_path: Path, moves_first: bool) -> None:
    b = FakeBridge()
    b.moves_first = moves_first
    b.cloud_write("a.txt", b"AAA")
    b.cloud_write("b.txt", b"BBB")
    s = _sync(tmp_path, b)
    mirror(s)
    (tmp_path / "Cloud/b.txt").write_bytes(b"BBB edited here")
    b.cloud_move("a.txt", "tmp.txt")
    b.cloud_move("b.txt", "a.txt")
    b.cloud_move("tmp.txt", "b.txt")
    run(s.pull_once())
    run(s.push_once())
    assert b.files["a.txt"]["data"] == b"BBB edited here" and b.files["b.txt"]["data"] == b"AAA"
    assert not [p for p in b.files if "conflict" in p]


@ORDERS
def test_2c_a_move_onto_a_placeholder_leaves_no_junk(tmp_path: Path, moves_first: bool) -> None:
    b = FakeBridge()
    b.moves_first = moves_first
    b.cloud_write("big.bin", b"x" * 5000)  # a placeholder on the machine
    b.cloud_write("Inbox/big.bin", b"y" * 10)
    s = _sync(tmp_path, b, mirror_max_file_bytes=1000)
    mirror(s)
    assert (tmp_path / "Cloud/big.bin").read_text().startswith(STUB_MAGIC)
    cloud_delete(b, "big.bin")
    b.cloud_move("Inbox/big.bin", "big.bin")
    run(s.pull_once())
    run(s.push_once())
    root = tmp_path / "Cloud"
    assert local_files(root) == ["big.bin"] and (root / "big.bin").read_bytes() == b"y" * 10
    assert sorted(b.files) == ["big.bin"]
    assert not list((tmp_path / ".matrx/cloud-sync").glob("parked/*"))


def test_3_a_tombstone_for_a_file_not_held_never_deletes_another_file_at_that_path(tmp_path: Path) -> None:
    b = FakeBridge()
    b.cloud_write("Images/logo.png", b"org A logo")
    s = _sync(tmp_path, b)
    mirror(s)
    # Another organization's row at the same path, stated gone for this machine, another id.
    b.deleted.append({"file_id": "orgB-1", "file_path": "Images/logo.png", "deleted": True,
                      "updated_at": b._stamp(), "checksum": "zzz"})
    run(s.pull_once())
    run(s.push_once())
    assert "Images/logo.png" in b.files
    assert (tmp_path / "Cloud/Images/logo.png").read_bytes() == b"org A logo"


class FlakyPut(FakeBridge):
    fail_conflict = True

    async def put(self, path, content, expected_checksum):
        if "conflict" in path and self.fail_conflict:
            self.fail_conflict = False
            raise BridgeError(503, "busy")
        return await super().put(path, content, expected_checksum)


@ORDERS
def test_4_a_failed_conflict_upload_never_re_uploads_the_moved_file_at_its_old_path(
    tmp_path: Path, moves_first: bool
) -> None:
    b = FlakyPut()
    b.moves_first = moves_first
    b.cloud_write("Inbox/x.txt", b"X")
    b.cloud_write("Docs/x.txt", b"other")
    s = _sync(tmp_path, b)
    mirror(s)
    (tmp_path / "Cloud/Docs/x.txt").write_bytes(b"other edited")  # edited here, deleted there
    cloud_delete(b, "Docs/x.txt")
    b.cloud_move("Inbox/x.txt", "Docs/x.txt")
    for _ in range(3):
        attempt(s.pull_once())
        attempt(s.push_once())
    assert "Inbox/x.txt" not in b.files, "the moved file was re-uploaded at its old path"
    assert b.files["Docs/x.txt"]["data"] == b"X"
    kept = [p for p in b.files if "conflict" in p]
    assert len(kept) == 1 and b.files[kept[0]]["data"] == b"other edited"  # the edit is never lost


def test_4b_a_relocation_that_cannot_be_written_keeps_the_old_record(tmp_path: Path) -> None:
    b = FakeBridge()
    b.cloud_write("Inbox/x.txt", b"X")
    s = _sync(tmp_path, b)
    mirror(s)
    (tmp_path / "Cloud/Docs").write_bytes(b"a file where the folder must go")  # the move fails
    b.cloud_move("Inbox/x.txt", "Docs/x.txt")
    run(s.pull_once())
    run(s.push_once())
    assert "Inbox/x.txt" not in b.files and "Inbox/x.txt" in s.entries
    (tmp_path / "Cloud/Docs").unlink()
    run(s.pull_once())  # the row was kept to retry
    run(s.push_once())
    assert (tmp_path / "Cloud/Docs/x.txt").read_bytes() == b"X"
    assert not (tmp_path / "Cloud/Inbox/x.txt").exists() and "Inbox/x.txt" not in b.files


def test_5_an_interrupted_bootstrap_keeps_a_new_local_file(tmp_path: Path) -> None:
    b = FakeBridge()
    for i in range(3):
        b.cloud_write(f"d/{i}.txt", f"{i}".encode())
    old = _sync(tmp_path, b)
    mirror(old)
    st = tmp_path / ".matrx/cloud-sync/state.json"
    data = json.loads(st.read_text())
    data.pop("feed", None)
    data.pop("feed_cursor", None)
    data["cursor"] = "2026-10-18T12:00:00+00:00"
    for e in data["files"].values():
        e["file_id"] = None
    st.write_text(json.dumps(data))
    s = _sync(tmp_path, b)
    calls = {"n": 0}
    orig = b.sync_changes

    async def flaky(cursor, limit):
        calls["n"] += 1
        if calls["n"] == 2:
            raise BridgeError(503, "busy")
        return await orig(cursor, 2)

    b.sync_changes = flaky
    attempt(s.pull_once())
    (tmp_path / "Cloud/new.txt").write_bytes(b"person's new file")
    run(s.push_once())
    run(s.pull_once())
    assert (tmp_path / "Cloud/new.txt").exists() and b.files["new.txt"]["data"] == b"person's new file"


def test_7_an_older_image_reads_an_iso_cursor_after_a_rollback(tmp_path: Path) -> None:
    """The old image reads ``state['cursor']`` as an ISO ``since`` for the legacy feed: an opaque
    cursor there answered 400 and stopped its pull and push. The new feed's cursor lives in its
    own key; ``cursor`` is an ISO watermark or absent."""
    from datetime import datetime

    b = FakeBridge()
    b.cloud_write("a.txt", b"a")
    s = _sync(tmp_path, b)
    mirror(s)
    data = json.loads((tmp_path / ".matrx/cloud-sync/state.json").read_text())
    assert data.get("cursor") is None or datetime.fromisoformat(data["cursor"])
    assert data["cursor"] == b.files["a.txt"]["updated_at"]
    assert data["feed_cursor"] == s.cursor
    again = CloudFilesSync(tmp_path / "Cloud", b, state_dir=tmp_path / ".matrx/cloud-sync")
    assert again.cursor == s.cursor


def test_7b_a_state_from_the_first_feed_image_keeps_its_cursor(tmp_path: Path) -> None:
    b = FakeBridge()
    b.cloud_write("a.txt", b"a")
    s = _sync(tmp_path, b)
    mirror(s)
    st = tmp_path / ".matrx/cloud-sync/state.json"
    data = json.loads(st.read_text())
    data["cursor"] = data.pop("feed_cursor")  # what the first feed image wrote
    st.write_text(json.dumps(data))
    again = CloudFilesSync(tmp_path / "Cloud", b, state_dir=tmp_path / ".matrx/cloud-sync")
    assert again.cursor == s.cursor


def test_first_sync_reports_running_until_the_tree_is_read(tmp_path: Path) -> None:
    b = FakeBridge()
    b.cloud_write("a.txt", b"a")
    s = _sync(tmp_path, b)
    assert s.work_signals()["first_sync_running"] is True
    run(s.pull_once())
    assert s.work_signals()["first_sync_running"] is False
