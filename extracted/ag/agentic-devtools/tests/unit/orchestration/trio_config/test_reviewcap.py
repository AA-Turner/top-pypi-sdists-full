"""Tests for ``ReviewCap``."""

import pytest

from agentic_devtools.orchestration.trio_config import ReviewCap


def test_reviewcap_rejects_invalid_values() -> None:
    with pytest.raises(ValueError):
        ReviewCap(mode="other")  # type: ignore[arg-type]
    with pytest.raises(ValueError):
        ReviewCap(max_rounds=True)  # type: ignore[arg-type]
    with pytest.raises(ValueError, match="max_rounds must be an integer from 1 through 2"):
        ReviewCap(mode="heavyweight_checkpoint")
    assert ReviewCap(mode="heavyweight_checkpoint", max_rounds=2).max_rounds == 2
