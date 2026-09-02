import pytest

from agentic_devtools.ai_providers.dispatch_policy import DispatchInputError, _canonical_repo


def test_canonical_repo_lowercases_valid_repo() -> None:
    assert _canonical_repo("Owner/Repo") == "owner/repo"


def test_canonical_repo_rejects_non_string() -> None:
    with pytest.raises(DispatchInputError):
        _canonical_repo(1)  # type: ignore[arg-type]
