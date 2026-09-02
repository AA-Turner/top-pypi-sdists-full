"""Tests for fires_t1 in derive_customization_disposition."""

from __future__ import annotations

from tests.scripts.derive_customization_disposition import derive, unit


def test_short_neutral_body_fires() -> None:
    """T1 is the instruction-file form: short, and scoped to nothing in particular."""
    assert derive.fires_t1(unit(body="Keep commits small.\n")) is True


def test_long_body_does_not_fire() -> None:
    """T1's threshold is 40 physical lines, not 40 non-blank lines."""
    assert derive.fires_t1(unit(body="line\n" * 40)) is False


def test_body_with_blanks_reaching_threshold_does_not_fire() -> None:
    """A body whose physical line count meets the threshold does not fire T1."""
    # 20 non-blank lines + 20 blank lines = 40 physical lines → should not fire.
    assert derive.fires_t1(unit(body=("line\n" + "\n") * 20)) is False


def test_body_with_blanks_below_threshold_fires() -> None:
    """Blank lines count toward the threshold; a 39-physical-line body still fires."""
    # 19 "line\n\n" pairs (38 physical lines) + 1 "line\n" = 39 physical lines → should fire.
    assert derive.fires_t1(unit(body=("line\n\n") * 19 + "line\n")) is True


def test_glob_disqualifies() -> None:
    """A body naming a glob belongs to T2, not T1."""
    assert derive.fires_t1(unit(body="Applies to `tests/**/*.py`.\n")) is False


def test_provider_disqualifies() -> None:
    """A body naming a provider is not provider-neutral."""
    assert derive.fires_t1(unit(body="Comment on the Jira issue.\n")) is False


def test_workflow_disqualifies() -> None:
    """A body naming a workflow is not workflow-neutral."""
    assert derive.fires_t1(unit(body="Advance the workflow.\n")) is False
