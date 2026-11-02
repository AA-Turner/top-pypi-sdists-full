"""Tests for bounded, identity-scoped active cloud-writer evidence."""

import json
import subprocess
from dataclasses import replace
from unittest.mock import patch

import pytest

from agentic_devtools.cli.ci.github_provider import GitHubActionsProvider
from agentic_devtools.cli.ci.models import AgentTaskLifecycle, AgentTaskSessionLifecycle
from agentic_devtools.cli.ci.reconciliation.models import CloudWriterRunInventory, WorkflowRun
from agentic_devtools.cli.ci.retry import ProviderRateLimitError, RetryableError


def _task(**changes) -> AgentTaskLifecycle:
    return replace(
        AgentTaskLifecycle(
            task_id="task-1",
            repository="owner/repo",
            pr_number=42,
            head_branch="copilot/pr-42",
            state="in_progress",
            created_at="2026-10-16T09:00:00Z",
            head_sha="a" * 40,
            sessions=(AgentTaskSessionLifecycle("session-1", "in_progress", head_sha="b" * 40),),
        ),
        **changes,
    )


def _run(**changes) -> WorkflowRun:
    return replace(
        WorkflowRun(
            id=700,
            name="Copilot",
            conclusion="",
            run_attempt=2,
            created_at="2026-09-01T09:00:00Z",
            run_started_at="2026-10-16T09:00:00Z",
            event="workflow_dispatch",
            head_branch="copilot/pr-42",
            repository_full_name="owner/repo",
            pr_number=42,
            status="in_progress",
        ),
        **changes,
    )


@pytest.mark.parametrize(
    ("run", "task"),
    [
        (_run(task_id="task-1"), _task()),
        (_run(session_id="session-1"), _task()),
        (_run(), _task(workflow_run_id="700")),
        (
            _run(session_id="session-1"),
            _task(sessions=(AgentTaskSessionLifecycle("session-1", "in_progress", workflow_run_id="700"),)),
        ),
        (_run(), _task(sessions=(AgentTaskSessionLifecycle("session-1", "in_progress", workflow_run_id="700"),))),
    ],
)
def test_exact_identity_associations_are_cancellation_candidates(run, task) -> None:
    provider = GitHubActionsProvider(repo="owner/repo")
    with patch.object(
        provider, "_list_active_cloud_writer_run_inventory", return_value=CloudWriterRunInventory(runs=(run,))
    ):
        result = provider.list_correlated_cloud_writer_runs(42, head_branch="copilot/pr-42", tasks=(task,))
    assert result.runs == (run,)
    assert result.uncorrelated_runs == ()
    assert result.complete


@pytest.mark.parametrize("run", [_run(head_sha="a" * 40), _run(head_sha="b" * 40), _run(task_id="unrelated")])
@pytest.mark.parametrize("tasks", [(), (_task(),)])
def test_sha_or_unmatched_identity_is_audit_evidence_not_cancellation_authority(run, tasks) -> None:
    provider = GitHubActionsProvider(repo="owner/repo")
    with patch.object(
        provider, "_list_active_cloud_writer_run_inventory", return_value=CloudWriterRunInventory(runs=(run,))
    ):
        result = provider.list_correlated_cloud_writer_runs(
            42, head_branch="copilot/pr-42", head_sha="a" * 40, tasks=tasks
        )
    assert result.runs == ()
    assert result.uncorrelated_runs == (run,)


@pytest.mark.parametrize(
    "changes",
    [
        {"repository_full_name": "other/repo"},
        {"repository_full_name": ""},
        {"pr_number": 99},
        {"pr_number": 0},
        {"head_branch": "other"},
    ],
)
def test_scope_mismatch_never_authorizes_cancellation(changes) -> None:
    provider = GitHubActionsProvider(repo="owner/repo")
    run = _run(task_id="task-1", **changes)
    with patch.object(
        provider, "_list_active_cloud_writer_run_inventory", return_value=CloudWriterRunInventory(runs=(run,))
    ):
        result = provider.list_correlated_cloud_writer_runs(42, head_branch="copilot/pr-42", tasks=(_task(),))
    assert result.runs == ()


@pytest.mark.parametrize(
    "task",
    [_task(repository="other/repo"), _task(pr_number=99), _task(head_branch="other")],
)
def test_task_scope_mismatch_never_authorizes_cancellation(task) -> None:
    provider = GitHubActionsProvider(repo="owner/repo")
    run = _run(task_id="task-1")
    with patch.object(
        provider, "_list_active_cloud_writer_run_inventory", return_value=CloudWriterRunInventory(runs=(run,))
    ):
        result = provider.list_correlated_cloud_writer_runs(42, head_branch="copilot/pr-42", tasks=(task,))
    assert result.runs == ()
    assert result.uncorrelated_runs == (run,)


def test_identity_cache_is_invalidated_and_includes_task_scope() -> None:
    provider = GitHubActionsProvider(repo="owner/repo")
    run = _run(task_id="task-1", head_branch="refs/heads/copilot/pr-42")
    with patch.object(
        provider, "_list_active_cloud_writer_run_inventory", return_value=CloudWriterRunInventory(runs=(run,))
    ) as load:
        first = provider.list_correlated_cloud_writer_runs(42, head_branch="copilot/pr-42", tasks=(_task(),))
        assert provider.list_correlated_cloud_writer_runs(42, head_branch="copilot/pr-42", tasks=(_task(),)) == first
        other = provider.list_correlated_cloud_writer_runs(
            42, head_branch="copilot/pr-42", tasks=(_task(repository="other/repo"),)
        )
        assert other.runs == ()
        provider.invalidate_agent_task_inventory(42)
        assert provider.list_correlated_cloud_writer_runs(42, head_branch="copilot/pr-42", tasks=(_task(),)) == first
        provider.invalidate_agent_task_inventory()
    assert first.runs == (run,)
    assert load.call_count == 3


def test_lifecycle_cache_identity_includes_session_creation_clock() -> None:
    provider = GitHubActionsProvider(repo="owner/repo")
    session = AgentTaskSessionLifecycle("session-1", "in_progress")
    first_task = _task(sessions=(session,))
    second_task = _task(sessions=(replace(session, created_at="2026-10-16T09:55:00Z"),))
    with patch.object(
        provider, "_list_active_cloud_writer_run_inventory", return_value=CloudWriterRunInventory()
    ) as load:
        provider.list_correlated_cloud_writer_runs(42, head_branch="copilot/pr-42", tasks=(first_task,))
        provider.list_correlated_cloud_writer_runs(42, head_branch="copilot/pr-42", tasks=(second_task,))

    assert load.call_count == 2


def test_old_rerun_is_inventoried_without_a_created_filter() -> None:
    provider = GitHubActionsProvider(repo="owner/repo")
    raw = {
        "id": 700,
        "run_attempt": 2,
        "created_at": "2026-09-01T09:00:00Z",
        "run_started_at": "2026-10-16T09:00:00Z",
        "status": "in_progress",
        "event": "workflow_dispatch",
        "head_branch": "copilot/pr-42",
        "repository": {"full_name": "owner/repo"},
        "pull_requests": [{"number": 42}],
    }

    def api(endpoint):
        if "/actions/runs/700" in endpoint:
            return json.dumps({"inputs": {"task_id": "task-1"}})
        assert "created=" not in endpoint
        assert "branch=copilot%2Fpr-42" in endpoint
        return json.dumps({"workflow_runs": [raw] if "status=in_progress&" in endpoint else []})

    with (
        patch.object(provider, "find_workflow_id_by_path", return_value="workflow-id") as resolve,
        patch("agentic_devtools.cli.ci.github_provider._gh_api", side_effect=api) as fetch,
    ):
        result = provider.list_correlated_cloud_writer_runs(42, head_branch="copilot/pr-42", tasks=(_task(),))
    assert [run.id for run in result.runs] == [700]
    assert result.runs[0].run_attempt == 2
    assert result.complete
    assert fetch.call_count == 6
    resolve.assert_called_once_with("dynamic/copilot-swe-agent/copilot")


def test_newer_attempt_observed_in_later_status_query_is_preserved_and_marks_inventory_incomplete() -> None:
    provider = GitHubActionsProvider(repo="owner/repo")
    old_attempt = {
        "id": 700,
        "run_attempt": 1,
        "created_at": "2026-10-16T08:00:00Z",
        "run_started_at": "2026-10-16T08:00:00Z",
        "status": "in_progress",
        "event": "workflow_dispatch",
        "head_branch": "copilot/pr-42",
        "repository": {"full_name": "owner/repo"},
        "pull_requests": [{"number": 42}],
    }
    new_attempt = {
        **old_attempt,
        "run_attempt": 2,
        "run_started_at": "2026-10-16T09:55:00Z",
        "status": "waiting",
    }
    older_attempt = {**old_attempt, "status": "pending"}

    def api(endpoint):
        if "/actions/runs/700" in endpoint:
            return json.dumps({"inputs": {"task_id": "task-1"}})
        if "status=in_progress&" in endpoint:
            return json.dumps({"workflow_runs": [old_attempt]})
        if "status=waiting&" in endpoint:
            return json.dumps({"workflow_runs": [new_attempt]})
        if "status=pending&" in endpoint:
            return json.dumps({"workflow_runs": [older_attempt]})
        return json.dumps({"workflow_runs": []})

    with (
        patch.object(provider, "find_workflow_id_by_path", return_value="workflow-id"),
        patch("agentic_devtools.cli.ci.github_provider._gh_api", side_effect=api),
    ):
        inventory = provider._list_active_cloud_writer_run_inventory("copilot/pr-42")

    assert len(inventory.runs) == 1
    assert inventory.runs[0].run_attempt == 2
    assert inventory.runs[0].status == "waiting"
    assert inventory.runs[0].run_started_at == "2026-10-16T09:55:00Z"
    assert not inventory.complete
    assert inventory.incomplete_reasons == ("conflicting-run-attempt:700",)


def test_full_last_page_preserves_evidence_but_marks_inventory_incomplete() -> None:
    provider = GitHubActionsProvider(repo="owner/repo")
    raw = {"id": 700, "status": "in_progress", "head_branch": "copilot/pr-42"}
    with (
        patch.object(provider, "find_workflow_id_by_path", return_value="workflow-id"),
        patch("agentic_devtools.cli.ci.github_provider._gh_api", return_value=json.dumps({"workflow_runs": [raw]})),
    ):
        result = provider._list_active_cloud_writer_run_inventory("copilot/pr-42", page_size=1, max_pages=1)
    assert result.runs
    assert not result.complete
    assert "page-limit:in_progress" in result.incomplete_reasons


@pytest.mark.parametrize("error", [RuntimeError("HTTP 404"), ProviderRateLimitError(), RetryableError("HTTP 503")])
def test_page_failure_is_explicitly_incomplete(error) -> None:
    provider = GitHubActionsProvider(repo="owner/repo")
    with (
        patch.object(provider, "find_workflow_id_by_path", return_value="workflow-id"),
        patch("agentic_devtools.cli.ci.github_provider._gh_api", side_effect=error),
    ):
        result = provider.list_correlated_cloud_writer_runs(42, head_branch="copilot/pr-42", tasks=())
    assert not result.complete
    assert result.incomplete_reasons


def test_missing_workflow_is_not_a_complete_empty_inventory() -> None:
    provider = GitHubActionsProvider(repo="owner/repo")
    with (
        patch.object(provider, "find_workflow_id_by_path", return_value=None),
        patch("agentic_devtools.cli.ci.github_provider._gh_api") as api,
    ):
        result = provider.list_correlated_cloud_writer_runs(42, head_branch="copilot/pr-42", tasks=())
    assert result.runs == ()
    assert not result.complete
    assert result.incomplete_reasons == ("unresolved-workflow",)
    api.assert_not_called()


@pytest.mark.parametrize(
    "kwargs",
    [{"page_size": 0}, {"page_size": 101}, {"page_size": True}, {"max_pages": 0}, {"max_dispatch_enrichments": -1}],
)
def test_invalid_inventory_budgets_fail_before_provider_reads(kwargs) -> None:
    provider = GitHubActionsProvider(repo="owner/repo")
    with patch.object(provider, "find_workflow_id_by_path") as lookup:
        with pytest.raises(ValueError):
            provider._list_active_cloud_writer_run_inventory("copilot/pr-42", **kwargs)
    lookup.assert_not_called()


def test_workflow_lookup_failure_marks_inventory_incomplete() -> None:
    provider = GitHubActionsProvider(repo="owner/repo")
    with patch.object(provider, "find_workflow_id_by_path", side_effect=RetryableError("HTTP 503")):
        result = provider._list_active_cloud_writer_run_inventory("copilot/pr-42")
    assert result.incomplete_reasons == ("workflow-lookup",)
    assert not result.complete


@pytest.mark.parametrize("payload", [[], {}, {"workflow_runs": None}, {"workflow_runs": [None, {}, {"id": True}]}])
def test_malformed_inventory_is_not_reported_as_complete(payload) -> None:
    provider = GitHubActionsProvider(repo="owner/repo")
    with (
        patch.object(provider, "find_workflow_id_by_path", return_value="workflow-id"),
        patch("agentic_devtools.cli.ci.github_provider._gh_api", return_value=json.dumps(payload)),
    ):
        result = provider._list_active_cloud_writer_run_inventory("copilot/pr-42")
    assert not result.complete
    assert result.incomplete_reasons


@pytest.mark.parametrize("detail", [[], {"inputs": None}, RetryableError("HTTP 503")])
def test_detail_failure_preserves_active_run_for_protective_blocking(detail) -> None:
    provider = GitHubActionsProvider(repo="owner/repo")
    raw = {"id": 700, "event": "workflow_dispatch", "head_branch": "copilot/pr-42", "status": "in_progress"}

    def api(endpoint):
        if "/actions/runs/700" in endpoint:
            if isinstance(detail, Exception):
                raise detail
            return json.dumps(detail)
        return json.dumps({"workflow_runs": [raw] if "status=in_progress&" in endpoint else []})

    with (
        patch.object(provider, "find_workflow_id_by_path", return_value="workflow-id"),
        patch("agentic_devtools.cli.ci.github_provider._gh_api", side_effect=api),
    ):
        result = provider.list_correlated_cloud_writer_runs(42, head_branch="copilot/pr-42", tasks=())
    assert result.runs == ()
    assert [run.id for run in result.uncorrelated_runs] == [700]
    assert not result.complete
    assert result.incomplete_reasons == ("dispatch-detail:700",)
    assert result.enumeration_complete is True
    assert result.corroboration_incomplete_reasons == ("dispatch-detail:700",)


def test_dispatch_budget_exhaustion_preserves_runs_without_claiming_complete_evidence() -> None:
    provider = GitHubActionsProvider(repo="owner/repo")
    raw = {"id": 700, "event": "workflow_dispatch", "head_branch": "copilot/pr-42"}
    with (
        patch.object(provider, "find_workflow_id_by_path", return_value="workflow-id"),
        patch(
            "agentic_devtools.cli.ci.github_provider._gh_api", return_value=json.dumps({"workflow_runs": [raw]})
        ) as api,
    ):
        result = provider._list_active_cloud_writer_run_inventory("copilot/pr-42", max_dispatch_enrichments=0)
    assert [run.id for run in result.runs] == [700]
    assert not result.complete
    assert result.incomplete_reasons == ("dispatch-detail:700", "missing-run-status:700")
    assert result.corroboration_incomplete_reasons == ("dispatch-detail:700",)
    assert api.call_count == 5


def test_pagination_visits_later_active_pages_and_keeps_dispatch_session_identity() -> None:
    provider = GitHubActionsProvider(repo="owner/repo")
    raw = {
        "id": 700,
        "event": "workflow_dispatch",
        "head_branch": "copilot/pr-42",
        "status": "in_progress",
        "repository": {"full_name": "owner/repo"},
    }

    def api(endpoint):
        if "/actions/runs/700" in endpoint:
            return json.dumps({"inputs": {"pr_number": "42", "session_id": "session-1"}})
        return json.dumps(
            {"workflow_runs": [raw] if "status=in_progress&" in endpoint and endpoint.endswith("&page=1") else []}
        )

    with (
        patch.object(provider, "find_workflow_id_by_path", return_value="workflow-id"),
        patch("agentic_devtools.cli.ci.github_provider._gh_api", side_effect=api) as fetch,
    ):
        result = provider._list_active_cloud_writer_run_inventory("copilot/pr-42", page_size=1)
    assert result.complete
    assert result.runs[0].pr_number == 42
    assert result.runs[0].session_id == "session-1"
    assert any("page=2" in call.args[0] for call in fetch.call_args_list)


def test_completed_run_observed_during_listing_race_is_not_an_active_writer() -> None:
    provider = GitHubActionsProvider(repo="owner/repo")
    with patch.object(
        provider,
        "_list_active_cloud_writer_run_inventory",
        return_value=CloudWriterRunInventory(runs=(_run(status="completed", task_id="task-1"),)),
    ):
        result = provider.list_correlated_cloud_writer_runs(42, head_branch="copilot/pr-42", tasks=(_task(),))
    assert result.complete
    assert result.runs == result.uncorrelated_runs == ()


@pytest.mark.parametrize("attempt", [None, "1", True, 0, -1, 1.5])
def test_unknown_run_attempt_never_defaults_to_original_attempt(attempt) -> None:
    provider = GitHubActionsProvider(repo="owner/repo")
    raw = {"id": 700, "status": "in_progress", "run_attempt": attempt}
    with (
        patch.object(provider, "find_workflow_id_by_path", return_value="workflow-id"),
        patch("agentic_devtools.cli.ci.github_provider._gh_api", return_value=json.dumps({"workflow_runs": [raw]})),
    ):
        result = provider._list_active_cloud_writer_run_inventory("copilot/pr-42")
    assert result.runs[0].run_attempt == 0


@pytest.mark.parametrize("error", [OSError("unavailable"), subprocess.TimeoutExpired("gh", 60)])
def test_transport_failure_preserves_previous_page_evidence(error) -> None:
    provider = GitHubActionsProvider(repo="owner/repo")
    raw = {"id": 700, "status": "in_progress"}
    with (
        patch.object(provider, "find_workflow_id_by_path", return_value="workflow-id"),
        patch(
            "agentic_devtools.cli.ci.github_provider._gh_api",
            side_effect=[json.dumps({"workflow_runs": [raw]}), error, error, error, error, error],
        ),
    ):
        result = provider._list_active_cloud_writer_run_inventory("copilot/pr-42", page_size=1)
    assert [run.id for run in result.runs] == [700]
    assert not result.complete
    assert "workflow-page:queued:2" in result.incomplete_reasons


@pytest.mark.parametrize(
    ("run", "task"),
    [
        (_run(task_id="other-task", session_id="session-1"), _task()),
        (_run(task_id="other-task"), _task(workflow_run_id="700")),
        (_run(task_id="task-1", session_id="other-session"), _task()),
        (_run(task_id="task-1"), _task(workflow_run_id="701")),
        (
            _run(task_id="task-1", session_id="session-1"),
            _task(sessions=(AgentTaskSessionLifecycle("session-1", "in_progress", workflow_run_id="701"),)),
        ),
        (
            _run(task_id="task-1", session_id="session-1"),
            _task(
                workflow_run_id="700",
                sessions=(AgentTaskSessionLifecycle("session-1", "in_progress", workflow_run_id="701"),),
            ),
        ),
    ],
)
def test_contradictory_identity_is_protective_not_cancellation_evidence(run, task) -> None:
    provider = GitHubActionsProvider(repo="owner/repo")
    with patch.object(
        provider, "_list_active_cloud_writer_run_inventory", return_value=CloudWriterRunInventory(runs=(run,))
    ):
        result = provider.list_correlated_cloud_writer_runs(42, head_branch="copilot/pr-42", tasks=(task,))
    assert result.runs == ()
    assert result.uncorrelated_runs == (run,)
