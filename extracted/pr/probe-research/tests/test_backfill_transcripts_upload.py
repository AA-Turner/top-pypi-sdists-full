"""Durable transcript delivery: protocol identity, crash windows and standalone stages."""

from __future__ import annotations

import hashlib
import json
import multiprocessing
import os
import signal
import sqlite3
from pathlib import Path
from uuid import uuid4

import pytest
from probe.cli import backfill_transcripts as bt
from probe.tap_core.session_journal import Journal, DeliveryPending, ReconciliationRequired
from probe.tap_core.session_identity import validate_identity, compatible_copy


class FakeWire:
    base_url = "http://synthetic.invalid"
    timeout = 1
    token = "synthetic"

    def __init__(self, source="claude_code"):
        self.source = source
        self.accepted = {}
        self.streams = {}
        self.calls = []
        self.status = 202
        self.finalize_status = 202
        self.legacy = False

    def receipts(self, sid):
        result = dict(
            protocol_version=2,
            customer_id="synthetic",
            source=self.source,
            session_id=sid,
            state="legacy" if self.legacy else "absent",
            receipts=[],
        )
        if sid in self.streams:
            result.update(state="ready", stream=self.streams[sid])
        return result

    def post(self, encoded):
        body = json.loads(encoded)
        self.calls.append(encoded)
        status = self.finalize_status if body.get("finalize") else self.status
        if status != 202:
            return status, {"detail": "synthetic failure"}
        key = body["session_id"], body["batch_seq"]
        if key in self.accepted and self.accepted[key] != encoded:
            return 409, {"detail": "immutable conflict"}
        self.accepted[key] = encoded
        receipt = {
            k: body[k]
            for k in (
                "batch_seq",
                "source_byte_end",
                "source_line_end",
                "event_end",
                "prefix_sha256",
            )
        }
        receipt.update(
            body_sha256=hashlib.sha256(encoded).hexdigest(), finalized=bool(body.get("finalize"))
        )
        self.streams[body["session_id"]] = dict(
            receipt, stream_id=body["stream_id"], last_seq=body["batch_seq"]
        )
        return 202, {"protocol_version": 2, "receipt": receipt}

    @property
    def events(self):
        return [e for body in self.accepted.values() for e in json.loads(body).get("events", [])]


def _transcript(tmp_path, *, lines=12, source="claude_code", sid=None, session=None):
    sid = sid or session or str(uuid4())
    path = tmp_path / f"{sid}.jsonl"
    header = []
    if source == "pi":
        header = [dict(type="session", id=sid, version=3, cwd="/synthetic")]
        events = [
            dict(
                type="message",
                id=str(i),
                parentId=str(i - 1),
                message=dict(
                    role="bashExecution",
                    command="echo synthetic",
                    output="private output",
                    exitCode=0,
                ),
            )
            for i in range(lines)
        ]
    elif source == "codex":
        header = [dict(type="session_meta", payload=dict(id=sid, cwd="/synthetic"))]
        events = [
            dict(
                type="response_item",
                payload=dict(
                    type="message", role="user", content=[dict(type="input_text", text=f"turn {i}")]
                ),
            )
            for i in range(lines)
        ]
    else:
        events = [
            dict(
                type="user",
                sessionId=sid,
                cwd="/synthetic",
                toolUseResult=dict(stdout="private output"),
                message=dict(role="user", content=f"turn {i}"),
            )
            for i in range(lines)
        ]
    path.write_bytes(
        b"\r\nnot-json\n" + b"".join(json.dumps(e).encode() + b"\r\n" for e in header + events)
    )
    return bt.Transcript(path, sid, source, "/synthetic", path.stat().st_size, path.stat().st_mtime)


@pytest.fixture(autouse=True)
def isolated_state(tmp_path, monkeypatch):
    monkeypatch.setenv("PROBE_TRANSCRIPT_STATE_DIR", str(tmp_path / "state"))


@pytest.fixture
def wire(monkeypatch):
    wire = FakeWire()
    monkeypatch.setattr(bt, "Wire", lambda *args, **kwargs: wire)
    return wire


def journal_for(transcript, wire, *, historical=True, **kwargs):
    journal = Journal(wire.base_url, "synthetic", transcript.agent, **kwargs)
    journal.ensure(
        transcript.session_id,
        transcript.path,
        wire.receipts(transcript.session_id),
        historical=historical,
        provenance=validate_identity(transcript.path, transcript.agent, transcript.session_id),
    )
    return journal


def drain(journal, transcript, wire, *, size=2600, historical_only=True, finalize=False):
    while journal.stage(
        transcript.session_id,
        cwd=transcript.cwd,
        historical_only=historical_only,
        finalize=finalize,
        max_body_bytes=size,
    ):
        journal.deliver(transcript.session_id, wire)


@pytest.mark.parametrize("source,expected", [("claude_code", 12), ("codex", 13), ("pi", 25)])
def test_raw_cursor_and_retained_ordinals_survive_many_batches(tmp_path, source, expected):
    transcript = _transcript(tmp_path, source=source)
    wire = FakeWire(source)
    with_journal = journal_for(transcript, wire)
    try:
        drain(with_journal, transcript, wire, size=2900)
        events = wire.events
        assert len(events) == expected
        assert [e["line_no"] for e in events] == list(range(expected))
        state = with_journal.get(transcript.session_id)
        assert state["source_byte_end"] == transcript.path.stat().st_size
        assert state["source_line_end"] == 14 + (source != "claude_code")
        assert state["event_end"] == expected and state["historical_complete"]
        assert len(wire.accepted) > 2
        assert "private output" not in b"".join(wire.accepted.values()).decode()
    finally:
        with_journal.close()


@pytest.mark.parametrize("status", [0, 401, 403, 409, 413, 422, 500])
def test_failure_preserves_exact_pending_bytes_and_cursor(tmp_path, wire, status):
    transcript = _transcript(tmp_path)
    journal = journal_for(transcript, wire)
    body = journal.stage(transcript.session_id, cwd=transcript.cwd)
    wire.status = status
    with pytest.raises((DeliveryPending, ReconciliationRequired)):
        journal.deliver(transcript.session_id, wire)
    assert journal.pending(transcript.session_id) == body
    assert journal.get(transcript.session_id)["source_byte_end"] == 0
    wire.status = 202
    journal.deliver(transcript.session_id, wire)
    assert wire.calls[-1] == body and journal.pending(transcript.session_id) is None
    journal.close()


def _kill_window(path, sid, directory, phase, received):
    transcript = bt.Transcript(Path(path), sid, "claude_code", "/synthetic", 0, 0)
    wire = FakeWire()
    journal = journal_for(transcript, wire, directory=Path(directory))
    body = journal.stage(sid, cwd=transcript.cwd)
    if phase != "reserved":
        with open(received, "wb") as handle:
            handle.write(body)
            handle.flush()
            os.fsync(handle.fileno())
        code, response = wire.post(body)
        if phase == "acknowledged":
            journal.acknowledge(sid, response)
    os.kill(os.getpid(), signal.SIGKILL)


@pytest.mark.parametrize("phase", ["reserved", "accepted", "acknowledged"])
def test_real_sigkill_reopens_durable_reservation_and_ack(tmp_path, phase):
    transcript = _transcript(tmp_path)
    directory = tmp_path / "kill-state"
    received = tmp_path / "remote-accepted"
    child = multiprocessing.get_context("fork").Process(
        target=_kill_window,
        args=(str(transcript.path), transcript.session_id, str(directory), phase, str(received)),
    )
    child.start()
    child.join(timeout=10)
    assert child.exitcode == -signal.SIGKILL
    wire = FakeWire()
    journal = Journal(wire.base_url, "synthetic", "claude_code", directory=directory)
    if phase == "acknowledged":
        assert journal.pending(transcript.session_id) is None
        assert journal.get(transcript.session_id)["source_byte_end"] > 0
    else:
        pending = journal.pending(transcript.session_id)
        assert pending and journal.get(transcript.session_id)["source_byte_end"] == 0
        if received.exists():
            assert pending == received.read_bytes()
        journal.deliver(transcript.session_id, wire)
        assert wire.calls == [pending]
    journal.close()


def test_live_and_historical_producers_share_one_atomic_pending_batch(tmp_path, wire):
    transcript = _transcript(tmp_path)
    first = journal_for(transcript, wire)
    second = Journal(wire.base_url, "synthetic", transcript.agent)
    second.ensure(
        transcript.session_id,
        transcript.path,
        wire.receipts(transcript.session_id),
        historical=False,
    )
    original = first.stage(transcript.session_id, cwd=transcript.cwd, max_body_bytes=2900)
    assert second.stage(transcript.session_id, cwd="ignored") == original
    first.deliver(transcript.session_id, wire)
    second.acknowledge(transcript.session_id, wire.post(original)[1])
    drain(second, transcript, wire, size=2900)
    assert len(wire.events) == 12
    assert [e["line_no"] for e in wire.events] == list(range(12))
    first.close()
    second.close()


def test_append_handoff_and_source_mutation_are_not_confused(tmp_path, wire):
    transcript = _transcript(tmp_path, lines=2)
    journal = journal_for(transcript, wire)
    drain(journal, transcript, wire)
    with transcript.path.open("ab") as handle:
        handle.write(
            json.dumps(
                dict(
                    type="user",
                    sessionId=transcript.session_id,
                    message=dict(role="user", content="tail"),
                )
            ).encode()
            + b"\n"
        )
    journal.ensure(
        transcript.session_id,
        transcript.path,
        wire.receipts(transcript.session_id),
        historical=False,
    )
    drain(journal, transcript, wire, historical_only=False, finalize=True)
    assert [e["line_no"] for e in wire.events] == [0, 1, 2]
    transcript.path.write_bytes(b"changed" + transcript.path.read_bytes()[7:])
    with pytest.raises(ReconciliationRequired):
        journal.stage(transcript.session_id, cwd="")
    journal.close()


def test_legacy_receipts_and_cross_tenant_adoption_never_stage(tmp_path, wire):
    transcript = _transcript(tmp_path)
    wire.legacy = True
    with pytest.raises(ReconciliationRequired):
        journal_for(transcript, wire)
    wire.legacy = False
    journal = Journal(wire.base_url, "other", transcript.agent)
    with pytest.raises(ReconciliationRequired):
        journal.ensure(
            transcript.session_id,
            transcript.path,
            wire.receipts(transcript.session_id),
            historical=True,
        )
    assert journal.pending(transcript.session_id) is None
    journal.close()


def test_capacity_backpressure_keeps_previous_pending(tmp_path, wire):
    transcript = _transcript(tmp_path)
    journal = journal_for(transcript, wire)
    body = journal.stage(transcript.session_id, cwd="")
    other = _transcript(tmp_path)
    journal.ensure(other.session_id, other.path, wire.receipts(other.session_id), historical=False)
    journal.cap_bytes = len(body)
    with pytest.raises(DeliveryPending, match="queue full"):
        journal.stage(other.session_id, cwd="")
    assert journal.pending(transcript.session_id) == body
    journal.close()


def test_identity_and_duplicate_checks_do_not_infer_from_size(tmp_path):
    transcript = _transcript(tmp_path, lines=3)
    valid = validate_identity(transcript.path, transcript.agent, transcript.session_id)
    assert valid["original_author"] == "unverified"
    with pytest.raises(ReconciliationRequired):
        validate_identity(transcript.path, transcript.agent, str(uuid4()))
    copy = tmp_path / "copy.jsonl"
    copy.write_bytes(transcript.path.read_bytes() + b"\n")
    assert compatible_copy(transcript.path, copy)
    copy.write_bytes(b"different" + copy.read_bytes())
    assert not compatible_copy(transcript.path, copy)


def test_finalize_failure_is_reported_and_retry_does_not_resend_events(tmp_path, wire):
    transcript = _transcript(tmp_path)
    wire.finalize_status = 500
    poster = bt.Poster(wire.base_url, wire.token)
    record = bt.SessionRecord(session_id=transcript.session_id)
    result = bt.upload_session(transcript, record, poster, device_id="")
    assert not result.ok and "500" in result.error
    accepted = len(wire.events)
    wire.finalize_status = 202
    result = bt.upload_session(transcript, record, poster, device_id="")
    assert result.ok and record.finalized and len(wire.events) == accepted


def test_a_finalized_session_is_not_re_sent_and_never_anchors(tmp_path, wire):
    """The lane is idempotent per session and `assignments` is inert.

    Re-running over a census whose sessions are already finalized must send no
    further events -- a reused batch sequence overwrites a stored blob rather
    than being rejected -- and a folder assignment must never become an entity
    link. (This used to also cover the digest submit/retry that ran after
    finalization; that stage went with the server-side digest lane.)
    """
    transcript = _transcript(tmp_path)
    stages = []

    args = dict(
        poster=bt.Poster(wire.base_url, wire.token),
        device_id="",
        ledger=bt.TranscriptLedger(tmp_path / "old-ledger"),
        assignments={"/synthetic": "forbidden"},
        on_stage=lambda done, total, transcript, phase: stages.append((done, total, phase)),
    )
    census = bt.Census(candidates=[transcript])
    first = bt.import_transcripts(census, **args)
    assert stages == [
        (0, 1, "Checking upload status"),
        (0, 1, "Uploading session"),
        (1, 1, "Session processed"),
    ]
    count = len(wire.events)
    assert first.uploaded == 1 and first.finalized == 1 and first.anchored == 0

    second = bt.import_transcripts(census, **args)
    assert second.finalized == 1 and second.failed == 0
    assert len(wire.events) == count


@pytest.fixture
def background_job(tmp_path, wire, monkeypatch):
    from types import SimpleNamespace
    from probe.cli import capabilities, import_jobs
    from probe.sdk import client as sdk_client, config

    class Client(FakeClient):
        settings = SimpleNamespace(base_url=wire.base_url, workspace=None, token="never-persist")
        identity = {"customer_id": "synthetic", "user_id": "person"}

        def me(self):
            return self.identity

        def __enter__(self):
            return self

        def __exit__(self, *args):
            return False

    client = Client()
    monkeypatch.setattr(sdk_client, "Client", lambda **kwargs: client)
    monkeypatch.setattr(config, "current_context_name", lambda: "approved-account")
    monkeypatch.setattr(config, "resolve", lambda **kwargs: client.settings)
    monkeypatch.setattr(capabilities, "resolved_capture_credential", lambda source: (wire.token, wire.base_url))
    monkeypatch.setattr(capabilities, "capture_device_id", lambda source: "approved-device")
    ledger = bt.TranscriptLedger(tmp_path / "transcript-ledger.jsonl")
    monkeypatch.setattr(bt.TranscriptLedger, "for_device", classmethod(lambda cls: ledger))
    monkeypatch.setattr(bt, "fetch_ingest_state", lambda *a: None)
    transcript = _transcript(tmp_path)
    payload = bt._background_payload(
        bt.Census(candidates=[transcript]), client=client,
        posters={bt.CLAUDE: bt.Poster(wire.base_url, wire.token)},
        devices={bt.CLAUDE: "approved-device"}, budget_bytes=None, unpaired=[],
    )
    return payload, transcript, client, import_jobs.JobError


def test_background_worker_imports_exact_reviewed_prefix_and_resumes_without_duplicates(
    background_job, tmp_path, wire, monkeypatch,
):
    payload, transcript, _client, _error = background_job
    _transcript(tmp_path)  # A newer session is outside this approval.
    with transcript.path.open("a") as handle:
        handle.write(json.dumps({
            "type": "user", "sessionId": transcript.session_id,
            "message": {"role": "user", "content": "after approval"},
        }) + "\n")
    monkeypatch.setattr(bt, "discover", lambda **kwargs: pytest.fail("background rediscovery"))
    progress = []
    lines = bt.run_background_job(payload, progress=lambda message, **fields: progress.append((message, fields)))
    assert len(wire.events) == 12
    assert all("after approval" not in json.dumps(event) for event in wire.events)
    assert set(wire.streams) == {transcript.session_id}
    assert progress[-1][1]["uploaded"] == 1
    assert any("uploaded" in line for line in lines)
    bt.run_background_job(payload, progress=lambda *a, **k: None)
    assert len(wire.events) == 12


def test_background_worker_refuses_changed_reviewed_bytes(background_job, wire):
    payload, transcript, _client, error = background_job
    transcript.path.write_bytes(transcript.path.read_bytes().replace(b"turn 0", b"EDIT 0"))
    with pytest.raises(error, match="review it again"):
        bt.run_background_job(payload, progress=lambda *a, **k: None)
    assert wire.calls == []


def test_background_worker_refuses_account_change_before_upload(background_job, wire):
    payload, _transcript, client, error = background_job
    client.identity = {"customer_id": "another-team", "user_id": "person"}
    with pytest.raises(error, match="account changed"):
        bt.run_background_job(payload, progress=lambda *a, **k: None)
    assert wire.calls == []


def test_background_worker_checks_capture_tenant_before_sending_bytes(background_job, wire, monkeypatch):
    payload, _transcript, _client, error = background_job
    original = wire.receipts

    def receipts(session):
        return {**original(session), "customer_id": "another-team"}

    monkeypatch.setattr(wire, "receipts", receipts)
    with pytest.raises(error, match="different team"):
        bt.run_background_job(payload, progress=lambda *a, **k: None)
    assert wire.calls == []


@pytest.mark.parametrize("status", [408, 429, 500, 503])
def test_background_network_retry_preserves_pending_bytes_and_reviewed_scope(
    background_job, wire, tmp_path, monkeypatch, status,
):
    from probe.cli import import_jobs

    payload, transcript, _client, _error = background_job
    wire.status = status
    with pytest.raises(import_jobs.RetryableJobError):
        bt.run_background_job(payload, progress=lambda *a, **k: None)
    pending = wire.calls[-1]
    assert wire.events == []
    _transcript(tmp_path)  # A new session while offline is not part of this approval.
    with transcript.path.open("a") as handle:
        handle.write(json.dumps({
            "type": "user", "sessionId": transcript.session_id,
            "message": {"role": "user", "content": "after approval"},
        }) + "\n")
    monkeypatch.setattr(bt, "discover", lambda **kwargs: pytest.fail("background rediscovery"))
    wire.status = 202
    bt.run_background_job(payload, progress=lambda *a, **k: None)
    assert wire.calls[1] == pending
    assert len(wire.events) == 12
    assert set(wire.streams) == {transcript.session_id}
    assert all("after approval" not in json.dumps(event) for event in wire.events)


def test_background_finalize_retry_reuses_accepted_event_receipts(background_job, wire):
    from probe.cli import import_jobs

    payload, _transcript, _client, _error = background_job
    wire.finalize_status = 503
    with pytest.raises(import_jobs.RetryableJobError):
        bt.run_background_job(payload, progress=lambda *a, **k: None)
    assert len(wire.events) == 12
    first_attempts = len(wire.calls)
    wire.finalize_status = 202
    bt.run_background_job(payload, progress=lambda *a, **k: None)
    assert len(wire.events) == 12
    assert all(json.loads(body).get("finalize") for body in wire.calls[first_attempts:])


def test_background_outage_waits_before_attempting_other_approved_sessions(
    background_job, wire, tmp_path,
):
    from probe.cli import import_jobs

    payload, transcript, client, _error = background_job
    another = _transcript(tmp_path)
    payload = bt._background_payload(
        bt.Census(candidates=[transcript, another]), client=client,
        posters={bt.CLAUDE: bt.Poster(wire.base_url, wire.token)},
        devices={bt.CLAUDE: "approved-device"}, budget_bytes=None, unpaired=[],
    )
    wire.status = 503
    with pytest.raises(import_jobs.RetryableJobError):
        bt.run_background_job(payload, progress=lambda *a, **k: None)
    assert {json.loads(body)["session_id"] for body in wire.calls} == {transcript.session_id}
    wire.status = 202
    bt.run_background_job(payload, progress=lambda *a, **k: None)
    assert set(wire.streams) == {transcript.session_id, another.session_id}


@pytest.mark.parametrize("status", [0, 400, 401, 403, 409, 422])
def test_background_auth_protocol_and_untyped_failures_need_attention(background_job, wire, status):
    from probe.cli import import_jobs

    payload, _transcript, _client, _error = background_job
    wire.status = status
    with pytest.raises(import_jobs.JobError) as error:
        bt.run_background_job(payload, progress=lambda *a, **k: None)
    assert not isinstance(error.value, import_jobs.RetryableJobError)


@pytest.mark.parametrize("stage,status", [("upload", 403), ("finalization", 409)])
def test_background_failure_names_session_stage_and_http_status_without_response_body(
    background_job, wire, monkeypatch, stage, status,
):
    from probe.cli import import_jobs

    payload, transcript, _client, _error = background_job
    post = wire.post

    def fail(encoded):
        if bool(json.loads(encoded).get("finalize")) == (stage == "finalization"):
            return status, {"detail": "Bearer private-token https://private.invalid/?secret=value"}
        return post(encoded)

    monkeypatch.setattr(wire, "post", fail)
    events = []
    with pytest.raises(import_jobs.JobError) as error:
        bt.run_background_job(payload, progress=lambda message, **fields: events.append((message, fields)))
    text = "\n".join([str(error.value), *(message for message, _ in events)])
    assert transcript.session_id in text
    assert f"{stage}: HTTP {status}" in text
    assert "Session failed" in text and "Session processed" not in text
    assert "0/1 finalized, 1 failed" in str(error.value)
    assert "private" not in text and "secret" not in text
    assert events[-1][1]["completion_completed"] == 0


def test_background_mixed_failures_log_each_reason_and_keep_confirmed_completion(
    background_job, wire, tmp_path, monkeypatch,
):
    from probe.cli import import_jobs

    payload, first, client, _error = background_job
    rejected, timed_out = _transcript(tmp_path), _transcript(tmp_path)
    payload = bt._background_payload(
        bt.Census(candidates=[first, rejected, timed_out]), client=client,
        posters={bt.CLAUDE: bt.Poster(wire.base_url, wire.token)},
        devices={bt.CLAUDE: "approved-device"}, budget_bytes=None, unpaired=[],
    )
    post = wire.post

    def fail(encoded):
        session = json.loads(encoded)["session_id"]
        if session == rejected.session_id:
            return 422, {"detail": "private server response"}
        if session == timed_out.session_id:
            wire.last_request_retryable = True
            wire.last_request_error = "TimeoutError"
            return 0, {"detail": "private signed URL"}
        return post(encoded)

    monkeypatch.setattr(wire, "post", fail)
    events = []
    with pytest.raises(import_jobs.JobError) as error:
        bt.run_background_job(payload, progress=lambda message, **fields: events.append((message, fields)))
    assert not isinstance(error.value, import_jobs.RetryableJobError)
    assert "1/3 finalized, 2 failed" in str(error.value)
    text = "\n".join(message for message, _ in events)
    assert f"{rejected.session_id} — delivery: upload: HTTP 422" in text
    assert f"{timed_out.session_id} — delivery: upload: request failed (TimeoutError)" in text
    assert "private" not in text
    assert events[-1][1]["completion_ids"] == [[bt.CLAUDE, first.session_id]]


def test_resumed_import_details_show_how_many_sessions_the_worker_has_processed(
    background_job, wire, tmp_path, monkeypatch,
):
    """A resumed import re-checks every approved session from the start while
    its bar already holds what Probe confirmed, so the bar alone reads as hung.
    The detail page names the walk position from what the real worker saves,
    and only on the walk's own updates."""
    from copy import deepcopy
    from probe.cli import import_jobs as jobs, import_jobs_ui as ui

    payload, confirmed, client, _error = background_job
    rejected = _transcript(tmp_path)
    payload = bt._background_payload(
        bt.Census(candidates=[confirmed, rejected]), client=client,
        posters={bt.CLAUDE: bt.Poster(wire.base_url, wire.token)},
        devices={bt.CLAUDE: "approved-device"}, budget_bytes=None, unpaired=[],
    )
    monkeypatch.setenv("XDG_STATE_HOME", str(tmp_path / "jobs"))
    monkeypatch.setattr(jobs, "_launch", lambda folder: jobs._read(folder))
    monkeypatch.setattr(jobs, "_post_failure_report", lambda *args: None)
    post = wire.post

    def reject(encoded):
        if json.loads(encoded)["session_id"] == rejected.session_id:
            return 422, {"detail": "synthetic rejection"}
        return post(encoded)

    saved, save = [], jobs._save

    def observe(folder, value):
        save(folder, value)
        saved.append(deepcopy(value))

    monkeypatch.setattr(jobs, "_save", observe)
    monkeypatch.setattr(wire, "post", reject)
    job = jobs.enqueue(jobs.Kind.TRANSCRIPTS, payload, "Sessions")
    assert jobs.run_worker(job["id"]) == 1

    monkeypatch.setattr(wire, "post", post)
    jobs.resume(job["id"])
    assert jobs.run_worker(job["id"]) == 0

    running = [value for value in saved if value["state"] == jobs.State.RUNNING]
    walking = [ui._summary(value) for value in running if value["attempt"] == 2
               and value["progress"]["message"] == "Checking upload status"]
    assert len(walking) == 2
    assert walking[0][1].endswith("  1/2")
    assert walking[0][2] == "  Checking upload status · 0/2 processed"
    assert walking[1][2] == "  Checking upload status · 1/2 processed"
    # Only the walk names a position. The start and the paused and finished
    # summaries, whose `completed` counts uploads, are saved RUNNING too.
    outside = {value["progress"].get("message") for value in running if not value["progress"].get("session_id")}
    assert {"Starting the approved import.", "Session import paused", "Session import finished"} <= outside
    for value in running:
        positioned = ui._status_message(value) != value["progress"].get("message", "")
        assert positioned == bool(value["progress"].get("session_id")), value["progress"].get("message")
    finished = jobs.get_job(job["id"])
    assert finished["state"] == jobs.State.SUCCEEDED
    assert ui._status_message(finished) == finished["progress"]["message"]


def test_background_receipt_timeout_names_receipt_stage(background_job, wire, monkeypatch):
    from probe.cli import import_jobs

    payload, transcript, _client, _error = background_job

    def fail(_session):
        raise DeliveryPending("private URL", retryable=True, safe_message="request failed (TimeoutError)")

    monkeypatch.setattr(wire, "receipts", fail)
    events = []
    with pytest.raises(import_jobs.RetryableJobError) as error:
        bt.run_background_job(payload, progress=lambda message, **fields: events.append(message))
    assert f"{transcript.session_id} — receipt check: request failed (TimeoutError)" in str(error.value)
    assert "private" not in str(error.value)
    assert wire.calls == []


def test_worker_persists_the_failure_reason_in_log_and_job_details(background_job, wire, tmp_path, monkeypatch):
    from types import SimpleNamespace
    from probe.cli import import_jobs

    payload, transcript, _client, _error = background_job
    monkeypatch.setenv("XDG_STATE_HOME", str(tmp_path))
    monkeypatch.setattr(import_jobs.subprocess, "Popen", lambda *a, **k: SimpleNamespace(pid=os.getpid(), wait=lambda: 0))
    monkeypatch.setattr(wire, "post", lambda encoded: (403, {"detail": "private signed URL"}))
    job = import_jobs.enqueue(import_jobs.Kind.TRANSCRIPTS, payload, "Session import")
    assert import_jobs.run_worker(job["id"]) == 1
    saved = import_jobs.get_job(job["id"])
    log = Path(saved["log_path"]).read_text()
    assert saved["state"] == import_jobs.State.FAILED
    assert "Session failed" in log
    for text in (log, saved["error"]):
        assert transcript.session_id in text and "upload: HTTP 403" in text
        assert "private" not in text
    assert saved["progress"]["completion_completed"] == 0


@pytest.mark.parametrize("failure", [PermissionError(13, "private path", "/private/file"), sqlite3.OperationalError("private SQL")])
def test_background_local_failure_does_not_expose_paths_or_sql(background_job, wire, monkeypatch, failure):
    from probe.cli import import_jobs

    payload, _transcript, _client, _error = background_job

    def fail(*args, **kwargs):
        raise failure

    monkeypatch.setattr(bt.Journal, "ensure", fail)
    events = []
    with pytest.raises(import_jobs.JobError) as error:
        bt.run_background_job(payload, progress=lambda message, **fields: events.append(message))
    text = "\n".join([str(error.value), *events])
    assert type(failure).__name__ in text
    assert "snapshot" in text and "private" not in text


def test_broken_journal_cleanup_keeps_original_failure_and_closes(background_job, monkeypatch):
    from probe.cli import import_jobs

    payload, _transcript, _client, _error = background_job
    closed = []
    close = bt.Journal.close

    def fail(*args, **kwargs):
        raise sqlite3.OperationalError("private database path")

    def record_close(self):
        closed.append(self)
        close(self)

    monkeypatch.setattr(bt.Journal, "ensure", fail)
    monkeypatch.setattr(bt.Journal, "pending", fail)
    monkeypatch.setattr(bt.Journal, "close", record_close)
    events = []
    with pytest.raises(import_jobs.JobError) as error:
        bt.run_background_job(payload, progress=lambda message, **fields: events.append(message))
    text = "\n".join([str(error.value), *events])
    assert "snapshot: local transcript journal failed (OperationalError)" in text
    assert "1 failed" in str(error.value)
    assert "Session failed" in text and "private" not in text
    assert len(closed) == 1


@pytest.mark.parametrize("response", [b"[]", b"null", b"not json", b'{"detail":"private token"}'])
@pytest.mark.parametrize("status", [403, 503])
def test_http_error_response_shape_preserves_safe_status_and_retryability(monkeypatch, response, status):
    import io
    import urllib.error
    import urllib.request
    from probe.tap_core.session_journal import Wire

    def fail(*args, **kwargs):
        raise urllib.error.HTTPError("https://private.invalid/?token=secret", status, "private", {}, io.BytesIO(response))

    monkeypatch.setattr(urllib.request, "urlopen", fail)
    transport = Wire("https://synthetic.invalid", "private-token", bt.CLAUDE)
    with pytest.raises(DeliveryPending) as error:
        transport.receipts("synthetic-session")
    assert f"HTTP {status}" in error.value.safe_message
    assert error.value.retryable == (status == 503)
    assert "private" not in error.value.safe_message and "secret" not in error.value.safe_message
    code, body = transport.post(b"{}")
    assert code == status and isinstance(body, dict)


@pytest.mark.parametrize("status", [403, 429, 503])
def test_http_error_body_timeout_keeps_known_status(monkeypatch, status):
    import io
    import urllib.error
    import urllib.request
    from probe.tap_core.session_journal import Wire

    class SlowBody(io.BytesIO):
        def read(self, *args):
            raise TimeoutError("private signed URL")

    def fail(*args, **kwargs):
        raise urllib.error.HTTPError("https://synthetic.invalid", status, "private", {}, SlowBody())

    monkeypatch.setattr(urllib.request, "urlopen", fail)
    transport = Wire("https://synthetic.invalid", "private-token", bt.CLAUDE)
    with pytest.raises(DeliveryPending) as error:
        transport.receipts("synthetic-session")
    assert f"HTTP {status}" in error.value.safe_message
    assert error.value.retryable == (status in (429, 503))
    assert "private" not in error.value.safe_message



def test_background_account_check_retries_connectivity_before_upload(background_job, wire, monkeypatch):
    from probe.cli import import_jobs
    from probe.sdk.errors import TransportError

    payload, _transcript, client, _error = background_job
    me = client.me

    def disconnected():
        raise TransportError("connection unavailable")

    monkeypatch.setattr(client, "me", disconnected)
    with pytest.raises(import_jobs.RetryableJobError):
        bt.run_background_job(payload, progress=lambda *a, **k: None)
    assert wire.calls == []
    monkeypatch.setattr(client, "me", me)
    bt.run_background_job(payload, progress=lambda *a, **k: None)
    assert len(wire.events) == 12


def test_background_ingest_check_retains_the_network_cause(background_job, wire, monkeypatch):
    from probe.cli import import_jobs
    from probe.sdk.errors import TransportError

    payload, _transcript, _client, _error = background_job

    def disconnected(*args):
        try:
            raise TransportError("connection unavailable")
        except TransportError as exc:
            raise bt.ProbeUnavailable("cannot check ingestion") from exc

    monkeypatch.setattr(bt, "fetch_ingest_state", disconnected)
    with pytest.raises(import_jobs.RetryableJobError):
        bt.run_background_job(payload, progress=lambda *a, **k: None)
    assert wire.calls == []
    monkeypatch.setattr(bt, "fetch_ingest_state", lambda *a: None)
    bt.run_background_job(payload, progress=lambda *a, **k: None)
    assert len(wire.events) == 12


@pytest.mark.parametrize("kind,retryable", [
    ("timeout", True), ("refused", True), ("dns", True),
    ("invalid-json", False), ("permission", False), ("tls", False),
])
def test_receipt_transport_preserves_only_real_network_interruptions(monkeypatch, kind, retryable):
    import socket
    import ssl
    import urllib.error
    import urllib.request
    from probe.tap_core.session_journal import Wire

    failure = {
        "timeout": TimeoutError("timeout"),
        "refused": urllib.error.URLError(ConnectionRefusedError("refused")),
        "dns": urllib.error.URLError(socket.gaierror("name unavailable")),
        "invalid-json": ValueError("invalid response"),
        "permission": PermissionError("local permission"),
        "tls": urllib.error.URLError(ssl.SSLCertVerificationError("bad certificate")),
    }[kind]

    def fail(*args, **kwargs):
        raise failure

    monkeypatch.setattr(urllib.request, "urlopen", fail)
    transport = Wire("http://synthetic.invalid", "synthetic", bt.CLAUDE)
    with pytest.raises(DeliveryPending) as error:
        transport.receipts("synthetic-session")
    assert error.value.retryable is retryable


class FakeTransport:
    def __init__(self, state: dict | None = None) -> None:
        self.state = state
        self.error: Exception | None = None
        self.posts: list[tuple[str, dict]] = []
        self.gets: list[str] = []

    def get(self, path: str, **_: object) -> dict:
        self.gets.append(path)
        if self.state is None:
            raise self.error or RuntimeError("route not found")
        return self.state

    def post(self, path: str, body: dict | None = None, **_: object) -> dict:
        self.posts.append((path, body or {}))
        return {"status": "accepted"}


class FakeClient:
    def __init__(self, state: dict | None = None) -> None:
        self.transport = FakeTransport(state)


def test_the_ledger_round_trips_a_session_and_survives_a_torn_line(tmp_path) -> None:
    ledger = bt.TranscriptLedger(tmp_path / "transcripts.jsonl")
    ledger.record_session(
        bt.SessionRecord(
            session_id="s-1",
            state=bt.SessionState.DONE,
            last_seq=3,
            byte_end=900,
            line_no=12,
            finalized=True,
        )
    )
    with ledger.path.open("a", encoding="utf-8") as handle:
        handle.write('{"t": "session", "session_id": "torn"')  # killed mid-write

    state = ledger.read()

    assert state["s-1"].last_seq == 3
    assert state["s-1"].line_no == 12
    assert state["s-1"].state is bt.SessionState.DONE
    assert "torn" not in state


def test_an_unknown_record_kind_is_ignored_not_fatal(tmp_path) -> None:
    """A newer importer may write facts this one does not know. Refusing the
    file would re-upload every session on the machine."""
    ledger = bt.TranscriptLedger(tmp_path / "t.jsonl")
    ledger.record_session(bt.SessionRecord(session_id="s-1", state=bt.SessionState.DONE))
    ledger._append({"t": "something-from-the-future", "wat": True})

    assert set(ledger.read()) == {"s-1"}


def test_done_sessions_are_skipped_and_partial_ones_resume(tmp_path) -> None:
    ledger = bt.TranscriptLedger(tmp_path / "t.jsonl")
    ledger.record_session(bt.SessionRecord(session_id="done", state=bt.SessionState.DONE))
    ledger.record_session(bt.SessionRecord(session_id="partial", state=bt.SessionState.PARTIAL))

    assert ledger.done_sessions() == {"done"}
    assert ledger.resumable_sessions() == {"partial"}


def test_a_session_already_in_probe_is_excluded(tmp_path) -> None:
    census = bt.Census(candidates=[_transcript(tmp_path, session="s-1")])
    client = FakeClient({"known": True, "ingested": True})

    bt.exclude_ingested(census, client)

    assert census.candidates == []
    assert census.already_in_probe == 1


def test_a_session_known_only_through_an_entity_write_is_still_uploaded(tmp_path) -> None:
    """`known` is not `ingested`. Conflating them strands the transcript."""
    census = bt.Census(candidates=[_transcript(tmp_path, session="s-1")])
    client = FakeClient({"known": True, "ingested": False})

    bt.exclude_ingested(census, client)

    assert len(census.candidates) == 1
    assert census.already_in_probe == 0


def test_our_own_partial_upload_is_not_mistaken_for_a_duplicate(tmp_path) -> None:
    """A PARTIAL session already has an activity row with a device id, so the
    server answers `ingested` -- and skipping it would strand the tail of the
    very conversation this importer was in the middle of shipping."""
    ledger = bt.TranscriptLedger(tmp_path / "t.jsonl")
    ledger.record_session(bt.SessionRecord(session_id="s-1", state=bt.SessionState.PARTIAL))
    census = bt.Census(candidates=[_transcript(tmp_path, session="s-1")])
    client = FakeClient({"known": True, "ingested": True})

    bt.exclude_ingested(census, client, ledger=ledger)

    assert len(census.candidates) == 1
    assert client.transport.gets == [], "the ledger answers before the network does"


def test_an_older_server_without_the_route_falls_back_to_shipping(tmp_path) -> None:
    from probe.sdk import errors

    census = bt.Census(candidates=[_transcript(tmp_path, session="s-1")])
    client = FakeClient(state=None)
    client.transport.error = errors.NotFoundError("no such route")

    bt.exclude_ingested(census, client)

    assert len(census.candidates) == 1


def test_a_transient_failure_stops_the_lane_rather_than_authorising_a_re_upload(
    tmp_path,
) -> None:
    """The difference between "no such route" and "the server blinked".

    Folding them together means a flaky link during the pre-flight pass reports
    every session as absent, and the importer re-POSTs from sequence 0 over
    sessions the server already holds -- overwriting their stored blobs.
    """
    census = bt.Census(candidates=[_transcript(tmp_path, session="s-1")])
    client = FakeClient(state=None)
    client.transport.error = TimeoutError("connection timed out")

    with pytest.raises(bt.ProbeUnavailable):
        bt.exclude_ingested(census, client)


def test_a_codex_filename_without_a_uuid_is_not_given_a_fabricated_id(tmp_path) -> None:
    """The tap's anchored pattern, so the two agree on what a session id is."""
    assert bt.session_id_for(tmp_path / "notes-a-b-c-d-e.jsonl", bt.CODEX) is None
    assert (
        bt.session_id_for(
            tmp_path / "rollout-2026-08-21T08-01-56-01a02357-44b8-7703-8ded-974b57fd1a8a.jsonl",
            bt.CODEX,
        )
        == "01a02357-44b8-7703-8ded-974b57fd1a8a"
    )
    # The sidechain rule applies to BOTH agents, not just Claude Code.
    assert bt.session_id_for(tmp_path / "agent-9f2b.jsonl", bt.CODEX) is None


def test_finalize_request_cannot_skip_the_frozen_unread_tail(tmp_path, wire):
    transcript = _transcript(tmp_path, lines=12)
    journal = journal_for(transcript, wire)
    first = journal.stage(transcript.session_id, cwd="", finalize=True, max_body_bytes=2600)
    assert first and not json.loads(first).get("finalize")
    assert json.loads(first)["source_byte_end"] < transcript.path.stat().st_size
    assert json.loads(first)["snapshot_byte_end"] == transcript.path.stat().st_size
    # A second producer requesting completion still sees the exact pending tail.
    assert journal.stage(transcript.session_id, cwd="", finalize=True) == first
    assert not journal.get(transcript.session_id)["finalized"]
    journal.close()


def test_cross_device_resume_preserves_the_remote_historical_prefix(tmp_path, wire):
    transcript = _transcript(tmp_path, lines=4)
    original_size = transcript.path.stat().st_size
    original_hash = hashlib.sha256(transcript.path.read_bytes()).hexdigest()
    local = journal_for(transcript, wire)
    first = local.stage(transcript.session_id, cwd="", max_body_bytes=2600)
    local.deliver(transcript.session_id, wire)
    remote = wire.receipts(transcript.session_id)
    remote["stream"].update(snapshot_byte_end=original_size, snapshot_sha256=original_hash)
    with transcript.path.open("ab") as handle:
        handle.write(
            json.dumps(
                dict(
                    type="user",
                    sessionId=transcript.session_id,
                    message=dict(role="user", content="later live tail"),
                )
            ).encode()
            + b"\n"
        )
    other = Journal(
        wire.base_url, "synthetic", transcript.agent, directory=tmp_path / "second-device"
    )
    state = other.ensure(transcript.session_id, transcript.path, remote, historical=False)
    assert state["historical_end"] == original_size and state["historical_hash"] == original_hash
    assert Path(state["snapshot_path"]).stat().st_size == original_size
    drain(other, transcript, wire, historical_only=False, finalize=True)
    assert len(wire.events) == 5 and [e["line_no"] for e in wire.events] == list(range(5))
    assert json.loads(first)["snapshot_sha256"] == original_hash
    local.close()
    other.close()


def _race_producer(path, sid, directory, barrier, results):
    journal = Journal(FakeWire.base_url, "synthetic", "claude_code", directory=Path(directory))
    barrier.wait(timeout=5)
    journal.ensure(sid, Path(path), FakeWire().receipts(sid), historical=True)
    results.put(journal.stage(sid, cwd="/synthetic", max_body_bytes=2900))
    journal.close()


def test_two_processes_reserve_one_body_and_one_event_range(tmp_path):
    transcript = _transcript(tmp_path)
    context = multiprocessing.get_context("fork")
    barrier = context.Barrier(2)
    results = context.Queue()
    directory = tmp_path / "concurrent"
    # Create the DB once; race source ownership and reservation transactions.
    Journal(FakeWire.base_url, "synthetic", "claude_code", directory=directory).close()
    children = [
        context.Process(
            target=_race_producer,
            args=(str(transcript.path), transcript.session_id, str(directory), barrier, results),
        )
        for _ in range(2)
    ]
    for child in children:
        child.start()
    bodies = [results.get(timeout=10) for _ in children]
    for child in children:
        child.join(timeout=5)
        assert child.exitcode == 0
    assert bodies[0] == bodies[1]
    journal = Journal(FakeWire.base_url, "synthetic", "claude_code", directory=directory)
    assert journal.pending(transcript.session_id) == bodies[0]
    assert journal.get(transcript.session_id)["source_byte_end"] == 0
    journal.close()


def test_late_ack_of_shared_batch_cannot_retire_its_successor(tmp_path, wire):
    transcript = _transcript(tmp_path)
    first = journal_for(transcript, wire)
    second = Journal(wire.base_url, "synthetic", transcript.agent)
    body = first.stage(transcript.session_id, cwd="", max_body_bytes=2600)
    response = wire.post(body)[1]
    second.acknowledge(transcript.session_id, response, sent_body=body)
    successor = second.stage(transcript.session_id, cwd="", max_body_bytes=2600)
    assert successor != body
    first.acknowledge(transcript.session_id, response, sent_body=body)
    assert first.pending(transcript.session_id) == successor
    first.close()
    second.close()


def test_background_payload_from_an_older_cli_still_imports(background_job, wire):
    """A job saved before the local summary stage was removed names an agent
    and a digest note. Both are ignored; the reviewed conversations upload."""
    payload, _transcript, _client, _error = background_job
    payload.update(agent="claude", digest_note=None)
    bt.run_background_job(payload, progress=lambda *a, **k: None)
    assert len(wire.events) == 12
