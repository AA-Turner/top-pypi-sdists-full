import pytest

from agentic_devtools.adapters.pull_request_threads import _split_github_repository


def test_returns_owner_and_repo() -> None:
    assert _split_github_repository("owner/repo") == ("owner", "repo")


@pytest.mark.parametrize("value", [None, "", "owner", "owner/repo/extra", "owner /repo", "owner/repo name"])
def test_rejects_invalid_repository_shape(value: object) -> None:
    with pytest.raises(ValueError, match="GitHub repository must be in owner/repo form"):
        _split_github_repository(value)
