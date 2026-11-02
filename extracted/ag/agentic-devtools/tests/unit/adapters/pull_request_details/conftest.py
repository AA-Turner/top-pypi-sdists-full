import pytest

from agentic_devtools.cli.ci.credential_roles import DEFAULT_CLASSIC_REPO_WORKFLOW_PAT


@pytest.fixture(autouse=True)
def configured_github_token(monkeypatch) -> None:
    monkeypatch.setenv(DEFAULT_CLASSIC_REPO_WORKFLOW_PAT, "test-workflow-token")
