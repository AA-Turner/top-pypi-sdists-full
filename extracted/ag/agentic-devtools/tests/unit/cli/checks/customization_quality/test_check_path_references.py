"""Tests for the Q13 path-reference rule."""

from __future__ import annotations

from pathlib import Path

import pytest

from agentic_devtools.cli.checks.customization_quality import check_path_references
from tests.unit.cli.checks.customization_quality._support import make_unit, write_file


@pytest.fixture
def repo(tmp_path: Path) -> Path:
    """A repository with one skill folder, a bundled resource and a top-level package."""
    write_file(tmp_path, ".agents/skills/demo/SKILL.md", "x")
    write_file(tmp_path, ".agents/skills/demo/reference/notes.md", "x")
    write_file(tmp_path, ".agents/skills/demo/reference/deeper/notes.md", "x")
    write_file(tmp_path, "agentic_devtools/cli/checks/lint.py", "x")
    write_file(tmp_path, "docs/agent-customization/authoring-standard.md", "x")
    return tmp_path


class TestCheckPathReferences:
    def test_accepts_a_resolving_link_one_level_deep(self, repo: Path) -> None:
        """A relative link to a bundled resource one level down passes."""
        unit = make_unit(body="See [notes](reference/notes.md).\n")

        assert check_path_references(unit, repo) == []

    def test_flags_a_link_that_does_not_resolve(self, repo: Path) -> None:
        """A link to a missing file is reported."""
        violations = check_path_references(make_unit(body="See [gone](reference/gone.md).\n"), repo)

        assert [v.rule for v in violations] == ["Q13"]
        assert "does not resolve" in violations[0].message

    def test_flags_a_resource_more_than_one_level_away(self, repo: Path) -> None:
        """Progressive disclosure allows only one level from the entry file."""
        violations = check_path_references(make_unit(body="See [deep](reference/deeper/notes.md).\n"), repo)

        assert any("more than one level" in v.message for v in violations)

    def test_resolves_parent_traversal(self, repo: Path) -> None:
        """``..`` segments walk back up from the entry file's directory."""
        unit = make_unit(body="See [up](../../../agentic_devtools/cli/checks/lint.py).\n")

        violations = check_path_references(unit, repo)

        assert [v.message for v in violations] == [
            "linked resource is more than one level from its entry file: ../../../agentic_devtools/cli/checks/lint.py"
        ]

    def test_flags_pure_upward_traversal_to_a_shallow_target(self, repo: Path) -> None:
        """``../../../README.md`` travels three levels up and must be rejected even though the
        target file has no downward path components."""
        write_file(repo, "README.md", "x")
        unit = make_unit(body="See [readme](../../../README.md).\n")

        violations = check_path_references(unit, repo)

        assert any("more than one level" in v.message for v in violations)

    def test_parent_traversal_never_escapes_the_repository_root(self, repo: Path) -> None:
        """More ``..`` segments than directories resolve at the root, not above it."""
        unit = make_unit(body="See [up](../../../../agentic_devtools/cli/checks/lint.py).\n")

        violations = check_path_references(unit, repo)

        assert all("does not resolve" not in v.message for v in violations)

    def test_ignores_redundant_current_directory_segments(self, repo: Path) -> None:
        """``./`` and empty segments do not change where a link points."""
        assert check_path_references(make_unit(body="See [notes](./reference/notes.md).\n"), repo) == []

    def test_accepts_a_repository_absolute_link(self, repo: Path) -> None:
        """A leading slash means repository-root-relative, not filesystem-absolute."""
        unit = make_unit(path=".agents/skills/demo/reference/notes.md", body="See [skill](/.agents/skills/demo).\n")

        assert check_path_references(unit, repo) == []

    def test_accepts_a_relative_repo_docs_cross_reference(self, repo: Path) -> None:
        """A relative link into top-level ``docs/`` is a repository cross-reference."""
        unit = make_unit(
            path=".github/instructions/agent-customization.instructions.md",
            kind="instruction",
            listing=".github/instructions",
            body="Read [standard](../../docs/agent-customization/authoring-standard.md).\n",
        )

        assert check_path_references(unit, repo) == []

    def test_absolute_link_with_traversal_is_clamped_at_repo_root(self, repo: Path) -> None:
        """``..`` and ``.`` segments in a repository-absolute link are resolved safely."""
        unit = make_unit(
            path=".agents/skills/demo/reference/notes.md",
            body="See [lint](/../agentic_devtools/./cli/../cli/checks/lint.py).\n",
        )

        violations = check_path_references(unit, repo)

        assert all("does not resolve" not in v.message for v in violations)

    def test_accepts_a_reference_style_link(self, repo: Path) -> None:
        """Reference-style links are resolved and checked like inline links."""
        body = "See [notes][guide].\n\n[guide]: reference/notes.md\n"

        assert check_path_references(make_unit(body=body), repo) == []

    def test_flags_a_missing_reference_style_link_target(self, repo: Path) -> None:
        """Reference definitions to missing repository files still fail Q13."""
        body = "See [notes][guide].\n\n[guide]: reference/missing.md\n"

        violations = check_path_references(make_unit(body=body), repo)

        assert [v.rule for v in violations] == ["Q13"]
        assert "does not resolve" in violations[0].message

    def test_ignores_a_reference_style_link_without_a_definition(self, repo: Path) -> None:
        """An unresolved label contributes no repository path to validate."""
        body = "See [notes][guide].\n"

        assert check_path_references(make_unit(body=body), repo) == []

    @pytest.mark.parametrize(
        "link",
        ["https://example.com/x.md", "http://example.com", "mailto:a@example.com", "#section", "<https://x.dev>"],
    )
    def test_ignores_non_repository_links(self, repo: Path, link: str) -> None:
        """URLs, mail links and in-page anchors are not repository paths."""
        assert check_path_references(make_unit(body=f"See [x]({link}).\n"), repo) == []

    def test_ignores_an_empty_link_target(self, repo: Path) -> None:
        """A link with a whitespace-only target has no path to check."""
        assert check_path_references(make_unit(body="See [x]( ).\n"), repo) == []

    def test_accepts_a_pointy_bracket_destination(self, repo: Path) -> None:
        """CommonMark's ``<...>`` destination form is unwrapped before resolving."""
        assert check_path_references(make_unit(body="See [notes](<reference/notes.md>).\n"), repo) == []

    def test_ignores_a_link_title_after_the_target(self, repo: Path) -> None:
        """A Markdown link title is not part of the path."""
        unit = make_unit(body='See [notes](reference/notes.md "Notes") and its [anchor](reference/notes.md#top).\n')

        assert check_path_references(unit, repo) == []

    def test_flags_an_inline_code_path_that_does_not_exist(self, repo: Path) -> None:
        """A documented repository path in inline code must resolve."""
        violations = check_path_references(make_unit(body="Edit `agentic_devtools/cli/checks/gone.py`.\n"), repo)

        assert any("documented path does not exist" in v.message for v in violations)

    def test_accepts_an_inline_code_path_that_exists(self, repo: Path) -> None:
        """An existing path, with or without a trailing slash, passes."""
        unit = make_unit(body="Edit `agentic_devtools/cli/checks/lint.py` under `agentic_devtools/cli/`.\n")

        assert check_path_references(unit, repo) == []

    def test_rejects_an_inline_code_path_that_escapes_the_repository_root(self, repo: Path) -> None:
        """Inline-code paths must stay inside the repository after resolution."""
        outside = repo.parent / (repo.name + "_outside")
        outside.mkdir(exist_ok=True)
        (outside / "secret.md").write_text("secret", encoding="utf-8")

        unit = make_unit(body=f"See `../{repo.name}_outside/secret.md`.\n")

        violations = check_path_references(unit, repo)

        assert [v.rule for v in violations] == ["Q13"]
        assert "documented path does not exist" in violations[0].message

    def test_rejects_an_inline_code_path_that_escapes_through_a_top_level_symlink(self, repo: Path) -> None:
        """A top-level symlink pointing outside the repo must not evade Q13.

        When the first segment of an inline-code candidate is a top-level
        symlink that resolves *outside* the repository, the containment-aware
        check used to classify it as 'not a repository path' and skip it
        entirely.  The first-segment guard now uses a plain lexical existence
        test so that the full candidate reaches ``_exists_within_repo``, which
        then correctly reports the containment violation.
        """
        outside = repo.parent / "outside_toplevel"
        outside.mkdir(exist_ok=True)
        (outside / "secret.md").write_text("secret", encoding="utf-8")
        (repo / "external").symlink_to(outside)

        unit = make_unit(body="See `external/secret.md`.\n")

        violations = check_path_references(unit, repo)

        assert [v.rule for v in violations] == ["Q13"]
        assert "documented path does not exist" in violations[0].message

    def test_rejects_an_inline_code_path_that_escapes_through_a_symlink(self, repo: Path) -> None:
        """A symlinked repository path still has to resolve under the repository root."""
        outside = repo.parent / (repo.name + "_outside_symlink")
        outside.mkdir()
        (outside / "secret.md").write_text("secret", encoding="utf-8")
        (repo / "agentic_devtools" / "alias").symlink_to(outside)

        unit = make_unit(body="See `agentic_devtools/alias/secret.md`.\n")

        violations = check_path_references(unit, repo)

        assert [v.rule for v in violations] == ["Q13"]
        assert "documented path does not exist" in violations[0].message

    def test_ignores_inline_code_that_is_not_a_path(self, repo: Path) -> None:
        """Commands and prose slashes are not treated as repository paths."""
        unit = make_unit(body="Run `agdt-test` and pick `jira | github`.\n")

        assert check_path_references(unit, repo) == []

    def test_ignores_a_path_whose_first_segment_is_not_in_the_repository(self, repo: Path) -> None:
        """Placeholder prose such as a branch pattern is not a repository path."""
        assert check_path_references(make_unit(body="Branch as `type/ISSUE-KEY/description`.\n"), repo) == []

    def test_depth_uses_the_normalized_relative_target(self, repo: Path) -> None:
        """A normalized sibling link is not treated as deeper than it resolves."""
        write_file(repo, ".agents/skills/demo/notes.md", "x")
        unit = make_unit(body="See [notes](reference/../notes.md).\n")

        assert check_path_references(unit, repo) == []

    def test_accepts_a_link_destination_with_balanced_parentheses(self, repo: Path) -> None:
        """A path containing parentheses, e.g. ``release_(v2).md``, is not truncated."""
        write_file(repo, ".agents/skills/demo/release_(v2).md", "x")
        unit = make_unit(body="See [notes](reference/../release_(v2).md).\n")

        assert check_path_references(unit, repo) == []

    def test_ignores_a_shortcut_reference_link_without_a_definition(self, repo: Path) -> None:
        """A shortcut reference with no matching definition contributes no target."""
        body = "See [guide].\n"

        assert check_path_references(make_unit(body=body), repo) == []

    def test_resolves_a_shortcut_reference_link(self, repo: Path) -> None:
        """CommonMark shortcut references ``[guide]`` are resolved against definitions."""
        body = "See [guide].\n\n[guide]: reference/notes.md\n"

        assert check_path_references(make_unit(body=body), repo) == []

    def test_flags_a_missing_shortcut_reference_link_target(self, repo: Path) -> None:
        """A shortcut reference whose definition points to a missing file fails Q13."""
        body = "See [guide].\n\n[guide]: reference/missing.md\n"

        violations = check_path_references(make_unit(body=body), repo)

        assert [v.rule for v in violations] == ["Q13"]
        assert "does not resolve" in violations[0].message

    @pytest.mark.parametrize(
        "link",
        ["ftp://example.com/file.md", "tel:+1234567890", "vscode://ms-python.python"],
    )
    def test_ignores_links_with_non_http_uri_schemes(self, repo: Path, link: str) -> None:
        """Any URI scheme is recognised as a non-repository link and skipped."""
        assert check_path_references(make_unit(body=f"See [x]({link}).\n"), repo) == []

    def test_ignores_markdown_links_inside_a_fenced_code_block(self, repo: Path) -> None:
        """Example code blocks do not contribute real path references to Q13."""
        unit = make_unit(body="```md\n[artifact](reference/missing.md)\n```\n")

        assert check_path_references(unit, repo) == []

    def test_ignores_inline_code_paths_inside_a_fenced_code_block(self, repo: Path) -> None:
        """Inline code inside fenced examples is code content, not documentation."""
        unit = make_unit(body="```md\nEdit `agentic_devtools/cli/checks/missing.py`.\n```\n")

        assert check_path_references(unit, repo) == []

    def test_ignores_markdown_like_syntax_inside_inline_code(self, repo: Path) -> None:
        """Regex patterns in inline code are not parsed as markdown link targets.

        A regex such as ``^[a-z0-9](-?[a-z0-9])*$`` contains the sequence
        ``[a-z0-9](-?[a-z0-9])`` which superficially matches the
        ``[text](link)`` inline-link syntax.  The link target ``-?[a-z0-9]``
        does not resolve to a repository path, so without inline-code stripping
        the check would emit a false-positive Q13 violation.
        """
        unit = make_unit(body="Validated against `^[a-z0-9](-?[a-z0-9])*$` and a length limit.\n")

        assert check_path_references(unit, repo) == []

    def test_ignores_markdown_like_syntax_inside_multibacktick_inline_code(self, repo: Path) -> None:
        """A longer backtick run still protects literal markdown syntax."""
        unit = make_unit(body="Validated against ``[name](reference/missing.md)``.\n")

        assert check_path_references(unit, repo) == []

    def test_ignores_markdown_like_syntax_inside_multiline_inline_code(self, repo: Path) -> None:
        """A code span may cross a line break within one paragraph."""
        unit = make_unit(body="Validated against `[name](reference/missing.md)\nwith extra text`.\n")

        assert check_path_references(unit, repo) == []

    def test_multiline_inline_code_preserves_line_breaks_for_reference_parsing(self, repo: Path) -> None:
        """Blanking a multiline code span must keep ``\\n`` so definitions are not synthesized."""
        unit = make_unit(body=("[guide]:`\n`reference/notes.md\nSee [guide].\n[guide]: reference/missing.md\n"))

        violations = check_path_references(unit, repo)

        assert [v.rule for v in violations] == ["Q13"]
        assert "does not resolve" in violations[0].message

    def test_inline_code_delimiters_are_not_replaced_with_definition_whitespace(self, repo: Path) -> None:
        """A split backtick token must not synthesize a second reference definition target."""
        unit = make_unit(body=("[guide]:`\n`reference/missing.md\nSee [guide].\n"))

        violations = check_path_references(unit, repo)

        assert [v.rule for v in violations] == ["Q13"]
        assert "reference/missing.md" not in violations[0].message

    def test_fenced_blocks_interrupt_paragraph_for_inline_code_parsing(self, repo: Path) -> None:
        """An opener before a fenced block cannot hide links after the block."""
        unit = make_unit(
            body="`unterminated\n```md\n[hidden](reference/missing.md)\n```\n[shown](reference/missing.md)`\n"
        )

        violations = check_path_references(unit, repo)

        assert [v.rule for v in violations] == ["Q13"]
        assert "reference/missing.md" in violations[0].message

    def test_fenced_blocks_with_crlf_line_endings_still_interrupt_inline_code(self, repo: Path) -> None:
        """CRLF-only fence lines still preserve a block boundary after stripping."""
        unit = make_unit(
            body="`unterminated\r\n```md\r\n[hidden](reference/missing.md)\r\n```\r\n[shown](reference/missing.md)`\r\n"
        )

        violations = check_path_references(unit, repo)

        assert [v.rule for v in violations] == ["Q13"]
        assert "reference/missing.md" in violations[0].message

    def test_fenced_blocks_without_terminal_newline_do_not_raise_path_findings(self, repo: Path) -> None:
        """A closing fence at EOF (without ``\\n``) stays non-visible to Q13."""
        unit = make_unit(body="```md\n[hidden](reference/missing.md)\n```")

        assert check_path_references(unit, repo) == []

    def test_ordered_list_items_starting_at_two_do_not_interrupt_inline_code(self, repo: Path) -> None:
        """Only ordered lists starting at ``1`` may interrupt a paragraph."""
        unit = make_unit(body="`literal\n2. [gone](reference/missing.md)`\n")

        assert check_path_references(unit, repo) == []

    def test_definition_allows_one_line_ending_before_destination(self, repo: Path) -> None:
        """A reference definition may place the destination on the next line."""
        unit = make_unit(body="[guide]:  \n reference/missing.md\nSee [guide].\n")

        violations = check_path_references(unit, repo)

        assert [v.rule for v in violations] == ["Q13"]
        assert "does not resolve" in violations[0].message

    def test_atx_heading_interrupts_paragraph_for_inline_code_parsing(self, repo: Path) -> None:
        """An unterminated span cannot consume a following heading line."""
        unit = make_unit(body="`unterminated\n# [gone](reference/gone.md)`\n")

        violations = check_path_references(unit, repo)

        assert [v.rule for v in violations] == ["Q13"]
        assert "does not resolve" in violations[0].message

    def test_atx_heading_is_self_terminating_for_inline_code_parsing(self, repo: Path) -> None:
        """An unmatched backtick inside a heading cannot consume the following paragraph."""
        # Without self-termination the heading backtick would pair with the
        # first backtick on the next line, hiding the link from Q13.
        unit = make_unit(body="# heading `unmatched\n[gone](reference/gone.md) and `closed`\n")

        violations = check_path_references(unit, repo)

        assert [v.rule for v in violations] == ["Q13"]
        assert "does not resolve" in violations[0].message

    def test_thematic_break_interrupts_paragraph_for_inline_code_parsing(self, repo: Path) -> None:
        """An unterminated span cannot consume links after a thematic break."""
        unit = make_unit(body="`unterminated\n---\n[shown](reference/missing.md)`\n")

        violations = check_path_references(unit, repo)

        assert [v.rule for v in violations] == ["Q13"]
        assert "does not resolve" in violations[0].message

    def test_setext_heading_interrupts_paragraph_for_inline_code_parsing(self, repo: Path) -> None:
        """An unterminated span cannot consume links after a setext underline."""
        unit = make_unit(body="`unterminated\n===\n[shown](reference/missing.md)`\n")

        violations = check_path_references(unit, repo)

        assert [v.rule for v in violations] == ["Q13"]
        assert "does not resolve" in violations[0].message

    def test_block_quote_continuation_keeps_multiline_code_span_in_one_block(self, repo: Path) -> None:
        """Consecutive block-quote lines belong to one block-quoted paragraph.

        A code span may span both lines; the link inside it must not be reported
        by Q13 because it is inside a code span.
        """
        unit = make_unit(body="> `[gone](reference/gone.md)\n> continued`\n")

        assert check_path_references(unit, repo) == []

    def test_block_quote_boundary_still_interrupts_preceding_paragraph(self, repo: Path) -> None:
        """A block quote following a plain paragraph still opens a new block."""
        unit = make_unit(body="`unterminated\n> [gone](reference/gone.md)`\n")

        violations = check_path_references(unit, repo)

        assert [v.rule for v in violations] == ["Q13"]
        assert "does not resolve" in violations[0].message

    def test_quote_only_block_quote_line_interrupts_paragraph_for_inline_code_parsing(self, repo: Path) -> None:
        """A quote-only line is blank and ends the current block-quoted paragraph."""
        unit = make_unit(body="> `open\n>\n> [gone](reference/gone.md)`\n")

        violations = check_path_references(unit, repo)

        assert [v.rule for v in violations] == ["Q13"]
        assert "does not resolve" in violations[0].message

    def test_flags_a_missing_link_inside_escaped_backticks(self, repo: Path) -> None:
        """Escaped backticks stay in prose, so the Markdown link remains active."""
        unit = make_unit(body="See \\`[gone](reference/gone.md)\\`.\n")

        violations = check_path_references(unit, repo)

        assert [v.rule for v in violations] == ["Q13"]
        assert "does not resolve" in violations[0].message

    def test_backslash_before_closing_backtick_does_not_prevent_span_close(self, repo: Path) -> None:
        """Inside a code span, backslash does not escape the closer (CommonMark §6.1).

        When the only backtick after an opener is preceded by a backslash the
        code span still closes there; content inside is hidden from Q13.
        """
        unit = make_unit(body="See `[gone](reference/gone.md)\\`.\n")

        assert check_path_references(unit, repo) == []

    def test_accepts_an_existing_path_inside_multibacktick_inline_code(self, repo: Path) -> None:
        """Documented repository paths are still checked when quoted with ````...````."""
        unit = make_unit(body="Edit ``agentic_devtools/cli/checks/lint.py``.\n")

        assert check_path_references(unit, repo) == []

    def test_unterminated_multibacktick_span_does_not_hide_later_links(self, repo: Path) -> None:
        """An unmatched opener remains literal, so later Markdown links are still validated."""
        unit = make_unit(body="Literal ``[name](reference/missing.md)` still prose.\n")

        violations = check_path_references(unit, repo)

        assert [v.rule for v in violations] == ["Q13"]
        assert "does not resolve" in violations[0].message

    def test_flags_a_missing_full_reference_image_target(self, repo: Path) -> None:
        """A reference-style image whose definition points to a missing file fails Q13."""
        body = "![diagram][arch]\n\n[arch]: reference/missing.png\n"

        violations = check_path_references(make_unit(body=body), repo)

        assert [v.rule for v in violations] == ["Q13"]
        assert "does not resolve" in violations[0].message

    def test_accepts_a_full_reference_image_to_an_existing_file(self, repo: Path) -> None:
        """A reference-style image pointing to an existing file passes Q13."""
        body = "![diagram][arch]\n\n[arch]: reference/notes.md\n"

        assert check_path_references(make_unit(body=body), repo) == []

    def test_flags_a_missing_shortcut_reference_image_target(self, repo: Path) -> None:
        """A shortcut reference image whose definition points to a missing file fails Q13."""
        body = "![diagram]\n\n[diagram]: reference/missing.png\n"

        violations = check_path_references(make_unit(body=body), repo)

        assert [v.rule for v in violations] == ["Q13"]
        assert "does not resolve" in violations[0].message

    def test_accepts_a_shortcut_reference_image_to_an_existing_file(self, repo: Path) -> None:
        """A shortcut reference image pointing to an existing file passes Q13."""
        body = "![diagram]\n\n[diagram]: reference/notes.md\n"

        assert check_path_references(make_unit(body=body), repo) == []

    def test_ignores_a_shortcut_reference_image_without_a_definition(self, repo: Path) -> None:
        """A shortcut reference image with no matching definition contributes no target."""
        body = "![diagram]\n"

        assert check_path_references(make_unit(body=body), repo) == []

    def test_ordered_list_continuation_item_interrupts_inline_code(self, repo: Path) -> None:
        """An ordered list item ``2.`` that continues a ``1.``-started list is a block boundary.

        An unterminated backtick in item 1 must not pair with a backtick in
        item 2, so the link in item 2 remains active and Q13 must report it.
        """
        unit = make_unit(body="1. `unterminated\n2. [gone](reference/missing.md)`\n")

        violations = check_path_references(unit, repo)

        assert [v.rule for v in violations] == ["Q13"]
        assert "does not resolve" in violations[0].message

    def test_nested_block_quote_keeps_multiline_code_span_in_one_block(self, repo: Path) -> None:
        """Consecutive depth-2 block-quote lines belong to one block.

        A code span may span both ``>>``-prefixed lines; the link inside it
        must not be reported by Q13 because it is inside a code span.
        """
        unit = make_unit(body=">> `[gone](reference/gone.md)\n>> continued`\n")

        assert check_path_references(unit, repo) == []

    def test_atx_heading_inside_block_quote_is_self_terminating(self, repo: Path) -> None:
        """An ATX heading inside a block quote is self-terminating.

        An unmatched backtick inside the heading must not consume the link in
        the following block-quote paragraph; Q13 must report that missing link.
        """
        unit = make_unit(body="> # heading `unmatched\n> [gone](reference/gone.md) and `closed`\n")

        violations = check_path_references(unit, repo)

        assert [v.rule for v in violations] == ["Q13"]
        assert "does not resolve" in violations[0].message

    def test_quote_depth_change_starts_new_block(self, repo: Path) -> None:
        """A change in block-quote nesting depth starts a new range.

        The backtick in the depth-2 line must not pair with any backtick in the
        depth-1 line below; Q13 must see the active link in the depth-1 line.
        """
        unit = make_unit(body=">> `unterminated\n> [gone](reference/missing.md) and `closed`\n")

        violations = check_path_references(unit, repo)

        assert [v.rule for v in violations] == ["Q13"]
        assert "does not resolve" in violations[0].message

    def test_ordered_list_starting_at_two_initialises_list_context(self, repo: Path) -> None:
        """An ordered list block that starts at item 2 must still isolate ranges.

        Item ``3.`` is a boundary, so the link in item 3 is visible to Q13 and
        must be reported.
        """
        unit = make_unit(body="2. `unterminated\n3. [gone](reference/missing.md)`\n")

        violations = check_path_references(unit, repo)

        assert [v.rule for v in violations] == ["Q13"]
        assert "does not resolve" in violations[0].message

    def test_ordered_list_after_paragraph_inherits_list_context(self, repo: Path) -> None:
        """A ``1.`` item that interrupts a paragraph starts list context.

        Item ``2.`` is then a boundary, so the link in item 2 is visible to
        Q13 and must be reported.
        """
        unit = make_unit(body="Some text\n1. `unterminated\n2. [gone](reference/missing.md)`\n")

        violations = check_path_references(unit, repo)

        assert [v.rule for v in violations] == ["Q13"]
        assert "does not resolve" in violations[0].message
