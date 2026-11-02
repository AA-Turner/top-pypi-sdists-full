"""Tests for loading typed Agent Tasks lifecycle evidence."""

import json
from datetime import UTC, datetime
from unittest.mock import patch

import pytest

from agentic_devtools.cli.ci.github_provider import GitHubActionsProvider
from agentic_devtools.cli.ci.models import AgentTaskInventory
from agentic_devtools.cli.ci.pipeline.session_detector import classify_agent_task_inventory
from agentic_devtools.cli.ci.reconciliation.models import CloudWriterRunInventory
from agentic_devtools.cli.ci.retry import ProviderRateLimitError, RetryableError

NOW = datetime(2026, 10, 16, 10, 0, tzinfo=UTC)


@pytest.fixture(autouse=True)
def _default_workflow_token(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("DEFAULT_CLASSIC_REPO_WORKFLOW_PAT", "workflow-token")


def test_lists_correlated_task_and_distinct_session_lifecycles() -> None:
    """Loads task detail and preserves each session's state and timestamps."""
    provider = GitHubActionsProvider(repo="owner/repo")
    summary = {
        "id": "task-1",
        "state": "failed",
        "pullRequestNumber": 42,
        "createdAt": "2026-10-16T08:00:00Z",
    }
    detail = {
        **summary,
        "sessions": [
            {"id": "session-1", "state": "failed", "startedAt": "2026-10-16T08:05:00Z"},
            {
                "id": "session-2",
                "state": "in_progress",
                "startedAt": "2026-10-16T09:55:00Z",
                "updatedAt": "2026-10-16T09:59:00Z",
            },
        ],
    }
    with (
        patch.object(provider, "_fetch_agent_task_pages", return_value=([summary], True, ())) as pages,
        patch.object(provider, "_fetch_agent_task_detail", return_value=json.dumps(detail)) as fetch_detail,
    ):
        inventory = provider.list_pr_agent_task_lifecycles(
            42,
            head_branch="copilot/pr-42",
            head_sha="a" * 40,
        )
        cached = provider.list_pr_agent_task_lifecycles(
            42,
            head_branch="copilot/pr-42",
            head_sha="a" * 40,
        )

    assert inventory.complete is True
    assert inventory.tasks[0].task_id == "task-1"
    assert [session.session_id for session in inventory.tasks[0].sessions] == ["session-1", "session-2"]
    assert inventory.tasks[0].sessions[1].started_at == "2026-10-16T09:55:00Z"
    assert inventory.tasks[0].sessions[1].idle_at == ""
    assert cached == inventory
    pages.assert_called_once_with("owner/repo", "workflow-token")
    fetch_detail.assert_called_once_with("owner/repo", "task-1", "workflow-token")


def test_lifecycle_page_failure_preserves_remote_404(monkeypatch: pytest.MonkeyPatch) -> None:
    """Propagates a remote page 404 instead of returning a successful empty inventory."""
    monkeypatch.setenv("DEFAULT_CLASSIC_REPO_WORKFLOW_PAT", "workflow-token")
    error = RuntimeError("GitHub API error: HTTP 404; http_status=404")
    with patch("agentic_devtools.cli.ci.github_provider._gh_api", side_effect=error):
        with pytest.raises(RuntimeError) as exc_info:
            GitHubActionsProvider(repo="owner/repo").list_pr_agent_task_lifecycles(42)

    assert exc_info.value is error
    assert "HTTP 404" in str(exc_info.value)


def test_matches_pull_artifact_by_database_id() -> None:
    """Matches a pull artifact's database ID without treating it as the PR number."""
    provider = GitHubActionsProvider(repo="owner/repo")
    task = {
        "id": "task-1",
        "state": "in_progress",
        "createdAt": "2026-10-16T09:00:00Z",
        "artifacts": [
            None,
            {"type": "issue", "data": {"id": 123456}},
            {"type": "pull", "data": "malformed"},
            {"type": "pull", "data": {"number": 42}},
            {"type": "pull", "data": {"id": "123456"}},
        ],
    }
    with (
        patch.object(provider, "_fetch_agent_task_pages", return_value=([task], True, ())),
        patch.object(provider, "_fetch_agent_task_detail", return_value=json.dumps(task)),
    ):
        inventory = provider.list_pr_agent_task_lifecycles(
            42,
            pr_id=123456,
            head_branch="copilot/pr-42",
        )

    assert inventory.complete is True
    assert len(inventory.tasks) == 1
    assert inventory.tasks[0].pr_number == 42


def test_matches_task_database_id_field_and_keeps_missing_artifacts_safe() -> None:
    provider = GitHubActionsProvider(repo="owner/repo")
    tasks = [
        {"id": "task-by-pr-id", "state": "in_progress", "pull_request_id": 123456},
        {"id": "task-by-pr-number", "state": "in_progress", "pullRequestNumber": 42, "artifacts": []},
    ]
    with (
        patch.object(provider, "_fetch_agent_task_pages", return_value=(tasks, True, ())),
        patch.object(
            provider,
            "_fetch_agent_task_detail",
            return_value=json.dumps({"state": "in_progress", "createdAt": "2026-10-16T09:00:00Z"}),
        ),
    ):
        inventory = provider.list_pr_agent_task_lifecycles(42, pr_id=123456, head_branch="copilot/pr-42")

    assert [task.task_id for task in inventory.tasks] == ["task-by-pr-id", "task-by-pr-number"]


@pytest.mark.parametrize("pr_id", [0, True, "123456"])
def test_rejects_invalid_pull_request_database_ids(pr_id) -> None:
    provider = GitHubActionsProvider(repo="owner/repo")

    with pytest.raises(ValueError, match="pr_id must be a positive integer"):
        provider.list_pr_agent_task_lifecycles(42, pr_id=pr_id)


@pytest.mark.parametrize(
    "error",
    [RuntimeError("HTTP 404"), ProviderRateLimitError(), RetryableError("HTTP 503")],
)
def test_detail_failure_marks_inventory_incomplete_without_dropping_task(error: Exception) -> None:
    """Preserves summary evidence after detail lookup failures, including exhausted retries."""
    provider = GitHubActionsProvider(repo="owner/repo")
    task = {
        "id": "task-1",
        "state": "in_progress",
        "pullRequestNumber": 42,
        "createdAt": "2026-10-16T09:00:00Z",
    }
    with (
        patch.object(provider, "_fetch_agent_task_pages", return_value=([task], True, ())),
        patch.object(
            provider,
            "_fetch_agent_task_detail",
            side_effect=error,
        ),
    ):
        inventory = provider.list_pr_agent_task_lifecycles(42, head_branch="copilot/pr-42")

    assert inventory.complete is False
    assert len(inventory.tasks) == 1
    assert inventory.tasks[0].state == "in_progress"
    assert inventory.tasks[0].created_at == "2026-10-16T09:00:00Z"
    assert inventory.incomplete_reasons == ("task-detail:task-1",)


def test_detail_omissions_preserve_terminal_summary_state_and_creation_clock() -> None:
    """A detail response without lifecycle fields retains terminal list evidence."""
    provider = GitHubActionsProvider(repo="owner/repo")
    task = {
        "id": "task-1",
        "state": "completed",
        "pullRequestNumber": 42,
        "createdAt": "2026-10-16T08:00:00Z",
    }
    detail = {"updatedAt": "2026-10-16T09:59:00Z", "outcome": None}
    with (
        patch.object(provider, "_fetch_agent_task_pages", return_value=([task], True, ())),
        patch.object(provider, "_fetch_agent_task_detail", return_value=json.dumps(detail)),
    ):
        inventory = provider.list_pr_agent_task_lifecycles(42, head_branch="copilot/pr-42")

    assessment = classify_agent_task_inventory(inventory, now=NOW)

    assert inventory.complete is True
    assert inventory.tasks[0].state == "completed"
    assert inventory.tasks[0].created_at == "2026-10-16T08:00:00Z"
    assert assessment.blocking is False


def test_missing_session_id_preserves_newer_session_clock_as_unknown_evidence() -> None:
    """A missing session ID degrades active evidence without erasing its clock."""
    provider = GitHubActionsProvider(repo="owner/repo")
    task = {
        "id": "task-1",
        "state": "in_progress",
        "pullRequestNumber": 42,
        "createdAt": "2026-10-16T08:00:00Z",
    }
    detail = {
        **task,
        "sessions": [
            {"state": "in_progress", "startedAt": "2026-10-16T09:50:00Z"},
        ],
    }
    with (
        patch.object(provider, "_fetch_agent_task_pages", return_value=([task], True, ())),
        patch.object(provider, "_fetch_agent_task_detail", return_value=json.dumps(detail)),
    ):
        inventory = provider.list_pr_agent_task_lifecycles(42, head_branch="copilot/pr-42")

    assessment = classify_agent_task_inventory(inventory, now=NOW)

    assert inventory.complete is False
    assert inventory.incomplete_reasons == ("missing-session-id:task-1",)
    assert inventory.tasks[0].sessions[0].session_id == ""
    assert inventory.tasks[0].sessions[0].started_at == "2026-10-16T09:50:00Z"
    assert assessment.blocking is None
    assert assessment.since == datetime(2026, 10, 16, 9, 50, tzinfo=UTC)
    assert assessment.reason == "malformed-lifecycle"


def test_top_level_session_clock_is_preserved_as_unknown_when_session_id_is_missing() -> None:
    """Retains available lifecycle timestamps while classifying malformed evidence as unknown."""
    provider = GitHubActionsProvider(repo="owner/repo")
    task = {
        "id": "task-1",
        "state": "in_progress",
        "pullRequestNumber": 42,
        "createdAt": "2026-10-16T08:00:00Z",
    }
    detail = {**task, "startedAt": "2026-10-16T09:50:00Z"}
    with (
        patch.object(provider, "_fetch_agent_task_pages", return_value=([task], True, ())),
        patch.object(provider, "_fetch_agent_task_detail", return_value=json.dumps(detail)),
    ):
        inventory = provider.list_pr_agent_task_lifecycles(42, head_branch="copilot/pr-42")

    assessment = classify_agent_task_inventory(inventory, now=NOW)

    assert inventory.complete is False
    assert inventory.incomplete_reasons == ("missing-session-id:task-1",)
    assert inventory.tasks[0].sessions[0].started_at == "2026-10-16T09:50:00Z"
    assert inventory.tasks[0].sessions[0].created_at == ""
    assert assessment.blocking is None
    assert assessment.since == datetime(2026, 10, 16, 9, 50, tzinfo=UTC)
    assert assessment.reason == "malformed-lifecycle"


def test_invalidating_inventory_forces_a_new_rest_read() -> None:
    """Invalidates cached task lifecycle evidence at a mutation boundary."""
    provider = GitHubActionsProvider(repo="owner/repo")
    with patch.object(provider, "_fetch_agent_task_pages", return_value=([], True, ())) as pages:
        provider.list_pr_agent_task_lifecycles(42, head_branch="copilot/pr-42")
        provider.invalidate_agent_task_inventory(42)
        provider.list_pr_agent_task_lifecycles(42, head_branch="copilot/pr-42")

    assert pages.call_count == 2


def test_bounded_task_pagination_marks_a_full_final_page_incomplete() -> None:
    """Stops at the configured page limit and reports possible truncation."""
    provider = GitHubActionsProvider(repo="owner/repo")
    payload = {"tasks": [{"id": f"task-{index}"} for index in range(2)]}
    with patch(
        "agentic_devtools.cli.ci.github_provider._gh_api",
        return_value=json.dumps(payload),
    ) as api:
        tasks, complete, reasons = provider._fetch_agent_task_pages(
            "owner/repo",
            "token",
            page_size=2,
            max_pages=1,
        )

    assert len(tasks) == 2
    assert complete is False
    assert reasons == ("page-limit",)
    api.assert_called_once()
    assert "per_page=2&page=1" in api.call_args.args[0]


@pytest.mark.parametrize(
    ("response", "expected_reason"),
    [
        ("not-json", "malformed-page-1"),
        (json.dumps({"unexpected": []}), "malformed-page-1"),
        (json.dumps({"tasks": [None]}), "malformed-records-page-1"),
    ],
)
def test_task_pages_preserve_malformed_page_provenance(response: str, expected_reason: str) -> None:
    """Malformed page payloads are incomplete with a stable page-scoped reason."""
    provider = GitHubActionsProvider(repo="owner/repo")
    with patch.object(provider, "_fetch_agent_task_page", return_value=response):
        tasks, complete, reasons = provider._fetch_agent_task_pages(
            "owner/repo",
            "token",
            page_size=2,
            max_pages=1,
        )

    assert tasks == []
    assert complete is False
    assert reasons == (expected_reason,)


def test_task_page_fetch_returns_complete_short_page() -> None:
    """A page shorter than the configured bound proves the bounded inventory complete."""
    provider = GitHubActionsProvider(repo="owner/repo")
    with patch.object(provider, "_fetch_agent_task_page", return_value=json.dumps({"tasks": [{"id": "task-1"}]})):
        tasks, complete, reasons = provider._fetch_agent_task_pages(
            "owner/repo",
            "token",
            page_size=2,
            max_pages=1,
        )

    assert tasks == [{"id": "task-1"}]
    assert complete is True
    assert reasons == ()


@pytest.mark.parametrize(("page_size", "max_pages"), [(0, 1), (1, 0)])
def test_task_page_fetch_rejects_nonpositive_bounds(page_size: int, max_pages: int) -> None:
    """REST inventory bounds are validated before any page request."""
    provider = GitHubActionsProvider(repo="owner/repo")
    with (
        patch.object(provider, "_fetch_agent_task_page") as fetch_page,
        pytest.raises(ValueError, match="page_size and max_pages must be positive"),
    ):
        provider._fetch_agent_task_pages("owner/repo", "token", page_size=page_size, max_pages=max_pages)
    fetch_page.assert_not_called()


@pytest.mark.parametrize(
    ("task", "expected"),
    [
        ({"head_ref": "refs/heads/feature"}, "feature"),
        ({"pull_request": {"head": {"ref": "refs/heads/pull-request"}}}, "pull-request"),
        (
            {
                "artifacts": [
                    {"type": "other", "data": {"ref": "ignored"}},
                    {"type": "branch", "data": {"head_ref": "refs/heads/artifact"}},
                ]
            },
            "artifact",
        ),
        ({"pull_request": "not-an-object"}, ""),
        ({"pull_request": {"head": []}}, ""),
        ({"pull_request": {"head": {"ref": None}}}, ""),
        (
            {"artifacts": [None, {"type": "branch", "data": []}, {"type": "branch", "data": {"head_ref": ""}}]},
            "",
        ),
    ],
)
def test_agent_task_branch_normalizes_supported_shapes(task: dict, expected: str) -> None:
    """Task correlation recognizes direct, pull-request, and artifact branch fields."""
    assert GitHubActionsProvider._agent_task_branch(task) == expected


def test_lifecycle_listing_rejects_invalid_pull_request_and_missing_repository(monkeypatch) -> None:
    """The REST task inventory requires a valid PR and repository identity."""
    with pytest.raises(ValueError, match="pr_number must be a positive integer"):
        GitHubActionsProvider(repo="owner/repo").list_pr_agent_task_lifecycles(0)

    monkeypatch.delenv("GITHUB_REPOSITORY", raising=False)
    with pytest.raises(ValueError, match="repository must be available"):
        GitHubActionsProvider(repo="").list_pr_agent_task_lifecycles(42)


def test_lifecycle_listing_skips_unrelated_records_and_audits_missing_task_ids() -> None:
    """Repository, PR, and branch correlation filters unrelated tasks before normalization."""
    provider = GitHubActionsProvider(repo="owner/repo")
    tasks = [
        {"id": "wrong-repo", "repository": {"full_name": "elsewhere/repo"}, "pullRequestNumber": 42},
        {"id": "wrong-pr", "repository": {"full_name": "owner/repo"}, "pullRequestNumber": 99},
        {"repository": "owner/repo", "pullRequestNumber": 42},
        {
            "id": "branch-match",
            "repository": "owner/repo",
            "pull_request": {"head": {"ref": "refs/heads/copilot/pr-42"}},
            "state": "completed",
        },
    ]
    with (
        patch.object(provider, "_fetch_agent_task_pages", return_value=(tasks, True, ())),
        patch.object(provider, "_fetch_agent_task_detail", return_value=json.dumps({"state": "completed"})),
    ):
        inventory = provider.list_pr_agent_task_lifecycles(42, head_branch="copilot/pr-42")

    assert [task.task_id for task in inventory.tasks] == ["branch-match"]
    assert inventory.complete is False
    assert inventory.incomplete_reasons == ("missing-task-id",)


def test_malformed_detail_and_session_records_are_retained_as_incomplete_evidence() -> None:
    """Malformed task details and session records do not erase listed task evidence."""
    provider = GitHubActionsProvider(repo="owner/repo")
    task = {"id": "task-1", "pullRequestNumber": 42, "state": "in_progress"}
    with (
        patch.object(provider, "_fetch_agent_task_pages", return_value=([task], True, ())),
        patch.object(
            provider,
            "_fetch_agent_task_detail",
            side_effect=[
                json.dumps(["not-an-object"]),
                json.dumps(
                    {
                        "startedAt": "2026-10-16T09:30:00Z",
                        "idleSince": "2026-10-16T09:45:00Z",
                        "sessions": [None, {}, {"state": "running"}],
                    }
                ),
                json.dumps({"sessions": {"bad": "shape"}}),
            ],
        ),
    ):
        invalid_detail = provider.list_pr_agent_task_lifecycles(42, head_branch="copilot/pr-42")
        provider.invalidate_agent_task_inventory(42)
        malformed_sessions = provider.list_pr_agent_task_lifecycles(42, head_branch="copilot/pr-42")
        provider.invalidate_agent_task_inventory(42)
        malformed_session_collection = provider.list_pr_agent_task_lifecycles(42, head_branch="copilot/pr-42")

    assert invalid_detail.complete is False
    assert invalid_detail.incomplete_reasons == ("task-detail:task-1",)
    assert malformed_sessions.complete is False
    assert malformed_sessions.incomplete_reasons == (
        "malformed-session:task-1",
        "missing-session-id:task-1",
    )
    assert malformed_sessions.tasks[0].started_at == "2026-10-16T09:30:00Z"
    assert malformed_sessions.tasks[0].idle_at == "2026-10-16T09:45:00Z"
    assert malformed_sessions.tasks[0].sessions[0].state == "running"
    assert malformed_session_collection.complete is False
    assert malformed_session_collection.incomplete_reasons == ("malformed-session:task-1",)


def test_unscoped_invalidation_clears_all_lifecycle_caches() -> None:
    """A global mutation invalidation clears every lifecycle-related cache."""
    provider = GitHubActionsProvider(repo="owner/repo")
    with (
        patch.object(provider, "_fetch_agent_task_pages", return_value=([], True, ())),
        patch.object(provider, "get_pr_token_login", return_value=""),
        patch.object(provider, "find_workflow_id_by_path", return_value="workflow-id"),
        patch.object(provider, "list_workflow_runs", return_value=[]),
    ):
        provider.list_pr_agent_task_lifecycles(42, head_branch="copilot/pr-42")
        provider.get_agent_task_first_observed_at(42, task_id="task-1")
        provider.list_correlated_cloud_writer_runs(42, head_branch="copilot/pr-42", tasks=())
        provider._pr_session_summaries_cache[42] = []

        provider.invalidate_agent_task_inventory()

    assert provider._agent_task_inventory_cache == {}
    assert provider._agent_task_first_observed_cache == {}
    assert provider._pr_session_summaries_cache == {}
    assert provider._cloud_writer_run_cache == {}


def test_pr_scoped_invalidation_preserves_other_pr_caches() -> None:
    """A PR-scoped mutation invalidates only cache entries for that PR."""
    provider = GitHubActionsProvider(repo="owner/repo")
    provider._agent_task_inventory_cache[(42, None, "branch-42", "sha-42")] = AgentTaskInventory(())
    provider._agent_task_inventory_cache[(43, None, "branch-43", "sha-43")] = AgentTaskInventory(())
    provider._agent_task_first_observed_cache[(42, "task-42", "", "branch-42", "sha-42")] = "timestamp"
    provider._agent_task_first_observed_cache[(43, "task-43", "", "branch-43", "sha-43")] = "timestamp"
    provider._pr_session_summaries_cache[42] = []
    provider._pr_session_summaries_cache[43] = []
    provider._cloud_writer_run_cache[(42, "branch-42", "sha-42", ())] = CloudWriterRunInventory()
    provider._cloud_writer_run_cache[(43, "branch-43", "sha-43", ())] = CloudWriterRunInventory()

    provider.invalidate_agent_task_inventory(42)

    assert list(provider._agent_task_inventory_cache) == [(43, None, "branch-43", "sha-43")]
    assert list(provider._agent_task_first_observed_cache) == [(43, "task-43", "", "branch-43", "sha-43")]
    assert provider._pr_session_summaries_cache == {43: []}
    assert list(provider._cloud_writer_run_cache) == [(43, "branch-43", "sha-43", ())]
