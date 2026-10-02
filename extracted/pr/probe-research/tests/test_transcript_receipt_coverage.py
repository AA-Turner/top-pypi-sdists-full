"""A reviewed prefix can finish without reopening a newer capture reservation."""

import copy
import hashlib
import json
from dataclasses import asdict, replace
from pathlib import Path

import pytest

from probe.cli import backfill_transcripts as bt
from probe.tap_core.session_journal import Journal, ReconciliationRequired
from test_backfill_transcripts_upload import FakeWire, _transcript


@pytest.fixture
def covered(tmp_path, monkeypatch):
    monkeypatch.setenv("PROBE_TRANSCRIPT_STATE_DIR", str(tmp_path / "state"))
    wire = FakeWire()
    monkeypatch.setattr(bt, "Wire", lambda *args, **kwargs: wire)
    transcript = _transcript(tmp_path)
    poster = bt.Poster(wire.base_url, wire.token)
    record = bt.SessionRecord(session_id=transcript.session_id)
    assert bt.upload_session(transcript, record, poster, device_id="").ok
    original = transcript.path.read_bytes()
    approved_bytes = b"".join(original.splitlines(keepends=True)[:8])
    approved = {
        **asdict(transcript),
        "size": len(approved_bytes),
        "sha256": hashlib.sha256(approved_bytes).hexdigest(),
    }
    return transcript, wire, poster, approved


def _import(covered, tmp_path, **kwargs):
    transcript, _wire, poster, approved = covered
    return bt.import_transcripts(
        bt.Census(candidates=[replace(transcript, size=approved["size"])]),
        poster=poster, device_id="", ledger=bt.TranscriptLedger(tmp_path / "ledger"),
        scratch=tmp_path / "job",
        approved_files={f"{transcript.agent}:{transcript.session_id}": approved},
        expected_customer_id="synthetic", **kwargs,
    )


def test_shorter_approved_prefix_already_finalized_finishes_without_copy_or_journal(
    covered, tmp_path, monkeypatch,
):
    transcript, wire, _poster, _approved = covered
    posts = list(wire.calls)
    monkeypatch.setattr(bt, "Journal", lambda *a, **k: pytest.fail("reopened shared journal"))
    monkeypatch.setattr(bt, "_approved_transcript", lambda *a: pytest.fail("made short source copy"))
    completions = []
    outcome = _import(covered, tmp_path, on_completion=lambda *args: completions.append(args))
    assert outcome.finalized == 1 and outcome.failed == 0 and outcome.bytes_sent == 0
    assert outcome.pending_batches == 0
    assert completions[-1] == (1, 1, [(transcript.agent, transcript.session_id)])
    assert wire.calls == posts


def test_equal_approved_hash_is_proof_even_after_local_source_disappears(covered, tmp_path):
    transcript, wire, _poster, approved = covered
    approved.update(size=transcript.size, sha256=hashlib.sha256(transcript.path.read_bytes()).hexdigest())
    transcript.path.unlink()
    posts = list(wire.calls)
    outcome = _import(covered, tmp_path)
    assert outcome.finalized == 1 and outcome.failed == 0
    assert wire.calls == posts


def test_covered_import_leaves_newer_pending_capture_bytes_unchanged(covered, tmp_path):
    transcript, wire, _poster, _approved = covered
    with transcript.path.open("ab") as handle:
        handle.write(json.dumps({
            "type": "user", "sessionId": transcript.session_id,
            "message": {"role": "user", "content": "new independently captured tail"},
        }).encode() + b"\n")
    journal = Journal(wire.base_url, "synthetic", transcript.agent)
    try:
        journal.ensure(
            transcript.session_id, transcript.path, wire.receipts(transcript.session_id),
            historical=False,
        )
        pending = journal.stage(transcript.session_id, cwd=transcript.cwd)
        assert pending and json.loads(pending)["source_byte_end"] > wire.streams[transcript.session_id]["source_byte_end"]
        state = journal.get(transcript.session_id)
        posts = list(wire.calls)
        outcome = _import(covered, tmp_path)
        assert outcome.finalized == 1 and outcome.failed == 0 and outcome.pending_batches == 0
        assert journal.get(transcript.session_id) == state
        assert journal.pending(transcript.session_id) == pending
        assert wire.calls == posts
    finally:
        journal.close()


def test_capture_finishes_between_receipt_reads_without_importing_or_touching_its_tail(
    covered, tmp_path, monkeypatch,
):
    _previous, wire, poster, _previous_approval = covered
    transcript = _transcript(tmp_path)
    reviewed_bytes = b"".join(transcript.path.read_bytes().splitlines(keepends=True)[:8])
    approved = {
        **asdict(transcript), "size": len(reviewed_bytes),
        "sha256": hashlib.sha256(reviewed_bytes).hexdigest(),
    }
    live = Journal(wire.base_url, "synthetic", transcript.agent)
    try:
        live.ensure(
            transcript.session_id, transcript.path, wire.receipts(transcript.session_id),
            historical=True,
        )
        assert live.stage(transcript.session_id, cwd=transcript.cwd)
        live.deliver(transcript.session_id, wire)
        assert not wire.streams[transcript.session_id]["finalized"]
        receipts = wire.receipts
        observed = {}
        reads = 0

        def advancing_receipts(session_id):
            nonlocal reads
            reads += 1
            if reads == 2:
                finalization = live.stage(session_id, cwd=transcript.cwd)
                assert finalization and json.loads(finalization)["finalize"]
                live.deliver(session_id, wire)
                with transcript.path.open("ab") as handle:
                    handle.write(json.dumps({
                        "type": "user", "sessionId": session_id,
                        "message": {"role": "user", "content": "unapproved live tail"},
                    }).encode() + b"\n")
                live.ensure(session_id, transcript.path, receipts(session_id), historical=False)
                observed["pending"] = live.stage(session_id, cwd=transcript.cwd)
                assert observed["pending"]
                observed["state"] = live.get(session_id)
                observed["snapshot_exists"] = Path(observed["state"]["snapshot_path"]).exists()
                observed["posts"] = list(wire.calls)
            return copy.deepcopy(receipts(session_id))

        monkeypatch.setattr(wire, "receipts", advancing_receipts)
        outcome = _import((transcript, wire, poster, approved), tmp_path)
        assert reads == 2
        assert outcome.finalized == 1 and outcome.failed == 0 and outcome.bytes_sent == 0
        assert outcome.pending_batches == 0
        assert live.get(transcript.session_id) == observed["state"]
        assert live.pending(transcript.session_id) == observed["pending"]
        assert Path(observed["state"]["snapshot_path"]).exists() == observed["snapshot_exists"]
        assert wire.calls == observed["posts"]
    finally:
        live.close()


@pytest.mark.parametrize("change", ["approved_prefix", "later_prefix", "truncated"])
def test_larger_receipt_requires_original_source_to_prove_both_prefixes(covered, change):
    transcript, wire, _poster, approved = covered
    data = transcript.path.read_bytes()
    if change == "approved_prefix":
        data = data.replace(b"turn 0", b"EDIT 0")
    elif change == "later_prefix":
        data = data.replace(b"turn 11", b"EDIT 11")
    else:
        data = data[:approved["size"]]
    transcript.path.write_bytes(data)
    if change == "truncated":
        with pytest.raises(ReconciliationRequired, match="truncated"):
            bt._finalized_coverage(transcript, wire.receipts(transcript.session_id), approved=approved)
    else:
        assert bt._finalized_coverage(transcript, wire.receipts(transcript.session_id), approved=approved) is None


def test_source_change_between_prefixes_cannot_combine_two_versions_as_proof(covered, monkeypatch):
    transcript, wire, _poster, approved = covered
    changed = transcript.path.read_bytes().replace(b"turn 0", b"EDIT 0")
    remote = copy.deepcopy(wire.receipts(transcript.session_id))
    remote["stream"]["prefix_sha256"] = hashlib.sha256(changed).hexdigest()
    real_open = Path.open

    class ChangingSource:
        def __init__(self):
            self.handle = real_open(transcript.path, "rb")
            self.changed = False

        def __enter__(self):
            return self

        def __exit__(self, *args):
            self.handle.close()

        def fileno(self):
            return self.handle.fileno()

        def read(self, size):
            chunk = self.handle.read(size)
            if not self.changed:
                self.changed = True
                with real_open(transcript.path, "r+b") as output:
                    output.write(changed)
            return chunk

    def open_source(path, *args, **kwargs):
        return ChangingSource() if path == transcript.path else real_open(path, *args, **kwargs)

    monkeypatch.setattr(Path, "open", open_source)
    with pytest.raises(ReconciliationRequired, match="source changed"):
        bt._finalized_coverage(transcript, remote, approved=approved)


@pytest.mark.parametrize("field,value", [
    ("customer_id", "other-team"), ("source", "codex"), ("session_id", "another-session"),
])
def test_coverage_never_crosses_destination_or_transcript_identity(covered, field, value):
    transcript, wire, _poster, approved = covered
    remote = copy.deepcopy(wire.receipts(transcript.session_id))
    remote[field] = value
    with pytest.raises(ReconciliationRequired):
        bt._finalized_coverage(transcript, remote, approved=approved, expected_customer_id="synthetic")


@pytest.mark.parametrize("change", ["unfinalized", "legacy", "wrong_hash", "shorter", "old_protocol"])
def test_unproven_receipts_do_not_count_as_completion(covered, change):
    transcript, wire, _poster, approved = covered
    remote = copy.deepcopy(wire.receipts(transcript.session_id))
    if change == "unfinalized":
        remote["stream"]["finalized"] = False
    elif change == "legacy":
        remote["state"] = "legacy"
    elif change == "wrong_hash":
        remote["stream"]["prefix_sha256"] = "0" * 64
    elif change == "shorter":
        remote["stream"]["source_byte_end"] = approved["size"] - 1
    else:
        remote["protocol_version"] = 1
    assert bt._finalized_coverage(transcript, remote, approved=approved) is None


def test_direct_upload_recognizes_finalized_source_without_reopening_journal(covered, monkeypatch):
    transcript, wire, poster, _approved = covered
    monkeypatch.setattr(bt, "Journal", lambda *a, **k: pytest.fail("reopened shared journal"))
    posts = list(wire.calls)
    record = bt.SessionRecord(session_id=transcript.session_id)
    result = bt.upload_session(transcript, record, poster, device_id="")
    assert result.ok and record.finalized and result.bytes_sent == 0
    assert wire.calls == posts
