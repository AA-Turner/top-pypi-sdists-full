"""Tests for _frontmatter_target_name in derive_customization_disposition."""

from __future__ import annotations

from tests.scripts.derive_customization_disposition import derive


def test_returns_unquoted_name() -> None:
    """An unquoted `name` is accepted when it matches the target slug pattern."""
    assert derive._frontmatter_target_name("name: ai-pr-loop-supervision-worker\n") == "ai-pr-loop-supervision-worker"


def test_returns_quoted_name() -> None:
    """A quoted `name` is normalized by removing wrapping quotes."""
    assert derive._frontmatter_target_name("name: 'ai-pr-loop-supervision-worker'\n") == "ai-pr-loop-supervision-worker"


def test_unmatched_quote_returns_none() -> None:
    """An unmatched quote is rejected instead of being stripped independently."""
    assert derive._frontmatter_target_name("name: 'ai-pr-loop-supervision-worker\n") is None


def test_mismatched_quotes_return_none() -> None:
    """Mismatched quote delimiters are rejected as malformed YAML."""
    assert derive._frontmatter_target_name("name: \"ai-pr-loop-supervision-worker'\n") is None


def test_empty_name_returns_none() -> None:
    """An explicitly empty `name` declaration is rejected."""
    assert derive._frontmatter_target_name("name:\n") is None


def test_comment_only_name_returns_none() -> None:
    """A comment-only `name` declaration is rejected."""
    assert derive._frontmatter_target_name("name: # no target\n") is None


def test_invalid_name_returns_none() -> None:
    """An invalid `name` is ignored so verification falls back safely."""
    assert derive._frontmatter_target_name("name: ai_pr_loop_supervision_worker\n") is None


def test_nested_name_is_ignored() -> None:
    """A nested metadata name must not override the top-level target name."""
    frontmatter = "metadata:\n  name: nested-target\n"
    assert derive._frontmatter_target_name(frontmatter) is None


def test_overlong_name_returns_none() -> None:
    """An overlength `name` is ignored instead of becoming a target identity."""
    overlong = "a" * (derive.TARGET_SLUG_MAX_LEN + 1)
    assert derive._frontmatter_target_name(f"name: {overlong}\n") is None
