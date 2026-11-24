"""A file in the Cloud folder is never removed because a listing left it out.

Carry-over gate, 2026-11-02 (ECS task 099b8506…): admin's machine was saved and stopped on an
image that read the old ``/cloud-files/changes`` feed, then woke on the image that reads THE
device feed. Its first pull bootstrapped THE feed and removed every file the old feed had
mirrored that the bootstrap did not deliver — 12 live, visible files: eight recording chunks
under ``.matrx-tmp/transcripts/`` (THE feed leaves dot folders out) and four crawl captures
(THE feed leaves crawl artifacts out). Their ``files.files`` rows were alive. Rows stamped in
the feed's last 10 s are left out the same way, so any file arriving during a stop was at risk.

The law these tests hold: a local file leaves only when the file service SAYS it is gone
(a tombstone, ``no_longer_visible``, or "no live file at this path" when asked) — never
because a feed or bootstrap omitted it. Drives the real ``CloudFilesSync`` against
``FakeBridge`` (both feeds over one dataset, ``feed_omits`` = what THE feed leaves out).
"""

from __future__ import annotations

import json
from pathlib import Path

from test_cloud_computer_cloud_files_sync import FakeBridge, _sync, mirror, run

CHUNK = ".matrx-tmp/transcripts/chunk_rec_1793621141339_b1ur9u_0000.webm"
CAPTURE = "web-crawls-884d1ce8/7aed3443/sessions/faea4e60/captures/815ddb3d/body.md"


def _as_old_feed_state(home: Path) -> None:
    """What the image on the old timestamp feed leaves: no file ids, no ``feed``, an ISO cursor."""
    state = home / ".matrx/cloud-sync/state.json"
    data = json.loads(state.read_text())
    data.pop("feed", None)
    data.pop("feed_cursor", None)
    data["cursor"] = "2026-11-02T12:15:00+00:00"
    for entry in data["files"].values():
        entry["file_id"] = None
    state.write_text(json.dumps(data))


def test_an_upgrade_bootstrap_never_removes_a_visible_file_the_feed_leaves_out(tmp_path: Path) -> None:
    bridge = FakeBridge()
    bridge.cloud_write("Notes/plan.txt", b"plan")
    bridge.cloud_write(CHUNK, b"recording chunk 0")
    bridge.cloud_write(CAPTURE, b"# captured page")
    bridge.cloud_write("Inbox/moved.txt", b"moved")
    bridge.cloud_write("Inbox/trashed.txt", b"trashed")
    old = _sync(tmp_path, bridge)
    mirror(old)  # the base image mirrored all of them
    _as_old_feed_state(tmp_path)
    # While the machine was stopped: one file moved, one trashed; THE feed leaves two out.
    bridge.cloud_move("Inbox/moved.txt", "Archive/moved.txt")
    run(bridge.delete("Inbox/trashed.txt"))
    bridge.feed_omits |= {CHUNK, CAPTURE}

    upgraded = _sync(tmp_path, bridge)
    assert upgraded.cursor is None  # the candidate bootstraps THE feed
    mirror(upgraded)
    run(upgraded.push_once())
    run(upgraded.push_once())
    root = tmp_path / "Cloud"
    # Left out of the listing, still the owner's live files: kept, byte for byte.
    assert (root / CHUNK).read_bytes() == b"recording chunk 0"
    assert (root / CAPTURE).read_bytes() == b"# captured page"
    assert upgraded.stats.kept_unlisted == 4
    # No live file at these paths, but an entry without a file id never proves the cloud held
    # these bytes: they stay (third gate run), and are never pushed back.
    assert (root / "Inbox/moved.txt").read_bytes() == b"moved" and (root / "Archive/moved.txt").read_bytes() == b"moved"
    assert (root / "Inbox/trashed.txt").read_bytes() == b"trashed"
    assert "Inbox/moved.txt" not in bridge.files and "Inbox/trashed.txt" not in bridge.files
    # Nothing was pushed back or deleted in the cloud on the way.
    assert CHUNK in bridge.files and CAPTURE in bridge.files
    assert all(p not in (CHUNK, CAPTURE) for p, _ in bridge.puts)


def test_an_unknown_answer_keeps_the_file(tmp_path: Path) -> None:
    """The cloud could not say (a bridge without the question, an outage): the file stays."""
    bridge = FakeBridge()
    bridge.cloud_write(CHUNK, b"recording chunk 0")
    mirror(_sync(tmp_path, bridge))
    _as_old_feed_state(tmp_path)
    bridge.feed_omits.add(CHUNK)

    async def cannot_say(path: str) -> bool | None:
        return None

    bridge.still_visible = cannot_say  # type: ignore[method-assign]
    upgraded = _sync(tmp_path, bridge)
    mirror(upgraded)
    assert (tmp_path / "Cloud" / CHUNK).read_bytes() == b"recording chunk 0"


def test_a_parked_file_whose_move_is_not_served_yet_is_never_removed(tmp_path: Path) -> None:
    """A file set aside because another file took its path stays set aside until its OWN
    change says where it went — a drained feed that has not served that move yet is not a
    tombstone (the move ledger and the keyset are served with a lag)."""
    bridge = FakeBridge()
    bridge.cloud_write("a.txt", b"first")
    sync = _sync(tmp_path, bridge)
    mirror(sync)
    bridge.cloud_move("a.txt", "Later/a.txt")
    late_mark = bridge.moves.pop()  # the move exists; the feed has not served it yet
    bridge.cloud_write("a.txt", b"second file at the same path")
    run(sync.pull_once())
    assert (tmp_path / "Cloud/a.txt").read_bytes() == b"second file at the same path"
    bridge.moves.append(late_mark)
    run(sync.pull_once())
    assert (tmp_path / "Cloud/Later/a.txt").read_bytes() == b"first"
    assert bridge.gets.count("Later/a.txt") == 0  # renamed by file id, never lost and refetched


def test_the_http_bridge_says_gone_only_for_a_plain_not_found() -> None:
    """``HttpBridge.still_visible`` reads the real bridge's ``/get`` answers: only FastAPI's plain
    404 (no live file at the path) is "gone"; a 404 for missing storage bytes (the row lives —
    this copy may be the last), a 403 and a 5xx are "cannot say"."""
    import asyncio

    import httpx

    from matrx_scraper.cloud_browser.worker.cloud_files_sync import HttpBridge

    answers = {
        "live.txt": httpx.Response(200, content=b"bytes never read"),
        "gone.txt": httpx.Response(404, json={"detail": "File not found: gone.txt"}),
        "nobytes.txt": httpx.Response(404, json={"detail": {"error": "storage_object_missing"}}),
        "denied.txt": httpx.Response(403, json={"detail": "forbidden"}),
        "busy.txt": httpx.Response(503, json={"detail": "busy"}),
    }

    def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.path == "/cloud-files/get"
        return answers[request.url.params["path"]]

    async def ask() -> dict[str, bool | None]:
        client = httpx.AsyncClient(transport=httpx.MockTransport(handler))
        bridge = HttpBridge("https://bridge.test", "a.b.c", client=client)
        return {p: await bridge.still_visible(p) for p in answers}

    assert asyncio.run(ask()) == {"live.txt": True, "gone.txt": False, "nobytes.txt": None,
                                  "denied.txt": None, "busy.txt": None}


# ── a file the sync keeps but does not manage is never uploaded as found ────────────
#
# Carry-over gate re-run, 2026-11-02 (ECS task cb7f33a3…): the candidate's first push uploaded
# 40 "(conflict from Cloud Computer …)" rows for crawl captures under ``web-crawls-…/sessions/
# 80358ad6…``. The machine held bytes at those paths that no sync ever placed (THE feed never
# delivers crawl captures; the older image's watermark skipped them), so the state did not
# know them; the push read "unknown local file" as "new here", put it, the immutable capture
# answered 409, and a conflict copy was uploaded beside it.

CRAWL = "web-crawls-884d1ce8/7aed3443/sessions/80358ad6/pages/0f19b745/captures/e9cdb60c/body.html"


def _unmanaged_machine(tmp_path: Path) -> tuple[FakeBridge, object]:
    bridge = FakeBridge()
    bridge.cloud_write("Notes/plan.txt", b"plan")
    bridge.cloud_write(CRAWL, b"<html>capture as stored</html>")
    bridge.immutable.add(CRAWL)
    bridge.feed_omits.add(CRAWL)
    sync = _sync(tmp_path, bridge)
    mirror(sync)
    # Bytes at the capture's path the sync never placed (another fetch of the same page).
    (tmp_path / "Cloud" / CRAWL).parent.mkdir(parents=True, exist_ok=True)
    (tmp_path / "Cloud" / CRAWL).write_bytes(b"<html>another fetch of the page</html>")
    return bridge, sync


def test_an_unmanaged_file_found_on_the_machine_is_never_uploaded(tmp_path: Path) -> None:
    bridge, sync = _unmanaged_machine(tmp_path)
    run(sync.push_once())
    run(sync.push_once())
    assert bridge.puts == []  # no put at the path, no conflict copy beside it
    assert not [p for p in bridge.files if "conflict" in p]
    assert (tmp_path / "Cloud" / CRAWL).read_bytes() == b"<html>another fetch of the page</html>"
    assert bridge.files[CRAWL]["data"] == b"<html>capture as stored</html>"
    assert "does not manage" in sync.skipped[CRAWL]
    flushed = run(sync.flush(5))
    assert flushed.get("left", 0) == 0 and bridge.puts == []  # the stop's flush waits on nothing


def test_an_edit_made_after_it_was_found_still_uploads(tmp_path: Path) -> None:
    bridge, sync = _unmanaged_machine(tmp_path)
    run(sync.push_once())
    (tmp_path / "Cloud" / CRAWL).write_bytes(b"<html>edited here on purpose</html>")
    run(sync.push_once())
    kept = [p for p in bridge.files if "conflict" in p]
    assert len(kept) == 1 and bridge.files[kept[0]]["data"] == b"<html>edited here on purpose</html>"
    assert bridge.files[CRAWL]["data"] == b"<html>capture as stored</html>"


def test_a_new_local_file_where_no_cloud_file_lives_still_uploads(tmp_path: Path) -> None:
    bridge = FakeBridge()
    bridge.cloud_write("Notes/plan.txt", b"plan")
    sync = _sync(tmp_path, bridge)
    mirror(sync)
    (tmp_path / "Cloud/Recordings/new.webm").parent.mkdir(parents=True)
    (tmp_path / "Cloud/Recordings/new.webm").write_bytes(b"new recording")
    run(sync.push_once())
    assert bridge.files["Recordings/new.webm"]["data"] == b"new recording"


def test_when_the_feed_starts_managing_the_path_the_found_bytes_are_never_overwritten(tmp_path: Path) -> None:
    bridge, sync = _unmanaged_machine(tmp_path)
    bridge.immutable.clear()
    run(sync.push_once())
    bridge.feed_omits.clear()
    bridge.cloud_write(CRAWL, b"<html>a newer cloud version</html>")
    run(sync.pull_once())
    root = tmp_path / "Cloud"
    assert (root / CRAWL).read_bytes() == b"<html>a newer cloud version</html>"
    kept = [p for p in bridge.files if "conflict" in p]
    assert len(kept) == 1 and bridge.files[kept[0]]["data"] == b"<html>another fetch of the page</html>"


# ── a file the cloud never confirmed holding is never removed ─────────────────────────
#
# Gate, third run 2026-11-02 (ECS task 3a820dbc…): 20 conflict copies (body … .md and
# screenshot … .png) made by the previous candidate's wake were "uploaded" without any cloud
# row; the state recorded them as synced. The next candidate bootstrapped, asked the file
# service, got "no file at that path", and removed them as clean copies. The cloud never held
# them, so the machine held the only copy.


class _NoRowPut(FakeBridge):
    """A put the bridge answers without naming a cloud row (nothing was stored)."""

    def __init__(self, paths: set[str]) -> None:
        super().__init__()
        self.no_row = paths

    async def put(self, path: str, content: bytes, expected_checksum: str | None) -> dict:
        if path in self.no_row:
            self.puts.append((path, expected_checksum))
            return {"file_path": path, "version": 1, "size_bytes": len(content)}
        return await super().put(path, content, expected_checksum)


def test_an_upload_without_a_cloud_row_is_never_recorded_as_synced(tmp_path: Path) -> None:
    new = "Notes/draft.md"
    bridge = _NoRowPut({new})
    bridge.cloud_write("Notes/plan.txt", b"plan")
    sync = _sync(tmp_path, bridge)
    mirror(sync)
    (tmp_path / "Cloud" / new).write_bytes(b"only on this machine")
    run(sync.push_once())
    assert new not in sync.entries  # not synced: nothing proves the cloud holds it
    assert "424" in sync.skipped[new]
    # A re-read of the whole tree (state reset to an upgrade) never removes it.
    _as_old_feed_state(tmp_path)
    upgraded = _sync(tmp_path, bridge)
    mirror(upgraded)
    run(upgraded.push_once())
    assert (tmp_path / "Cloud" / new).read_bytes() == b"only on this machine"


def test_a_file_the_old_state_recorded_but_the_cloud_never_held_survives_the_upgrade(tmp_path: Path) -> None:
    """The exact third-run shape: the state says synced (no file id), the cloud has no file there."""
    junk = CRAWL.replace("body.html", "body (conflict from Cloud Computer 2026-11-02 135501).md")
    bridge = FakeBridge()
    bridge.cloud_write("Notes/plan.txt", b"plan")
    sync = _sync(tmp_path, bridge)
    mirror(sync)
    (tmp_path / "Cloud" / junk).parent.mkdir(parents=True, exist_ok=True)
    (tmp_path / "Cloud" / junk).write_bytes(b"# a conflict copy the cloud never took")
    run(sync.push_once())
    bridge.files.pop(junk)  # the cloud never kept it
    _as_old_feed_state(tmp_path)
    upgraded = _sync(tmp_path, bridge)
    mirror(upgraded)
    run(upgraded.push_once())
    assert (tmp_path / "Cloud" / junk).read_bytes() == b"# a conflict copy the cloud never took"


def test_a_tombstone_for_other_bytes_never_removes_an_entry_without_a_file_id(tmp_path: Path) -> None:
    bridge = FakeBridge()
    bridge.cloud_write("Notes/a.txt", b"cloud bytes")
    sync = _sync(tmp_path, bridge)
    mirror(sync)
    sync.entries["Notes/a.txt"].file_id = None  # as the old feed left it
    (tmp_path / "Cloud/Notes/a.txt").write_bytes(b"local bytes the cloud never had")
    st = (tmp_path / "Cloud/Notes/a.txt").stat()
    e = sync.entries["Notes/a.txt"]
    import hashlib
    e.local_sha = e.remote_checksum = hashlib.sha256(b"local bytes the cloud never had").hexdigest()
    e.local_size, e.local_mtime = st.st_size, st.st_mtime
    run(bridge.delete("Notes/a.txt"))  # a tombstone at the path, for the cloud's own bytes
    run(sync.pull_once())
    assert (tmp_path / "Cloud/Notes/a.txt").read_bytes() == b"local bytes the cloud never had"
