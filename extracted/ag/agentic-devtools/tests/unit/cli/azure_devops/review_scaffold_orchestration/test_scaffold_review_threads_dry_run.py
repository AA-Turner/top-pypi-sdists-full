"""Tests for scaffold_review_threads function."""

from unittest.mock import MagicMock, patch

from agentic_devtools.cli.azure_devops.config import AzureDevOpsConfig
from agentic_devtools.cli.azure_devops.review_scaffold_orchestration import scaffold_review_threads

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


class TestScaffoldReviewThreadsDryRun:
    """Tests for dry-run mode in scaffold_review_threads."""

    def test_returns_none_in_dry_run(self):
        """Returns None in dry-run mode without making any API calls."""
        requests_mock = MagicMock()

        with patch(
            "agentic_devtools.cli.azure_devops.review_scaffold_orchestration.load_review_state",
            side_effect=FileNotFoundError,
        ):
            result = scaffold_review_threads(
                pull_request_id=_PR_ID,
                files=["/src/app.ts"],
                config=_make_config(),
                repo_id=_REPO_ID,
                repo_name=_REPO,
                latest_iteration_id=2,
                requests_module=requests_mock,
                headers={},
                dry_run=True,
            )

        assert result is None
        requests_mock.post.assert_not_called()

    def test_prints_dry_run_plan(self, capsys):
        """Prints the scaffolding plan in dry-run mode."""
        with patch(
            "agentic_devtools.cli.azure_devops.review_scaffold_orchestration.load_review_state",
            side_effect=FileNotFoundError,
        ):
            scaffold_review_threads(
                pull_request_id=_PR_ID,
                files=["/src/app.ts", "/utils/helpers.ts"],
                config=_make_config(),
                repo_id=_REPO_ID,
                repo_name=_REPO,
                latest_iteration_id=1,
                requests_module=MagicMock(),
                headers={},
                dry_run=True,
            )

        out = capsys.readouterr().out
        assert f"Scaffolding plan for PR {_PR_ID}" in out
        assert "Would create file summary thread for /src/app.ts" in out
        assert "Would create file summary thread for /utils/helpers.ts" in out
        assert "Would group files under folder: src" in out
        assert "Would group files under folder: utils" in out
        assert "Would create overall PR summary thread" in out
        assert "Would create Review Activity Log thread" in out
