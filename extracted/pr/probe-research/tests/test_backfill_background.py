"""A detached folder import only executes its durable, reviewed file scope."""

from contextlib import nullcontext
import json
from pathlib import Path

import pytest

from probe.cli import backfill_import as imp
from probe.cli import backfill_run as runner
from probe.cli import import_jobs, tui
from probe.cli.backfill_coverage import CoverageError
from probe.cli.backfill_ledger import Ledger, Unit
from probe.cli.import_jobs import enqueue as enqueue_job
from probe.sdk import journal
from tests.test_backfill_scoped_orchestration import make_harness


@pytest.fixture
def background_harness(tmp_path, monkeypatch):
    harness = make_harness(tmp_path, monkeypatch)
    queued = []

    def enqueue(*, kind, payload, label):
        assert kind == "folder" and label.startswith("Folder · ")
        # Dispatch must release the foreground writer before the detached
        # process can open this checkpoint.
        with harness.coverage().writer():
            pass
        queued.append(json.loads(json.dumps(payload)))
        return {"id": "folder-job-1"}

    monkeypatch.setattr(import_jobs, "enqueue", enqueue)
    monkeypatch.setattr(imp, "_background_client", lambda payload: nullcontext(harness.client))
    monkeypatch.setattr(harness.client, "flush", lambda **kwargs: journal.drain(
        harness.client.journal, client_factory=lambda _: harness.remote, **kwargs,
    ))
    return harness, queued


def _resume(payload):
    progress = []
    lines = imp.run_background_job(payload, progress=lambda message, **fields: progress.append(
        (message, fields)
    ))
    return lines, progress


def test_approval_queues_a_serializable_plan_before_any_file_execution(background_harness):
    h, queued = background_harness
    lines = h.run(background=True)
    assert h.classified == [["a.py"]]
    assert h.manifested == [] and h.remote.calls == []
    assert len(h.created) == len(queued) == 1
    assert any("Folder import queued: folder-job-1" in line for line in lines)
    saved = queued[0]
    assert saved["targets"] == ["a.py"]
    assert saved["scope"]["customer_id"] == "tenant"
    assert saved["scope"]["workspace_id"] == "workspace"
    assert saved["source_id"] == h.coverage().source_id
    assert "test-token" not in json.dumps(saved)
    assert "value = 1" not in json.dumps(saved)


@pytest.mark.parametrize("state,wording", [("failed", "needs attention"), ("succeeded", "already complete")])
def test_repeated_folder_approval_reports_the_existing_job_state(
    background_harness, monkeypatch, state, wording,
):
    h, _queued = background_harness
    monkeypatch.setattr(
        import_jobs, "enqueue", lambda **kwargs: {
            "id": "existing-job", "state": state,
            "error": "Restore the approved folder." if state == "failed" else None,
        },
    )
    lines = h.run(background=True)
    text = "\n".join(lines)
    assert h.manifested == [] and h.remote.calls == []
    assert f"Folder import {wording}: existing-job" in text
    assert "Existing imports" in text
    assert "import queued" not in text and "continues in the background" not in text
    assert ("Restore the approved folder." in text) == (state == "failed")


def test_background_resume_never_replans_and_does_not_import_new_files(
    background_harness, monkeypatch
):
    h, queued = background_harness
    h.run(background=True)
    (h.folder / "b.py").write_text("unreviewed = True\n")

    def forbidden(*args, **kwargs):
        pytest.fail("A saved background job must not classify, discover sources, or prompt again")

    monkeypatch.setattr(runner, "classify", forbidden)
    monkeypatch.setattr(imp.github, "collect_evidence", forbidden)
    monkeypatch.setattr(tui, "review", forbidden)
    lines, progress = _resume(queued[0])
    assert h.manifested == [("a.py", "value = 1\n")]
    assert h.report()["delivered"] == ["a.py"]
    assert h.report()["new"] == ["b.py"]
    assert any("1 new" in line for line in lines)
    assert progress[-1] == ("Folder import complete", {
        "completed": 1, "total": 1, "completion_completed": 1, "completion_total": 1,
    })
    _resume(queued[0])
    assert len(h.manifested) == len(h.created) == len(h.remote.calls) == 1


def test_changed_approved_bytes_remain_pending_and_original_version_can_resume(background_harness):
    h, queued = background_harness
    h.run(background=True)
    (h.folder / "a.py").write_text("value = 2\n")
    with pytest.raises(CoverageError, match="approved file.*remain unfinished"):
        _resume(queued[0])
    assert h.manifested == h.remote.calls == []
    assert h.report()["changed"] == ["a.py"]
    (h.folder / "a.py").write_text("value = 1\n")
    _resume(queued[0])
    assert h.report()["delivered"] == ["a.py"]
    assert len(h.classified) == 1


def test_failed_unit_resumes_from_the_saved_plan(background_harness):
    h, queued = background_harness
    h.run(background=True)
    h.failed_model = True
    with pytest.raises(CoverageError, match="approved file.*remain unfinished"):
        _resume(queued[0])
    h.failed_model = False
    _resume(queued[0])
    assert len(h.classified) == len(h.created) == len(h.manifested) == 1
    assert h.report()["delivered"] == ["a.py"]


def test_lost_completion_after_upload_resumes_receipts_without_duplicate_files(
    background_harness, monkeypatch
):
    h, queued = background_harness
    h.run(background=True)

    drain = h.client.flush

    def lost_response(**kwargs):
        drain(**kwargs)
        raise ConnectionError("connection lost after upload")

    monkeypatch.setattr(h.client, "flush", lost_response)
    with pytest.raises(import_jobs.RetryableJobError, match="connection is unavailable"):
        _resume(queued[0])
    monkeypatch.setattr(h.client, "flush", drain)
    _resume(queued[0])
    assert h.report()["delivered"] == ["a.py"]
    assert len(h.remote.calls) == len(h.manifested) == len(h.classified) == 1


def test_worker_retries_extended_outage_with_the_same_file_receipts(
    background_harness, monkeypatch,
):
    """A long outage must not exhaust the outbox's ordinary retry ceiling."""
    from probe.sdk.errors import TransportError

    h, queued = background_harness
    h.run(background=True)
    payload = queued[0]
    monkeypatch.setenv("XDG_STATE_HOME", str(h.root / "jobs"))
    monkeypatch.setattr(import_jobs, "_launch", lambda folder: import_jobs._read(folder))
    # Use the real scheduler after inspecting the foreground handoff; launching
    # is disabled so this test runs the worker against the local fake remote.
    job = enqueue_job("folder", payload, "Approved folder")
    folder = Path(job["log_path"]).parent
    remote_upload = h.remote.upload_fingerprinted
    attempts, waits = [], []
    # A zero transient budget and a two-attempt floor prove the import retry
    # policy keeps the immutable operation pending instead of sending it to
    # failed/ during an extended outage.
    monkeypatch.setenv("PROBE_OUTBOX_TRANSIENT_BUDGET_SEC", "0")
    monkeypatch.setattr(journal, "MIN_TRANSIENT_ATTEMPTS", 2)

    def intermittent(*args, **kwargs):
        attempts.append(kwargs["digest"])
        if len(attempts) <= 3:
            raise TransportError("private transport details")
        return remote_upload(*args, **kwargs)

    def reconnect(delay):
        waits.append(delay)
        assert h.report()["queued"] == ["a.py"]
        assert len(h.manifested) == len(h.classified) == 1
        assert import_jobs.get_job(folder.name)["state"] == import_jobs.State.RUNNING

    monkeypatch.setattr(h.remote, "upload_fingerprinted", intermittent)
    monkeypatch.setattr(import_jobs.time, "sleep", reconnect)
    assert import_jobs.run_worker(folder.name) == 0
    assert waits == [2, 4, 8]
    assert len(set(attempts)) == 1
    assert h.report()["delivered"] == ["a.py"]
    assert len(h.remote.calls) == len(h.manifested) == len(h.classified) == 1
    saved = import_jobs.get_job(folder.name)
    assert saved["state"] == import_jobs.State.SUCCEEDED
    assert saved["payload"] == payload
    assert "private transport details" not in (folder / "output.log").read_text()


@pytest.mark.parametrize("failure", ["auth", "unexpected", "model_and_network"])
def test_folder_worker_does_not_retry_failures_requiring_attention(
    background_harness, monkeypatch, failure,
):
    from probe.sdk.errors import AuthError, TransportError

    h, queued = background_harness
    h.run(background=True)
    monkeypatch.setenv("XDG_STATE_HOME", str(h.root / "jobs"))
    monkeypatch.setattr(import_jobs, "_launch", lambda folder: import_jobs._read(folder))
    job = enqueue_job("folder", queued[0], "Approved folder")

    def fail_upload(*args, **kwargs):
        if failure == "auth":
            raise AuthError("private credentials", status=401)
        raise ValueError("unknown problem")

    def fail_flush(**kwargs):
        raise TransportError("private transport details")

    if failure == "model_and_network":
        h.failed_model = True
        monkeypatch.setattr(h.client, "flush", fail_flush)
    else:
        monkeypatch.setattr(h.remote, "upload_fingerprinted", fail_upload)
    monkeypatch.setattr(import_jobs.time, "sleep", lambda _: pytest.fail("This failure needs attention"))
    assert import_jobs.run_worker(job["id"]) == 1
    saved = import_jobs.get_job(job["id"])
    assert saved["state"] == import_jobs.State.FAILED
    assert saved["progress"]["message"] == "Import needs attention before retrying."
    assert h.remote.calls == []
    assert "private" not in saved["error"]


def test_a_previously_changed_file_left_pending_does_not_expand_the_background_job(
    background_harness, monkeypatch
):
    h, queued = background_harness
    h.run()
    h.drain()
    (h.folder / "a.py").write_text("value = 2\n")
    (h.folder / "b.py").write_text("new = True\n")
    monkeypatch.setattr(
        tui, "review",
        lambda title, lines, choices: False if title == "Review changed files" else "import",
    )
    h.run(background=True, interactive=True, yes=False)
    assert queued[0]["targets"] == ["b.py"]
    _resume(queued[0])
    assert h.report()["changed"] == ["a.py"]
    assert h.report()["delivered"] == ["b.py"]
    assert h.manifested == [("a.py", "value = 1\n"), ("b.py", "new = True\n")]


@pytest.mark.parametrize(
    "scope_change", [{"tenant": "other-tenant"}, {"backend": "https://other.invalid"}]
)
def test_background_worker_rejects_changed_authenticated_scope(
    background_harness, monkeypatch, scope_change
):
    h, queued = background_harness
    h.run(background=True)
    changed_client = h.new_client(**scope_change)
    monkeypatch.setattr(imp, "_background_client", lambda payload: nullcontext(changed_client))
    with pytest.raises(CoverageError, match="account or destination differs"):
        _resume(queued[0])
    assert h.manifested == h.remote.calls == []


def test_background_worker_keeps_approved_workspace_when_current_selection_changes(background_harness):
    h, queued = background_harness
    h.run(background=True)
    approved_workspace = queued[0]["scope"]["workspace_id"]
    h.client.settings.workspace = "other-workspace"
    _resume(queued[0])
    assert h.manifested and h.remote.calls
    assert {row["workspace_id"] for row in h.created} == {approved_workspace}


def test_background_worker_rejects_a_replaced_saved_approval(background_harness):
    h, queued = background_harness
    h.run(background=True)
    with h.coverage().writer() as coverage:
        units = coverage.meta("approved_units")
        next(iter(units.values()))["hashes"]["a.py"] = "different-approved-version"
        coverage.put_meta("approved_units", units)
    with pytest.raises(CoverageError, match="saved file approvals changed"):
        _resume(queued[0])
    assert h.manifested == h.remote.calls == []


def test_background_worker_rejects_a_rewritten_unit_plan(background_harness):
    h, queued = background_harness
    h.run(background=True)
    ledger = Ledger(h.coverage().directory / "units.jsonl")
    unit = next(iter(ledger.read().units.values())).unit
    ledger.record_plan([Unit(unit.unit_id, "changed-project", unit.paths)], ["changed-project"])
    with pytest.raises(CoverageError, match="saved file approvals changed"):
        _resume(queued[0])
    assert h.manifested == h.remote.calls == []


def test_background_worker_rejects_another_user_in_the_same_workspace(
    background_harness, monkeypatch
):
    h, queued = background_harness
    h.run(background=True)
    monkeypatch.setattr(h.client, "me", lambda: {"customer_id": "tenant", "user_id": "another"})
    with pytest.raises(CoverageError, match="account or destination differs"):
        _resume(queued[0])
    assert h.manifested == h.remote.calls == []


def test_canceling_the_plan_does_not_queue_a_job(background_harness, monkeypatch):
    h, queued = background_harness
    monkeypatch.setattr(tui, "review", lambda *args, **kwargs: "cancel")
    with pytest.raises(KeyboardInterrupt):
        h.run(background=True, interactive=True, yes=False)
    assert queued == [] and h.manifested == [] and h.created == []
