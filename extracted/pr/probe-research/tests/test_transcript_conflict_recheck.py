"""A racing finalize can be complete even when its request body conflicts."""

import copy
import hashlib
import json
from dataclasses import asdict, replace
from pathlib import Path

import pytest

from probe.cli import backfill_transcripts as bt
from probe.tap_core.session_journal import DeliveryPending, Journal
from test_backfill_transcripts_upload import FakeWire, _transcript


def _racing_import(tmp_path, monkeypatch, *, change=None, longer_source=False):
    monkeypatch.setenv("PROBE_TRANSCRIPT_STATE_DIR", str(tmp_path / "state"))
    transcript = _transcript(tmp_path)
    source = transcript
    approved = {
        **asdict(transcript),
        "sha256": hashlib.sha256(transcript.path.read_bytes()).hexdigest(),
    }
    if longer_source:
        approved_bytes = b"".join(source.path.read_bytes().splitlines(keepends=True)[:8])
        approved.update(size=len(approved_bytes), sha256=hashlib.sha256(approved_bytes).hexdigest())
        reviewed = tmp_path / "reviewed.jsonl"
        reviewed.write_bytes(approved_bytes)
        transcript = replace(source, path=reviewed, size=len(approved_bytes))

    wire = FakeWire()
    post = wire.post
    receipts = wire.receipts
    observation = {"reads": 0}

    def racing_post(encoded):
        body = json.loads(encoded)
        if body.get("finalize"):
            # Another producer finalized the same source with different request
            # metadata. Its accepted receipt is authoritative, but replaying our
            # immutable reservation correctly gets a 409 for the reused seq.
            competing = dict(body, cwd="/other-producer")
            assert post(json.dumps(competing).encode())[0] == 202
            if longer_source:
                stream = wire.streams[transcript.session_id]
                stream.update(
                    source_byte_end=source.size,
                    prefix_sha256=hashlib.sha256(source.path.read_bytes()).hexdigest(),
                )
            observation["pending"] = encoded
        return post(encoded)

    def refreshed_receipts(session_id):
        observation["reads"] += 1
        remote = copy.deepcopy(receipts(session_id))
        if observation["reads"] > 1:
            if change in ("customer_id", "source", "session_id"):
                remote[change] = "different-identity"
            elif change == "wrong_hash":
                remote["stream"]["prefix_sha256"] = "0" * 64
            elif change == "shorter":
                remote["stream"]["source_byte_end"] = approved["size"] - 1
            elif change == "unfinalized":
                remote["stream"]["finalized"] = False
            elif change == "legacy":
                remote["state"] = "legacy"
            elif change == "unavailable":
                raise DeliveryPending(
                    "private server detail", retryable=True,
                    safe_message="HTTP 503: transcript request was not accepted",
                )
            elif change == "approved_prefix_changed":
                source.path.write_bytes(source.path.read_bytes().replace(b"turn 0", b"EDIT 0"))
            elif change == "later_prefix_changed":
                source.path.write_bytes(source.path.read_bytes().replace(b"turn 11", b"EDIT 11"))
        return remote

    monkeypatch.setattr(wire, "post", racing_post)
    monkeypatch.setattr(wire, "receipts", refreshed_receipts)
    journal = Journal(wire.base_url, "synthetic", transcript.agent)
    try:
        record = bt.SessionRecord(session_id=transcript.session_id)
        result = bt.upload_session(
            transcript, record, bt.Poster(wire.base_url, wire.token), device_id="",
            journal=journal, wire=wire, coverage_source=source, approved=approved,
        )
        # An import-level coverage proof must not acknowledge/rewrite a shared
        # pending reservation or clear the source snapshot another writer needs.
        assert journal.pending(transcript.session_id) == observation["pending"]
        state = journal.get(transcript.session_id)
        assert state["last_seq"] == 0 and not state["historical_complete"]
        assert state["error"] == "http 409: immutable conflict"
        assert Path(state["snapshot_path"]).exists()
    finally:
        journal.close()
    assert len(wire.calls) == 3  # data + competing finalize + our one finalize
    return result, record, observation, wire


@pytest.mark.parametrize("longer_source", [False, True])
def test_conflicting_finalize_rechecks_and_proves_completed_approved_prefix(
    tmp_path, monkeypatch, longer_source,
):
    result, record, observation, wire = _racing_import(
        tmp_path, monkeypatch, longer_source=longer_source,
    )
    assert result.ok and result.already_finalized and result.error is None
    assert not result.retryable
    assert record.finalized
    assert record.byte_end == wire.streams[record.session_id]["source_byte_end"]
    assert observation["reads"] == 2
    assert result.batches == 1  # No accepted response was fabricated for the 409.


@pytest.mark.parametrize("change", [
    "customer_id", "source", "session_id", "wrong_hash", "shorter",
    "unfinalized", "legacy", "unavailable",
])
def test_conflicting_finalize_does_not_skip_unproven_or_unavailable_receipts(
    tmp_path, monkeypatch, change,
):
    result, record, observation, _wire = _racing_import(tmp_path, monkeypatch, change=change)
    assert not result.ok and not result.already_finalized and not record.finalized
    if change == "unavailable":
        assert result.error == "receipt recheck: HTTP 503: transcript request was not accepted"
        assert result.retryable
    else:
        assert result.error == (
            "finalization: HTTP 409: transcript conflicts with accepted data; reconciliation required"
        )
        assert not result.retryable
    assert observation["reads"] == 2


@pytest.mark.parametrize("change", ["approved_prefix_changed", "later_prefix_changed"])
def test_larger_conflicting_receipt_must_prove_both_original_source_prefixes(
    tmp_path, monkeypatch, change,
):
    result, record, observation, _wire = _racing_import(
        tmp_path, monkeypatch, change=change, longer_source=True,
    )
    assert not result.ok and not result.already_finalized and not record.finalized
    assert "HTTP 409" in result.error
    assert observation["reads"] == 2


def test_import_lane_counts_reconciled_race_without_counting_shared_pending_as_failed(
    tmp_path, monkeypatch,
):
    monkeypatch.setenv("PROBE_TRANSCRIPT_STATE_DIR", str(tmp_path / "state"))
    transcript = _transcript(tmp_path)
    approved = {
        **asdict(transcript),
        "sha256": hashlib.sha256(transcript.path.read_bytes()).hexdigest(),
    }
    wire = FakeWire()
    post = wire.post
    pending = []

    def racing_post(encoded):
        body = json.loads(encoded)
        if body.get("finalize"):
            assert post(json.dumps(dict(body, cwd="/other-producer")).encode())[0] == 202
            pending.append(encoded)
        return post(encoded)

    monkeypatch.setattr(wire, "post", racing_post)
    monkeypatch.setattr(bt, "Wire", lambda *args, **kwargs: wire)
    completions = []
    outcome = bt.import_transcripts(
        bt.Census(candidates=[transcript]), poster=bt.Poster(wire.base_url, wire.token),
        device_id="", ledger=bt.TranscriptLedger(tmp_path / "ledger"), scratch=tmp_path / "job",
        approved_files={f"{transcript.agent}:{transcript.session_id}": approved},
        expected_customer_id="synthetic", on_completion=lambda *args: completions.append(args),
    )
    assert outcome.finalized == 1 and outcome.failed == 0 and outcome.pending_batches == 0
    assert completions[-1] == (1, 1, [(transcript.agent, transcript.session_id)])
    assert len(wire.calls) == 3
    journal = Journal(wire.base_url, "synthetic", transcript.agent)
    try:
        assert journal.pending(transcript.session_id) == pending[0]
        assert Path(journal.get(transcript.session_id)["snapshot_path"]).exists()
    finally:
        journal.close()


@pytest.mark.parametrize("status", [422, 503])
def test_non_conflict_failure_does_not_trigger_receipt_recheck(tmp_path, monkeypatch, status):
    monkeypatch.setenv("PROBE_TRANSCRIPT_STATE_DIR", str(tmp_path / "state"))
    transcript = _transcript(tmp_path)
    wire = FakeWire()
    wire.finalize_status = status
    receipts = wire.receipts
    calls = []

    def counted_receipts(session_id):
        calls.append(session_id)
        return receipts(session_id)

    monkeypatch.setattr(wire, "receipts", counted_receipts)
    record = bt.SessionRecord(session_id=transcript.session_id)
    result = bt.upload_session(
        transcript, record, bt.Poster(wire.base_url, wire.token), device_id="", wire=wire,
    )
    assert not result.ok and not record.finalized
    assert result.retryable == (status == 503)
    assert len(calls) == 1
