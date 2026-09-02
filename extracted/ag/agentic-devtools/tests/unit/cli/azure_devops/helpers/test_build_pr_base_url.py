"""Tests for build_pr_base_url (now defined in helpers.py)."""

from agentic_devtools.cli.azure_devops.config import AzureDevOpsConfig
from agentic_devtools.cli.azure_devops.helpers import build_pr_base_url

_ORG = "https://dev.azure.com/testorg"
_PROJECT = "TestProject"
_REPO = "test-repo"


def _make_config(org=_ORG, project=_PROJECT, repo=_REPO) -> AzureDevOpsConfig:
    return AzureDevOpsConfig(organization=org, project=project, repository=repo)


class TestBuildPrBaseUrl:
    """Tests for build_pr_base_url defined in helpers.py."""

    def test_builds_correct_url(self):
        """Builds the expected PR web URL."""
        config = _make_config()
        result = build_pr_base_url(config, 42)
        assert result == f"{_ORG}/{_PROJECT}/_git/{_REPO}/pullrequest/42"

    def test_strips_trailing_slash_from_org(self):
        """Handles trailing slash in organization URL."""
        config = _make_config(org="https://dev.azure.com/testorg/")
        result = build_pr_base_url(config, 1)
        assert result == f"https://dev.azure.com/testorg/{_PROJECT}/_git/{_REPO}/pullrequest/1"

    def test_normalizes_short_org_name(self):
        """Normalizes a short org name to a full Azure DevOps URL."""
        config = _make_config(org="myorg")
        result = build_pr_base_url(config, 7)
        assert result == f"https://dev.azure.com/myorg/{_PROJECT}/_git/{_REPO}/pullrequest/7"

    def test_url_encodes_project_with_spaces(self):
        """URL-encodes project names containing spaces."""
        config = _make_config(project="My Project")
        result = build_pr_base_url(config, 1)
        assert result == f"{_ORG}/My%20Project/_git/{_REPO}/pullrequest/1"

    def test_url_encodes_repo_with_spaces(self):
        """URL-encodes repository names containing spaces."""
        config = _make_config(repo="my repo")
        result = build_pr_base_url(config, 1)
        assert result == f"{_ORG}/{_PROJECT}/_git/my%20repo/pullrequest/1"

    def test_backward_compat_alias_in_review_scaffold(self):
        """The _build_pr_base_url alias in review_scaffold still resolves correctly."""
        from agentic_devtools.cli.azure_devops.review_scaffold import _build_pr_base_url

        config = _make_config()
        assert _build_pr_base_url(config, 99) == build_pr_base_url(config, 99)
