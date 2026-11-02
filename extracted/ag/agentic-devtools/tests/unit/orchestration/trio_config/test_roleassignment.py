"""Tests for ``RoleAssignment``."""

import pytest

from agentic_devtools.orchestration.trio_config import RoleAssignment


def test_roleassignment_rejects_invalid_values() -> None:
    with pytest.raises(ValueError):
        RoleAssignment("tier-9", "main")  # type: ignore[arg-type]
    with pytest.raises(ValueError):
        RoleAssignment("tier-1", "")  # type: ignore[arg-type]
    assert RoleAssignment("tier-1", "main", ["main"]).fallback_models == ("main",)
    with pytest.raises(ValueError):
        RoleAssignment("tier-1", "main", "fallback")  # type: ignore[arg-type]
    with pytest.raises(ValueError):
        RoleAssignment("tier-1", "main", {"a", "b"})  # type: ignore[arg-type]
    with pytest.raises(ValueError):
        RoleAssignment("tier-1", "main", ("a", "a"))
    with pytest.raises(ValueError):
        RoleAssignment("tier-1", "main", ("a", 1))  # type: ignore[arg-type]
