"""Tests for SupervisorConfig construction and validation."""

from typing import Any, cast

import pytest

from agentic_devtools.cli.ci.supervisor import SupervisorConfig


@pytest.mark.parametrize(
    "field,value",
    [
        ("loop_stale_seconds", 0),
        ("task_stale_seconds", True),
        ("review_wait_seconds", -1),
    ],
)
def test_supervisorconfig_rejects_invalid_thresholds(field: str, value: object) -> None:
    with pytest.raises(ValueError, match=field):
        SupervisorConfig(**cast(dict[str, Any], {field: value}))
