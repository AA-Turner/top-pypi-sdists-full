"""Tests for extract_suppressed_comment_entries() in the CCR review-format parser."""

import pytest

from agentic_devtools.cli.github.ccr_review_format import (
    UNKNOWN_FILE,
    extract_suppressed_comment_entries,
    parse_suppressed_count,
)


def _legacy(inner: str, count: int = 1) -> str:
    return f"<details>\n<summary>Comments suppressed due to low confidence ({count})</summary>\n\n{inner}\n\n</details>"


def _suppressed_comments_summary(inner: str, count: int = 1) -> str:
    """Wrap *inner* in the new CCR ``<summary>Suppressed comments (N)</summary>`` block."""
    return f"<details>\n<summary>Suppressed comments ({count})</summary>\n\n{inner}\n\n</details>"


class TestExtractSuppressedCommentEntries:
    """Tests for extract_suppressed_comment_entries()."""

    def test_empty_body_returns_empty(self) -> None:
        assert extract_suppressed_comment_entries("") == []

    def test_no_block_returns_empty(self) -> None:
        assert extract_suppressed_comment_entries("No suppressed section here.") == []

    def test_legacy_empty_block_returns_empty(self) -> None:
        body = "<details>\n<summary>Comments suppressed due to low confidence (0)</summary>\n\n</details>"
        assert extract_suppressed_comment_entries(body) == []

    def test_legacy_bold_path_entry(self) -> None:
        result = extract_suppressed_comment_entries(_legacy("**src/foo.py**: Fix the null check"))
        assert result == [("src/foo.py", "Fix the null check")]

    def test_legacy_multiple_entries(self) -> None:
        inner = "**a.py**: Comment A\n**b.py**: Comment B"
        result = extract_suppressed_comment_entries(_legacy(inner, count=2))
        assert result == [("a.py", "Comment A"), ("b.py", "Comment B")]

    def test_legacy_blank_path_uses_unknown_file(self) -> None:
        result = extract_suppressed_comment_entries(_legacy("**   **: Body text"))
        assert result == [(UNKNOWN_FILE, "Body text")]

    def test_legacy_empty_body_falls_back_to_raw_line(self) -> None:
        body = (
            "<details>\n<summary>Comments suppressed due to low confidence (1)</summary>\n\n**foo.py**:\n\n</details>"
        )
        assert extract_suppressed_comment_entries(body) == [(UNKNOWN_FILE, "**foo.py**:")]

    def test_legacy_no_path_falls_back_to_unknown_file(self) -> None:
        result = extract_suppressed_comment_entries(_legacy("A standalone note without a path"))
        assert result == [(UNKNOWN_FILE, "A standalone note without a path")]

    def test_fallback_skips_blank_lines(self) -> None:
        body = (
            "<details>\n"
            "<summary>Comments suppressed due to low confidence (2)</summary>\n"
            "\n"
            "first note\n"
            "\n"
            "second note\n"
            "\n"
            "</details>"
        )
        assert extract_suppressed_comment_entries(body) == [
            (UNKNOWN_FILE, "first note"),
            (UNKNOWN_FILE, "second note"),
        ]

    def test_fallback_ignores_fenced_lines(self) -> None:
        body = (
            "<details>\n"
            "<summary>Comments suppressed due to low confidence (1)</summary>\n\n"
            "plain note\n"
            "```markdown\n"
            "**Deliverable:** this must not become a fallback entry\n"
            "```\n"
            "</details>"
        )
        assert extract_suppressed_comment_entries(body) == [(UNKNOWN_FILE, "plain note")]

    def test_new_format_single_entry(self) -> None:
        body = (
            "### 🟡 Not ready to approve\n\n"
            "<details>\n<summary>Review details</summary>\n\n"
            "### Comments suppressed due to low confidence (1)\n\n"
            "**src/app.py:42**\n"
            "* Consider guarding against None here.\n\n"
            "- **Files reviewed:** 3/3 changed files\n"
            "- **Comments generated:** 0 new\n"
            "</details>"
        )
        result = extract_suppressed_comment_entries(body)
        assert result == [("src/app.py:42", "Consider guarding against None here.")]

    def test_new_format_multiple_entries_excludes_metrics_footer(self) -> None:
        body = (
            "### 🟡 Not ready to approve\n\n"
            "<details>\n<summary>Review details</summary>\n\n"
            "### Comments suppressed due to low confidence (2)\n\n"
            "**a/b.py:10**\n"
            "* First finding.\n\n"
            "**c/d.py:20**\n"
            "* Second finding.\n\n"
            "- **Files reviewed:** 2/2 changed files\n"
            "- **Comments generated:** 0 new\n"
            "- **Review effort level:** Low\n"
            "</details>"
        )
        result = extract_suppressed_comment_entries(body)
        assert result == [
            ("a/b.py:10", "First finding."),
            ("c/d.py:20", "Second finding."),
        ]
        # The metrics footer must never be captured as an entry path.
        paths = [p for p, _ in result]
        assert not any("Files reviewed" in p or "Comments generated" in p for p in paths)

    def test_new_format_entry_with_code_block(self) -> None:
        body = (
            "### 🟡 Not ready to approve\n\n"
            "<details>\n<summary>Review details</summary>\n\n"
            "### Comments suppressed due to low confidence (1)\n\n"
            "**tasks.md:49**\n"
            "* The ordering looks off:\n"
            "```\n"
            "- [ ] T001 do a thing\n"
            "- [ ] T002 do another\n"
            "```\n\n"
            "- **Files reviewed:** 1/1 changed files\n"
            "</details>"
        )
        result = extract_suppressed_comment_entries(body)
        assert len(result) == 1
        assert result[0][0] == "tasks.md:49"
        assert "The ordering looks off" in result[0][1]

    def test_new_format_empty_section_returns_empty(self) -> None:
        body = (
            "### ✅ Ready to approve\n\n"
            "<details>\n<summary>Review details</summary>\n\n"
            "### Comments suppressed due to low confidence (0)\n\n"
            "- **Files reviewed:** 3/3 changed files\n"
            "</details>"
        )
        assert extract_suppressed_comment_entries(body) == []

    def test_legacy_preferred_when_both_markers_present(self) -> None:
        """A legacy <details> summary block is preferred over a new-format heading."""
        body = (
            "### Comments suppressed due to low confidence (1)\n"
            "**new/only.py:1**\n"
            "* new-format entry\n\n"
            "<details>\n"
            "<summary>Comments suppressed due to low confidence (1)</summary>\n"
            "\n"
            "**legacy/path.py**: legacy entry\n"
            "\n"
            "</details>"
        )
        assert extract_suppressed_comment_entries(body) == [("legacy/path.py", "legacy entry")]

    def test_new_summary_suppressed_comments_single_entry(self) -> None:
        """The bare ``<summary>Suppressed comments (N)</summary>`` block is parsed."""
        body = _suppressed_comments_summary("**src/foo.py:12**\n* Guard against None here.")
        assert extract_suppressed_comment_entries(body) == [("src/foo.py:12", "Guard against None here.")]

    def test_new_summary_suppressed_comments_pr_3548_body(self) -> None:
        """Regression for PR swai-factory/agentic-devtools#3548 review 4840056140.

        Both suppressed comments (including the one wrapping a fenced code block)
        are recovered from the ``<summary>Suppressed comments (2)</summary>`` body.
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
        result = extract_suppressed_comment_entries(body)
        assert len(result) == 2
        assert result[0][0] == "specs/1793-subtask-property-section-mapping/spec.md:59"
        assert result[0][1].startswith("The configuration example maps")
        assert '"labels": "body:Metadata"' in result[0][1]
        assert result[1] == (
            "specs/1793-subtask-property-section-mapping/spec.md:50",
            "The spec references `project.json` but should reference the config file.",
        )

    def test_suppressed_comments_heading_inside_review_details(self) -> None:
        """The ``### Suppressed comments (N)`` heading spelling is recovered.

        Regression for swai-factory/agentic-devtools#3638 root cause A: this
        heading sits inside a generic ``<summary>Review details</summary>``
        block, so neither the ``<summary>``-anchored spelling nor the literal
        ``Comments suppressed due to low confidence`` heading matched — the loop
        saw zero findings while the gate declared three.
        """
        body = (
            "### 🟡 Not ready to approve\n\n"
            "<details>\n<summary>Review details</summary>\n\n"
            "### Suppressed comments (3)\n\n"
            "**specs/2316-subtask/tasks.md:25**\n"
            "* [US1] is combined with explicit FR references:\n"
            "```\n"
            "- [ ] T009 [US1] Write failing test ...\n"
            "```\n\n"
            "**src/app.py:10**\n"
            "* Guard against None here.\n\n"
            "**src/app.py:20**\n"
            "* This branch is unreachable.\n\n"
            "- **Files reviewed:** 3/3 changed files\n"
            "- **Comments generated:** 0 new\n"
            "</details>"
        )
        result = extract_suppressed_comment_entries(body)
        assert len(result) == 3
        assert [path for path, _ in result] == [
            "specs/2316-subtask/tasks.md:25",
            "src/app.py:10",
            "src/app.py:20",
        ]
        assert "T009 [US1] Write failing test" in result[0][1]

    def test_bold_run_inside_fenced_excerpt_is_not_an_entry(self) -> None:
        """Bold runs inside a fenced excerpt never become phantom entries.

        Regression for swai-factory/agentic-devtools#3638 root cause B: the
        ``**Deliverable:**`` / ``**Changes:**`` lines CCR embeds in its code
        excerpts were parsed as extra entries and handed to the repair agent as
        work items.
        """
        body = (
            "<details>\n<summary>Review details</summary>\n\n"
            "### Suppressed comments (1)\n\n"
            "**docs/plan.md:3**\n"
            "* The plan section is inconsistent with the template:\n"
            "```markdown\n"
            "**Deliverable:** a thing\n"
            "**Changes:** another thing\n"
            "```\n"
        )
        result = extract_suppressed_comment_entries(body)
        assert len(result) == 1
        assert result[0][0] == "docs/plan.md:3"
        assert "**Deliverable:**" in result[0][1]

    def test_h1_heading_yields_entries(self) -> None:
        """An h1 ``# Suppressed comments (N)`` heading yields its entries.

        Guards the count/block heading-level parity: the count regex and the
        block regex both accept h1–h6, so no heading level can declare a count
        the block regex refuses to read (which would be a new stall class).
        """
        body = "# Suppressed comments (2)\n\n**a.py:1**\n* First finding.\n\n**b.py:2**\n* Second finding.\n"
        assert extract_suppressed_comment_entries(body) == [
            ("a.py:1", "First finding."),
            ("b.py:2", "Second finding."),
        ]

    def test_fenced_heading_does_not_split_an_entry(self) -> None:
        """A ``###`` heading inside a fenced excerpt does not terminate the block."""
        body = (
            "### Suppressed comments (1)\n\n"
            "**docs/guide.md:5**\n"
            "* The example heading is wrong:\n"
            "```markdown\n"
            "### Comments suppressed due to low confidence (99)\n"
            "```\n"
        )
        result = extract_suppressed_comment_entries(body)
        assert len(result) == 1
        assert result[0][0] == "docs/guide.md:5"
        assert "(99)" in result[0][1]

    def test_unbalanced_fence_fails_open_without_crashing(self) -> None:
        """An unbalanced fence masks the tail of the block but never raises.

        CCR occasionally emits an opening fence it never closes.  The masked tail
        can no longer yield its own entry header, so the remaining text is folded
        into the preceding entry verbatim — a known residual that is preferred
        over disabling fence masking (which would reinstate phantom entries).
        """
        body = "### Suppressed comments (2)\n\n**a.py:1**\n* Close the snippet:\n```\n**b.py:2**\n* Second finding.\n"
        result = extract_suppressed_comment_entries(body)
        assert len(result) == 1
        assert result[0][0] == "a.py:1"
        assert "Second finding." in result[0][1]

    def test_crlf_body_yields_entries(self) -> None:
        """CRLF is a live GitHub input; entries must match the parsed count.

        Regression for swai-factory/agentic-devtools#3638: a body whose count
        parses while its entries do not is exactly the stall (gate blocks, repair
        agent dispatched with zero findings) this parser exists to prevent.
        """
        body = (
            "### 🟡 Not ready to approve\r\n\r\n"
            "<details>\r\n<summary>Review details</summary>\r\n\r\n"
            "### Suppressed comments (2)\r\n\r\n"
            "**src/app.py:10**\r\n* Guard against None here.\r\n\r\n"
            "**src/app.py:20**\r\n* Unreachable branch.\r\n\r\n"
            "- **Comments generated:** 0 new\r\n</details>\r\n"
        )
        assert extract_suppressed_comment_entries(body) == [
            ("src/app.py:10", "Guard against None here."),
            ("src/app.py:20", "Unreachable branch."),
        ]

    def test_heading_with_trailing_qualifier_yields_entries(self) -> None:
        body = "### Suppressed comments (1) — low confidence\n\n**a.py:1**\n* A finding.\n"
        assert extract_suppressed_comment_entries(body) == [("a.py:1", "A finding.")]

    def test_summary_anchored_count_yields_entries(self) -> None:
        """Every anchor the count reads must also yield entries.

        ``parse_suppressed_count`` anchors on ``<summary>`` as well as on
        headings, so a ``<summary>`` outside a recognised ``<details>`` wrapper
        must still open a block — otherwise it declares a count with zero
        entries, which is the swai-factory/agentic-devtools#3638 stall.
        """
        body = "<summary>Suppressed comments (1)</summary>\n\n**a.py:1**\n* A finding.\n"
        assert parse_suppressed_count(body) == 1
        assert extract_suppressed_comment_entries(body) == [("a.py:1", "A finding.")]

    def test_legacy_summary_anchored_count_yields_entries(self) -> None:
        """The legacy ``<summary>Suppressed (N)</summary>`` anchor still yields entries."""
        body = "<summary>Suppressed (2)</summary>\n\n**a.py:1**\n* A finding.\n\n**b.py:2**\n* B finding.\n"
        assert parse_suppressed_count(body) == 2
        assert extract_suppressed_comment_entries(body) == [("a.py:1", "A finding."), ("b.py:2", "B finding.")]

    def test_low_confidence_anchored_count_yields_entries(self) -> None:
        """The low-confidence fallback count has the same parity requirement."""
        body = "### Low confidence (1)\n\n**a.py:1**\n* A finding.\n"
        assert parse_suppressed_count(body) == 1
        assert extract_suppressed_comment_entries(body) == [("a.py:1", "A finding.")]

    def test_new_summary_singular_suppressed_comment(self) -> None:
        """The singular ``<summary>Suppressed comment (1)</summary>`` spelling is parsed.

        CCR pluralises the label from the count, so a review with exactly one
        suppressed finding renders ``comment`` rather than ``comments``.
        """
        body = "<details>\n<summary>Suppressed comment (1)</summary>\n\n**`src/foo.py`**: * Comment text\n\n</details>"
        assert extract_suppressed_comment_entries(body) == [("src/foo.py", "Comment text")]

    @pytest.mark.parametrize(
        ("summary", "inner", "expected"),
        [
            (
                "3 comments suppressed due to low confidence",
                "**a.py**: Comment A\n**b.py**: Comment B\n**c.py**: Comment C",
                [("a.py", "Comment A"), ("b.py", "Comment B"), ("c.py", "Comment C")],
            ),
            (
                "1 comment suppressed due to low confidence",
                "**a.py**: Comment A",
                [("a.py", "Comment A")],
            ),
        ],
    )
    def test_legacy_count_prefixed_summary_is_preserved(
        self, summary: str, inner: str, expected: list[tuple[str, str]]
    ) -> None:
        """FR-002: the legacy count-prefixed summary keeps working after FR-006 hardening.

        Here the count precedes the phrase (``3 comments suppressed …``) instead
        of trailing it, and there is no parenthesised count at all — the word
        boundaries added for FR-006 must not narrow this ordering out.
        """
        body = f"<details>\n<summary>{summary}</summary>\n\n{inner}\n\n</details>"
        assert extract_suppressed_comment_entries(body) == expected

    @pytest.mark.parametrize(
        "body",
        [
            # New bare-summary format (the swai-factory/agentic-devtools#3585 body).
            _suppressed_comments_summary("**src/app.py:42**\n* Guard against None here.", count=1),
            # Legacy <details><summary> format.
            _legacy("**src/foo.py**: Fix the null check"),
            # New-format heading nested in a "Review details" block.
            "### 🟡 Not ready to approve\n\n"
            "<details>\n<summary>Review details</summary>\n\n"
            "### Comments suppressed due to low confidence (1)\n\n"
            "**src/app.py:42**\n* Consider guarding against None here.\n\n"
            "- **Comments generated:** 0 new\n"
            "</details>",
            # Heading-only spelling, no <details> wrapper.
            "### Suppressed comments (2)\n\n**a.py:1**\n* First finding.\n\n**b.py:2**\n* Second finding.\n",
        ],
    )
    def test_declared_count_always_yields_entries(self, body: str) -> None:
        """SC-004: for every well-formed format, count > 0 implies entries > 0.

        A body whose count parses while its entries do not is the
        swai-factory/agentic-devtools#3585 stall itself: the gate blocks the
        merge on the count and the repair agent is dispatched with nothing to
        act on.
        """
        assert parse_suppressed_count(body) > 0
        assert extract_suppressed_comment_entries(body)

    def test_nonzero_declaration_with_empty_block_returns_empty_without_error(self) -> None:
        """An empty block yields ``[]`` rather than raising (the FR-007 warning case)."""
        body = _suppressed_comments_summary("", count=2)
        assert extract_suppressed_comment_entries(body) == []

    def test_partial_block_returns_the_entries_it_can_parse(self) -> None:
        """A block with fewer parseable entries than its count parses what it can.

        The count is advisory — it comes from the summary label — so partial
        extraction is preferred over failing and dropping every finding.
        """
        body = _suppressed_comments_summary(
            "**a.py:1**\n* Only this entry has a header.\n\na stray line with no entry header",
            count=3,
        )
        result = extract_suppressed_comment_entries(body)
        assert len(result) == 1
        assert result[0][0] == "a.py:1"
        assert "Only this entry has a header." in result[0][1]

    def test_large_review_body_recovers_every_entry(self) -> None:
        """NFR-001: a representative 50 KB body still recovers all of its entries.

        The oracle is structural rather than wall-clock — timing assertions are
        flaky on shared CI runners.  Pathological backtracking on a body this
        size surfaces as a job timeout, while a silent parsing regression at
        scale surfaces as a short entry list.
        """
        entry_count = 125
        filler = "Consider extracting this branch into a helper; it is duplicated across call sites. " * 4
        entries_md = "".join(
            f"**src/module_{index:03d}.py:{index + 1}**\n"
            f"* Finding {index}: {filler}\n"
            "```python\n"
            f"    value_{index} = compute(value_{index})\n"
            "```\n\n"
            for index in range(entry_count)
        )
        body = _suppressed_comments_summary(entries_md, count=entry_count)
        assert len(body) >= 50_000

        result = extract_suppressed_comment_entries(body)
        assert len(result) == entry_count
        assert result[0][0] == "src/module_000.py:1"
        assert result[-1][0] == f"src/module_{entry_count - 1:03d}.py:{entry_count}"
        assert result[0][1].startswith("Finding 0:")
