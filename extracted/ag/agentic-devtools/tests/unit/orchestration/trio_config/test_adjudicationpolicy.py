"""Tests for ``AdjudicationPolicy``."""

import pytest

from agentic_devtools.orchestration.trio_config import AdjudicationPolicy


def test_adjudicationpolicy_rejects_invalid_values() -> None:
    with pytest.raises(ValueError):
        AdjudicationPolicy(True, "yes", True)  # type: ignore[arg-type]
