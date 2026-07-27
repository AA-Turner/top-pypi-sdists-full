"""Tests for cross-token thinking suppression (no Rich dependency)."""

from sage.core.thinking_filter import ThinkingSuppressionFilter


def test_thinking_suppression_simple():
    f = ThinkingSuppressionFilter()
    assert f.feed("hello ") == "hello "
    assert f.feed("world") == "world"


def test_thinking_suppression_split_open_tag():
    f = ThinkingSuppressionFilter()
    assert f.feed("pre <thi") == "pre "
    assert f.feed("nking>secret</thinking>") == ""
    assert f.feed("after") == "after"


def test_thinking_suppression_remainder_same_feed_after_close():
    """Text after ``</thinking>`` in the same chunk must not be dropped."""
    f = ThinkingSuppressionFilter()
    assert f.feed("x<thin") == "x"
    assert f.feed("king>y</thinking>z") == "z"


def test_thinking_suppression_flush_tail():
    f = ThinkingSuppressionFilter()
    assert f.feed("visible") == "visible"
    assert f.flush_display_tail() == ""


def test_thinking_suppression_unclosed_thinking_dropped():
    f = ThinkingSuppressionFilter()
    assert f.feed("<thinking>hidden") == ""
    assert f.flush_display_tail() == ""


def test_dedupe_numbered_list_items():
    from sage.core.list_generator import dedupe_numbered_list_items

    text = """1. First item here
2. Second unique
3. First item here
4. Another
"""
    out = dedupe_numbered_list_items(text)
    assert out.count("First item here") == 1
    assert "Second unique" in out
    assert "Another" in out
