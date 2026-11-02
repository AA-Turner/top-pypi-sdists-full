"""Tests for count_numbered_steps in derive_customization_disposition."""

from __future__ import annotations

from tests.scripts.derive_customization_disposition import derive


def test_counts_numbered_steps_outside_code_blocks() -> None:
    """T3 counts the procedure's steps, not numbering inside a sample."""
    body = "1. First.\n2. Second.\n\n```text\n1. Not a step.\n```\n"
    assert derive.count_numbered_steps(body) == 2


def test_prose_is_not_a_step() -> None:
    """A body with no numbering has no steps."""
    assert derive.count_numbered_steps("Just prose.\n") == 0
