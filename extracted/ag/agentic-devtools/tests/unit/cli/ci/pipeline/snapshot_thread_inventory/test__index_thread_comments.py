"""Tests for indexing comments in validated review-thread state."""

from typing import cast

from agentic_devtools.cli.ci.pipeline.snapshot_thread_inventory import _index_thread_comments


def test_returns_empty_index_for_no_threads() -> None:
    assert _index_thread_comments({}, 1) == {}


def test_maps_all_comments_to_their_thread() -> None:
    states = {"thread-1": (False, (1, 2)), "thread-2": (True, (3,))}

    assert _index_thread_comments(states, 1) == {1: "thread-1", 2: "thread-1", 3: "thread-2"}


def test_keeps_repeated_comment_mapping_to_same_thread() -> None:
    assert _index_thread_comments({"thread-1": (False, (1, 1))}, 1) == {1: "thread-1"}


def test_returns_none_for_invalid_thread_state() -> None:
    invalid = cast(dict[str, tuple[bool, tuple[int, ...]]], {"thread-1": (False, ("invalid",))})
    assert _index_thread_comments(invalid, 1) is None


def test_returns_none_for_comment_mapped_to_multiple_threads() -> None:
    states: dict[str, tuple[bool, tuple[int, ...]]] = {
        "thread-1": (False, (1,)),
        "thread-2": (False, (1,)),
    }

    assert _index_thread_comments(states, 1) is None
