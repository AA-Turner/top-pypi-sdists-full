"""Raw snapshot headroom is separate from the immutable sanitized upload queue."""

from __future__ import annotations

import json
from contextlib import closing
from pathlib import Path
from types import SimpleNamespace

import pytest

from probe.tap_core import session_journal as sj
from tests import test_backfill_transcripts_upload as fixtures

isolated_state = fixtures.isolated_state


def _ensure(journal, transcript, wire):
    return journal.ensure(
        transcript.session_id,
        transcript.path,
        wire.receipts(transcript.session_id),
        historical=True,
    )


def _disk_space(monkeypatch, free):
    monkeypatch.setattr(sj.shutil, "disk_usage", lambda _path: SimpleNamespace(free=free))


def _append(transcript):
    with transcript.path.open("ab") as handle:
        handle.write(
            json.dumps(
                dict(
                    type="user",
                    sessionId=transcript.session_id,
                    message=dict(role="user", content="later live turn"),
                )
            ).encode()
            + b"\n"
        )


def test_raw_snapshot_larger_than_queue_cap_imports_in_bounded_batches(tmp_path, monkeypatch):
    transcript = fixtures._transcript(tmp_path, lines=48)
    wire = fixtures.FakeWire()
    queue_cap = 4096
    assert transcript.size > queue_cap
    _disk_space(monkeypatch, sj.SNAPSHOT_FREE_RESERVE_BYTES + transcript.size)

    with closing(sj.Journal(wire.base_url, "synthetic", wire.source, cap_bytes=queue_cap)) as journal:
        state = _ensure(journal, transcript, wire)
        assert Path(state["snapshot_path"]).read_bytes() == transcript.path.read_bytes()
        fixtures.drain(journal, transcript, wire)
        assert journal.get(transcript.session_id)["historical_complete"]
        assert len(wire.events) == 48
        assert all(len(body) <= queue_cap for body in wire.accepted.values())


@pytest.mark.parametrize("headroom_delta", [-1, 0])
def test_snapshot_requires_its_full_size_plus_free_space_reserve(
    tmp_path, monkeypatch, headroom_delta
):
    transcript = fixtures._transcript(tmp_path)
    wire = fixtures.FakeWire()
    original = transcript.path.read_bytes()
    _disk_space(monkeypatch, transcript.size + sj.SNAPSHOT_FREE_RESERVE_BYTES + headroom_delta)

    with closing(sj.Journal(wire.base_url, "synthetic", wire.source)) as journal:
        if headroom_delta < 0:
            with pytest.raises(sj.DeliveryPending, match="free disk space.*resume"):
                _ensure(journal, transcript, wire)
            assert journal.get(transcript.session_id) is None
            assert not list(journal.directory.glob("*.snapshot.jsonl"))
            assert not list(journal.directory.glob("tmp*"))
        else:
            state = _ensure(journal, transcript, wire)
            assert Path(state["snapshot_path"]).read_bytes() == original
        assert transcript.path.read_bytes() == original
        assert journal.pending(transcript.session_id) is None
        assert wire.calls == []


def test_disk_pressure_preserves_pending_snapshot_and_queue_cap(tmp_path, monkeypatch):
    first = fixtures._transcript(tmp_path)
    second = fixtures._transcript(tmp_path)
    wire = fixtures.FakeWire()
    _disk_space(monkeypatch, 2 * sj.SNAPSHOT_FREE_RESERVE_BYTES)

    with closing(fixtures.journal_for(first, wire)) as journal:
        assert journal.cap_bytes == 100 * 1024 * 1024
        pending = journal.stage(first.session_id, cwd=first.cwd, max_body_bytes=2600)
        before = journal.get(first.session_id)
        snapshot = Path(before["snapshot_path"])
        contents = snapshot.read_bytes()

        _disk_space(monkeypatch, second.size + sj.SNAPSHOT_FREE_RESERVE_BYTES - 1)
        with pytest.raises(sj.DeliveryPending, match="free disk space"):
            _ensure(journal, second, wire)
        assert snapshot.read_bytes() == contents
        assert journal.pending(first.session_id) == pending
        assert journal.get(first.session_id) == before

        # Existing files already consume filesystem space. Their sizes must not
        # be deducted a second time from the available headroom for this copy.
        _disk_space(monkeypatch, second.size + sj.SNAPSHOT_FREE_RESERVE_BYTES)
        journal.cap_bytes = len(pending)
        _ensure(journal, second, wire)
        with pytest.raises(sj.DeliveryPending, match="queue full"):
            journal.stage(second.session_id, cwd=second.cwd, max_body_bytes=2600)
        assert snapshot.read_bytes() == contents
        assert journal.pending(first.session_id) == pending
        assert journal.pending(second.session_id) is None


@pytest.mark.parametrize("fresh_device", [False, True])
def test_finalized_receipt_needs_no_snapshot_allocation_on_retry(
    tmp_path, monkeypatch, fresh_device
):
    transcript = fixtures._transcript(tmp_path)
    wire = fixtures.FakeWire()
    with closing(fixtures.journal_for(transcript, wire)) as journal:
        fixtures.drain(journal, transcript, wire)
        snapshot = Path(journal.get(transcript.session_id)["snapshot_path"])
        journal.release_snapshot(transcript.session_id)
        assert not snapshot.exists()
    accepted = dict(wire.accepted)

    def no_allocation(*_args, **_kwargs):
        pytest.fail("an unchanged finalized transcript must not allocate another raw snapshot")

    monkeypatch.setattr(sj.tempfile, "mkstemp", no_allocation)
    _disk_space(monkeypatch, 0)
    directory = tmp_path / "other-device" if fresh_device else None
    with closing(sj.Journal(wire.base_url, "synthetic", wire.source, directory=directory)) as journal:
        state = _ensure(journal, transcript, wire)
        assert state["historical_complete"]
        assert state["historical_end"] == transcript.size
        fixtures.drain(journal, transcript, wire)
        assert wire.accepted == accepted
        assert not list(journal.directory.glob("*.snapshot.jsonl"))


def test_snapshot_gc_reclaims_only_completed_sessions_without_pending(tmp_path, monkeypatch):
    complete = fixtures._transcript(tmp_path)
    pending = fixtures._transcript(tmp_path)
    unread = fixtures._transcript(tmp_path)
    next_session = fixtures._transcript(tmp_path)
    wire = fixtures.FakeWire()
    _disk_space(monkeypatch, 2 * sj.SNAPSHOT_FREE_RESERVE_BYTES)

    with closing(fixtures.journal_for(complete, wire)) as journal:
        _ensure(journal, pending, wire)
        _ensure(journal, unread, wire)
        complete_copy = Path(journal.get(complete.session_id)["snapshot_path"])
        pending_copy = Path(journal.get(pending.session_id)["snapshot_path"])
        unread_copy = Path(journal.get(unread.session_id)["snapshot_path"])
        body = journal.stage(pending.session_id, cwd=pending.cwd, max_body_bytes=2600)
        fixtures.drain(journal, complete, wire)
        assert complete_copy.exists()  # Crash before release_snapshot would leave this copy.

        _ensure(journal, next_session, wire)
        assert not complete_copy.exists()
        assert pending_copy.read_bytes() == pending.path.read_bytes()
        assert unread_copy.read_bytes() == unread.path.read_bytes()
        assert journal.pending(pending.session_id) == body


def test_completed_snapshot_with_pending_live_tail_is_not_reclaimed(tmp_path, monkeypatch):
    transcript = fixtures._transcript(tmp_path)
    other = fixtures._transcript(tmp_path)
    wire = fixtures.FakeWire()
    _disk_space(monkeypatch, 2 * sj.SNAPSHOT_FREE_RESERVE_BYTES)

    with closing(fixtures.journal_for(transcript, wire)) as journal:
        snapshot = Path(journal.get(transcript.session_id)["snapshot_path"])
        original = snapshot.read_bytes()
        fixtures.drain(journal, transcript, wire)
        _append(transcript)
        body = journal.stage(transcript.session_id, cwd=transcript.cwd)
        assert body is not None
        assert journal.get(transcript.session_id)["historical_complete"]

        _ensure(journal, other, wire)
        assert snapshot.read_bytes() == original
        assert journal.pending(transcript.session_id) == body


@pytest.mark.parametrize("delivery", ["unread", "pending", "acknowledged"])
def test_missing_snapshot_restores_saved_prefix_without_importing_appended_tail(
    tmp_path, monkeypatch, delivery
):
    transcript = fixtures._transcript(tmp_path)
    wire = fixtures.FakeWire()
    original = transcript.path.read_bytes()
    with closing(fixtures.journal_for(transcript, wire)) as journal:
        if delivery != "unread":
            journal.stage(transcript.session_id, cwd=transcript.cwd, max_body_bytes=2600)
            if delivery == "acknowledged":
                journal.deliver(transcript.session_id, wire)
        before = journal.get(transcript.session_id)
        pending = journal.pending(transcript.session_id)
        Path(before["snapshot_path"]).unlink()
    _append(transcript)
    # Enough room for the saved prefix, but not the larger source with its new tail.
    _disk_space(monkeypatch, len(original) + sj.SNAPSHOT_FREE_RESERVE_BYTES)

    with closing(sj.Journal(wire.base_url, "synthetic", wire.source)) as journal:
        state = _ensure(journal, transcript, wire)
        assert state["historical_end"] == before["historical_end"] == len(original)
        assert state["historical_hash"] == before["historical_hash"]
        assert Path(state["snapshot_path"]).read_bytes() == original
        assert journal.pending(transcript.session_id) == pending
        fixtures.drain(journal, transcript, wire)
        assert journal.get(transcript.session_id)["historical_complete"]
        assert len(wire.events) == 12
        assert b"later live turn" not in b"".join(wire.accepted.values())
        assert transcript.path.stat().st_size > state["historical_end"]


@pytest.mark.parametrize("acknowledged", [False, True])
def test_missing_snapshot_cannot_repin_a_changed_unread_tail(tmp_path, monkeypatch, acknowledged):
    transcript = fixtures._transcript(tmp_path)
    wire = fixtures.FakeWire()
    original = transcript.path.read_bytes()
    _disk_space(monkeypatch, 2 * sj.SNAPSHOT_FREE_RESERVE_BYTES)

    with closing(fixtures.journal_for(transcript, wire)) as journal:
        body = journal.stage(transcript.session_id, cwd=transcript.cwd, max_body_bytes=2600)
        assert json.loads(body)["source_byte_end"] < original.index(b"turn 11")
        if acknowledged:
            journal.deliver(transcript.session_id, wire)
        before = journal.get(transcript.session_id)
        pending = journal.pending(transcript.session_id)
        Path(before["snapshot_path"]).unlink()
        transcript.path.write_bytes(original.replace(b"turn 11", b"edit 11"))

        with pytest.raises(sj.ReconciliationRequired, match="pinned historical snapshot"):
            _ensure(journal, transcript, wire)
        assert journal.get(transcript.session_id) == before
        assert journal.pending(transcript.session_id) == pending
        assert not list(journal.directory.glob("*.snapshot.jsonl"))
        assert not list(journal.directory.glob("tmp*"))

        transcript.path.write_bytes(original)
        _ensure(journal, transcript, wire)
        fixtures.drain(journal, transcript, wire)
        assert journal.get(transcript.session_id)["historical_complete"]
        assert len(wire.events) == 12


@pytest.mark.parametrize("missing_copy", [False, True])
@pytest.mark.parametrize("conflict", ["boundary", "hash"])
def test_remote_pin_conflict_preserves_local_snapshot_and_pending(
    tmp_path, monkeypatch, missing_copy, conflict
):
    transcript = fixtures._transcript(tmp_path)
    wire = fixtures.FakeWire()
    _disk_space(monkeypatch, 2 * sj.SNAPSHOT_FREE_RESERVE_BYTES)

    with closing(fixtures.journal_for(transcript, wire)) as journal:
        journal.stage(transcript.session_id, cwd=transcript.cwd, max_body_bytes=2600)
        journal.deliver(transcript.session_id, wire)
        pending = journal.stage(transcript.session_id, cwd=transcript.cwd, max_body_bytes=2600)
        before = journal.get(transcript.session_id)
        snapshot = Path(before["snapshot_path"])
        contents = snapshot.read_bytes()
        if missing_copy:
            snapshot.unlink()
        wire.streams[transcript.session_id].update(
            snapshot_byte_end=before["historical_end"] - (conflict == "boundary"),
            snapshot_sha256="0" * 64 if conflict == "hash" else before["historical_hash"],
        )

        with pytest.raises(sj.ReconciliationRequired, match="local pinned prefix"):
            _ensure(journal, transcript, wire)
        assert journal.get(transcript.session_id) == before
        assert journal.pending(transcript.session_id) == pending
        if missing_copy:
            assert not snapshot.exists()
        else:
            assert snapshot.read_bytes() == contents
