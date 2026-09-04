"""Tests for ``AdjudicationResult``."""

import pytest

from agentic_devtools.orchestration.trio_config import AdjudicationResult


def test_adjudicationresult_rejects_non_point_verdict_values() -> None:
    with pytest.raises(ValueError):
        AdjudicationResult((object(),))  # type: ignore[arg-type]
