"""Tests for scaffold_review_threads function."""

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


class TestScaffoldReviewThreadsRecovery:
    """Tests for the recovery path when review-state.json is missing but PR has threads."""

    def test_returns_recovered_state_when_state_json_missing(self):
        """Returns recovered state from PR threads when state.json doesn't exist."""
        recovered = ReviewState(
            prId=_PR_ID,
            repoId=_REPO_ID,
            repoName=_REPO,
            project=_PROJECT,
            organization=_ORG,
            latestIterationId=3,
            scaffoldedUtc="2026-01-01T00:00:00+00:00",
            overallSummary=OverallSummary(threadId=500, commentId=501),
            folders={"src": FolderGroup(files=["/src/app.ts"])},
        )

        with (
            patch(
                "agentic_devtools.cli.azure_devops.review_scaffold_orchestration.load_review_state",
                side_effect=FileNotFoundError("No review-state.json"),
            ),
            patch(
                "agentic_devtools.cli.azure_devops.review_scaffold_orchestration._try_recover_state_from_pr_threads",
                return_value=recovered,
            ) as mock_recover,
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

        assert result is recovered
        mock_recover.assert_called_once()
