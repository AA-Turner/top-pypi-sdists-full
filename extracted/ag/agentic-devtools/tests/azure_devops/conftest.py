"""
Shared fixtures for Azure DevOps tests.
"""

from unittest.mock import patch

import pytest

from agentic_devtools import state


@pytest.fixture(autouse=True)
def mock_git_remote_detection(request, monkeypatch):
    """
    Auto-mock git remote detection for all Azure DevOps tests except
    tests in TestRepositoryDetection / TestGetAzureDevOpsContextFromGitRemote
    classes which specifically test those functions.

    This prevents the git remote detection from interfering with test mocks
    by making it always return None (which causes fallback to defaults).
    """
    # Skip this fixture for tests that specifically test git remote detection
    skip_classes = ("TestRepositoryDetection", "TestGetAzureDevOpsContextFromGitRemote")
    if any(cls in request.node.nodeid for cls in skip_classes):
        yield
        return

    from agentic_devtools.cli.azure_devops import config

    monkeypatch.setattr(config, "get_repository_name_from_git_remote", lambda: None)
    monkeypatch.setattr(config, "get_azure_devops_context_from_git_remote", lambda: None)
    yield


@pytest.fixture(autouse=True)
def _mock_resolve_pr_body_legacy(request):
    """Mock resolve_pr_body so create_pull_request tests use state description.

    This preserves the existing test semantics where description comes from
    state. Only applies to tests that exercise create_pull_request.
    """
    skip_classes = ("TestCreatePullRequestActualCall", "TestCreatePullRequest")
    if not any(cls in request.node.nodeid for cls in skip_classes):
        yield
        return

    with patch("agentic_devtools.cli.pr_template.resolve_pr_body") as mock:

        def _from_state():
            return state.get_value("description") or ""

        mock.side_effect = _from_state
        yield mock


@pytest.fixture(autouse=True)
def _mock_generate_v2_review_artifacts_legacy():
    """Prevent the additive v2 artifact generation from running real I/O.

    ``setup_pull_request_review`` calls ``generate_v2_review_artifacts`` with a
    ``MagicMock`` ``prompts_dir`` in these legacy tests. ``Path(MagicMock())``
    resolves to a junk path rather than raising, so the real function would
    create stray ``MagicMock/`` directories and perform real disk/git I/O.
    Mocking it keeps these tests hermetic.
    """
    with patch("agentic_devtools.cli.azure_devops.pr_review_artifacts.generate_v2_review_artifacts"):
        yield
