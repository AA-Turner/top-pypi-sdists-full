import time
from unittest.mock import patch

import pytest

from agentic_devtools.ai_providers.copilot_discovery import _time_budget
from agentic_devtools.ai_providers.errors import ProviderError


def test_returns_the_step_timeout_when_the_overall_budget_is_larger() -> None:
    deadline = time.monotonic() + 30

    assert _time_budget(deadline, 5.0) == 5.0


def test_returns_the_remaining_budget_when_it_is_smaller() -> None:
    with patch("agentic_devtools.ai_providers.copilot_discovery.time.monotonic", return_value=100.0):
        assert _time_budget(101.0, 5.0) == pytest.approx(1.0)


def test_raises_when_the_overall_budget_is_exhausted() -> None:
    with pytest.raises(ProviderError, match="overall ACP discovery timeout"):
        _time_budget(time.monotonic() - 1, 5.0)
