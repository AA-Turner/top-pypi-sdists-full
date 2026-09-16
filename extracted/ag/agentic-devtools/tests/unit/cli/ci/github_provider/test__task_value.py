"""Tests for _task_value."""

from agentic_devtools.cli.ci.github_provider import _task_value


def test_prefers_top_level_keys_in_order() -> None:
    """Returns the first matching top-level value."""
    assert _task_value({"first": "value", "metadata": {"first": "nested"}}, "first") == "value"


def test_reads_metadata_when_top_level_key_is_missing() -> None:
    """Falls back to a matching metadata value."""
    assert _task_value({"metadata": {"second": 2}}, "first", "second") == 2


def test_returns_none_without_a_matching_value_or_mapping_metadata() -> None:
    """Returns None when neither task nor metadata contains a requested key."""
    assert _task_value({"metadata": []}, "missing") is None
    assert _task_value({"metadata": {}}, "missing") is None
