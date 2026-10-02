"""A new reviewed folder import can verify completed work without duplicating it."""

from contextlib import nullcontext

from probe.cli import backfill as bf, backfill_import as imp, import_jobs as jobs
from probe.cli import import_jobs_ui, tui
from tests import test_backfill_auto_import as fixtures

automatic = fixtures.automatic
queued = fixtures.queued
_run = fixtures._run


def test_reviewed_import_after_completion_gets_a_new_job_and_reuses_receipts(automatic):
    h = automatic
    h.run(background=True)
    first = jobs.list_jobs()[0]
    _run(first)
    assert h.report()["delivered"] == ["a.py"]

    h.run(background=True)
    pending = [job for job in jobs.list_jobs() if job["state"] == jobs.State.QUEUED]
    assert len(pending) == 1
    second = pending[0]
    assert second["id"] != first["id"]
    _run(second)

    assert len(h.classified) == len(h.created) == len(h.manifested) == len(h.remote.calls) == 1
    assert h.report()["delivered"] == ["a.py"]


def test_reviewed_import_after_completion_discovers_new_files(automatic):
    h = automatic
    h.run(background=True)
    first = jobs.list_jobs()[0]
    _run(first)
    (h.folder / "b.py").write_text("new = True\n")

    h.run(background=True)
    second = next(job for job in jobs.list_jobs() if job["id"] != first["id"])
    _run(second)

    assert h.classified == [["a.py"], ["b.py"]]
    assert len(h.created) == 1
    assert len(h.manifested) == len(h.remote.calls) == 2
    assert h.report()["delivered"] == ["a.py", "b.py"]


def test_repeated_review_while_queued_reuses_the_active_job(automatic, queued):
    h = automatic
    h.run(background=True)
    h.run(background=True)

    assert len(jobs.list_jobs()) == len(queued) == 1
    assert h.manifested == h.remote.calls == []


def test_canceling_reviewed_import_does_not_block_new_approval(automatic):
    h = automatic
    h.run(background=True)
    first = jobs.list_jobs()[0]
    # This harness records our own PID instead of spawning a worker. Clear the
    # placeholder so cancellation operates on an unowned queued approval.
    jobs._update(jobs.default_dir() / first["id"], pid=None, pid_identity=None, launch_pid=None)
    jobs.cancel(first["id"])

    h.run(background=True)
    second = next(job for job in jobs.list_jobs() if job["id"] != first["id"])
    assert jobs.get_job(first["id"])["state"] == jobs.State.CANCELED
    _run(second)
    assert h.report()["delivered"] == ["a.py"]
    assert len(h.remote.calls) == 1


def test_legacy_completed_approval_does_not_block_another_request(automatic):
    h = automatic
    h.run(background=True)
    initial = jobs.list_jobs()[0]
    _run(initial)
    payload = dict(initial["payload"])
    payload.pop("request_id", None)
    legacy = jobs.enqueue(jobs.Kind.FOLDER, payload, "Old folder import")
    _run(legacy)

    again = imp._enqueue_reviewed_import(payload, label="Folder import")
    assert again["id"] not in {initial["id"], legacy["id"]}
    assert again["state"] == jobs.State.QUEUED
    assert imp._enqueue_reviewed_import(payload, label="Folder import")["id"] == again["id"]
    _run(again)
    assert len(h.remote.calls) == len(h.created) == len(h.manifested) == 1


def test_public_folder_picker_flow_reimports_unchanged_completed_folder(automatic, monkeypatch):
    monkeypatch.setattr(bf, "choose_folder_wandb", lambda *a, **k: (None, False))
    h = automatic
    h.run(background=True)
    first = jobs.list_jobs()[0]
    _run(first)
    monkeypatch.setattr(bf, "choose_directory", lambda start: h.folder)
    monkeypatch.setattr(bf, "resolve_agent", lambda *a, **kw: (bf.Agent.CLAUDE, None))
    monkeypatch.setattr(bf, "choose_import_mode", lambda *a: bf.FolderImportMode.REVIEW_FIRST)
    monkeypatch.setattr(tui, "review", lambda title, lines, choices: choices[0][1])
    watching = []

    def show_started(job):
        watching.append(job)
        return job

    monkeypatch.setattr(import_jobs_ui, "show_started_import", show_started)
    lines = bf.run(
        client_factory=lambda: nullcontext(h.client),
        interactive=True, background=True, concurrency=1,
    )
    assert len(watching) == 1 and watching[0]["id"] != first["id"]
    assert watching[0]["state"] == jobs.State.QUEUED
    assert any("Folder import queued" in line for line in lines)
    _run(watching[0])
    assert len(h.remote.calls) == len(h.created) == len(h.manifested) == 1
