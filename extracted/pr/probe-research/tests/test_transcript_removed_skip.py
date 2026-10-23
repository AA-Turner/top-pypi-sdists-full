"""A session file deleted between review and upload is a SKIP, not a failure.

Claude Code deletes transcripts nobody has opened for `cleanupPeriodDays` (30 by
default), silently, in a sweep after any session starts. A background import
freezes each approved file's path, size and hash at review; when the sweep runs
before the upload reaches a file, opening it raises `FileNotFoundError`. That
used to fail the session, and so the job, and mail "Session import stopped ...
Resume from Existing imports to retry" -- advice that could never work, because
no resume brings the file back (47/49 finalized, 2 failed, 2026-10-21).

The skip is narrow on purpose. It needs the error to name the session file, the
file to be provably gone, the folder that held it to still exist, and no upload
of the session to be in progress. Anything else stays a failure, so a
lost drive or a half-finished upload still stops the import and reaches its
owner.
"""

from __future__ import annotations

import contextlib
import hashlib
import json
import shutil
from dataclasses import asdict, replace
from pathlib import Path
from uuid import uuid4

import pytest
from probe.cli import backfill_transcripts as bt
from probe.tap_core.session_journal import ReconciliationRequired

from test_backfill_transcripts_upload import FakeWire, _transcript

REMOVED = "Removed from this machine before upload; nothing sent"


@pytest.fixture(autouse=True)
def isolated_state(tmp_path, monkeypatch):
    monkeypatch.setenv("PROBE_TRANSCRIPT_STATE_DIR", str(tmp_path / "state"))


@pytest.fixture
def wire(monkeypatch):
    wire = FakeWire()
    monkeypatch.setattr(bt, "Wire", lambda *a, **kw: wire)
    return wire


def _approved(transcript, size=None):
    data = transcript.path.read_bytes()[:size]
    return {**asdict(transcript), "size": len(data), "sha256": hashlib.sha256(data).hexdigest()}


def _approved_files(*transcripts):
    return {f"{t.agent}:{t.session_id}": _approved(t) for t in transcripts}


def _lane(census, wire, tmp_path, approved_files, **overrides):
    stages = []
    completions = []
    args = dict(
        poster=bt.Poster(wire.base_url, wire.token),
        device_id="",
        ledger=bt.TranscriptLedger(tmp_path / "ledger"),
        assignments={},
        scratch=tmp_path / "job",
        approved_files=approved_files,
        expected_customer_id="synthetic",
        on_stage=lambda done, total, transcript, phase: stages.append((done, total, phase)),
        on_completion=lambda done, total, ids: completions.append((done, total)),
    )
    args.update(overrides)
    return bt.import_transcripts(census, **args), stages, completions


def test_a_session_removed_after_review_is_skipped_and_nothing_is_sent(tmp_path, wire):
    transcript = _transcript(tmp_path)
    approved = _approved_files(transcript)
    transcript.path.unlink()

    outcome, stages, completions = _lane(bt.Census(candidates=[transcript]), wire, tmp_path, approved)

    assert outcome.skipped_removed == 1
    assert outcome.failed == 0 and outcome.errors == []
    assert outcome.finalized == 0 and outcome.uploaded == 0
    assert wire.accepted == {}
    # Exactly one terminal stage per session: the estimator and job record count them.
    assert [stage for stage in stages if stage[0] == 1] == [(1, 1, REMOVED)]
    assert completions[-1] == (1, 1), "the bar must still reach its total"


def test_the_other_sessions_in_the_census_still_upload(tmp_path, wire):
    removed = _transcript(tmp_path, sid=str(uuid4()))
    kept = _transcript(tmp_path, sid=str(uuid4()))
    approved = _approved_files(removed, kept)
    removed.path.unlink()

    outcome, _, _ = _lane(bt.Census(candidates=[removed, kept]), wire, tmp_path, approved)

    assert (outcome.skipped_removed, outcome.finalized, outcome.failed) == (1, 1, 0)
    uploaded = {json.loads(body)["session_id"] for body in wire.accepted.values()}
    assert uploaded == {kept.session_id}


def test_a_resume_skips_it_again_and_finishes(tmp_path, wire):
    """The path the old email pointed at: a resume replays the same frozen
    inventory, and the removed session must not turn into a failure there."""
    transcript = _transcript(tmp_path)
    approved = _approved_files(transcript)
    transcript.path.unlink()
    census = bt.Census(candidates=[transcript])

    _lane(census, wire, tmp_path, approved)
    again, _, completions = _lane(census, wire, tmp_path, approved)

    assert (again.skipped_removed, again.failed) == (1, 0)
    assert completions[-1] == (1, 1) and wire.accepted == {}


def test_the_foreground_import_skips_it_too(tmp_path, wire):
    """Without an approved inventory the source is read inside `upload_session`,
    which reports errors on its result rather than raising them."""
    transcript = _transcript(tmp_path)
    transcript.path.unlink()

    outcome, _, _ = _lane(
        bt.Census(candidates=[transcript]), wire, tmp_path, None, scratch=None,
    )

    assert (outcome.skipped_removed, outcome.failed) == (1, 0)
    assert wire.accepted == {}


def test_a_longer_copy_the_server_already_finalized_is_skipped_untouched(tmp_path, wire):
    """Capture finalized more than was reviewed. Proving the reviewed prefix
    belongs to that stream needs the file, so a removed file lands in the skip,
    and the server's copy is neither re-sent nor called a failure."""
    transcript = _transcript(tmp_path)
    record = bt.SessionRecord(session_id=transcript.session_id)
    assert bt.upload_session(transcript, record, bt.Poster(wire.base_url, wire.token), device_id="").ok
    approved = {f"{transcript.agent}:{transcript.session_id}": _approved(transcript, size=transcript.size // 2)}
    transcript.path.unlink()
    posts = list(wire.calls)

    outcome, _, _ = _lane(
        bt.Census(candidates=[replace(transcript, size=transcript.size // 2)]), wire, tmp_path, approved,
    )

    assert (outcome.skipped_removed, outcome.failed) == (1, 0)
    assert wire.calls == posts
    assert wire.streams[transcript.session_id]["finalized"] is True


def test_a_partial_upload_on_the_server_stays_a_failure(tmp_path, wire):
    """Part of the session already reached the server: skipping would hide an
    upload left half done, so it keeps failing loudly."""
    transcript = _transcript(tmp_path)
    approved = _approved_files(transcript)
    wire.streams[transcript.session_id] = {
        "finalized": False, "source_byte_end": 10, "prefix_sha256": "0" * 64,
        "last_seq": 0, "stream_id": "partial",
    }
    transcript.path.unlink()

    outcome, _, _ = _lane(bt.Census(candidates=[transcript]), wire, tmp_path, approved)

    assert (outcome.skipped_removed, outcome.failed) == (0, 1)
    assert "FileNotFoundError" in outcome.errors[0]


def test_a_batch_still_staged_in_the_journal_stays_a_failure(tmp_path, wire):
    """An earlier run staged a batch the server never acknowledged, then the
    file went. The journal still holds that batch, so it is not nothing-to-do."""
    transcript = _transcript(tmp_path)
    approved = _approved_files(transcript)
    census = bt.Census(candidates=[transcript])
    wire.status = 503
    first, _, _ = _lane(census, wire, tmp_path, approved)
    assert first.pending_batches == 1
    wire.status = 202
    transcript.path.unlink()

    outcome, _, _ = _lane(census, wire, tmp_path, approved)

    assert (outcome.skipped_removed, outcome.failed) == (0, 1)


def test_a_missing_folder_stays_a_failure_even_when_its_root_is_back(tmp_path, wire):
    """Every file gone because its folder is (an unmounted drive, a moved
    config directory) is not the cleanup sweep, which deletes files and leaves
    the project folder. Claude Code recreates an empty `projects/` on its next
    start, so the root existing again proves nothing. Skipping here would
    report a finished import with nothing uploaded and no email."""
    root = tmp_path / "projects"
    project = root / "-home-someone-repo"
    project.mkdir(parents=True)
    transcript = _transcript(project)
    approved = _approved_files(transcript)
    shutil.rmtree(root)
    root.mkdir()

    outcome, _, _ = _lane(bt.Census(candidates=[transcript]), wire, tmp_path, approved)

    assert (outcome.skipped_removed, outcome.failed) == (0, 1)


def test_a_journal_that_cannot_answer_fails_one_session_not_the_import(tmp_path, wire, monkeypatch):
    """The in-progress check opens the journal inside the error handler. A
    journal it cannot read (a newer tap's format) leaves the removal unproved:
    one counted failure, and the next session still uploads."""
    removed = _transcript(tmp_path, sid=str(uuid4()))
    kept = _transcript(tmp_path, sid=str(uuid4()))
    approved = _approved_files(removed, kept)
    removed.path.unlink()
    real = bt.Journal
    calls = []

    def journal(*args, **kwargs):
        calls.append(args)
        if len(calls) == 1:
            raise ReconciliationRequired("unsupported journal version")
        return real(*args, **kwargs)

    monkeypatch.setattr(bt, "Journal", journal)

    outcome, _, _ = _lane(bt.Census(candidates=[removed, kept]), wire, tmp_path, approved)

    assert (outcome.skipped_removed, outcome.failed, outcome.finalized) == (0, 1, 1)


def test_a_journal_that_breaks_mid_check_is_closed_before_cleanup(tmp_path, wire, monkeypatch):
    """The cleanup after each session reads the journal again. A journal opened
    only for the check, whose state cannot be read, must not reach it: that
    second read would end the whole import."""
    removed = _transcript(tmp_path, sid=str(uuid4()))
    kept = _transcript(tmp_path, sid=str(uuid4()))
    approved = _approved_files(removed, kept)
    removed.path.unlink()
    real = bt.Journal

    class Corrupt(real):
        def get(self, session_id):
            raise json.JSONDecodeError("malformed state", "{", 0)

    calls = []

    def journal(*args, **kwargs):
        calls.append(args)
        return (Corrupt if len(calls) == 1 else real)(*args, **kwargs)

    monkeypatch.setattr(bt, "Journal", journal)

    outcome, _, _ = _lane(bt.Census(candidates=[removed, kept]), wire, tmp_path, approved)

    assert (outcome.skipped_removed, outcome.failed, outcome.finalized) == (0, 1, 1)


def test_an_upload_that_started_after_the_first_receipts_stays_a_failure(tmp_path, monkeypatch):
    """The lane read receipts before the upload began; a stream that appeared
    since is only in a fresh read, which the decision must use."""

    class Racing(FakeWire):
        reads = 0

        def receipts(self, sid):
            self.reads += 1
            if self.reads > 1:
                self.streams[sid] = {
                    "finalized": False, "source_byte_end": 10, "prefix_sha256": "0" * 64,
                    "last_seq": 0, "stream_id": "elsewhere",
                }
            return super().receipts(sid)

    wire = Racing()
    monkeypatch.setattr(bt, "Wire", lambda *a, **kw: wire)
    transcript = _transcript(tmp_path)
    approved = _approved_files(transcript)
    transcript.path.unlink()

    outcome, _, _ = _lane(bt.Census(candidates=[transcript]), wire, tmp_path, approved)

    assert (outcome.skipped_removed, outcome.failed) == (0, 1)


class _Journal:
    def __init__(self, pending=None, state=None):
        self._pending, self._state = pending, state

    @contextlib.contextmanager
    def transaction(self):
        yield

    def pending(self, _session_id):
        return self._pending

    def get(self, _session_id):
        return self._state


@pytest.mark.parametrize("remote, journal, started", [
    ({"state": "absent"}, _Journal(), False),
    ({"state": "ready", "stream": {"finalized": True}}, _Journal(), False),
    ({"state": "ready", "stream": {"finalized": False}}, _Journal(), True),
    ({"state": "absent"}, _Journal(pending=b"batch"), True),
    # Acknowledged batches, not finalized: the server's copy is partial even
    # when the receipts this run read first predate them.
    ({"state": "absent"}, _Journal(state={"last_seq": 0, "historical_complete": False}), True),
    ({"state": "absent"}, _Journal(state={"last_seq": -1}), False),
    ({"state": "ready", "stream": {"finalized": True}},
     _Journal(state={"last_seq": 3, "historical_complete": True}), False),
])
def test_what_counts_as_an_upload_in_progress(remote, journal, started):
    assert bt._upload_started(remote, journal, "s-1") is started


def test_a_missing_file_that_is_not_the_source_is_still_a_failure(tmp_path, wire, monkeypatch):
    """Even with the source gone too, an error naming another file (the
    scratch copy, a certificate bundle) is not this removal."""
    transcript = _transcript(tmp_path)
    approved = _approved_files(transcript)
    transcript.path.unlink()

    def lost_scratch(*_args):
        raise FileNotFoundError(2, "No such file or directory", str(tmp_path / "job" / "copy"))

    monkeypatch.setattr(bt, "_approved_transcript", lost_scratch)

    outcome, _, _ = _lane(bt.Census(candidates=[transcript]), wire, tmp_path, approved)

    assert outcome.skipped_removed == 0
    assert outcome.failed == 1
    assert "reviewed snapshot: local transcript access failed (FileNotFoundError, errno 2)" in outcome.errors[0]


def test_an_absence_that_cannot_be_proved_is_not_a_removal(tmp_path, monkeypatch):
    path = tmp_path / "session.jsonl"
    missing = FileNotFoundError(2, "No such file or directory", str(path))
    assert bt._removed_from_machine(missing, path)

    path.write_text("{}\n")
    assert not bt._removed_from_machine(missing, path), "the file is back"
    path.unlink()

    real_lstat = Path.lstat

    def denied(self):
        if self == path:
            raise PermissionError(13, "Permission denied", str(self))
        return real_lstat(self)

    monkeypatch.setattr(Path, "lstat", denied)
    assert not bt._removed_from_machine(missing, path)


def test_the_skip_is_named_in_the_report():
    report = "\n".join(bt.LaneOutcome(found=3, finalized=2, skipped_removed=1).lines())
    assert "1 removed from this machine before upload (nothing sent)" in report
    assert "failed" not in report


def test_the_background_job_finishes_instead_of_failing(tmp_path, wire, monkeypatch):
    """The job-level consequence: no `JobError`, so no "Session import stopped"
    mail and no "Resume to retry" on the Existing imports screen."""
    removed = _transcript(tmp_path, sid=str(uuid4()))
    kept = _transcript(tmp_path, sid=str(uuid4()))
    approved = _approved_files(removed, kept)
    removed.path.unlink()
    monkeypatch.setattr(bt, "fetch_ingest_state", lambda *a, **k: None)
    phases = []

    lines = bt._execute_census(
        bt.Census(candidates=[removed, kept]),
        client=object(),
        posters={"claude_code": bt.Poster(wire.base_url, wire.token)},
        devices={"claude_code": ""},
        ledger=bt.TranscriptLedger(tmp_path / "ledger"),
        work_dir=tmp_path / "job",
        approved_files=approved,
        expected_customer_id="synthetic",
        progress=lambda phase, **fields: phases.append((phase, fields)),
    )

    phase, fields = phases[-1]
    assert phase == "Session import finished"
    assert (fields["failed"], fields["skipped_removed"]) == (0, 1)
    assert (fields["completion_completed"], fields["completion_total"]) == (2, 2)
    assert any("1 removed from this machine before upload" in line for line in lines)
