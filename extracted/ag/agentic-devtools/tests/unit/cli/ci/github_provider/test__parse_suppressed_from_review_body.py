"""Tests for _parse_suppressed_from_review_body() in the GitHub provider."""

import logging

from agentic_devtools.cli.ci.github_provider import _parse_suppressed_from_review_body


class TestParseSuppressedFromReviewBody:
    """Tests for _parse_suppressed_from_review_body()."""

    def test_returns_empty_list_for_empty_body(self) -> None:
        assert _parse_suppressed_from_review_body("") == []

    def test_returns_empty_list_when_no_details_block(self) -> None:
        body = "Some review text without any suppressed comments."
        assert _parse_suppressed_from_review_body(body) == []

    def test_returns_empty_list_for_empty_details_block(self) -> None:
        body = "<details>\n<summary>Comments suppressed due to low confidence (0)</summary>\n\n</details>"
        assert _parse_suppressed_from_review_body(body) == []

    def test_parses_bold_file_path_entry(self) -> None:
        body = (
            "<details>\n"
            "<summary>Comments suppressed due to low confidence (1)</summary>\n"
            "\n"
            "**src/foo.py**: Fix the null check here\n"
            "\n"
            "</details>"
        )
        result = _parse_suppressed_from_review_body(body)
        assert len(result) == 1
        assert result[0].path == "src/foo.py"
        assert result[0].body == "Fix the null check here"
        assert result[0].is_suppressed is True
        assert result[0].id < 0
        assert result[0].html_url == ""

    def test_parses_code_formatted_file_path(self) -> None:
        body = (
            "<details>\n"
            "<summary>Comments suppressed due to low confidence (1)</summary>\n"
            "\n"
            "`src/bar.py`: Use a helper function\n"
            "\n"
            "</details>"
        )
        result = _parse_suppressed_from_review_body(body)
        assert len(result) == 1
        assert result[0].path == "src/bar.py"
        assert result[0].body == "Use a helper function"
        assert result[0].is_suppressed is True

    def test_parses_bold_code_formatted_file_path(self) -> None:
        body = (
            "<details>\n"
            "<summary>Comments suppressed due to low confidence (1)</summary>\n"
            "\n"
            "**`src/baz.py`**: Add error handling\n"
            "\n"
            "</details>"
        )
        result = _parse_suppressed_from_review_body(body)
        assert len(result) == 1
        assert result[0].path == "src/baz.py"
        assert result[0].body == "Add error handling"

    def test_parses_multiple_entries(self) -> None:
        body = (
            "<details>\n"
            "<summary>Comments suppressed due to low confidence (3)</summary>\n"
            "\n"
            "**src/foo.py**: Fix null check\n"
            "**src/bar.py**: Add error handling\n"
            "**src/baz.py**: Use helper\n"
            "\n"
            "</details>"
        )
        result = _parse_suppressed_from_review_body(body)
        assert len(result) == 3
        assert result[0].path == "src/foo.py"
        assert result[1].path == "src/bar.py"
        assert result[2].path == "src/baz.py"

    def test_parses_entries_separated_by_blank_lines(self) -> None:
        """Blank lines between entries (common Markdown layout) are handled correctly."""
        body = (
            "<details>\n"
            "<summary>Comments suppressed due to low confidence (2)</summary>\n"
            "\n"
            "**src/foo.py**: Fix null check\n"
            "\n"
            "**src/bar.py**: Add error handling\n"
            "\n"
            "</details>"
        )
        result = _parse_suppressed_from_review_body(body)
        assert len(result) == 2
        assert result[0].path == "src/foo.py"
        assert result[0].body == "Fix null check"
        assert result[1].path == "src/bar.py"
        assert result[1].body == "Add error handling"

    def test_parses_multiline_body_with_blank_line_before_next_entry(self) -> None:
        """Multi-line body followed by a blank line before the next header is parsed correctly."""
        body = (
            "<details>\n"
            "<summary>Comments suppressed due to low confidence (2)</summary>\n"
            "\n"
            "**src/foo.py**: This is a longer explanation\n"
            "that spans multiple lines.\n"
            "\n"
            "**src/bar.py**: Another finding\n"
            "\n"
            "</details>"
        )
        result = _parse_suppressed_from_review_body(body)
        assert len(result) == 2
        assert result[0].path == "src/foo.py"
        assert "longer explanation" in result[0].body
        assert "spans multiple lines" in result[0].body
        assert result[1].path == "src/bar.py"
        assert result[1].body == "Another finding"

    def test_assigns_unique_negative_sentinel_ids(self) -> None:
        body = (
            "<details>\n"
            "<summary>Comments suppressed due to low confidence (2)</summary>\n"
            "\n"
            "**a.py**: Comment A\n"
            "**b.py**: Comment B\n"
            "\n"
            "</details>"
        )
        result = _parse_suppressed_from_review_body(body)
        assert len(result) == 2
        assert result[0].id == -1
        assert result[1].id == -2
        assert result[0].id != result[1].id

    def test_all_entries_have_is_suppressed_true(self) -> None:
        body = (
            "<details>\n"
            "<summary>Comments suppressed due to low confidence (1)</summary>\n"
            "\n"
            "**x.py**: Some comment\n"
            "\n"
            "</details>"
        )
        result = _parse_suppressed_from_review_body(body)
        assert all(c.is_suppressed for c in result)

    def test_source_review_id_applied_to_recovered_entries(self) -> None:
        body = (
            "<details>\n"
            "<summary>Comments suppressed due to low confidence (1)</summary>\n"
            "\n"
            "**x.py**: Some comment\n"
            "\n"
            "</details>"
        )
        result = _parse_suppressed_from_review_body(body, source_review_id=456)
        assert result[0].source_review_id == 456

    def test_fallback_to_unknown_file_when_no_path(self) -> None:
        """Lines without a file path pattern use (unknown file) marker."""
        body = (
            "<details>\n"
            "<summary>Comments suppressed due to low confidence (1)</summary>\n"
            "\n"
            "Some standalone comment without a file path\n"
            "\n"
            "</details>"
        )
        result = _parse_suppressed_from_review_body(body)
        assert len(result) == 1
        assert result[0].path == "(unknown file)"
        assert "standalone comment" in result[0].body

    def test_case_insensitive_summary_match(self) -> None:
        body = (
            "<details>\n"
            "<summary>Comments Suppressed Due To Low Confidence (1)</summary>\n"
            "\n"
            "**f.py**: Comment\n"
            "\n"
            "</details>"
        )
        result = _parse_suppressed_from_review_body(body)
        assert len(result) == 1

    def test_preserves_surrounding_review_text(self) -> None:
        """Parser only extracts from the <details> block, ignoring surrounding text."""
        body = (
            "## Review Summary\n\n"
            "This PR has issues.\n\n"
            "<details>\n"
            "<summary>Comments suppressed due to low confidence (1)</summary>\n"
            "\n"
            "**src/x.py**: Fix this\n"
            "\n"
            "</details>\n\n"
            "## Conclusion\n\nPlease address the above."
        )
        result = _parse_suppressed_from_review_body(body)
        assert len(result) == 1
        assert result[0].path == "src/x.py"

    def test_multiline_body_text(self) -> None:
        body = (
            "<details>\n"
            "<summary>Comments suppressed due to low confidence (1)</summary>\n"
            "\n"
            "**src/foo.py**: First line\n"
            "continuation of the comment\n"
            "\n"
            "</details>"
        )
        result = _parse_suppressed_from_review_body(body)
        assert len(result) == 1
        assert "First line" in result[0].body

    def test_structured_entry_with_blank_path_uses_unknown_file(self) -> None:
        body = (
            "<details>\n"
            "<summary>Comments suppressed due to low confidence (1)</summary>\n"
            "\n"
            "**   **: Body text\n"
            "\n"
            "</details>"
        )
        result = _parse_suppressed_from_review_body(body)
        assert len(result) == 1
        assert result[0].path == "(unknown file)"
        assert result[0].body == "Body text"

    def test_structured_entry_with_empty_body_falls_back_to_raw_line(self) -> None:
        body = (
            "<details>\n<summary>Comments suppressed due to low confidence (1)</summary>\n\n**foo.py**:\n\n</details>"
        )
        result = _parse_suppressed_from_review_body(body)
        assert len(result) == 1
        assert result[0].path == "(unknown file)"
        assert result[0].body == "**foo.py**:"

    def test_fallback_ignores_blank_lines(self) -> None:
        body = (
            "<details>\n"
            "<summary>Comments suppressed due to low confidence (1)</summary>\n"
            "\n"
            "first fallback comment\n"
            "\n"
            "second fallback comment\n"
            "\n"
            "</details>"
        )
        result = _parse_suppressed_from_review_body(body)
        assert len(result) == 2
        assert result[0].path == "(unknown file)"
        assert result[0].body == "first fallback comment"
        assert result[1].path == "(unknown file)"
        assert result[1].body == "second fallback comment"


class TestParseSuppressedFromReviewBodyNewCcrFormat:
    """New CCR private-preview format: suppressed comments live under a
    ``### Comments suppressed due to low confidence (N)`` heading inside a
    ``<details><summary>Review details</summary>`` block."""

    def _new_format_body(self, entries_md: str, count: int) -> str:
        return (
            "### 🟡 Not ready to approve\n\n"
            "Some prose summary.\n\n"
            "<details>\n<summary>Review details</summary>\n\n"
            f"### Comments suppressed due to low confidence ({count})\n\n"
            f"{entries_md}\n"
            "- **Files reviewed:** 3/3 changed files\n"
            "- **Comments generated:** 0 new\n"
            "- **Review effort level:** Low\n"
            "</details>"
        )

    def test_recovers_single_new_format_entry(self) -> None:
        body = self._new_format_body("**src/app.py:42**\n* Guard against None here.\n", count=1)
        result = _parse_suppressed_from_review_body(body)
        assert len(result) == 1
        assert result[0].path == "src/app.py:42"
        assert result[0].body == "Guard against None here."
        assert result[0].is_suppressed is True
        assert result[0].id == -1
        assert result[0].html_url == ""

    def test_recovers_multiple_new_format_entries_with_sentinel_ids(self) -> None:
        entries = "**a/b.py:10**\n* First finding.\n\n**c/d.py:20**\n* Second finding.\n"
        body = self._new_format_body(entries, count=2)
        result = _parse_suppressed_from_review_body(body)
        assert [(c.path, c.body) for c in result] == [
            ("a/b.py:10", "First finding."),
            ("c/d.py:20", "Second finding."),
        ]
        assert [c.id for c in result] == [-1, -2]
        assert all(c.is_suppressed for c in result)

    def test_metrics_footer_not_recovered_as_entry(self) -> None:
        """The metrics footer lines must never become suppressed comments."""
        body = self._new_format_body("**tasks.md:5**\n* Ordering looks off.\n", count=1)
        result = _parse_suppressed_from_review_body(body)
        paths = [c.path for c in result]
        assert all("Files reviewed" not in p and "Comments generated" not in p for p in paths)
        assert len(result) == 1

    def test_new_format_entry_with_code_block(self) -> None:
        entries = "**tasks.md:49**\n* The ordering looks off:\n```\n- [ ] T001 thing\n- [ ] T002 other\n```\n"
        body = self._new_format_body(entries, count=1)
        result = _parse_suppressed_from_review_body(body)
        assert len(result) == 1
        assert result[0].path == "tasks.md:49"
        assert "ordering looks off" in result[0].body


class TestParseSuppressedFromReviewBodyBareSuppressedCommentsSummary:
    """New CCR format where suppressed comments live directly under a bare
    ``<details><summary>Suppressed comments (N)</summary>`` block (no
    ``### Comments suppressed …`` heading and no ``Review details`` wrapper)."""

    def test_recovers_single_bare_summary_entry(self) -> None:
        body = (
            "<details>\n"
            "<summary>Suppressed comments (1)</summary>\n"
            "\n"
            "**src/app.py:42**\n"
            "* Guard against None here.\n"
            "</details>"
        )
        result = _parse_suppressed_from_review_body(body)
        assert len(result) == 1
        assert result[0].path == "src/app.py:42"
        assert result[0].body == "Guard against None here."
        assert result[0].is_suppressed is True
        assert result[0].id == -1
        assert result[0].html_url == ""

    def test_recovers_pr_3548_two_entries(self) -> None:
        """Regression for PR swai-factory/agentic-devtools#3548 review 4840056140.

        Both suppressed comments (one wrapping a fenced code block) are recovered
        as ``ReviewCommentInfo`` objects with ``is_suppressed=True`` and unique
        negative sentinel IDs.
        """
        body = (
            "<details>\n"
            "<summary>Suppressed comments (2)</summary>\n"
            "\n"
            "**specs/1793-subtask-property-section-mapping/spec.md:59**\n"
            "* The configuration example maps `labels` to `body:Metadata`, but the schema disallows it:\n"
            "```\n"
            '        "labels": "body:Metadata",\n'
            "```\n"
            "**specs/1793-subtask-property-section-mapping/spec.md:50**\n"
            "* The spec references `project.json` but should reference the config file.\n"
            "</details>"
        )
        result = _parse_suppressed_from_review_body(body)
        assert len(result) == 2
        assert result[0].path == "specs/1793-subtask-property-section-mapping/spec.md:59"
        assert result[0].body.startswith("The configuration example maps")
        assert '"labels": "body:Metadata"' in result[0].body
        assert result[1].path == "specs/1793-subtask-property-section-mapping/spec.md:50"
        assert result[1].body == "The spec references `project.json` but should reference the config file."
        assert [c.id for c in result] == [-1, -2]
        assert all(c.is_suppressed for c in result)


class TestParseSuppressedFromReviewBodyCountEntryMismatchWarning:
    """FR-007: a declared suppressed count that recovers no entries is logged.

    The parser is built so that every count it reads also opens a block, which
    makes the mismatch unreachable for the supported formats.  An unsupported or
    malformed body can still declare a count with nothing recoverable inside it,
    and that silent drop is exactly the swai-factory/agentic-devtools#3585 stall,
    so it must be observable in diagnostics rather than inferred from an empty
    dispatch comment.
    """

    #: A ``(1)`` declaration whose ``<details>`` block has no content at all.
    EMPTY_BLOCK_BODY = "<details>\n<summary>Suppressed comments (1)</summary>\n\n</details>"

    def test_warns_when_count_is_positive_but_no_entries_recovered(self, caplog) -> None:
        with caplog.at_level(logging.WARNING, logger="agentic_devtools.cli.ci.github_provider"):
            assert _parse_suppressed_from_review_body(self.EMPTY_BLOCK_BODY) == []

        warnings = [r for r in caplog.records if r.levelno == logging.WARNING]
        assert len(warnings) == 1
        message = warnings[0].getMessage()
        assert "1" in message
        assert "suppressed" in message.lower()

    def test_no_warning_when_entries_are_recovered(self, caplog) -> None:
        body = "<details>\n<summary>Suppressed comments (1)</summary>\n\n**src/app.py:42**\n* A finding.\n</details>"
        with caplog.at_level(logging.WARNING, logger="agentic_devtools.cli.ci.github_provider"):
            assert len(_parse_suppressed_from_review_body(body)) == 1

        assert [r for r in caplog.records if r.levelno == logging.WARNING] == []

    def test_no_warning_when_no_suppressed_comments_are_declared(self, caplog) -> None:
        with caplog.at_level(logging.WARNING, logger="agentic_devtools.cli.ci.github_provider"):
            assert _parse_suppressed_from_review_body("A clean review with nothing suppressed.") == []

        assert [r for r in caplog.records if r.levelno == logging.WARNING] == []
