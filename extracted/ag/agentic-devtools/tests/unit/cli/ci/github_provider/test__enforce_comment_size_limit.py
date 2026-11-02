"""Tests for _enforce_comment_size_limit()."""

import pytest

from agentic_devtools.cli.ci import github_provider
from agentic_devtools.cli.ci.github_provider import _enforce_comment_size_limit, _fence


def _comments_body(fence_count: int) -> str:
    """Build a repair body holding *fence_count* actionable comment fences."""
    parts = ["@copilot"]
    for index in range(fence_count):
        parts += [
            "<!-- repair-comment-section -->",
            f"### Comment {index} - src/file_{index}.py",
            "",
            "Comment:",
            _fence(f"review feedback {index} " * 40),
            "",
        ]
    return "\n".join(parts)


class TestEnforceCommentSizeLimit:
    """Tests for bounding the repair-comment body under the GitHub size limit."""

    def test_returns_body_unchanged_when_within_limit(self) -> None:
        body = "small body"
        assert _enforce_comment_size_limit(body, hard_limit=1000) == body

    def test_trims_largest_fenced_block_when_over_limit(self) -> None:
        big = _fence("X" * 5000)
        small = _fence("y" * 10)
        body = f"intro\n{big}\nmiddle\n{small}\nend"
        result = _enforce_comment_size_limit(body, hard_limit=200)
        assert "[… embedded content trimmed to fit comment size limit …]" in result
        assert "X" * 5000 not in result
        # The small block (smaller than the marker) is left intact.
        assert "y" * 10 in result
        assert len(result) <= 200

    def test_last_resort_truncation_when_no_trimmable_blocks(self) -> None:
        body = "x" * 100  # no fenced blocks to trim
        # hard_limit must exceed the suffix length so the marker is still present in result.
        result = _enforce_comment_size_limit(body, hard_limit=80)
        # Last-resort hard truncation is applied instead of returning body unchanged.
        assert result != body
        assert "[… embedded content trimmed to fit comment size limit …]" in result
        assert len(result) <= 80

    def test_last_resort_truncation_preserves_details_close_tag(self) -> None:
        """The repair dispatch is flat, but other callers (e.g. conflict dispatch) still nest."""
        body = "x" * 100 + "\n</details>"  # over-limit, ends with a </details> tag
        # hard_limit must exceed the suffix (marker + </details>) length.
        result = _enforce_comment_size_limit(body, hard_limit=100)
        # The closing </details> tag is re-appended so the comment structure stays valid.
        assert result.rstrip().endswith("</details>")
        assert "[… embedded content trimmed to fit comment size limit …]" in result
        assert len(result) <= 100

    def test_last_resort_truncation_never_exceeds_hard_limit(self) -> None:
        body = "x" * 100  # no fenced blocks to trim
        # Pathologically small limit: even the marker suffix exceeds the limit.
        result = _enforce_comment_size_limit(body, hard_limit=10)
        assert len(result) <= 10

    def test_prefers_trimming_ci_logs_before_comment_body(self) -> None:
        """CI log fences are trimmed before actionable review-comment bodies."""
        comment_text = "COMMENT_BODY " + ("c" * 1_500)
        ci_text = "CI_LOG " + ("l" * 600)
        comment_fence = _fence(comment_text)
        ci_fence = _fence(ci_text)
        marker = _fence("[… embedded content trimmed to fit comment size limit …]")
        body = "\n".join(
            [
                "<!-- repair-comment-section -->",
                "### Comment 1 - foo.py",
                "",
                "Comment:",
                comment_fence,
                "",
                "### Failure 1 from checks / build (pull_request)",
                "",
                "**Failing step:** run checks",
                "",
                ci_fence,
            ]
        )
        hard_limit = len(body) - len(ci_fence) + len(marker)

        result = _enforce_comment_size_limit(body, hard_limit=hard_limit)

        assert comment_text in result
        assert ci_text not in result
        assert "[… embedded content trimmed to fit comment size limit …]" in result

    def test_ci_step_summary_starting_with_comment_does_not_reclassify_ci_logs(self) -> None:
        """A CI step label that looks like a comment heading must stay in CI priority 0."""
        comment_text = "COMMENT_BODY " + ("c" * 1_500)
        ci_text = "CI_LOG " + ("l" * 600)
        marker = _fence("[… embedded content trimmed to fit comment size limit …]")
        body = "\n".join(
            [
                "@copilot",
                "<!-- repair-comment-section -->",
                "### Comment 1 - foo.py",
                "",
                "Comment:",
                _fence(comment_text),
                "",
                "### Failure 1 from checks / build (pull_request)",
                "",
                "**Failing step:** Comment 1 - cleanup",
                "",
                _fence(ci_text),
            ]
        )
        hard_limit = len(body) - len(_fence(ci_text)) + len(marker)

        result = _enforce_comment_size_limit(body, hard_limit=hard_limit)

        assert comment_text in result
        assert ci_text not in result

    def test_hard_truncation_cuts_trailing_instructions_before_leading_comments(self) -> None:
        """Tail truncation keeps a prefix, so trailing Instructions prose is dropped first.

        Exercises the last-resort truncation on a hand-built body ordered
        comments -> Instructions. It does not itself guard ``_build_repair_comment``'s
        section ordering (covered by its own ordering tests), and it is not a universal
        invariant: a body whose comment blocks alone exceed the limit can still be cut.
        """
        comment_marker = "ACTIONABLE_COMMENT_BODY"
        instruction_marker = "INSTRUCTION_PROSE"
        body = "\n".join(
            [
                "@copilot",
                "<!-- repair-comment-section -->",
                "### Comment 1 - foo.py",
                "",
                f"{comment_marker} {'c' * 500}",
                "",
                "## Instructions",
                "",
                f"{instruction_marker} {'i' * 5_000}",
            ]
        )

        # No fenced blocks exist, so the priority-ordered trim loop cannot help and the
        # last-resort tail truncation runs.
        result = _enforce_comment_size_limit(body, hard_limit=300)

        assert comment_marker in result
        assert instruction_marker not in result
        assert len(result) <= 300

    def test_priority_scan_runs_per_trim_not_per_fence(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Regression guard for the O(fences^2 x body) blowup in the trim loop.

        The old implementation re-derived every fence's fence-stripped prefix once per
        fence per trim iteration, so a few hundred review comments took minutes. Ranking
        is now a single batched pass per trim, memoised while the non-fence gaps are
        unchanged. Replacing a fence with the (also fenced) marker leaves every gap
        untouched, so this fixture must rank exactly once no matter how many trims run:
        a per-fence loop would scan ~fence_count times per trim, and dropping the memo
        alone would scan once per trim (400 times here).
        """
        fence_count = 400
        body = _comments_body(fence_count)

        real_scan = github_provider._priorities_from_cleaned
        scans: list[int] = []

        def _counting_scan(cleaned: str, cum: list[int]) -> list[int]:
            scans.append(len(cum))
            return real_scan(cleaned, cum)

        monkeypatch.setattr(github_provider, "_priorities_from_cleaned", _counting_scan)

        result = _enforce_comment_size_limit(body, hard_limit=20_000)

        assert len(result) <= 20_000
        assert "[… embedded content trimmed to fit comment size limit …]" in result
        assert len(scans) == 1, "the memoised ranking must be computed exactly once for this body"
        assert scans[0] == fence_count, "the single scan must rank every fence, not just the trimmable ones"

    def test_untrimmable_quoted_heading_fence_still_shields_later_comment_fences(self) -> None:
        """Every fence must be fed to the priority pass, not just the trimmable ones.

        A fence shorter than the trim marker can never be trimmed, but it must still be
        stripped out of the prefixes the ranking is derived from. Here a sub-marker fence
        quotes a CI failure heading; if it leaked into the fence-stripped text, the
        following actionable comment fence would rank 0 (CI logs) instead of 2
        and — being the largest fence at that priority — would be destroyed before the
        real CI log fence.
        """
        quoted_heading_fence = _fence("### Failure 1 from build")
        marker = _fence("[… embedded content trimmed to fit comment size limit …]")
        assert len(quoted_heading_fence) < len(marker), "fixture fence must be too small to trim"

        comment_text = "COMMENT_BODY " + ("c" * 1_500)
        ci_text = "CI_LOG " + ("l" * 600)
        ci_fence = _fence(ci_text)
        # The comment fence is the larger of the two, so a misranking to priority 0 would
        # win the "largest fence first" tie-break against the real CI Failures fence.
        assert len(_fence(comment_text)) > len(ci_fence)

        body = "\n".join(
            [
                "@copilot",
                "<!-- repair-comment-section -->",
                "### Comment 1 - foo.py",
                "",
                "Comment:",
                quoted_heading_fence,
                "",
                "Comment:",
                _fence(comment_text),
                "",
                "### Failure 1 from checks / build (pull_request)",
                "",
                ci_fence,
            ]
        )
        hard_limit = len(body) - len(ci_fence) + len(marker)

        result = _enforce_comment_size_limit(body, hard_limit=hard_limit)

        assert comment_text in result
        assert ci_text not in result
        assert quoted_heading_fence in result

    def test_hard_truncation_never_leaves_a_split_html_comment_opener(self) -> None:
        """A cut inside an opener must not hide the section that follows it.

        The author section comes first in a repair dispatch, so an unterminated
        ``<!--`` there would swallow the whole Code Review Agent section that
        follows it in the rendered comment.
        """
        opener = "<!-- repair-section:author-comments -->"
        prefix = "@copilot\nauthor lead-in\n"
        body = prefix + opener + "\n" + ("tail prose\n" * 500)
        suffix_len = len("\n" + _fence("[… embedded content trimmed to fit comment size limit …]"))
        # Land the hard cut five characters into the opener.
        hard_limit = len(prefix) + 5 + suffix_len

        result = _enforce_comment_size_limit(body, hard_limit=hard_limit)

        assert "<!--" not in result
        assert result.startswith(prefix)
        assert len(result) <= hard_limit

    def test_hard_truncation_in_ordinary_prose_is_unchanged(self) -> None:
        opener = "<!-- repair-comment-section -->\n"
        body = "@copilot\n" + opener + ("p" * 5_000)
        suffix = "\n" + _fence("[… embedded content trimmed to fit comment size limit …]")
        hard_limit = 200

        result = _enforce_comment_size_limit(body, hard_limit=hard_limit)

        # The closed opener survives and the prose is cut mid-line, exactly as before.
        assert result == body[: hard_limit - len(suffix)] + suffix
        assert opener in result

    def test_hard_truncation_of_body_without_html_comments_is_unchanged(self) -> None:
        body = "z" * 5_000
        suffix = "\n" + _fence("[… embedded content trimmed to fit comment size limit …]")
        hard_limit = 200

        result = _enforce_comment_size_limit(body, hard_limit=hard_limit)

        assert result == body[: hard_limit - len(suffix)] + suffix
