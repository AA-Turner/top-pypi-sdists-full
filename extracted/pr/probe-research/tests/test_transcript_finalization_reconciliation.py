"""An accepted completion can unblock a stale control without dropping data."""

import copy
import hashlib
import json
from types import SimpleNamespace

import pytest

from probe.cli import backfill_transcripts as bt
from probe.tap_core import session_journal as sj
from test_backfill_transcripts_upload import FakeWire, _transcript


@pytest.fixture
def stale(tmp_path):
    transcript = _transcript(tmp_path)
    wire = FakeWire()
    journal = sj.Journal(wire.base_url, "synthetic", transcript.agent, directory=tmp_path / "journal")
    journal.ensure(transcript.session_id, transcript.path, wire.receipts(transcript.session_id), historical=True)
    assert journal.stage(transcript.session_id, cwd=transcript.cwd)
    journal.deliver(transcript.session_id, wire)
    pending = journal.stage(transcript.session_id, cwd=transcript.cwd)
    assert json.loads(pending)["finalize"]
    # Another producer attests the same boundary with different metadata,
    # retaining the unfinished snapshot's required identity fields.
    accepted = json.loads(pending)
    accepted["cwd"] = "/other-producer"
    assert wire.post(sj.canonical_payload(accepted))[0] == 202
    assert wire.post(pending)[0] == 409
    try:
        yield transcript, journal, wire, pending
    finally:
        journal.close()


def _append(transcript):
    with transcript.path.open("ab") as handle:
        handle.write(json.dumps({
            "type": "user", "sessionId": transcript.session_id,
            "message": {"role": "user", "content": "New approved work"},
        }).encode() + b"\n")


def test_reconcile_accepted_finalize_then_upload_new_tail_once(stale):
    transcript, journal, wire, pending = stale
    previous = journal.get(transcript.session_id)
    _append(transcript)
    record = bt.SessionRecord(session_id=transcript.session_id)
    result = bt.upload_session(
        transcript, record, bt.Poster(wire.base_url, wire.token),
        device_id="", journal=journal, wire=wire,
    )
    assert result.ok and record.finalized
    assert result.batches == 2  # Only the new tail and its completion were sent.
    assert len(wire.events) == 13
    assert [event["line_no"] for event in wire.events] == list(range(13))
    assert journal.pending(transcript.session_id) is None
    state = journal.get(transcript.session_id)
    assert state["source_byte_end"] == transcript.path.stat().st_size
    assert state["historical_complete"]
    new_data = json.loads(wire.calls[-2])
    assert new_data["source_byte_start"] == previous["source_byte_end"]
    assert new_data["batch_seq"] == json.loads(pending)["batch_seq"] + 1
    posts = list(wire.calls)
    assert bt.upload_session(
        transcript, record, bt.Poster(wire.base_url, wire.token),
        device_id="", journal=journal, wire=wire,
    ).already_finalized
    assert wire.calls == posts


@pytest.mark.parametrize("change", [
    "byte", "line", "event", "hash", "unfinished", "behind", "protocol",
    "absent", "stream", "team", "source", "session", "boolean_cursor",
    "events", "not_finalize", "start", "pending_sequence", "pending_prefix",
    "pending_session", "digest", "changed_source", "truncated_source",
])
def test_unproven_boundary_preserves_pending_and_acknowledged_state(stale, change):
    transcript, journal, wire, pending = stale
    remote = copy.deepcopy(wire.receipts(transcript.session_id))
    stream = remote["stream"]
    if change in ("byte", "line", "event"):
        key = {"byte": "source_byte_end", "line": "source_line_end", "event": "event_end"}[change]
        stream[key] += 1
    elif change == "hash":
        stream["prefix_sha256"] = "0" * 64
    elif change == "unfinished":
        stream["finalized"] = False
    elif change == "behind":
        stream["last_seq"] = 0
    elif change == "protocol":
        remote["protocol_version"] = 1
    elif change == "absent":
        remote["state"] = "absent"
    elif change == "stream":
        stream["stream_id"] = "another-stream"
    elif change in ("team", "source", "session"):
        remote[{"team": "customer_id", "source": "source", "session": "session_id"}[change]] = "other"
    elif change == "boolean_cursor":
        stream["event_end"] = True
    elif change in ("events", "not_finalize", "start", "pending_sequence", "pending_prefix", "pending_session"):
        payload = json.loads(pending)
        if change == "events":
            payload["events"] = [{"line_no": 12, "raw": {"text": "keep this data"}}]
        elif change == "not_finalize":
            payload.pop("finalize")
        elif change == "start":
            payload["source_byte_start"] -= 1
        elif change == "pending_sequence":
            payload["batch_seq"] += 1
        elif change == "pending_prefix":
            payload["prefix_sha256"] = "0" * 64
        else:
            payload["session_id"] = "another-session"
        pending = sj.canonical_payload(payload)
        journal.conn.execute("UPDATE pending SET body=?,digest=? WHERE session_id=?", (
            pending, hashlib.sha256(pending).hexdigest(), transcript.session_id,
        ))
    elif change == "digest":
        journal.conn.execute("UPDATE pending SET digest=?", ("0" * 64,))
    elif change == "changed_source":
        transcript.path.write_bytes(transcript.path.read_bytes().replace(b"turn 0", b"EDIT 0"))
    else:
        transcript.path.write_bytes(transcript.path.read_bytes()[:-20])
    before = journal.get(transcript.session_id)
    stored = journal.conn.execute("SELECT body,digest FROM pending").fetchone()
    try:
        journal.ensure(transcript.session_id, transcript.path, remote, historical=True)
    except sj.ReconciliationRequired:
        pass
    assert journal.pending(transcript.session_id) == pending
    assert journal.conn.execute("SELECT body,digest FROM pending").fetchone() == stored
    assert journal.get(transcript.session_id) == before


def test_snapshot_failure_rolls_back_finalization_adoption(stale, monkeypatch):
    transcript, journal, wire, pending = stale
    before = journal.get(transcript.session_id)
    _append(transcript)
    monkeypatch.setattr(sj.shutil, "disk_usage", lambda _: SimpleNamespace(free=0))
    with pytest.raises(sj.DeliveryPending, match="free disk space"):
        journal.ensure(transcript.session_id, transcript.path, wire.receipts(transcript.session_id), historical=True)
    assert journal.pending(transcript.session_id) == pending
    assert journal.get(transcript.session_id) == before


def test_late_finalize_acknowledgment_cannot_remove_a_new_pending_tail(stale):
    transcript, journal, wire, pending = stale
    accepted = wire.accepted[(transcript.session_id, json.loads(pending)["batch_seq"])]
    code, late_response = wire.post(accepted)
    assert code == 202
    _append(transcript)
    journal.ensure(transcript.session_id, transcript.path, wire.receipts(transcript.session_id), historical=True)
    successor = journal.stage(transcript.session_id, cwd=transcript.cwd)
    assert successor and json.loads(successor)["events"]
    before = journal.get(transcript.session_id)
    journal.acknowledge(transcript.session_id, late_response, sent_body=accepted)
    assert journal.pending(transcript.session_id) == successor
    assert journal.get(transcript.session_id) == before


@pytest.fixture
def late(stale, monkeypatch):
    transcript, journal, wire, pending = stale
    _append(transcript)
    # The first receipt read predates the competing completion. Only the
    # conflict's refresh can see that the old boundary is already finalized.
    receipts = wire.receipts
    reads = []

    def delayed_receipts(session_id):
        reads.append(session_id)
        remote = copy.deepcopy(receipts(session_id))
        if len(reads) == 1:
            remote["stream"].update(finalized=False, last_seq=0)
        return remote

    monkeypatch.setattr(wire, "receipts", delayed_receipts)
    wire.calls.clear()
    return transcript, journal, wire, pending, reads


def _late_upload(late, *, explicit_approval=True):
    transcript, journal, wire, _pending, _reads = late
    record = bt.SessionRecord(session_id=transcript.session_id)
    approved = {
        "size": transcript.path.stat().st_size,
        "sha256": hashlib.sha256(transcript.path.read_bytes()).hexdigest(),
    }
    result = bt.upload_session(
        transcript, record, bt.Poster(wire.base_url, wire.token), device_id="",
        journal=journal, wire=wire, approved=approved if explicit_approval else None,
    )
    return result, record


def test_late_conflict_recovers_old_finalization_and_finishes_approved_tail(late):
    transcript, journal, wire, pending, reads = late
    result, record = _late_upload(late)
    assert result.ok and record.finalized and not result.already_finalized
    assert result.batches == 2
    assert result.bytes_sent == sum(len(body) for body in wire.calls[1:])
    assert len(reads) == 2 and len(wire.calls) == 3
    assert wire.calls[0] == pending
    assert len(wire.events) == 13
    assert [event["line_no"] for event in wire.events] == list(range(13))
    assert journal.pending(transcript.session_id) is None


def test_second_conflict_does_not_start_another_reconciliation_loop(late):
    transcript, journal, wire, pending, reads = late
    wire.status = 409  # Reject the new data after the old finalize is reconciled.
    result, record = _late_upload(late)
    assert not result.ok and not result.retryable and not record.finalized
    assert result.error.startswith("upload: HTTP 409")
    assert result.batches == 0 and result.bytes_sent == 0
    assert len(reads) == 2 and len(wire.calls) == 2
    assert wire.calls[0] == pending
    assert journal.pending(transcript.session_id) == wire.calls[-1]
    assert json.loads(wire.calls[-1])["events"]


@pytest.mark.parametrize("explicit_approval", [False, True])
def test_source_growth_during_conflict_cannot_widen_the_requested_import(
    late, monkeypatch, explicit_approval,
):
    transcript, journal, wire, pending, reads = late
    before = journal.get(transcript.session_id)
    receipts = wire.receipts

    def growing_source(session_id):
        remote = receipts(session_id)
        if len(reads) == 2:
            _append(transcript)
        return remote

    monkeypatch.setattr(wire, "receipts", growing_source)
    result, record = _late_upload(late, explicit_approval=explicit_approval)
    assert not result.ok and not record.finalized
    assert result.error.startswith("finalization: HTTP 409")
    assert len(reads) == 2 and len(wire.calls) == 1
    assert journal.pending(transcript.session_id) == pending
    assert journal.get(transcript.session_id) == dict(before, error="http 409: immutable conflict")


def test_late_recovery_preserves_successor_reserved_before_reconciliation(late, monkeypatch):
    transcript, journal, wire, _pending, reads = late
    ensure = journal.ensure
    observed = {}

    def competing_ensure(session_id, path, remote, **kwargs):
        if kwargs.get("reconcile_body") is not None:
            ensure(session_id, path, remote, historical=True)
            observed["pending"] = journal.stage(session_id, cwd=transcript.cwd)
            observed["state"] = journal.get(session_id)
        return ensure(session_id, path, remote, **kwargs)

    monkeypatch.setattr(journal, "ensure", competing_ensure)
    result, record = _late_upload(late)
    assert not result.ok and not record.finalized
    assert len(reads) == 2 and len(wire.calls) == 1
    assert journal.pending(transcript.session_id) == observed["pending"]
    assert journal.get(transcript.session_id) == observed["state"]


@pytest.mark.parametrize("change", ["pending", "snapshot"])
def test_late_recovery_staging_refuses_changed_reservation_or_approved_history(
    late, monkeypatch, change,
):
    transcript, journal, wire, _pending, reads = late
    stage = journal.stage
    observed = {}

    def changed_stage(session_id, **kwargs):
        if kwargs.get("require_no_pending"):
            if change == "pending":
                observed["pending"] = stage(session_id, cwd=transcript.cwd)
            else:
                journal.update(session_id, historical_hash="0" * 64)
            observed["state"] = journal.get(session_id)
        return stage(session_id, **kwargs)

    monkeypatch.setattr(journal, "stage", changed_stage)
    result, record = _late_upload(late)
    assert not result.ok and not record.finalized
    assert "during reconciliation" in result.error
    assert len(reads) == 2 and len(wire.calls) == 1
    assert journal.get(transcript.session_id) == observed["state"]
    assert journal.pending(transcript.session_id) == observed.get("pending")


def test_pinned_delivery_replays_approved_body_without_sending_or_retiring_successor(stale):
    transcript, journal, wire, _pending = stale
    _append(transcript)
    journal.ensure(transcript.session_id, transcript.path, wire.receipts(transcript.session_id), historical=True)
    staged = journal.stage(transcript.session_id, cwd=transcript.cwd)
    assert staged and json.loads(staged)["events"]
    # Another drainer commits our staged data, then reserves its completion.
    journal.deliver(transcript.session_id, wire)
    successor = journal.stage(transcript.session_id, cwd=transcript.cwd)
    before = journal.get(transcript.session_id)
    posts = len(wire.calls)
    assert journal.deliver(transcript.session_id, wire, expected_body=staged)
    assert wire.calls[posts:] == [staged]
    assert journal.pending(transcript.session_id) == successor
    assert journal.get(transcript.session_id) == before
