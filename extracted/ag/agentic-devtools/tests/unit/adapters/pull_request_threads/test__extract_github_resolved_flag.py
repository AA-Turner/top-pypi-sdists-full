import pytest

from agentic_devtools.adapters.pull_request_threads import (
    _extract_github_resolved_flag,
    _ProviderResponseError,
)


def test_returns_boolean_flag() -> None:
    assert _extract_github_resolved_flag({"isResolved": True}) is True


@pytest.mark.parametrize("payload", [None, [], {"isResolved": "false"}])
def test_rejects_non_boolean_provider_values(payload: object) -> None:
    with pytest.raises(_ProviderResponseError, match="malformed_response"):
        _extract_github_resolved_flag(payload)
