"""Tests for GitHubActionsProvider._clean_sdk_commit_message static method.

After the squash-message refactor this helper validates the **title only**:
it strips fences and a ``commit message:`` prefix, strips a leading
Conventional-Commit ``type(scope):`` wrapper when present, rejects empty input
and conversational openers, and **clips** (never discards) an over-long title.
"""

import pytest

from agentic_devtools.cli.ci.github_provider import GitHubActionsProvider

_clean = GitHubActionsProvider._clean_sdk_commit_message


class TestCleanSdkCommitMessage:
    """Tests for the static title cleaning/clipping helper."""

    def test_empty_string_returns_none(self) -> None:
        assert _clean("") is None

    def test_whitespace_only_returns_none(self) -> None:
        assert _clean("   \n  ") is None

    def test_plain_title_returned_unchanged(self) -> None:
        # No type/scope prefix is required — the title is returned verbatim.
        assert _clean("add squash feature") == "add squash feature"

    def test_title_with_type_prefix_is_stripped(self) -> None:
        assert _clean("feat: add new thing") == "add new thing"

    def test_title_with_type_scope_and_breaking_marker_is_stripped(self) -> None:
        assert _clean("fix(PROJECT-1234)!: rework api") == "rework api"

    def test_title_with_unknown_type_is_not_stripped(self) -> None:
        assert _clean("feature: add new thing") == "feature: add new thing"

    def test_first_line_taken_as_title(self) -> None:
        assert _clean("add feature\n\n- detail one\n- detail two") == "add feature"

    # ── Markdown fence stripping ─────────────────────────────────────────────

    def test_fenced_title_strips_fences(self) -> None:
        assert _clean("```\nadd feature\n```") == "add feature"

    def test_fenced_title_with_language_strips_fences(self) -> None:
        assert _clean("```text\nadd feature\n```") == "add feature"

    def test_incomplete_fence_returned_as_is(self) -> None:
        # A single "```add feature" line is not a complete fence block; no format
        # validation rejects it now, so it is returned as the title verbatim.
        assert _clean("```add feature") == "```add feature"

    # ── "commit message:" prefix stripping ──────────────────────────────────

    def test_commit_message_prefix_stripped(self) -> None:
        assert _clean("commit message: add feature") == "add feature"

    def test_commit_message_prefix_case_insensitive(self) -> None:
        assert _clean("Commit Message: patch null dereference") == "patch null dereference"

    def test_commit_message_prefix_leaves_only_whitespace_returns_none(self) -> None:
        assert _clean("commit message:   ") is None

    # ── Conversational opener rejection ─────────────────────────────────────

    @pytest.mark.parametrize(
        "opener",
        [
            "Here is your commit message: feat: add",
            "Here's the message: fix: patch",
            "I'll generate that: chore: squash",
            "I've created: docs: update",
            "I would suggest: perf: improve",
            "Sure, here it is: feat: done",
            "Below is the message: chore: update",
            "Certainly add the feature here",
            "The following commit message covers: feat: add",
            "This commit adds: feat: new",
        ],
    )
    def test_conversational_opener_returns_none(self, opener: str) -> None:
        assert _clean(opener) is None

    # ── Title length cap: CLIP, do not discard ───────────────────────────────

    def test_title_exactly_100_chars_unchanged(self) -> None:
        title = "x" * 100
        assert _clean(title) == title

    def test_title_over_100_chars_is_clipped_not_discarded(self) -> None:
        title = "x" * 135
        result = _clean(title)
        assert result is not None
        assert len(result) <= 100
        assert result == "x" * 100

    def test_clip_strips_trailing_whitespace(self) -> None:
        # Char 100 lands on a space; clipping then rstrips it.
        title = ("y" * 99) + "   tail"
        result = _clean(title)
        assert result == "y" * 99

    def test_custom_max_length_clips(self) -> None:
        result = _clean("abcdefghijklmnopqrstuvwxyz", max_length=10)
        assert result == "abcdefghij"

    def test_zero_max_length_returns_none(self) -> None:
        assert _clean("title", max_length=0) is None
