"""Tests for _split_fence_gaps()."""

from agentic_devtools.cli.ci.github_provider import _FENCE_BLOCK_RE, _split_fence_gaps


def _spans(body: str) -> list[tuple[int, int]]:
    return [m.span() for m in _FENCE_BLOCK_RE.finditer(body)]


class TestSplitFenceGaps:
    """Tests for the fence-stripped prefix representation used by the batch priority pass."""

    def test_returns_empty_result_when_there_are_no_fences(self) -> None:
        assert _split_fence_gaps("plain body with no fences", []) == ("", [])

    def test_concatenates_only_the_non_fence_gaps(self) -> None:
        body = "A```\nx\n```B```\ny\n```C"
        cleaned, cum = _split_fence_gaps(body, _spans(body))
        assert cleaned == "AB"
        assert cum == [1, 2]

    def test_every_cleaned_prefix_matches_a_full_regex_sub(self) -> None:
        """``cleaned[: cum[i]]`` is exactly the value the reference implementation computes."""
        body = (
            "<details><summary>Comment 1 - a.py</summary>\n"
            "```diff\n@@ -1 +1 @@\n-a\n+b\n```\n"
            "Comment:\n```\n<details><summary>CI Failures</summary>\nquoted\n```\n"
            "trailing prose```\ninline fence\n```\n"
        )
        spans = _spans(body)
        assert len(spans) == 3
        cleaned, cum = _split_fence_gaps(body, spans)
        for (start, _end), prefix_len in zip(spans, cum, strict=True):
            assert cleaned[:prefix_len] == _FENCE_BLOCK_RE.sub("", body[:start])
