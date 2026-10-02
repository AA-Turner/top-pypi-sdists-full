"""Explicit auto approval prepares and delivers within one durable folder job."""

from contextlib import nullcontext
import json

import pytest

from probe.cli import backfill as bf, backfill_import as imp, backfill_run as runner
from probe.cli import import_jobs as jobs, tui
from probe.cli.backfill_coverage import CoverageError
from probe.sdk import journal
from tests.test_backfill_scoped_orchestration import make_harness
from tests import test_import_jobs

queued = test_import_jobs.queued


@pytest.fixture
def automatic(tmp_path, monkeypatch, queued):
    h = make_harness(tmp_path, monkeypatch)
    monkeypatch.setattr(bf, "degraded_note", lambda *a: None)
    monkeypatch.setattr(bf, "git_context", lambda *a: None)
    monkeypatch.setattr(imp, "_background_client", lambda payload: nullcontext(h.client))
    monkeypatch.setattr(h.client, "flush", lambda **kwargs: journal.drain(
        h.client.journal, client_factory=lambda _: h.remote, **kwargs,
    ))
    monkeypatch.setattr(tui, "review", lambda *a, **k: pytest.fail("Opt-in worker must not prompt"))
    return h


def _enqueue(h, **kwargs):
    return imp.enqueue_auto_import(
        client_factory=lambda: nullcontext(h.client), folder=h.folder, agent=bf.Agent.CLAUDE,
        concurrency=1, auto_approve=True, **kwargs,
    )


def _run(job):
    code = jobs.run_worker(job["id"])
    saved = jobs.get_job(job["id"])
    assert code == 0 and saved["state"] == jobs.State.SUCCEEDED, saved
    return saved


def test_automatic_import_requires_explicit_opt_in_before_any_account_or_file_work(automatic):
    with pytest.raises(CoverageError, match="explicit approval"):
        imp.enqueue_auto_import(
            client_factory=lambda: pytest.fail("No approval"), folder=automatic.folder,
            agent=bf.Agent.CLAUDE, auto_approve=False,
        )


def test_enqueue_does_not_scan_and_reuses_one_active_folder_job(automatic, monkeypatch, queued):
    h = automatic
    monkeypatch.setattr(runner, "_index", lambda *a: pytest.fail("Scan belongs in worker"))
    job = _enqueue(h)
    assert _enqueue(h)["id"] == job["id"]
    assert job["kind"] == jobs.Kind.FOLDER and job["payload"]["auto_approve"] is True
    assert len(queued) == 1
    assert h.classified == h.created == h.manifested == h.remote.calls == []
    assert "test-token" not in json.dumps(job)


def test_worker_saves_exact_plan_before_delivery_without_enqueuing_another_job(automatic, monkeypatch, queued):
    h = automatic
    job = _enqueue(h)
    real_deliver = imp._deliver_approved
    seen = []

    def deliver(*args, **kwargs):
        if not kwargs.get("background"):
            checkpoint, identity = imp._auto_checkpoint(job["payload"])
            prepared = imp._read_auto_checkpoint(checkpoint, identity)
            assert prepared["targets"] == ["a.py"]
            assert prepared["scope"] == job["payload"]["scope"]
            assert checkpoint.stat().st_mode & 0o777 == 0o600
            seen.append(True)
        return real_deliver(*args, **kwargs)

    monkeypatch.setattr(imp, "_deliver_approved", deliver)
    _run(job)
    assert seen == [True] and len(queued) == 1 and len(jobs.list_jobs()) == 1
    assert h.classified == [["a.py"]]
    assert h.manifested == [("a.py", "value = 1\n")]
    assert len(h.created) == len(h.remote.calls) == 1


def test_reconnect_after_preparation_uses_same_snapshot_and_ignores_new_files(automatic, monkeypatch):
    h = automatic
    job = _enqueue(h)
    real_deliver = imp._deliver_approved

    def interrupted(*args, **kwargs):
        if not kwargs.get("background"):
            raise jobs._Interrupted
        return real_deliver(*args, **kwargs)

    monkeypatch.setattr(imp, "_deliver_approved", interrupted)
    assert jobs.run_worker(job["id"]) == 130
    assert jobs.get_job(job["id"])["state"] == jobs.State.INTERRUPTED
    assert h.remote.calls == []
    (h.folder / "b.py").write_text("new = True\n")
    monkeypatch.setattr(imp, "_deliver_approved", real_deliver)
    monkeypatch.setattr(imp, "_run", lambda *a, **k: pytest.fail("Prepared job must not replan"))
    jobs.recover_jobs()
    _run(job)
    assert h.classified == [["a.py"]]
    assert h.manifested == [("a.py", "value = 1\n")]
    assert h.report()["new"] == ["b.py"] and len(h.remote.calls) == 1


def test_changed_approved_bytes_are_not_automatically_reapproved_after_preparation(automatic, monkeypatch):
    h = automatic
    job = _enqueue(h)
    real_deliver = imp._deliver_approved

    def changed(*args, **kwargs):
        if not kwargs.get("background"):
            (h.folder / "a.py").write_text("changed after approval\n")
        return real_deliver(*args, **kwargs)

    monkeypatch.setattr(imp, "_deliver_approved", changed)
    assert jobs.run_worker(job["id"]) == 1
    saved = jobs.get_job(job["id"])
    assert "approved file(s) remain unfinished" in saved["error"]
    assert h.remote.calls == []
    assert h.classified == [["a.py"]]


def test_new_request_after_success_finds_new_files_and_regular_backfill_stays_idempotent(automatic):
    h = automatic
    first = _enqueue(h)
    _run(first)
    (h.folder / "b.py").write_text("new = True\n")
    second = _enqueue(h)
    assert second["id"] != first["id"]
    _run(second)
    assert h.classified == [["a.py"], ["b.py"]]
    assert len(h.created) == 1 and len(h.remote.calls) == 2
    h.run()
    assert len(h.created) == 1 and len(h.remote.calls) == 2 and len(h.manifested) == 2


@pytest.mark.parametrize("change", ["user", "tenant", "folder"])
def test_changed_scope_fails_before_classification(automatic, monkeypatch, change):
    h = automatic
    job = _enqueue(h)
    if change == "folder":
        h.folder.rename(h.folder.with_name("previous"))
        h.folder.mkdir()
        (h.folder / "a.py").write_text("replacement folder\n")
    else:
        monkeypatch.setattr(h.client, "me", lambda: {
            "customer_id": "other" if change == "tenant" else "tenant",
            "user_id": "other" if change == "user" else "user",
        })
    assert jobs.run_worker(job["id"]) == 1
    assert h.classified == h.created == h.manifested == h.remote.calls == []


def test_network_retry_keeps_the_single_intent_and_completed_project(automatic, monkeypatch):
    h = automatic
    h.lost_create_ack = True
    waits = []
    monkeypatch.setattr(jobs.time, "sleep", lambda delay: waits.append(delay))
    job = _enqueue(h)
    _run(job)
    assert waits == [2]
    assert len(h.created) == len(h.classified) == len(h.manifested) == len(h.remote.calls) == 1


def test_corrupt_prepared_checkpoint_fails_without_replanning(automatic, monkeypatch):
    h = automatic
    job = _enqueue(h)
    real_deliver = imp._deliver_approved

    def interrupted(*args, **kwargs):
        if not kwargs.get("background"):
            raise jobs._Interrupted
        return real_deliver(*args, **kwargs)

    monkeypatch.setattr(imp, "_deliver_approved", interrupted)
    jobs.run_worker(job["id"])
    checkpoint, _ = imp._auto_checkpoint(job["payload"])
    checkpoint.write_text("broken saved plan")
    monkeypatch.setattr(imp, "_run", lambda *a, **k: pytest.fail("Do not rebuild corrupt approvals"))
    jobs.resume(job["id"])
    assert jobs.run_worker(job["id"]) == 1
    assert "could not be verified" in jobs.get_job(job["id"])["error"]
    assert h.remote.calls == []


def test_missing_prepared_checkpoint_never_becomes_permission_to_replan(automatic, monkeypatch):
    h = automatic
    job = _enqueue(h)
    real_deliver = imp._deliver_approved

    def interrupted(*args, **kwargs):
        if not kwargs.get("background"):
            raise jobs._Interrupted
        return real_deliver(*args, **kwargs)

    monkeypatch.setattr(imp, "_deliver_approved", interrupted)
    assert jobs.run_worker(job["id"]) == 130
    checkpoint, _ = imp._auto_checkpoint(job["payload"])
    checkpoint.unlink()
    monkeypatch.setattr(imp, "_run", lambda *a, **k: pytest.fail("Do not replace missing approved plan"))
    resumed = _enqueue(h)
    assert resumed["id"] == job["id"] and resumed["state"] == jobs.State.QUEUED
    assert jobs.run_worker(job["id"]) == 1
    assert "plan is missing" in jobs.get_job(job["id"])["error"]
    assert h.remote.calls == []


def test_fresh_opt_in_can_replace_a_failed_pinned_request(automatic, monkeypatch):
    h = automatic
    first = _enqueue(h)
    original_me = h.client.me
    monkeypatch.setattr(h.client, "me", lambda: {"customer_id": "tenant", "user_id": "someone-else"})
    assert jobs.run_worker(first["id"]) == 1
    monkeypatch.setattr(h.client, "me", original_me)
    second = _enqueue(h)
    assert second["id"] != first["id"]
    _run(second)
    assert len(h.classified) == len(h.created) == len(h.remote.calls) == 1


def test_folder_replacement_during_preparation_fails_before_publishing_the_plan(automatic, monkeypatch):
    h = automatic
    job = _enqueue(h)
    original_run = imp._run

    def replace(*args, **kwargs):
        result = original_run(*args, **kwargs)
        h.folder.rename(h.folder.with_name("previous"))
        h.folder.mkdir()
        (h.folder / "a.py").write_text("value = 1\n")
        return result

    monkeypatch.setattr(imp, "_run", replace)
    assert jobs.run_worker(job["id"]) == 1
    assert "folder was replaced" in jobs.get_job(job["id"])["error"]
    checkpoint, _ = imp._auto_checkpoint(job["payload"])
    assert not checkpoint.exists() and h.remote.calls == []
