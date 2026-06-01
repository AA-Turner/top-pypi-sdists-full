"""Tests for domain.files module."""

import pytest
from bacore.domain.files import MarkdownFile, TOMLFile
from pathlib import Path

pytestmark = pytest.mark.domain


def test_markdown_file(fixt_dir_with_files):
    readme_file = fixt_dir_with_files / "readme.md"
    content = MarkdownFile(path=readme_file, skip_title=False).read()
    assert (
        content
        == """# BACore ReadMe File

    This is some markdown content.

    ## With sub-heading

    - and some
    - bullets

    End of file.
    """
    )


def test_markdown_file_without_title(fixt_dir_with_files):
    readme_file = fixt_dir_with_files / "readme.md"
    content = MarkdownFile(path=readme_file, skip_title=True).read()
    assert (
        content
        == """This is some markdown content.

    ## With sub-heading

    - and some
    - bullets

    End of file.
    """
    )


class TestTOMLFile:
    """Tests for TOML entity."""

    def test_path(self, fixt_dir_with_files):
        """Test path."""
        toml_file = TOMLFile(path=fixt_dir_with_files / "pyproject.toml")
        assert isinstance(toml_file.path, Path)

    def test_data_to_dict(self, fixt_dir_with_files):
        """Test toml_file_content."""
        content = TOMLFile(path=fixt_dir_with_files / "pyproject.toml")
        assert isinstance(content.data_to_dict(), dict)
