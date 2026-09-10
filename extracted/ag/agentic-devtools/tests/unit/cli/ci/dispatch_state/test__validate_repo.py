import pytest

from agentic_devtools.cli.ci import dispatch_state as dispatch_state_module


def test_returns_lowercase_repo_name() -> None:
    assert dispatch_state_module._validate_repo("Repo.Name") == "repo.name"


def test_rejects_owner_repo_paths() -> None:
    with pytest.raises(ValueError, match="repo must be a repository name"):
        dispatch_state_module._validate_repo("owner/repo")
