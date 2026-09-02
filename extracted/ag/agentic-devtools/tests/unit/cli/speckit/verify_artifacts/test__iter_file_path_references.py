"""Tests for the ``_iter_file_path_references()`` helper."""

from _pytest.monkeypatch import MonkeyPatch

import agentic_devtools.cli.speckit.verify_artifacts as verify_artifacts
from agentic_devtools.cli.speckit.pass_g.models import Reference, ReferenceKind
from agentic_devtools.cli.speckit.verify_artifacts import _iter_file_path_references


class TestIterFilePathReferences:
    """Filtering extracted references down to file paths."""

    def test_returns_only_file_path_references(self) -> None:
        content = "Update `agentic_devtools/cli/runner.py` and call `run_as_script()`."

        references = _iter_file_path_references(content)

        assert references
        assert all(ref.kind is ReferenceKind.FILE_PATH for ref in references)
        assert "agentic_devtools/cli/runner.py" in {ref.text for ref in references}

    def test_excludes_symbol_references(self) -> None:
        content = "Call `run_as_script()` to dispatch."

        assert _iter_file_path_references(content) == []

    def test_returns_empty_list_for_empty_content(self) -> None:
        assert _iter_file_path_references("") == []

    def test_extracts_markdown_link_destinations(self) -> None:
        content = "Write findings to [research.md](research.md)."

        references = _iter_file_path_references(content)

        assert "research.md" in {ref.text for ref in references}

    def test_extracts_empty_label_markdown_link_destinations(self) -> None:
        content = "Write findings to [](docs/research.md)."

        references = _iter_file_path_references(content)

        assert "docs/research.md" in {ref.text for ref in references}

    def test_ignores_path_like_tokens_in_markdown_link_titles_with_parentheses(self) -> None:
        content = 'See [spec](docs/spec.md "title with ) and docs/missing.md inside").'

        references = _iter_file_path_references(content)

        assert "docs/spec.md" in {ref.text for ref in references}
        assert "docs/missing.md" not in {ref.text for ref in references}

    def test_deduplicates_backtick_and_markdown_link_reference(self) -> None:
        content = "Create `research.md` and link [research.md](research.md)."

        references = _iter_file_path_references(content)

        assert [ref.text for ref in references].count("research.md") == 1

    def test_ignores_markdown_links_to_urls(self) -> None:
        content = "See [external](https://example.com/research.md)."

        assert _iter_file_path_references(content) == []

    def test_ignores_path_shaped_markdown_link_labels(self) -> None:
        content = "See [docs/missing.md](https://example.com)."

        assert _iter_file_path_references(content) == []

    def test_ignores_code_formatted_markdown_link_labels(self) -> None:
        content = "See [`docs/missing.md`](https://example.com)."

        assert _iter_file_path_references(content) == []

    def test_ignores_markdown_links_without_file_path_kind(self) -> None:
        content = "See [ticket](FR-001)."

        assert _iter_file_path_references(content) == []

    def test_includes_checkable_bare_file_reference_even_if_classifier_kind_differs(self) -> None:
        content = "Update `yarn.lock`."

        references = _iter_file_path_references(content)

        assert "yarn.lock" in {ref.text for ref in references}

    def test_skips_empty_or_duplicate_references_from_extractor(self, monkeypatch: MonkeyPatch) -> None:
        def _fake_extract_references(_content: str, *, dedup: bool = True) -> list[Reference]:
            return [
                Reference(
                    text="",
                    kind=ReferenceKind.FILE_PATH,
                    plan_location="L1",
                    context_sentence="",
                ),
                Reference(
                    text="yarn.lock",
                    kind=ReferenceKind.FILE_PATH,
                    plan_location="L2",
                    context_sentence="Update `yarn.lock`.",
                ),
                Reference(
                    text="yarn.lock",
                    kind=ReferenceKind.FILE_PATH,
                    plan_location="L3",
                    context_sentence="Update `yarn.lock` again.",
                ),
            ]

        monkeypatch.setattr(verify_artifacts, "extract_references", _fake_extract_references)

        references = _iter_file_path_references("ignored")

        assert [ref.text for ref in references] == ["yarn.lock"]

    def test_falls_back_to_clause_occurrence_zero_when_global_occurrence_exceeds_sliced_context(
        self,
        monkeypatch: MonkeyPatch,
    ) -> None:
        def _fake_extract_references(_content: str, *, dedup: bool = True) -> list[Reference]:
            return [
                Reference(
                    text="missing.py",
                    kind=ReferenceKind.FILE_PATH,
                    plan_location="L1",
                    context_sentence="For example, inspect `missing.py`.",
                ),
                Reference(
                    text="missing.py",
                    kind=ReferenceKind.FILE_PATH,
                    plan_location="L1",
                    context_sentence="Update `missing.py`.",
                ),
            ]

        monkeypatch.setattr(verify_artifacts, "extract_references", _fake_extract_references)

        refs = _iter_file_path_references("ignored", dedup=False)

        assert [ref.occurrence_index for ref in refs] == [0, 0]

    def test_extracts_bare_path_token_from_plain_prose_line(self) -> None:
        content = "Update agentic_devtools/cli/runner.py to add the new feature."

        references = _iter_file_path_references(content)

        assert "agentic_devtools/cli/runner.py" in {ref.text for ref in references}

    def test_does_not_duplicate_bare_path_already_captured_as_backtick(self) -> None:
        content = "Update `agentic_devtools/cli/runner.py` or agentic_devtools/cli/runner.py."

        references = _iter_file_path_references(content)

        assert [ref.text for ref in references].count("agentic_devtools/cli/runner.py") == 1

    def test_bare_path_scanner_skips_url_path_segments(self) -> None:
        content = "See https://example.com/path/file.md for details."

        references = _iter_file_path_references(content)

        assert not any("example.com" in ref.text for ref in references)

    def test_bare_path_scanner_skips_non_checkable_tokens(self) -> None:
        """P1/P2/P3 matches the regex but fails is_checkable_path_reference (no extension)."""
        content = "See result P1/P2/P3 for details."

        references = _iter_file_path_references(content)

        assert not any("P1" in ref.text for ref in references)

    def test_extracts_root_level_filename_from_plain_prose(self) -> None:
        content = "Update README.md to document the new gate."

        references = _iter_file_path_references(content)

        assert "README.md" in {ref.text for ref in references}

    def test_extracts_conventional_extensionless_root_filename_from_plain_prose(self) -> None:
        content = "Update Makefile to run the new validation step."

        references = _iter_file_path_references(content)

        assert "Makefile" in {ref.text for ref in references}

    def test_extracts_root_filename_with_non_whitelisted_extension_from_plain_prose(self) -> None:
        content = "Update uv.lock to keep dependencies in sync."

        references = _iter_file_path_references(content)

        assert "uv.lock" in {ref.text for ref in references}

    def test_extracts_dot_prefixed_root_filename_from_plain_prose(self) -> None:
        content = "Update .gitignore to include generated artifacts."

        references = _iter_file_path_references(content)

        assert ".gitignore" in {ref.text for ref in references}

    def test_bare_path_scanner_skips_domain_like_root_token(self) -> None:
        content = "See example.com for the external reference."

        references = _iter_file_path_references(content)

        assert "example.com" not in {ref.text for ref in references}

    def test_bare_path_scanner_skips_version_string(self) -> None:
        content = "Use Python 3.12 for this project."

        references = _iter_file_path_references(content)

        assert "3.12" not in {ref.text for ref in references}

    def test_bare_path_scanner_skips_semver_string(self) -> None:
        content = "Requires library v1.2.3 or later."

        references = _iter_file_path_references(content)

        assert "v1.2.3" not in {ref.text for ref in references}

    def test_drops_shadowed_basenames_when_full_paths_are_already_present(self) -> None:
        content = "Update `.github/workflows/ai-pr-loop.yml` and `docs/agdt-cli-reference.md`.\n"

        references = _iter_file_path_references(content)

        assert ".github/workflows/ai-pr-loop.yml" in {ref.text for ref in references}
        assert "docs/agdt-cli-reference.md" in {ref.text for ref in references}
        assert "ai-pr-loop.yml" not in {ref.text for ref in references}
        assert "agdt-cli-reference.md" not in {ref.text for ref in references}

    def test_preserves_a_real_standalone_basename_on_the_same_line(self) -> None:
        content = "Update `docs/ai-pr-loop.yml` and `loop.yml`.\n"

        references = _iter_file_path_references(content)

        assert "docs/ai-pr-loop.yml" in {ref.text for ref in references}
        assert "loop.yml" in {ref.text for ref in references}

    def test_drops_basename_that_appears_only_as_markdown_link_label(self) -> None:
        content = "Write findings to [research.md](docs/research.md).\n"

        references = _iter_file_path_references(content)

        assert "docs/research.md" in {ref.text for ref in references}
        assert "research.md" not in {ref.text for ref in references}

    def test_preserves_basename_referenced_on_a_later_line(self) -> None:
        content = "Update `docs/ai-pr-loop.yml`.\nAlso update ai-pr-loop.yml.\n"

        references = _iter_file_path_references(content)

        assert "docs/ai-pr-loop.yml" in {ref.text for ref in references}
        assert "ai-pr-loop.yml" in {ref.text for ref in references}

    def test_occurrence_index_is_clause_local_when_same_path_in_two_illustrative_clauses(self) -> None:
        # Regression: when the same path appears in two distinct illustrative
        # clauses separated by a semicolon, each Reference's occurrence_index
        # must be relative to its own sliced clause.  Before the fix, the
        # second occurrence received global index 1, which was out of range in
        # the single-match sliced clause; _is_illustrative_example_reference
        # then returned False and the illustrative reference was incorrectly
        # reported as missing.
        content = "For example, inspect `missing.py`; for example, inspect missing.py."

        refs = _iter_file_path_references(content, dedup=False)
        path_refs = [r for r in refs if r.text == "missing.py"]

        assert len(path_refs) == 2
        for ref in path_refs:
            assert ref.occurrence_index == 0, (
                f"Expected clause-local occurrence_index=0 for '{ref.context_sentence}', got {ref.occurrence_index}"
            )

    def test_fenced_illustrative_reference_gets_clause_local_occurrence_index(self) -> None:
        # Regression (comment 3): the bare-path third pass must not re-scan
        # code-fence lines that extract_references() already handled.  Before
        # the fix, the shared occurrences counter was bumped by pass 1 (fence),
        # then pass 3 re-read occurrence=1 and called
        # _reference_context_for_occurrence with a count that was out of range
        # for the single-match clause; clause_occurrences then returned index 1
        # and _is_illustrative_example_reference returned False.
        content = "```\nFor example, inspect missing.py\n```"

        refs = _iter_file_path_references(content, dedup=False)
        path_refs = [r for r in refs if r.text == "missing.py"]

        assert len(path_refs) == 1
        assert path_refs[0].occurrence_index == 0

    def test_second_link_destination_gets_non_illustrative_clause(self) -> None:
        # Regression (comment 4): when the link label contains a backtick-
        # formatted path identical to the destination, the occurrence counter
        # used to be shifted by the backtick label, causing the second
        # destination to be sliced into the first (illustrative) clause instead
        # of its own "then update" clause.
        content = "For example, inspect [`missing.py`](missing.py); then update [required](missing.py)"

        refs = _iter_file_path_references(content, dedup=False)
        path_refs = [r for r in refs if r.text == "missing.py"]

        # Two destinations must produce two References.
        assert len(path_refs) == 2
        sentences = {ref.context_sentence for ref in path_refs}
        # The second destination is after "; then update", so its clause must
        # NOT contain "for example" (i.e. it is not suppressed as illustrative).
        assert any("for example" not in s.lower() for s in sentences), (
            f"Expected at least one non-illustrative context sentence, got: {sentences}"
        )
