"""Tests for _build_comment_thread_index."""

import pytest

from agentic_devtools.cli.ci.pipeline.snapshot_review_comments import _build_comment_thread_index


def test_indexes_known_and_resolved_comment_ids() -> None:
    """The index records each comment's thread and resolved membership."""
    thread_states = {
        "thread-a": (True, (101,)),
        "thread-b": (False, (102, -1)),
    }

    assert _build_comment_thread_index(thread_states) == (
        {101},
        {101, 102, -1},
        {101: "thread-a", 102: "thread-b", -1: "thread-b"},
    )


@pytest.mark.parametrize(
    "thread_states",
    [
        [],
        {None: (False, (101,))},
        {"": (False, (101,))},
        {"thread-a": []},
        {"thread-a": (False,)},
        {"thread-a": (1, (101,))},
        {"thread-a": (False, [101])},
        {"thread-a": (False, (True,))},
        {"thread-a": (False, ("101",))},
        {"thread-a": (False, (101,)), "thread-b": (True, (101,))},
    ],
)
def test_rejects_malformed_or_conflicting_thread_state(thread_states: object) -> None:
    """Malformed keys, state tuples, comment IDs, and duplicate mappings are unknown."""
    assert _build_comment_thread_index(thread_states) is None
