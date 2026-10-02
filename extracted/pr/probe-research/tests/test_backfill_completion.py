"""Progress credits durable deliveries, never prepared or merely processed work."""

import json
from pathlib import Path
from types import SimpleNamespace

import pytest

from probe.cli import backfill_import as folder_import
from probe.cli import backfill_transcripts as transcripts
from probe.cli import backfill
from probe.cli.backfill_coverage import CoverageError
from probe.sdk.errors import TransportError
from tests import test_backfill_background as folder_fixtures
from tests import test_backfill_transcripts_upload as transcript_fixtures
from tests.test_backfill_delivery import Store

background_harness = folder_fixtures.background_harness
background_job = transcript_fixtures.background_job
isolated_state = transcript_fixtures.isolated_state
wire = transcript_fixtures.wire
_transcript = transcript_fixtures._transcript


def _import(tmp_path, wire, candidates, *, completion, **kwargs):
    return transcripts.import_transcripts(
        transcripts.Census(candidates=candidates),
        poster=transcripts.Poster(wire.base_url, wire.token), device_id="device",
        ledger=transcripts.TranscriptLedger(tmp_path / "ledger.jsonl"),
        on_completion=lambda done, total, ids: completion.append((done, total, ids)),
        **kwargs,
    )


def test_failed_finalization_does_not_fill_completion_and_receipt_retry_does(
    tmp_path, wire, monkeypatch,
):
    failed, successful = _transcript(tmp_path), _transcript(tmp_path)
    post = wire.post

    def reject_one_finalize(encoded):
        body = json.loads(encoded)
        wire.finalize_status = 500 if body["session_id"] == failed.session_id else 202
        return post(encoded)

    monkeypatch.setattr(wire, "post", reject_one_finalize)
    completion, stages = [], []
    outcome = _import(
        tmp_path, wire, [failed, successful], completion=completion,
        on_stage=lambda done, total, item, phase: stages.append((done, phase)),
    )
    assert outcome.failed == 1 and outcome.finalized == 1
    assert stages[-1] == (2, "Session processed")  # Compatibility is separate from completion.
    assert completion == [(0, 2, []), (1, 2, [(successful.agent, successful.session_id)])]
    event_count = len(wire.events)

    monkeypatch.setattr(wire, "post", post)
    wire.finalize_status = 202
    completion.clear()
    outcome = _import(tmp_path, wire, [failed, successful], completion=completion)
    assert outcome.finalized == 2 and outcome.failed == 0
    assert completion[-1] == (
        2, 2, sorted([(failed.agent, failed.session_id), (successful.agent, successful.session_id)]),
    )
    assert len(wire.events) == event_count  # Only the pending finalization is retried.


def test_byte_budget_defers_without_crediting_a_session(tmp_path, wire):
    completion = []
    outcome = _import(
        tmp_path, wire, [_transcript(tmp_path)], completion=completion, budget_bytes=0,
    )
    assert outcome.deferred == 1 and outcome.finalized == 0
    assert completion == [(0, 1, [])]
    assert wire.calls == []


def test_background_events_keep_verified_completion_separate_from_processed_count(
    background_job, wire,
):
    payload, transcript, _client, error = background_job
    wire.finalize_status = 400
    events = []
    with pytest.raises(error, match="incomplete"):
        transcripts.run_background_job(
            payload, progress=lambda message, **fields: events.append((message, fields)),
        )
    assert any(fields.get("completed") == 1 for _, fields in events)
    assert all(fields["completion_completed"] == 0 for _, fields in events)
    assert all(fields["completion_total"] == 1 for _, fields in events)
    assert all(fields["completion_ids"] == [] for _, fields in events)

    wire.finalize_status = 202
    events.clear()
    transcripts.run_background_job(
        payload, progress=lambda message, **fields: events.append((message, fields)),
    )
    assert events[-1][1]["completion_completed"] == 1
    assert events[-1][1]["completion_ids"] == [[transcript.agent, transcript.session_id]]


def test_folder_completion_updates_between_uploads_and_ignores_unrelated_outbox_work(
    background_harness, monkeypatch,
):
    h, queued = background_harness
    (h.folder / "b.py").write_text("value = 2\n")
    h.run(background=True)
    h.client.enqueue_artifact_upload(
        correlation="unrelated", anchor="project", anchor_id=h.created[0]["id"],
        name="another-import.py", path=h.folder / "a.py",
    )
    events, before_upload = [], []
    upload = h.remote.upload_fingerprinted

    def observe_upload(*args, **kwargs):
        before_upload.append((args[2], events[-1][1]["completion_completed"]))
        return upload(*args, **kwargs)

    monkeypatch.setattr(h.remote, "upload_fingerprinted", observe_upload)
    folder_import.run_background_job(
        queued[0], progress=lambda message, **fields: events.append((message, fields)),
    )
    prepared = [fields for message, fields in events if message == "Reading reviewed files"]
    assert prepared[-1]["completed"] == 2
    assert prepared[0]["completion_completed"] == 0
    # The monitor's final read can now see receipts delivered by on_complete.
    assert prepared[-1]["completion_completed"] == 2
    # Uploads no longer go strictly one after another, so the count a file sees
    # when its own upload STARTS depends on whether a sibling has finished. What
    # must still hold: every file uploads exactly once, unrelated outbox work is
    # not counted, and the count never goes backwards.
    assert sorted(name for name, _ in before_upload) == ["a.py", "another-import.py", "b.py"]
    seen = [count for _, count in before_upload]
    assert seen == sorted(seen), "completion must never count down"
    assert seen[0] == 0
    measured = [fields for _, fields in events if "completion_completed" in fields]
    assert {fields["completion_total"] for fields in measured} == {2}
    counts = [fields["completion_completed"] for fields in measured]
    assert counts == sorted(counts) and list(dict.fromkeys(counts)) == [0, 1, 2]
    assert h.report()["delivered"] == ["a.py", "b.py"]

    # Recovery credits both verified receipts before any preparation, without re-uploading.
    events.clear()
    folder_import.run_background_job(
        queued[0], progress=lambda message, **fields: events.append((message, fields)),
    )
    measured = [fields for _, fields in events if "completion_completed" in fields]
    assert all(fields["completion_completed"] == 2 for fields in measured)
    assert len(h.remote.calls) == 3


def test_prepared_files_and_failed_uploads_leave_completion_at_zero(
    background_harness, monkeypatch,
):
    from probe.cli.import_jobs import RetryableJobError

    h, queued = background_harness
    h.run(background=True)

    def offline(*args, **kwargs):
        raise TransportError("synthetic offline")

    monkeypatch.setattr(h.remote, "upload_fingerprinted", offline)
    events = []
    with pytest.raises(RetryableJobError):
        folder_import.run_background_job(
            queued[0], progress=lambda message, **fields: events.append((message, fields)),
        )
    assert h.manifested and not h.report()["delivered"]
    assert any(message == "Reading reviewed files" and fields["completed"] == 1
               for message, fields in events)
    measured = [fields for _, fields in events if "completion_completed" in fields]
    assert measured and all(fields["completion_completed"] == 0 for fields in measured)


def test_changed_approved_file_stays_in_completion_denominator(background_harness):
    h, queued = background_harness
    (h.folder / "b.py").write_text("value = 2\n")
    h.run(background=True)
    (h.folder / "b.py").write_text("changed after approval\n")
    (h.folder / "new.py").write_text("not approved\n")
    events = []
    with pytest.raises(CoverageError, match="1 approved file"):
        folder_import.run_background_job(
            queued[0], progress=lambda message, **fields: events.append((message, fields)),
        )
    assert events[-1][1]["completion_completed"] == 1
    assert events[-1][1]["completion_total"] == 2
    assert h.report()["delivered"] == ["a.py"]


def test_folder_reference_counts_only_after_its_matching_receipt(background_harness, monkeypatch):
    h, queued = background_harness
    h.run(background=True)
    launch = backfill.launch_agent

    def describe_reference(folder, prompt, **kwargs):
        result = launch(folder, prompt, **kwargs)
        manifest = Path(next(
            line.split("Write JSONL to:", 1)[1].strip()
            for line in prompt.splitlines() if line.strip().startswith("Write JSONL to:")
        ))
        rows = [json.loads(line) for line in manifest.read_text().splitlines()]
        manifest.write_text("".join(json.dumps({**row, "reference": True}) + "\n" for row in rows))
        return result

    monkeypatch.setattr(backfill, "launch_agent", describe_reference)
    store = Store()
    events = []

    def reference(*args, **kwargs):
        assert events[-1][1]["completion_completed"] == 0
        return store.reference(*args, **kwargs)

    h.remote.transport = SimpleNamespace(request=reference)
    folder_import.run_background_job(
        queued[0], progress=lambda message, **fields: events.append((message, fields)),
    )
    measured = [fields["completion_completed"] for _, fields in events
                if "completion_completed" in fields]
    assert measured == sorted(measured) and list(dict.fromkeys(measured)) == [0, 1]
    assert h.report()["references"] == ["a.py"] and not h.report()["delivered"]
    assert len(store.calls) == 1 and not h.remote.calls
