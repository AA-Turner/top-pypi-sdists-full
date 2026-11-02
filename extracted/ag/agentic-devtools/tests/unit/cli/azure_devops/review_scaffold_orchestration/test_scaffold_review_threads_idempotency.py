"""Tests for scaffold_review_threads function."""

from itertools import count
from unittest.mock import MagicMock, patch

from agentic_devtools.cli.azure_devops.config import AzureDevOpsConfig
from agentic_devtools.cli.azure_devops.review_scaffold_orchestration import scaffold_review_threads
from agentic_devtools.cli.azure_devops.review_state import (
    FolderGroup,
    OverallSummary,
    ReviewState,
)

# ---------------------------------------------------------------------------
# Fixtures / helpers
# ---------------------------------------------------------------------------

_ORG = "https://dev.azure.com/testorg"
_PROJECT = "TestProject"
_REPO = "test-repo"
_REPO_ID = "repo-guid-abc"
_PR_ID = 25365


def _make_config(org=_ORG, project=_PROJECT, repo=_REPO) -> AzureDevOpsConfig:
    return AzureDevOpsConfig(organization=org, project=project, repository=repo)


def _make_post_response(thread_id: int, comment_id: int) -> MagicMock:
    """Build a mock requests.post response for thread creation."""
    resp = MagicMock()
    resp.raise_for_status = MagicMock()
    resp.json.return_value = {
        "id": thread_id,
        "comments": [{"id": comment_id}],
    }
    return resp


# ---------------------------------------------------------------------------
# Tests: scaffold_review_threads — idempotency
# ---------------------------------------------------------------------------


class TestScaffoldReviewThreadsIdempotency:
    """Tests for idempotency in scaffold_review_threads."""

    def test_returns_existing_state_when_already_scaffolded(self, tmp_path):
        """Returns existing ReviewState when complete review-state.json exists."""
        existing = ReviewState(
            prId=_PR_ID,
            repoId=_REPO_ID,
            repoName=_REPO,
            project=_PROJECT,
            organization=_ORG,
            latestIterationId=3,
            scaffoldedUtc="2026-01-01T00:00:00+00:00",
            overallSummary=OverallSummary(threadId=999, commentId=888),
            folders={"src": FolderGroup(files=["/src/app.ts"])},
        )

        with patch(
            "agentic_devtools.cli.azure_devops.review_scaffold_orchestration.load_review_state",
            return_value=existing,
        ):
            result = scaffold_review_threads(
                pull_request_id=_PR_ID,
                files=["/src/app.ts"],
                config=_make_config(),
                repo_id=_REPO_ID,
                repo_name=_REPO,
                latest_iteration_id=3,
                requests_module=MagicMock(),
                headers={},
            )

        assert result is existing
        assert result.overallSummary.threadId == 999

    def test_prints_skip_message_when_already_scaffolded(self, capsys, tmp_path):
        """Prints skip message when complete scaffolding already exists."""
        existing = ReviewState(
            prId=_PR_ID,
            repoId=_REPO_ID,
            repoName=_REPO,
            project=_PROJECT,
            organization=_ORG,
            latestIterationId=3,
            scaffoldedUtc="2026-01-01T00:00:00+00:00",
            overallSummary=OverallSummary(threadId=1, commentId=1),
            folders={"src": FolderGroup(files=["/src/app.ts"])},
        )

        with patch(
            "agentic_devtools.cli.azure_devops.review_scaffold_orchestration.load_review_state",
            return_value=existing,
        ):
            scaffold_review_threads(
                pull_request_id=_PR_ID,
                files=["/src/app.ts"],
                config=_make_config(),
                repo_id=_REPO_ID,
                repo_name=_REPO,
                latest_iteration_id=3,
                requests_module=MagicMock(),
                headers={},
            )

        out = capsys.readouterr().out
        assert f"Scaffolding already exists for PR {_PR_ID}" in out

    def test_rescaffolds_when_overall_thread_is_zero(self, capsys):
        """Re-scaffolds when existing state has overallSummary.threadId == 0."""
        incomplete = ReviewState(
            prId=_PR_ID,
            repoId=_REPO_ID,
            repoName=_REPO,
            project=_PROJECT,
            organization=_ORG,
            latestIterationId=3,
            scaffoldedUtc="2026-01-01T00:00:00+00:00",
            overallSummary=OverallSummary(threadId=0, commentId=0),
            folders={"src": FolderGroup(files=["/src/app.ts"])},
        )

        id_gen = count(1)

        def make_resp(*args, **kwargs):
            i = next(id_gen)
            return _make_post_response(i * 100, i * 100 + 1)

        requests_mock = MagicMock()
        requests_mock.post.side_effect = make_resp

        with patch(
            "agentic_devtools.cli.azure_devops.review_scaffold_orchestration.load_review_state",
            return_value=incomplete,
        ):
            with patch("agentic_devtools.cli.azure_devops.review_scaffold_fresh.save_review_state"):
                result = scaffold_review_threads(
                    pull_request_id=_PR_ID,
                    files=["/src/app.ts"],
                    config=_make_config(),
                    repo_id=_REPO_ID,
                    repo_name=_REPO,
                    latest_iteration_id=3,
                    requests_module=requests_mock,
                    headers={},
                )

        # Should have created new threads (not returned incomplete state)
        assert result.overallSummary.threadId != 0
        out = capsys.readouterr().out
        assert "Incomplete scaffolding detected" in out

    def test_returns_existing_when_folders_empty_but_overall_complete(self, capsys):
        """Returns existing state when overall is complete, even if folders are empty.

        With lightweight folder groups (no folder threads), empty folders dict
        is not considered incomplete — the overall threadId is the only completeness check.
        """
        existing = ReviewState(
            prId=_PR_ID,
            repoId=_REPO_ID,
            repoName=_REPO,
            project=_PROJECT,
            organization=_ORG,
            latestIterationId=3,
            scaffoldedUtc="2026-01-01T00:00:00+00:00",
            overallSummary=OverallSummary(threadId=500, commentId=501),
            folders={},
        )

        with patch(
            "agentic_devtools.cli.azure_devops.review_scaffold_orchestration.load_review_state",
            return_value=existing,
        ):
            result = scaffold_review_threads(
                pull_request_id=_PR_ID,
                files=["/src/app.ts"],
                config=_make_config(),
                repo_id=_REPO_ID,
                repo_name=_REPO,
                latest_iteration_id=3,
                requests_module=MagicMock(),
                headers={},
            )

        # Should return existing state (overall threadId is non-zero = complete)
        assert result is existing
        assert result.overallSummary.threadId == 500
        out = capsys.readouterr().out
        assert f"Scaffolding already exists for PR {_PR_ID}" in out
