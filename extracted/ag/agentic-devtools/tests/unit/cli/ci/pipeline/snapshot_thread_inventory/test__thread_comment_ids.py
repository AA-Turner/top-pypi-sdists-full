"""Tests for validating one provider thread-state entry."""

from agentic_devtools.cli.ci.pipeline.snapshot_thread_inventory import _thread_comment_ids


def test_rejects_non_string_thread_key() -> None:
    assert _thread_comment_ids(None, (False, (1,)), 1) == (False, None)


def test_rejects_empty_thread_key() -> None:
    assert _thread_comment_ids("", (False, (1,)), 1) == (False, None)


def test_rejects_non_tuple_or_wrong_length_state() -> None:
    assert _thread_comment_ids("thread", [False, (1,)], 1) == (False, None)
    assert _thread_comment_ids("thread", (False,), 1) == (False, None)


def test_rejects_non_boolean_resolved_flag() -> None:
    assert _thread_comment_ids("thread", (1, (1,)), 1) == (False, None)


def test_rejects_non_tuple_comment_ids() -> None:
    assert _thread_comment_ids("thread", (False, [1]), 1) == (False, None)


def test_rejects_non_integer_comment_id() -> None:
    assert _thread_comment_ids("thread", (False, (1, "invalid")), 1) == (False, None)


def test_returns_valid_comment_ids() -> None:
    assert _thread_comment_ids("thread", (False, (1, 2)), 1) == (True, (1, 2))
