"""Tests for evaluator lock ownership error handling."""

from unittest.mock import Mock

import pytest

from agentic_devtools.cli.ci.evaluator.critique_actions import _lock_ownership_error
from agentic_devtools.cli.shared.retry import ProviderRateLimitError
from tests.unit.cli.ci.evaluator.critique_actions._support import _make_snapshot


@pytest.mark.parametrize(
    "guard",
    [
        None,
        Mock(return_value=True),
        Mock(return_value=False),
        Mock(side_effect=RuntimeError("lock lookup failed")),
        Mock(side_effect=ProviderRateLimitError(is_rate_limit=False)),
    ],
)
def test_returns_error_only_when_guard_does_not_confirm_ownership(guard: Mock | None) -> None:
    result = _lock_ownership_error(_make_snapshot(), 1, guard)

    assert (result is None) is (guard is None or guard.return_value is True)
    if result is not None:
        assert result.success is False
        assert result.error_details == "Evaluator lock ownership changed before critique mutation"


def test_propagates_rate_limit_from_ownership_guard() -> None:
    guard = Mock(side_effect=ProviderRateLimitError(is_rate_limit=True))

    with pytest.raises(ProviderRateLimitError):
        _lock_ownership_error(_make_snapshot(), 1, guard)
