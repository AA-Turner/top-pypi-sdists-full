"""A saved folder job preserves its attempt cap and explains explicit recovery."""

import json
from pathlib import Path
import shlex

import pytest

from probe.cli import backfill as bf, backfill_import as imp, import_jobs, import_jobs_ui, tui
from probe.cli.backfill_coverage import Coverage, CoverageError
from probe.cli.backfill_ledger import Ledger, MAX_UNIT_ATTEMPTS, UnitState
from probe.cli.import_jobs import enqueue as enqueue_job
from tests import test_backfill_background, test_import_jobs

background_harness = test_backfill_background.background_harness
queued = test_import_jobs.queued


def _approved(background_harness, *, files=1):
    harness, payloads = background_harness
    if files == 2:
        (harness.folder / "b.py").write_text("other = 2\n")
    harness.run(background=True)
    payload = payloads[0]
    ledger = Ledger(Path(payload["directory"]) / "units.jsonl")
    record, = ledger.read().units.values()
    return harness, payload, ledger, record.unit


def _fail_attempts(ledger, unit, count=MAX_UNIT_ATTEMPTS):
    for _ in range(count):
        ledger.start_unit(unit.unit_id)
        ledger.finish_unit(unit.unit_id, ok=False, error="agent could not finish")


def _resume(payload):
    return imp.run_background_job(payload, progress=lambda *args, **kwargs: None)


@pytest.mark.parametrize("manifest_files", [0, 1, 2])
def test_unretired_exhausted_unit_recovers_manifest_without_another_agent_attempt(
    background_harness, monkeypatch, manifest_files,
):
    h, payload, ledger, unit = _approved(background_harness, files=2)
    original_approval = json.dumps(payload, sort_keys=True)
    _fail_attempts(ledger, unit)
    if manifest_files:
        manifest = Path(payload["directory"]) / "manifests" / f"{unit.unit_id}.jsonl"
        manifest.write_text("".join(json.dumps({"path": path}) + "\n"
                                    for path in ("a.py", "b.py")[:manifest_files]))
    monkeypatch.setattr(bf, "launch_agent", lambda *a, **k: pytest.fail("attempt limit exceeded"))

    for _ in range(2):
        if manifest_files == 2:
            _resume(payload)
        else:
            with pytest.raises(CoverageError, match="failed repeatedly"):
                _resume(payload)
        record = ledger.read().units[unit.unit_id]
        assert record.state is UnitState.DEAD and record.attempts == MAX_UNIT_ATTEMPTS
        assert len(h.remote.calls) == manifest_files
        assert len(h.report()["delivered"]) == manifest_files
        assert len(h.report()["dead"]) == 2 - manifest_files
        with h.coverage().writer() as coverage:
            assert imp._approval_snapshot(coverage) == payload["approved"]
            assert imp._unit_snapshot(ledger) == payload["unit_plan"]
        assert json.dumps(payload, sort_keys=True) == original_approval


@pytest.mark.parametrize("interruption,expected", [
    (import_jobs._Interrupted, import_jobs._Interrupted),
    (import_jobs.RetryableJobError, CoverageError),
])
def test_last_attempt_is_retired_before_flush_can_interrupt_it(
    background_harness, monkeypatch, interruption, expected,
):
    h, payload, ledger, unit = _approved(background_harness)
    _fail_attempts(ledger, unit, MAX_UNIT_ATTEMPTS - 1)
    h.failed_model = True

    def interrupted_flush(*args, **kwargs):
        assert ledger.read().units[unit.unit_id].state is UnitState.DEAD
        raise interruption("flush interrupted")

    with monkeypatch.context() as patch:
        patch.setattr(imp, "_flush_uploads", interrupted_flush)
        with pytest.raises(expected):
            _resume(payload)
    monkeypatch.setattr(bf, "launch_agent", lambda *a, **k: pytest.fail("retired unit restarted"))
    with pytest.raises(CoverageError, match="failed repeatedly"):
        _resume(payload)
    assert ledger.read().units[unit.unit_id].attempts == MAX_UNIT_ATTEMPTS
    assert not h.remote.calls


def test_worker_error_and_import_details_explain_fresh_review_without_resetting_approval(
    background_harness, queued, monkeypatch,
):
    harness, _ = background_harness
    renamed = harness.folder.with_name("folder with 'quotes'")
    harness.folder.rename(renamed)
    harness.folder = renamed
    h, payload, ledger, unit = _approved(background_harness)
    _fail_attempts(ledger, unit)
    monkeypatch.setattr(bf, "launch_agent", lambda *a, **k: pytest.fail("retired unit restarted"))
    job = enqueue_job(import_jobs.Kind.FOLDER, payload, "Reviewed folder")

    for _ in range(2):
        assert import_jobs.run_worker(job["id"]) == 1
        saved = import_jobs.get_job(job["id"])
        assert saved["state"] == import_jobs.State.FAILED
        assert saved["payload"] == payload
        detail = " ".join(" ".join(import_jobs_ui._detail(job["id"])).split())
        assert "1 failed repeatedly" in detail
        assert "will not retry those agent units" in detail
        assert "account and workspace" in detail
        assert "Per-file report:" in detail and "coverage.json" in detail
        assert str(Path(payload["directory"]) / "coverage.json") in saved["error"]
        command = saved["error"].split("`", 2)[1]
        argv = shlex.split(command)
        assert argv[argv.index("backfill") + 1] == str(h.folder)
        assert "--retry-dead" in argv and "--no-transcripts" in argv
        assert argv[argv.index("--source-id") + 1] == payload["source_id"]
        assert ledger.read().units[unit.unit_id].attempts == MAX_UNIT_ATTEMPTS
        import_jobs.resume(job["id"])
    assert h.classified == [["a.py"]] and not h.remote.calls


def test_explicit_retry_dead_reviews_a_new_plan_and_keeps_old_job_approval(
    background_harness, monkeypatch,
):
    h, payload, ledger, unit = _approved(background_harness)
    _fail_attempts(ledger, unit)
    with pytest.raises(CoverageError, match="failed repeatedly"):
        _resume(payload)
    old_approval = json.dumps(payload, sort_keys=True)
    reviews = []

    def review(title, lines, choices):
        reviews.append(title)
        return "import"

    monkeypatch.setattr(tui, "review", review)
    monkeypatch.setattr(import_jobs_ui, "show_started_import", lambda job: job)
    h.run(retry_dead=True, interactive=True, yes=False, background=True)
    assert "Review the import plan" in reviews
    assert h.classified == [["a.py"], ["a.py"]]
    assert len(ledger.read().units) == 2
    assert ledger.read().units[unit.unit_id].state is UnitState.DEAD
    assert json.dumps(payload, sort_keys=True) == old_approval
    with pytest.raises(CoverageError, match="saved file approvals changed"):
        _resume(payload)


@pytest.mark.parametrize("resume_first", [False, True])
@pytest.mark.parametrize("retired_before_interruption", [False, True])
def test_retirement_interruption_is_repaired_without_poisoning_a_fresh_retry(
    background_harness, monkeypatch, resume_first, retired_before_interruption,
):
    h, payload, ledger, unit = _approved(background_harness)
    _fail_attempts(ledger, unit)

    def interrupted_marker(*args, **kwargs):
        assert ledger.read().units[unit.unit_id].state is UnitState.DEAD
        raise import_jobs._Interrupted("interrupted after ledger retirement")

    if retired_before_interruption:
        with monkeypatch.context() as patch:
            patch.setattr(Coverage, "mark_dead", interrupted_marker)
            with pytest.raises(import_jobs._Interrupted):
                _resume(payload)
    else:
        assert ledger.read().units[unit.unit_id].exhausted
    assert h.report()["dead"] == []
    assert ledger.read().units[unit.unit_id].attempts == MAX_UNIT_ATTEMPTS
    if resume_first:
        with pytest.raises(CoverageError, match="failed repeatedly"):
            _resume(payload)
        assert h.report()["dead"] == ["a.py"]

    reviews = []

    def review(title, lines, choices):
        reviews.append(title)
        return "import"

    monkeypatch.setattr(tui, "review", review)
    monkeypatch.setattr(import_jobs_ui, "show_started_import", lambda job: job)
    h.run(retry_dead=True, interactive=True, yes=False, background=True)
    assert "Review the import plan" in reviews
    assert h.report()["dead"] == []
    assert len(ledger.read().units) == 2
    _resume(background_harness[1][-1])
    assert h.report()["delivered"] == ["a.py"]
    assert h.report()["dead"] == []
    assert len(h.remote.calls) == 1
    assert ledger.read().units[unit.unit_id].state is UnitState.DEAD
    assert ledger.read().units[unit.unit_id].attempts == MAX_UNIT_ATTEMPTS
