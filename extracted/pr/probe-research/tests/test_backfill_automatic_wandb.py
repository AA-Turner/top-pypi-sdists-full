"""Automatic folder jobs carry explicit W&B destinations, never deferred prompts."""

from contextlib import nullcontext
from pathlib import Path

import httpx
import pytest

from probe.cli import backfill as bf, backfill_import as imp, backfill_wandb as wb
from probe.cli import import_jobs as jobs, tui
from probe.cli.backfill_coverage import CoverageError
from probe.sdk import journal
from probe.sdk.transport import Transport
from tests import test_backfill_wandb as history, test_import_jobs as job_tests
from tests.test_backfill_scoped_orchestration import make_harness

queued = job_tests.queued


@pytest.fixture
def automatic_history(tmp_path, monkeypatch, queued):
    h = make_harness(tmp_path, monkeypatch)
    h.client.close()
    h.client = h.new_client(tenant="synthetic", workspace=history.WORKSPACE, backend="https://api.invalid")
    remote = history.Remote(tmp_path / "not-created.sqlite3")
    monkeypatch.setattr(bf, "degraded_note", lambda *a: None)
    monkeypatch.setattr(bf, "git_context", lambda *a: None)
    monkeypatch.setattr(imp, "_background_client", lambda payload: nullcontext(h.client))
    monkeypatch.setattr(h.client, "flush", lambda **kw: journal.drain(
        h.client.journal, client_factory=lambda _: h.remote, **kw,
    ))
    # Use the actual team-workspace shape, without retired personal/owner fields.
    workspace = {"id": history.WORKSPACE, "customer_id": "synthetic", "slug": "my-work",
                 "name": "My work", "created_by": "user:user", "created_at": "2026-09-12T01:00:00Z"}
    monkeypatch.setattr(h.client, "get_workspace", lambda ident: dict(workspace, id=ident))
    monkeypatch.setattr(h.client, "list_workspaces", lambda: [workspace])
    h.client.settings.workspace = None
    with httpx.Client(base_url=h.client.settings.base_url, transport=httpx.MockTransport(lambda request: remote.respond(request))) as http:
        monkeypatch.setattr(h.client, "transport", Transport(h.client.settings, client=http, max_retries=0,
                                                           attribution="backfill"))
        yield h, remote
        h.client.close()


def source(h):
    return {"schema": wb.SOURCE_SCHEMA, **wb._selection_identity(h.client),
            "connection_id": history.CONNECTION, "external_id": "lab/training"}


def answer(monkeypatch, responses):
    replies = iter(responses)
    seen = []

    def review(title, lines, choices, **kwargs):
        seen.append((title, lines))
        reply = next(replies)
        return choices[reply][1] if isinstance(reply, int) else reply

    monkeypatch.setattr(tui, "review", review)
    return seen


def approve(h, monkeypatch):
    answer(monkeypatch, [1, "import"])
    return wb.choose_automatic_destination(h.client, folder=h.folder, wandb_source=source(h))


def enqueue(h, remote, approval):
    job = imp.enqueue_auto_import(client_factory=lambda: nullcontext(h.client), folder=h.folder,
                                  agent=bf.Agent.CLAUDE, auto_approve=True, wandb_approval=approval)
    remote.path = Path(job["payload"]["directory"]) / "coverage.sqlite3"
    return job


def run(job):
    assert jobs.run_worker(job["id"]) == 0, jobs.get_job(job["id"])["error"]
    return jobs.get_job(job["id"])


def test_approve_new_destination_does_not_scan_or_admit_history(automatic_history, monkeypatch):
    h, remote = automatic_history
    seen = answer(monkeypatch, [1, "import"])
    approval = wb.choose_automatic_destination(h.client, folder=h.folder, wandb_source=source(h))
    assert approval["schema"] == wb.AUTOMATIC_APPROVAL_SCHEMA
    assert approval["project_id"] == h.created[0]["id"]
    assert approval["workspace_id"] == history.WORKSPACE
    assert any("Both this folder's files" in line for _, lines in seen for line in lines)
    assert len(h.created) == 1 and h.classified == h.manifested == []
    assert jobs.list_jobs() == [] and not remote.jobs and not remote.attachments
    assert all(method == "GET" for method, _, _ in remote.requests)


def test_folder_picker_to_automatic_worker_with_wandb_and_default_workspace(automatic_history, monkeypatch):
    from probe.cli import import_jobs_ui

    h, remote = automatic_history
    monkeypatch.setattr(bf, "choose_directory", lambda *a: h.folder)
    monkeypatch.setattr(bf, "resolve_agent", lambda *a, **k: (bf.Agent.CLAUDE, None))
    monkeypatch.setattr(tui, "working", lambda *a, **k: nullcontext())
    monkeypatch.setattr(import_jobs_ui, "show_started_import", lambda job: job)
    seen = answer(monkeypatch, [1, 1, bf.FolderImportMode.AUTOMATIC, 1, "import"])
    result = bf.run(client_factory=lambda: nullcontext(h.client), background=True, back_to_selection=True)
    assert isinstance(result, bf.StartedFolderImport)
    assert [title for title, _ in seen] == [
        "Choose a W&B account", "Choose W&B history", "Import files and W&B history",
        "Choose a destination for files and W&B", "Start automatic import",
    ]
    assert h.client.settings.workspace is None and h.classified == h.manifested == []
    assert not remote.jobs and not remote.attachments
    assert len(jobs.list_jobs()) == 1
    remote.path = Path(result.job["payload"]["directory"]) / "coverage.sqlite3"
    monkeypatch.setattr(tui, "review", lambda *a, **k: pytest.fail("Automatic worker prompted"))
    assert run(result.job)["state"] == jobs.State.SUCCEEDED
    assert len(h.classified) == len(remote.jobs) == len(remote.attachments) == 1


@pytest.mark.parametrize("replies,expected", [([tui.BACK], tui.BACK), ([0], None),
                                             ([1, "skip"], None), ([1, tui.BACK, tui.BACK], tui.BACK)])
def test_skip_back_before_creation_does_no_work(automatic_history, monkeypatch, replies, expected):
    h, remote = automatic_history
    answer(monkeypatch, replies)
    assert wb.choose_automatic_destination(h.client, folder=h.folder, wandb_source=source(h)) is expected
    assert not h.created and not remote.attachments and not remote.jobs


def test_create_response_loss_reuses_project_after_retry(automatic_history, monkeypatch):
    h, remote = automatic_history
    h.lost_create_ack = True
    with pytest.raises(TimeoutError):
        approve(h, monkeypatch)
    approval = approve(h, monkeypatch)
    assert len(h.created) == 1 and approval["project_id"] == h.created[0]["id"]
    assert not remote.jobs


def test_automatic_job_scans_without_prompt_then_imports_exact_destination(automatic_history, monkeypatch):
    h, remote = automatic_history
    approval = approve(h, monkeypatch)
    job = enqueue(h, remote, approval)
    assert job["payload"]["scope"]["project_id"] == approval["project_id"]
    assert job["payload"]["wandb_approval"] == approval
    assert not h.classified and not remote.jobs
    monkeypatch.setattr(tui, "review", lambda *a, **k: pytest.fail("Automatic work cannot prompt"))
    saved = run(job)
    assert saved["state"] == jobs.State.SUCCEEDED
    assert h.classified == [["a.py"]] and len(h.created) == len(h.manifested) == len(h.remote.calls) == 1
    assert len(remote.attachments) == len(remote.jobs) == 1
    record = remote.saved()["imports"][0]
    assert record["project_id"] == approval["project_id"]
    assert record["external_id"] == approval["external_id"]


@pytest.mark.parametrize("lost", ["attach", "launch"])
def test_automatic_wandb_retry_reuses_scan_project_and_request(automatic_history, monkeypatch, lost):
    h, remote = automatic_history
    approval = approve(h, monkeypatch)
    job = enqueue(h, remote, approval)
    monkeypatch.setattr(tui, "review", lambda *a, **k: pytest.fail("Retry cannot prompt"))
    waits = []
    monkeypatch.setattr(jobs.time, "sleep", lambda delay: waits.append(delay))
    remote.lose = lost
    run(job)
    assert waits == [2]
    assert h.classified == [["a.py"]] and len(h.created) == len(h.manifested) == 1
    assert len(remote.attachments) == len(remote.jobs) == 1


def test_another_automatic_import_reuses_existing_files_and_wandb_job(automatic_history, monkeypatch):
    h, remote = automatic_history
    approval = approve(h, monkeypatch)
    monkeypatch.setattr(tui, "review", lambda *a, **k: pytest.fail("No post-import prompt"))
    first = enqueue(h, remote, approval)
    run(first)
    second = enqueue(h, remote, approval)
    assert second["id"] != first["id"]
    run(second)
    assert h.classified == [["a.py"]] and len(h.created) == len(h.manifested) == 1
    assert len(remote.attachments) == len(remote.jobs) == 1


@pytest.mark.parametrize("change", ["user", "workspace", "binding"])
def test_changed_approval_fails_before_scan_or_history_admission(automatic_history, monkeypatch, change):
    h, remote = automatic_history
    approval = approve(h, monkeypatch)
    job = enqueue(h, remote, approval)
    if change == "user":
        monkeypatch.setattr(h.client, "me", lambda: {"customer_id": "synthetic", "user_id": "different"})
    elif change == "workspace":
        h.projects[approval["project_id"]]["workspace_id"] = "moved"
    else:
        remote.bound_project = history.OTHER
    assert jobs.run_worker(job["id"]) == 1
    assert h.classified == h.manifested == [] and not remote.jobs and not remote.attachments


def test_missing_approval_and_extra_fields_cannot_admit(automatic_history, monkeypatch):
    h, remote = automatic_history
    approval = approve(h, monkeypatch)
    for invalid in ({}, source(h), {**approval, "unreviewed": True}):
        with pytest.raises(CoverageError, match="valid W&B destination approval"):
            enqueue(h, remote, invalid)
    assert not jobs.list_jobs() and not remote.jobs


def test_scope_validation_is_not_reported_as_a_login_failure(automatic_history, monkeypatch):
    h, _ = automatic_history
    h.client.settings.workspace = history.WORKSPACE
    monkeypatch.setattr(h.client, "get_workspace", lambda *a: {"customer_id": "another-team"})
    lines = h.run()
    assert any("workspace" in line for line in lines)
    assert not any("probe login" in line or "Could not reach Probe" in line for line in lines)


def test_create_in_current_workspace_does_not_adopt_same_slug_elsewhere(automatic_history, monkeypatch):
    h, _ = automatic_history
    original = h.client.create_project("folder", "Folder", kind="general", workspace_id="other-workspace")
    approval = approve(h, monkeypatch)
    assert approval["project_id"] != original["id"]
    assert h.projects[approval["project_id"]]["workspace_id"] == history.WORKSPACE
    assert h.projects[approval["project_id"]]["slug"].startswith("folder-")
    assert approve(h, monkeypatch)["project_id"] == approval["project_id"]
    assert len(h.created) == 2


def test_existing_wandb_binding_restricts_destination_and_reuses_project(automatic_history, monkeypatch):
    h, remote = automatic_history
    destination = h.client.create_project("existing", "Existing project", kind="general",
                                          workspace_id=history.WORKSPACE)
    remote.bound_project = destination["id"]
    seen = answer(monkeypatch, [1, "import"])
    approval = wb.choose_automatic_destination(h.client, folder=h.folder, wandb_source=source(h))
    assert approval["project_id"] == destination["id"] and len(h.created) == 1
    assert "Existing project" in seen[1][1][2]
    run(enqueue(h, remote, approval))
    assert len(remote.jobs) == len(remote.attachments) == 1


def test_empty_folder_can_still_start_approved_wandb_history(automatic_history, monkeypatch):
    h, remote = automatic_history
    (h.folder / "a.py").unlink()
    approval = approve(h, monkeypatch)
    monkeypatch.setattr(tui, "review", lambda *a, **k: pytest.fail("No deferred review"))
    run(enqueue(h, remote, approval))
    assert h.classified == h.manifested == [] and len(remote.jobs) == 1


def test_current_workspace_change_does_not_redirect_queued_destination(automatic_history, monkeypatch):
    h, remote = automatic_history
    approval = approve(h, monkeypatch)
    job = enqueue(h, remote, approval)
    h.client.settings.workspace = "newly-selected-workspace"
    monkeypatch.setattr(tui, "review", lambda *a, **k: pytest.fail("No deferred review"))
    run(job)
    assert remote.saved()["scope"]["workspace_id"] == history.WORKSPACE
    assert remote.saved()["imports"][0]["project_id"] == approval["project_id"]


@pytest.mark.parametrize("state", ["failed", "canceled", "cancel_requested"])
def test_failed_wandb_receipt_is_reported_without_automatic_history_retry(automatic_history, monkeypatch, state):
    h, remote = automatic_history
    approval = approve(h, monkeypatch)
    job = enqueue(h, remote, approval)
    respond = remote.respond

    def terminal_receipt(request):
        remote.override = {"state": state} if "/backfills" in request.url.path else None
        return respond(request)

    monkeypatch.setattr(remote, "respond", terminal_receipt)
    monkeypatch.setattr(tui, "review", lambda *a, **k: pytest.fail("No deferred review"))
    assert jobs.run_worker(job["id"]) == 1
    error = jobs.get_job(job["id"])["error"]
    assert f"W&B history lab/training is {state}" in error
    assert "dashboard" in error and not h.manifested
    key = remote.saved()["imports"][0]["idempotency_key"]
    jobs.resume(job["id"])
    assert jobs.run_worker(job["id"]) == 1
    assert len(remote.jobs) == 1 and remote.saved()["imports"][0]["idempotency_key"] == key
    assert h.classified == [["a.py"]]
