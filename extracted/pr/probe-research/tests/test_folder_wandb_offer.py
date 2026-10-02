"""Choose and review W&B during the folder flow, before import starts."""

from contextlib import nullcontext
from types import SimpleNamespace

import pytest

from probe.cli import backfill as bf, backfill_import as imp, backfill_run as runner, backfill_wandb as wb
from probe.cli.backfill_coverage import CoverageError
from probe.cli import import_jobs as jobs, import_jobs_ui, tui
from tests.test_import_jobs import queued as queued


@pytest.fixture
def flow(tmp_path, monkeypatch, queued):
    h = SimpleNamespace(folder=tmp_path, events=[], calls=[], auto_calls=[], source={
        "schema": "probe.wandb-source/1", "backend": "https://api.test",
        "customer_id": "lab", "user_id": "user", "connection_id": "connection",
        "external_id": "lab/training",
    })
    h.approval = {**h.source, "schema": "probe.wandb-import-approval/1",
                  "workspace_id": "workspace", "project_id": "project"}
    monkeypatch.setattr(bf, "choose_directory", lambda start: h.events.append("folder") or h.folder)
    monkeypatch.setattr(bf, "choose_folder_wandb", lambda *a, **k: (h.events.append("wandb") or h.source, True))
    monkeypatch.setattr(bf, "resolve_agent", lambda *a, **k: h.events.append("agent") or (bf.Agent.CODEX, None))
    monkeypatch.setattr(bf, "choose_import_mode", lambda *a, **k: bf.FolderImportMode.REVIEW_FIRST
                        if h.source else bf.FolderImportMode.AUTOMATIC)

    def enqueue(**kwargs):
        h.auto_calls.append(kwargs)
        h.events.append("queued")
        return jobs.enqueue(jobs.Kind.FOLDER, {
            "scope": {"backend": "https://api.test", "customer_id": "lab"}, "user_id": "user",
        }, "Folder import")

    def status(job):
        h.events.append("status")
        return job

    def reviewed(**kwargs):
        h.calls.append(kwargs)
        assert jobs.list_jobs() == []
        h.events.append("review")
        return bf.StartedFolderImport(status(enqueue()), ["Started"])

    monkeypatch.setattr(runner, "execute", reviewed)
    monkeypatch.setattr(imp, "enqueue_auto_import", enqueue)
    monkeypatch.setattr(import_jobs_ui, "show_started_import", status)
    monkeypatch.setattr(wb, "choose_automatic_destination",
                        lambda *a, **k: h.events.append("destination") or h.approval, raising=False)
    return h


def run():
    return bf.run(client_factory=lambda: nullcontext(object()), background=True, back_to_selection=True)


def test_wandb_source_is_chosen_after_folder_and_reviewed_before_background_import(flow):
    result = run()
    assert isinstance(result, bf.StartedFolderImport)
    assert flow.events == ["folder", "wandb", "agent", "review", "queued", "status"]
    assert flow.calls[0]["wandb_source"] == flow.source
    assert "pending_wandb" not in result.job


@pytest.mark.parametrize("source", [None, "chosen"])
def test_reviewed_mode_carries_upfront_choice_without_a_duplicate_offer(flow, monkeypatch, source):
    flow.source = flow.source if source else None
    monkeypatch.setattr(bf, "choose_import_mode", lambda *a, **k: bf.FolderImportMode.REVIEW_FIRST)
    calls = []
    monkeypatch.setattr(runner, "execute", lambda **kw: calls.append(kw))
    assert run() is None
    assert calls[0]["wandb_source"] == flow.source
    assert calls[0]["offer_wandb"] is False
    assert flow.events == ["folder", "wandb", "agent"]


def test_back_from_mode_reopens_wandb_with_selection_preserved(flow, monkeypatch):
    modes = iter([tui.BACK, bf.FolderImportMode.REVIEW_FIRST])
    monkeypatch.setattr(bf, "choose_import_mode", lambda *a, **k: next(modes))
    defaults = []

    def source(*a, **kwargs):
        defaults.append(kwargs["default"])
        return flow.source, True

    monkeypatch.setattr(bf, "choose_folder_wandb", source)
    assert isinstance(run(), bf.StartedFolderImport)
    assert defaults == [None, flow.source]
    assert flow.events.count("queued") == 1


def test_back_from_wandb_reopens_folder_then_offers_again(flow, monkeypatch):
    choices = iter([(tui.BACK, True), (flow.source, True)])
    monkeypatch.setattr(bf, "choose_folder_wandb", lambda *a, **k: next(choices))
    assert isinstance(run(), bf.StartedFolderImport)
    assert flow.events.count("folder") == 2
    assert flow.events.count("queued") == 1


@pytest.mark.parametrize("explicit_folder", [False, True])
def test_back_from_missing_agent_reopens_wandb_choice(flow, monkeypatch, explicit_folder):
    agents = iter([(None, "Install a supported coding agent."), (bf.Agent.CODEX, None)])
    monkeypatch.setattr(bf, "resolve_agent", lambda *a, **k: next(agents))
    monkeypatch.setattr(tui, "review", lambda *a, **k: tui.BACK)
    defaults = []

    def source(*a, **kwargs):
        defaults.append(kwargs["default"])
        return flow.source, True

    monkeypatch.setattr(bf, "choose_folder_wandb", source)
    result = bf.run(client_factory=object, background=True, back_to_selection=True,
                    folder=flow.folder if explicit_folder else None)
    assert isinstance(result, bf.StartedFolderImport)
    assert defaults == [None, flow.source]
    assert flow.events.count("folder") == (0 if explicit_folder else 1)
    assert flow.events.count("queued") == 1


def test_retry_does_not_ask_for_wandb_again(flow, monkeypatch):
    reviewed = runner.execute
    attempts = []

    def attempt(**kwargs):
        attempts.append(True)
        if len(attempts) == 1:
            return ["Offline"]
        return reviewed(**kwargs)

    monkeypatch.setattr(runner, "execute", attempt)
    monkeypatch.setattr(tui, "review", lambda *a, **k: "retry")
    assert isinstance(run(), bf.StartedFolderImport)
    assert flow.events.count("wandb") == 1 and len(attempts) == 2


def test_files_only_keeps_the_automatic_import_path(flow):
    flow.source = None
    assert isinstance(run(), bf.StartedFolderImport)
    assert flow.events == ["folder", "wandb", "agent", "queued", "status"]


def test_wandb_mode_keeps_automatic_import_available(monkeypatch, tmp_path):
    def review(title, lines, choices):
        assert "W&B" in title
        assert "in the background without file review" in " ".join(lines)
        assert "one Probe project for both files and W&B history" in " ".join(lines)
        assert ("Scan and import in background", bf.FolderImportMode.AUTOMATIC) in choices
        return bf.FolderImportMode.AUTOMATIC

    monkeypatch.setattr(tui, "review", review)
    assert bf.choose_import_mode(tmp_path, bf.Agent.CODEX, wandb_source={"external_id": "lab/training"}) == (
        bf.FolderImportMode.AUTOMATIC
    )


def test_automatic_wandb_import_approves_destination_then_queues_without_scanning(flow, monkeypatch):
    monkeypatch.setattr(bf, "choose_import_mode", lambda *a, **k: bf.FolderImportMode.AUTOMATIC)
    result = run()
    assert isinstance(result, bf.StartedFolderImport)
    assert flow.events == ["folder", "wandb", "agent", "destination", "queued", "status"]
    assert flow.auto_calls[0]["wandb_approval"] == flow.approval
    assert flow.auto_calls[0]["auto_approve"] is True
    assert flow.calls == []


def test_skipping_automatic_wandb_destination_still_imports_files(flow, monkeypatch):
    monkeypatch.setattr(bf, "choose_import_mode", lambda *a, **k: bf.FolderImportMode.AUTOMATIC)
    monkeypatch.setattr(wb, "choose_automatic_destination", lambda *a, **k: None, raising=False)
    assert isinstance(run(), bf.StartedFolderImport)
    assert "wandb_approval" not in flow.auto_calls[0]
    assert flow.calls == []


def test_back_from_automatic_destination_returns_to_import_mode(flow, monkeypatch):
    modes = iter([bf.FolderImportMode.AUTOMATIC, bf.FolderImportMode.REVIEW_FIRST])
    monkeypatch.setattr(bf, "choose_import_mode", lambda *a, **k: next(modes))
    monkeypatch.setattr(wb, "choose_automatic_destination", lambda *a, **k: tui.BACK, raising=False)
    assert isinstance(run(), bf.StartedFolderImport)
    assert flow.calls[0]["wandb_source"] == flow.source
    assert flow.events == ["folder", "wandb", "agent", "review", "queued", "status"]


def test_quit_from_automatic_destination_never_queues_an_import(flow, monkeypatch):
    monkeypatch.setattr(bf, "choose_import_mode", lambda *a, **k: bf.FolderImportMode.AUTOMATIC)

    def quit(*a, **k):
        raise KeyboardInterrupt

    monkeypatch.setattr(wb, "choose_automatic_destination", quit, raising=False)
    with pytest.raises(KeyboardInterrupt):
        run()
    assert jobs.list_jobs() == [] and flow.calls == [] and flow.auto_calls == []


@pytest.mark.parametrize("failure_action,destination_calls", [("retry", 1), (tui.BACK, 2)])
def test_automatic_retry_preserves_approval_and_back_reopens_it(flow, monkeypatch, failure_action, destination_calls):
    monkeypatch.setattr(bf, "choose_import_mode", lambda *a, **k: bf.FolderImportMode.AUTOMATIC)
    monkeypatch.setattr(tui, "review", lambda *a, **k: failure_action)
    enqueue = imp.enqueue_auto_import
    attempts = []

    def attempt(**kwargs):
        attempts.append(kwargs)
        if len(attempts) == 1:
            raise CoverageError("Connection unavailable.")
        return enqueue(**kwargs)

    monkeypatch.setattr(imp, "enqueue_auto_import", attempt)
    assert isinstance(run(), bf.StartedFolderImport)
    assert len(attempts) == 2 and attempts[0]["wandb_approval"] == attempts[1]["wandb_approval"]
    assert flow.events.count("destination") == destination_calls
    assert flow.events.count("folder") == flow.events.count("wandb") == flow.events.count("queued") == 1


def test_no_connected_wandb_account_skips_the_offer(monkeypatch):
    from probe.cli import backfill_wandb

    monkeypatch.setattr(backfill_wandb, "eligible_connections", lambda client: [], raising=False)
    monkeypatch.setattr(backfill_wandb, "choose_source", lambda *a, **k: pytest.fail("No account to offer"), raising=False)
    monkeypatch.setattr(tui, "working", lambda *a: nullcontext())
    assert bf.choose_folder_wandb(lambda: nullcontext(object())) == (None, False)


def test_unavailable_wandb_can_be_skipped_without_exposing_provider_data(monkeypatch):
    def factory():
        raise RuntimeError("credential-bearing response")

    def review(title, lines, choices, **kwargs):
        assert "credential-bearing" not in " ".join(lines)
        return "files"

    monkeypatch.setattr(tui, "review", review)
    assert bf.choose_folder_wandb(factory) == (None, True)
