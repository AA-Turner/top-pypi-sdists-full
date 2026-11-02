"""Tests for substantive move-comparison lines."""

from agentic_devtools.cli.checks.changed_files import _python_content_lines


def test_excludes_blank_comment_and_import_lines():
    assert _python_content_lines("\n# comment\nimport os\nfrom os import path\n return tasks\n") == {"return tasks"}
