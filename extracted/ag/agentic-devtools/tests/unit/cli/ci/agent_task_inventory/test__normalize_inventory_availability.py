"""Tests for conservative explicit availability normalization."""

import pytest

from agentic_devtools.cli.ci.agent_task_inventory import _normalize_inventory_availability


def test_omitted_availability_preserves_legacy_inference() -> None:
    assert _normalize_inventory_availability(None, has_tasks=False) is None


@pytest.mark.parametrize(("has_tasks", "expected"), [(True, "partial"), (False, "unavailable")])
def test_invalid_availability_is_downgraded(has_tasks, expected) -> None:
    assert _normalize_inventory_availability("unknown", has_tasks=has_tasks) == expected
