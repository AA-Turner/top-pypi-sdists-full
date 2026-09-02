"""Tests for the ``_has_standalone_reference_on_line()`` helper."""

from agentic_devtools.cli.speckit.verify_artifacts import _has_standalone_reference_on_line


class TestHasStandaloneReferenceOnLine:
    def test_backtick_reference_returns_true(self) -> None:
        assert _has_standalone_reference_on_line("Update `file.md`.", "file.md")

    def test_markdown_link_destination_returns_true(self) -> None:
        assert _has_standalone_reference_on_line("See [text](file.md).", "file.md")

    def test_markdown_link_empty_label_destination_returns_true(self) -> None:
        assert _has_standalone_reference_on_line("See [](file.md).", "file.md")

    def test_boundary_word_in_prose_returns_true(self) -> None:
        assert _has_standalone_reference_on_line("Update file.md now.", "file.md")

    def test_link_label_only_returns_false(self) -> None:
        assert not _has_standalone_reference_on_line("[file.md](docs/file.md)", "file.md")

    def test_embedded_in_slash_path_returns_false(self) -> None:
        assert not _has_standalone_reference_on_line("See docs/file.md.", "file.md")

    def test_markdown_link_title_with_parenthesis_does_not_create_standalone_match(self) -> None:
        line = 'See [spec](docs/spec.md "title with ) and docs/missing.md inside").'

        assert not _has_standalone_reference_on_line(line, "docs/missing.md")
