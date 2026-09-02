"""Tests for _priorities_from_cleaned()."""

from agentic_devtools.cli.ci.github_provider import (
    _FENCE_BLOCK_RE,
    _priorities_from_cleaned,
    _split_fence_gaps,
)
from tests.unit.cli.ci.github_provider._fence_priority_oracle import _get_fence_trim_priority

# A comment body that literally embeds a structural heading. The fence-stripping guard
# must stop it from reclassifying the fences that follow it.
_QUOTED_HEADING_BODY = "For example:\n### Failure 1 from checks / build\n❌ some-check"

MIXED_BODY = "\n".join(
    [
        "@copilot please repair",
        "<!-- repair-comment-section -->",
        "### Comment 1 - src/example.py:12",
        "",
        "**File:** `src/### Failure 1 from checks / build.py`",
        "```diff",
        "@@ -1 +1 @@",
        "-old line",
        "+new line",
        "```",
        "Comment:",
        f"```\n{_QUOTED_HEADING_BODY}\n```",
        "",
        "<!-- repair-comment-section -->",
        "### Comment 2 - src/other.py",
        "",
        "Comment:",
        "```",
        "second actionable comment",
        "```",
        "",
        "### Failure 1 from checks / build",
        "",
        "❌ checks / build Comment: still failing",
        "```text",
        "condensed log output",
        "```",
        "prose that runs straight into a fence```",
        "mid-line fenced content",
        "```",
    ]
)


def _priority_of(body: str, fence_index: int) -> int:
    """Rank fence *fence_index* of *body* through the production batched pass."""
    spans = [m.span() for m in _FENCE_BLOCK_RE.finditer(body)]
    assert spans, "No fence block found in body"
    cleaned, cum = _split_fence_gaps(body, spans)
    return _priorities_from_cleaned(cleaned, cum)[fence_index]


class TestPrioritiesFromCleaned:
    """Tests for ranking every fence from the pre-computed fence-stripped prefixes."""

    def test_matches_the_single_fence_reference_implementation(self) -> None:
        """The batched pass must rank a realistic repair comment exactly like the reference.

        Exercises both priority levels plus both classification guards: a fenced comment
        body quoting ``### Failure 1 from checks / build``, and a CI check name containing
        ``Comment:``. It also covers a mid-line fence, whose prefix ends mid-line.
        """
        expected = [_get_fence_trim_priority(MIXED_BODY, m) for m in _FENCE_BLOCK_RE.finditer(MIXED_BODY)]
        assert len(expected) == 5, "fixture must exercise every priority level"
        assert set(expected) == {0, 2}

        spans = [m.span() for m in _FENCE_BLOCK_RE.finditer(MIXED_BODY)]
        cleaned, cum = _split_fence_gaps(MIXED_BODY, spans)

        assert _priorities_from_cleaned(cleaned, cum) == expected

    def test_returns_empty_list_when_there_are_no_fences(self) -> None:
        assert _priorities_from_cleaned("<!-- repair-comment-section -->\n### Comment 1 - a.py\n", []) == []

    def test_defaults_to_two_when_no_structural_markers_exist(self) -> None:
        cleaned = "just prose\nmore prose\n"
        assert _priorities_from_cleaned(cleaned, [len(cleaned)]) == [2]

    def test_ranks_each_prefix_from_its_own_trailing_section(self) -> None:
        """Only the trailing section heading ranks a prefix; body labels never do."""
        cleaned = (
            "### Failure 1 from checks / build\n"  # prefix 1 ends here
            "<!-- repair-comment-section -->\n"
            "### Comment 2 - a.py\n"
            "**File:** `a.py`\n"  # prefix 2 ends here
            "Comment:\n"  # prefix 3 ends here
        )
        cum = [
            cleaned.index("<!-- repair-comment-section -->"),
            cleaned.index("Comment:\n"),
            len(cleaned),
        ]
        assert _priorities_from_cleaned(cleaned, cum) == [0, 2, 2]

    def test_partial_final_line_can_complete_a_section_marker(self) -> None:
        """A mid-line fence anchors ``$`` at the prefix end, so a bare heading still counts."""
        cleaned = "prose\n### Failure 1 from checks / build"
        assert _priorities_from_cleaned(cleaned, [len(cleaned)]) == [0]

    def test_marker_only_completed_by_later_text_is_not_applied_early(self) -> None:
        """A heading that only matches once the *next* gap arrives must not leak backwards."""
        cleaned = "### Failure 1 from checks / build\n"
        # The first prefix stops before ``from``, which ``Failure \\d+ from`` requires.
        early = cleaned.index(" from")
        assert _priorities_from_cleaned(cleaned, [early, len(cleaned)]) == [2, 0]

    def test_marker_starting_at_the_final_line_is_not_applied_when_cut_short(self) -> None:
        """A marker starting exactly at ``line_start`` is re-tested, never inherited.

        The marker cursors skip anything starting at or after ``line_start`` (strict ``<``),
        so a prefix that cuts a real marker mid-way falls back to the default priority
        instead of adopting a heading its own text never completes.
        """
        cleaned = "### Failure 1 from checks / build\nmore prose\n"
        assert _priorities_from_cleaned(cleaned, [len("### Failure 1 fr")]) == [2]

    def test_incomplete_partial_line_is_ignored(self) -> None:
        """A section marker cut short by the prefix end never classifies the fence."""
        cleaned = "<!-- repair-comment-section -->\n### Comme"
        assert _priorities_from_cleaned(cleaned, [len(cleaned)]) == [2]


class TestPrioritiesFromCleanedFenceSemantics:
    """The documented 0/2 fence ranking, asserted on realistic repair-comment bodies.

    These previously targeted the single-fence reference implementation (now the test-tree
    oracle in ``_fence_priority_oracle.py``); they are pinned to the production batched pass
    so the shipped ranking rules stay covered by name.
    """

    def test_ci_failures_section_returns_zero(self) -> None:
        """A fence inside the CI failure section has priority 0."""
        body = "### Failure 1 from checks / build\n\n```\nsome log output\n```\n"
        assert _priority_of(body, 0) == 0

    def test_comment_section_returns_two(self) -> None:
        """A fence inside a non-Failure section has priority 2."""
        body = "<!-- repair-comment-section -->\n### Comment 1 - a.py\nComment:\n```\nThis needs fixing\n```\n"
        assert _priority_of(body, -1) == 2

    def test_section_heading_inside_comment_body_does_not_reclassify_later_fence(self) -> None:
        """A quoted '### Failure 1 from checks / build' must not reclassify later comment fences.

        Searching the raw prefix would find the structural-looking text embedded inside the
        completed fence; stripping completed fences first keeps the next fence at 2.
        """
        fake_ci_in_body = "Here is an example:\n### Failure 1 from checks / build\n❌ some-check"
        body = (
            "<!-- repair-comment-section -->\n"
            "### Comment 1 - a.py\n"
            "Comment:\n"
            f"```\n{fake_ci_in_body}\n```\n"
            "Comment:\n"
            "```\nsecond actionable comment\n```\n"
        )
        assert _priority_of(body, -1) == 2

    def test_section_like_text_in_comment_metadata_stays_at_comment_priority(self) -> None:
        """A section-looking string in metadata must not reclassify the comment fence."""
        body = (
            "<!-- repair-comment-section -->\n"
            "### Comment 1 - a.py\n"
            "**File:** `src/### Failure 1 from checks / build.py`\n"
            "Comment:\n"
            "```\nactionable feedback\n```\n"
        )
        assert _priority_of(body, -1) == 2

    def test_ci_section_label_like_text_does_not_upgrade_ci_log_to_comment_priority(self) -> None:
        """CI check names containing 'Comment:' must not reclassify CI log fences."""
        body = (
            "### Failure 1 from checks / build\n"
            "❌ some check name Comment: still failing\n"
            "```text\nci log output\n```\n"
        )
        assert _priority_of(body, -1) == 0
