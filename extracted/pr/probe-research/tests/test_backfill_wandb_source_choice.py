"""A source chosen upfront never substitutes for destination approval."""

from contextlib import nullcontext

import pytest

from probe.cli import backfill as bf, backfill_run as runner
from probe.cli import backfill_wandb as wb, import_jobs as jobs, import_jobs_ui, tui
from tests import test_backfill_wandb as history
from tests import test_backfill_auto_import as auto_tests

history_harness = history.harness
automatic = auto_tests.automatic
queued = auto_tests.queued


def answer(monkeypatch, responses):
    responses = iter(responses)
    seen = []

    def review(title, lines, choices, **kwargs):
        seen.append((title, list(lines), choices))
        value = next(responses)
        return choices[value][1] if isinstance(value, int) else value

    monkeypatch.setattr(tui, "review", review)
    return seen


def selection(client, *, connection=history.CONNECTION, source="lab/training"):
    return {"schema": wb.SOURCE_SCHEMA, **wb._selection_identity(client),
            "connection_id": connection, "external_id": source}


@pytest.fixture
def source_history(history_harness, monkeypatch):
    client, coverage, remote = history_harness
    monkeypatch.setattr(client, "me", lambda: {"customer_id": "synthetic", "user_id": "user"})
    return client, coverage, remote


def test_upfront_source_uses_connected_accounts_but_never_saves_or_launches_import(source_history, monkeypatch):
    client, _, remote = source_history
    accounts = wb.eligible_connections(client)
    assert [row["id"] for row in accounts] == [history.CONNECTION]
    seen = answer(monkeypatch, [1, 1])
    selected = wb.choose_source(client, accounts=accounts)
    assert selected == selection(client)
    assert [title for title, _, _ in seen] == ["Choose a W&B account", "Choose W&B history"]
    assert all(method == "GET" for method, _, _ in remote.requests)
    assert remote.saved() is None and not remote.jobs and not remote.attachments


@pytest.mark.parametrize("responses,expected", [([tui.BACK], tui.BACK), ([0], None),
                                              ([1, tui.BACK, tui.BACK], tui.BACK), ([1, 0], None)])
def test_upfront_back_and_skip_remain_before_any_approval(source_history, monkeypatch, responses, expected):
    client, _, remote = source_history
    answer(monkeypatch, responses)
    assert wb.choose_source(client) is expected
    assert remote.saved() is None and not remote.jobs


def test_upfront_ctrl_c_propagates_and_no_accounts_do_not_prompt(source_history, monkeypatch):
    client, _, remote = source_history
    seen = answer(monkeypatch, [None])
    assert wb.choose_source(client, accounts=[]) is None and seen == []
    with pytest.raises(KeyboardInterrupt):
        wb.choose_source(client)
    assert remote.saved() is None


def test_selected_source_starts_at_destination_and_reuses_durable_receipts(source_history, monkeypatch):
    client, coverage, remote = source_history
    selected = selection(client)
    seen = answer(monkeypatch, [2, "import"])
    result = wb.run(client, coverage, interactive=True, offer=True, back_to_selection=True, wandb_source=selected)
    assert [title for title, _, _ in seen] == ["Choose a Probe destination", "Review W&B history import"]
    assert result.source_resolved
    saved = remote.saved()["imports"][0]
    assert saved["project_id"] == history.OTHER and len(remote.jobs) == 1
    answer(monkeypatch, [])  # A repeated source keeps its already reviewed mapping.
    assert wb.run(client, coverage, interactive=True, offer=True, wandb_source=selected).source_resolved
    assert remote.saved()["imports"][0]["idempotency_key"] == saved["idempotency_key"]
    assert len(remote.jobs) == 1


@pytest.mark.parametrize("responses,expected", [([tui.BACK], "back"), ([0], "skip"),
                                              ([1, "skip"], "skip"), ([None], "interrupt")])
def test_selected_destination_back_skip_and_quit_do_not_admit(source_history, monkeypatch, responses, expected):
    client, coverage, remote = source_history
    answer(monkeypatch, responses)
    def call():
        return wb.run(client, coverage, interactive=True, offer=True, back_to_selection=True,
                      wandb_source=selection(client))
    if expected == "interrupt":
        with pytest.raises(KeyboardInterrupt):
            call()
    else:
        result = call()
        assert result is tui.BACK if expected == "back" else result.source_resolved
    assert remote.saved() is None and not remote.jobs


@pytest.mark.parametrize("field,value", [("backend", "https://other.invalid"), ("user_id", "other-user"),
                                         ("customer_id", "other-team"), ("connection_id", history.OTHER),
                                         ("external_id", "unavailable/project")])
def test_selected_selection_is_revalidated_without_silently_changing_source(source_history, monkeypatch, field, value):
    client, coverage, remote = source_history
    selected = {**selection(client), field: value}
    answer(monkeypatch, [])
    result = wb.run(client, coverage, interactive=True, offer=True, wandb_source=selected)
    assert result and not result.source_resolved
    assert remote.saved() is None and not remote.jobs


@pytest.mark.parametrize("lost", ["attach", "launch"])
def test_selected_admission_outage_remains_retryable_without_duplicate_history(source_history, monkeypatch, lost):
    client, coverage, remote = source_history
    selected = selection(client)
    remote.lose = lost
    answer(monkeypatch, [1, "import"])
    assert not wb.run(client, coverage, interactive=True, offer=True, wandb_source=selected).source_resolved
    key = remote.saved()["imports"][0]["idempotency_key"]
    answer(monkeypatch, [])
    assert wb.run(client, coverage, interactive=True, offer=True, wandb_source=selected).source_resolved
    assert remote.saved()["imports"][0]["idempotency_key"] == key
    assert len(remote.attachments) == len(remote.jobs) == 1


@pytest.mark.parametrize("resolved", [False, True])
def test_reviewed_folder_requires_wandb_success_or_explicit_continue_before_queue(automatic, monkeypatch, resolved):
    h = automatic
    selected = selection(h.client)
    seen = []

    def history_lane(client, coverage, **kwargs):
        seen.append(kwargs)
        return wb.HistoryResult(["History status"], source_resolved=resolved)

    monkeypatch.setattr(wb, "run", history_lane)
    decisions = []

    def review(title, lines, choices):
        decisions.append(title)
        assert jobs.list_jobs() == []
        return tui.SKIP if title == "W&B import could not start" else "import"

    monkeypatch.setattr(tui, "review", review)
    monkeypatch.setattr(import_jobs_ui, "show_started_import", lambda job: job)
    result = runner.execute(
        client_factory=lambda: nullcontext(h.client), folder=h.folder, agent=bf.Agent.CLAUDE,
        interactive=True, yes=False, background=True, back_to_selection=True,
        wandb_source=selected, offer_wandb=False,
    )
    assert isinstance(result, bf.StartedFolderImport)
    assert seen[0]["wandb_source"] == selected and seen[0]["offer"] is True
    saved = jobs.get_job(result.job["id"])
    assert "wandb_source" not in saved and "pending_wandb" not in saved
    assert "wandb_source" not in saved["payload"]
    assert ("W&B import could not start" in decisions) is not resolved
    assert h.manifested == h.remote.calls == []


def test_upfront_skip_suppresses_later_generic_offer(automatic, monkeypatch):
    h = automatic
    seen = []

    def history_lane(client, coverage, **kwargs):
        seen.append(kwargs)
        return []

    monkeypatch.setattr(wb, "run", history_lane)
    monkeypatch.setattr(tui, "review", lambda title, lines, choices: "import")
    monkeypatch.setattr(import_jobs_ui, "show_started_import", lambda job: job)
    h.run(interactive=True, yes=False, background=True, offer_wandb=False)
    assert seen[0]["offer"] is False and seen[0]["wandb_source"] is None


@pytest.mark.parametrize("decision", [tui.BACK, None])
def test_wandb_error_back_or_interrupt_never_queues_files(automatic, monkeypatch, decision):
    h = automatic
    monkeypatch.setattr(wb, "run", lambda *a, **k: wb.HistoryResult(["Connection unavailable"]))
    monkeypatch.setattr(tui, "review", lambda title, lines, choices:
                        decision if title == "W&B import could not start" else "import")
    kwargs = dict(interactive=True, yes=False, background=True, back_to_selection=True,
                  wandb_source=selection(h.client), offer_wandb=False)
    if decision is None:
        with pytest.raises(KeyboardInterrupt):
            h.run(**kwargs)
    else:
        assert h.run(**kwargs) is tui.BACK
    assert jobs.list_jobs() == [] and h.manifested == h.remote.calls == []


def test_wandb_retry_reuses_folder_plan_and_only_queues_after_source_resolves(automatic, monkeypatch):
    h = automatic
    attempts = []

    def history_lane(*args, **kwargs):
        attempts.append(kwargs)
        assert jobs.list_jobs() == [] and h.manifested == h.remote.calls == []
        return wb.HistoryResult(["History status"], source_resolved=len(attempts) == 2)

    monkeypatch.setattr(wb, "run", history_lane)
    monkeypatch.setattr(tui, "review", lambda title, lines, choices:
                        "retry" if title == "W&B import could not start" else "import")
    monkeypatch.setattr(import_jobs_ui, "show_started_import", lambda job: job)
    result = h.run(interactive=True, yes=False, background=True, back_to_selection=True,
                   wandb_source=selection(h.client), offer_wandb=False)
    assert isinstance(result, bf.StartedFolderImport)
    assert len(attempts) == 2 and h.classified == [["a.py"]]
    assert len(jobs.list_jobs()) == 1 and h.manifested == h.remote.calls == []


@pytest.mark.parametrize("interactive,yes", [(False, False), (True, True)])
def test_selected_source_cannot_bypass_foreground_review(automatic, monkeypatch, interactive, yes):
    h = automatic
    monkeypatch.setattr(runner, "_index", lambda *a: pytest.fail("Review mode must be checked first"))
    lines = h.run(interactive=interactive, yes=yes, background=True, wandb_source=selection(h.client))
    assert any("foreground review" in line for line in lines)
    assert jobs.list_jobs() == [] and h.classified == h.created == h.manifested == h.remote.calls == []
