"""Tests for _split_into_comments and _chunk_oversized_sections."""

from agentic_devtools.cli.azure_devops.consolidated_review import (
    HARD_CAP_CHARS,
    SMART_CUTOFF_CHARS,
    _chunk_oversized_sections,
    _split_into_comments,
)


class TestChunkOversizedSections:
    """Tests for _chunk_oversized_sections."""

    def test_small_sections_unchanged(self):
        sections = ["short", "also short"]
        assert _chunk_oversized_sections(sections) == sections

    def test_empty_list(self):
        assert _chunk_oversized_sections([]) == []

    def test_section_at_exact_cap_is_unchanged(self):
        section = "x" * HARD_CAP_CHARS
        result = _chunk_oversized_sections([section])
        assert result == [section]

    def test_section_exceeding_cap_is_split(self):
        section = "y" * (HARD_CAP_CHARS + 1)
        result = _chunk_oversized_sections([section])
        assert len(result) == 2
        assert result[0] == "y" * HARD_CAP_CHARS
        assert result[1] == "y"

    def test_section_twice_cap_produces_two_chunks(self):
        section = "z" * (HARD_CAP_CHARS * 2)
        result = _chunk_oversized_sections([section])
        assert len(result) == 2
        assert all(len(chunk) == HARD_CAP_CHARS for chunk in result)

    def test_mixed_sections(self):
        small = "a" * 10
        big = "b" * (HARD_CAP_CHARS + 5)
        result = _chunk_oversized_sections([small, big])
        assert result[0] == small
        assert result[1] == "b" * HARD_CAP_CHARS
        assert result[2] == "b" * 5


class TestSplitIntoComments:
    """Tests for _split_into_comments."""

    _HEADLINE = "<!-- consolidated v2 -->\n## 🔍 Review"
    _PR_ID = 42
    _HASH = "abc123def456"

    def test_single_small_section_produces_one_comment(self):
        sections = ["small section"]
        comments = _split_into_comments(self._HEADLINE, sections, self._PR_ID, self._HASH)
        assert len(comments) == 1
        assert "small section" in comments[0]

    def test_no_sections_produces_root_only(self):
        comments = _split_into_comments(self._HEADLINE, [], self._PR_ID, self._HASH)
        assert len(comments) == 1
        assert self._HEADLINE in comments[0]

    def test_sections_within_soft_cutoff_stay_in_one_comment(self):
        # Two sections together well below SMART_CUTOFF_CHARS
        sections = ["a" * 1000, "b" * 1000]
        comments = _split_into_comments(self._HEADLINE, sections, self._PR_ID, self._HASH)
        assert len(comments) == 1

    def test_sections_beyond_soft_cutoff_overflow_to_continuation(self):
        # First section slightly above SMART_CUTOFF_CHARS; second overflows.
        sections = ["a" * (SMART_CUTOFF_CHARS + 100), "b" * 100]
        comments = _split_into_comments(self._HEADLINE, sections, self._PR_ID, self._HASH)
        assert len(comments) == 2
        assert "b" * 100 in comments[1]

    def test_continuation_carries_marker(self):
        sections = ["a" * (SMART_CUTOFF_CHARS + 100), "b" * 100]
        comments = _split_into_comments(self._HEADLINE, sections, self._PR_ID, self._HASH)
        assert "continuation" in comments[1]

    def test_oversized_single_section_is_split_across_comments(self):
        """A section larger than HARD_CAP_CHARS must never appear in one comment."""
        big_section = "X" * (HARD_CAP_CHARS + 1)
        comments = _split_into_comments(self._HEADLINE, [big_section], self._PR_ID, self._HASH)
        # Max overhead per comment = max(len(headline), len(cont_header)) + 3 separators.
        # With this _HEADLINE (36 chars) and a cont_header of ~100 chars, max overhead = 103.
        _MAX_OVERHEAD = 103
        for comment in comments:
            assert len(comment) <= HARD_CAP_CHARS + _MAX_OVERHEAD

    def test_no_comment_exceeds_hard_cap(self):
        """All comments must stay within HARD_CAP_CHARS (plus header overhead)."""
        # Multiple large sections to exercise chunking + continuation logic.
        sections = ["Y" * (HARD_CAP_CHARS // 2 + 1) for _ in range(6)]
        comments = _split_into_comments(self._HEADLINE, sections, self._PR_ID, self._HASH)
        # Max overhead per comment = max(len(headline), len(cont_header)) + 3 separators.
        # With this _HEADLINE (36 chars) and a cont_header of ~100 chars, max overhead = 103.
        _MAX_OVERHEAD = 103
        for comment in comments:
            assert len(comment) <= HARD_CAP_CHARS + _MAX_OVERHEAD
