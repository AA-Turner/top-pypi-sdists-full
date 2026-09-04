"""Tests for ``RotationPolicy``."""

import pytest

from agentic_devtools.orchestration.trio_config import RotationPolicy


def test_rotationpolicy_rejects_invalid_values() -> None:
    with pytest.raises(ValueError):
        RotationPolicy(require_distinct_models="yes")  # type: ignore[arg-type]
    with pytest.raises(ValueError):
        RotationPolicy(require_distinct_reviewer_families="yes")  # type: ignore[arg-type]
    with pytest.raises(ValueError):
        RotationPolicy(on_exhaustion="other")  # type: ignore[arg-type]
    with pytest.raises(ValueError):
        RotationPolicy(require_distinct_models=False)
