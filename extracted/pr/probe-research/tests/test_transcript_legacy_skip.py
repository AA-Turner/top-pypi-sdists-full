"""A conversation the server already holds from before protocol 2 is a SKIP.

`state: "legacy"` means the engine has the session from the old capture path and
can name no byte cursor for it. `Journal.ensure` refuses to replay onto that --
correctly, since a blind replay overwrites stored blobs -- but the lane used to
let that refusal become a FAILURE, and the consequences were not cosmetic:

  * it is not retryable, and no `probe` command reconciles it, so "Resume from
    Existing imports to retry" was advice that could never work;
  * one non-retryable failure downgrades the whole job to "needs attention",
    so 166 of these turned a 2619-session success into a red panel;
  * and the conversations were never missing. Pulling one back out of
    `/v1/sessions/{id}/transcript` returns its full text.

The census cannot see this coming: it is reproducible offline on purpose, and
the local capture cursor only reaches back as far as protocol 2 (2026-09-08), so
every older conversation looks untracked. The receipt read in the delivery loop
is the first and only place that knows -- and it is a request the lane already
makes for every session, so recognising this costs nothing.
"""

from __future__ import annotations

import json
from uuid import uuid4

import pytest
from probe.cli import backfill_transcripts as bt

from test_backfill_transcripts_upload import FakeWire, _transcript  # noqa: F401


@pytest.fixture(autouse=True)
def isolated_state(tmp_path, monkeypatch):
    monkeypatch.setenv("PROBE_TRANSCRIPT_STATE_DIR", str(tmp_path / "state"))


class SelectiveWire(FakeWire):
    """A server that holds SOME of this machine's history from the old path."""

    def __init__(self, legacy_sessions=()):
        super().__init__()
        self.legacy_sessions = set(legacy_sessions)

    def receipts(self, sid):
        result = super().receipts(sid)
        if sid in self.legacy_sessions and sid not in self.streams:
            result.update(state="legacy")
        return result


def _lane(census, wire, tmp_path, **overrides):
    stages = []
    completions = []
    args = dict(
        poster=bt.Poster(wire.base_url, wire.token),
        device_id="",
        ledger=bt.TranscriptLedger(tmp_path / "ledger"),
        assignments={},
        on_stage=lambda done, total, transcript, phase: stages.append((done, total, phase)),
        on_completion=lambda done, total, ids: completions.append((done, total)),
    )
    args.update(overrides)
    return bt.import_transcripts(census, **args), stages, completions


def test_a_legacy_conversation_is_skipped_and_nothing_is_sent(tmp_path, monkeypatch):
    transcript = _transcript(tmp_path)
    wire = SelectiveWire([transcript.session_id])
    monkeypatch.setattr(bt, "Wire", lambda *a, **kw: wire)

    outcome, _, _ = _lane(bt.Census(candidates=[transcript]), wire, tmp_path)

    assert outcome.skipped_legacy == 1
    assert outcome.failed == 0 and outcome.errors == []
    assert outcome.finalized == 0 and outcome.uploaded == 0
    assert wire.events == [], "a session with unverifiable coverage must not be replayed"


def test_the_skip_is_named_in_the_report_and_never_folded_into_the_other_one(tmp_path):
    """`already in Probe` was PROVED absent from this import's work; this was
    proved present with coverage nobody can verify. A reader deciding whether
    their history is complete has to be able to tell those apart."""
    outcome = bt.LaneOutcome(
        found=3, finalized=1, skipped_live=1, skipped_in_probe=1, skipped_legacy=1
    )
    report = "\n".join(outcome.lines())
    assert "1 already in Probe from an earlier capture" in report
    assert "coverage not verifiable, nothing re-sent" in report
    assert "1 already captured live · 1 already in Probe" in report


def test_one_stage_message_per_session_and_it_says_what_happened(tmp_path, monkeypatch):
    """The progress estimator and the durable job record both assume exactly one
    terminal `on_stage` per session; a skip that emitted two would double-count."""
    transcript = _transcript(tmp_path)
    wire = SelectiveWire([transcript.session_id])
    monkeypatch.setattr(bt, "Wire", lambda *a, **kw: wire)

    _, stages, _ = _lane(bt.Census(candidates=[transcript]), wire, tmp_path)

    assert stages == [
        (0, 1, "Checking upload status"),
        (1, 1, "Already in Probe from an earlier capture"),
    ]


def test_a_skipped_session_still_counts_toward_completion(tmp_path, monkeypatch):
    """Otherwise the bar can never reach its total on a machine with pre-09-08
    history, which reads as an import that never finished."""
    transcript = _transcript(tmp_path)
    wire = SelectiveWire([transcript.session_id])
    monkeypatch.setattr(bt, "Wire", lambda *a, **kw: wire)

    _, _, completions = _lane(bt.Census(candidates=[transcript]), wire, tmp_path)

    assert completions[-1] == (1, 1)


def test_new_conversations_in_the_same_census_still_upload(tmp_path, monkeypatch):
    """The failure mode this replaces: one permanent refusal used to stop
    nothing but still marked the whole import as needing attention."""
    old = _transcript(tmp_path, sid=str(uuid4()))
    fresh = _transcript(tmp_path, sid=str(uuid4()))
    wire = SelectiveWire([old.session_id])
    monkeypatch.setattr(bt, "Wire", lambda *a, **kw: wire)

    outcome, _, _ = _lane(bt.Census(candidates=[old, fresh]), wire, tmp_path)

    assert (outcome.skipped_legacy, outcome.finalized, outcome.failed) == (1, 1, 0)
    uploaded = {json.loads(body)["session_id"] for body in wire.accepted.values()}
    assert uploaded == {fresh.session_id}


def test_the_identity_checks_still_run_before_the_skip(tmp_path, monkeypatch):
    """`legacy` must not become a way past the tenancy check.

    `_finalized_coverage` refuses a receipt from another team before anything
    looks at the state, and that refusal is a real failure, not a skip.
    """
    transcript = _transcript(tmp_path)
    wire = SelectiveWire([transcript.session_id])
    monkeypatch.setattr(bt, "Wire", lambda *a, **kw: wire)

    outcome, _, _ = _lane(
        bt.Census(candidates=[transcript]), wire, tmp_path,
        expected_customer_id="somebody-else",
    )

    assert outcome.skipped_legacy == 0
    assert outcome.failed == 1
    assert "different team" in outcome.errors[0]


def test_a_session_the_server_can_prove_is_not_treated_as_legacy(tmp_path, monkeypatch):
    """Once a session HAS a protocol-2 stream, the ordinary proof path owns it;
    the skip must not shadow a resumable upload."""
    transcript = _transcript(tmp_path)
    wire = SelectiveWire([transcript.session_id])
    monkeypatch.setattr(bt, "Wire", lambda *a, **kw: wire)

    first, _, _ = _lane(bt.Census(candidates=[transcript]), wire, tmp_path)
    assert first.skipped_legacy == 1

    # The same machine, after live capture has finalized that session properly.
    wire.legacy_sessions.clear()
    second, _, _ = _lane(bt.Census(candidates=[transcript]), wire, tmp_path)
    assert second.skipped_legacy == 0
    assert second.finalized == 1
