"""Tests for _load_recovered_file_diff."""

from types import SimpleNamespace
from unittest.mock import patch

from agentic_devtools.cli.azure_devops.review_prompt_generation import _load_recovered_file_diff


def test_loads_line_metadata_and_text_patch() -> None:
    info = SimpleNamespace(
        added=SimpleNamespace(is_binary=False, lines=[SimpleNamespace(line_number=5, content="+line")]),
        removed=SimpleNamespace(is_binary=False, lines=[SimpleNamespace(line_number=2, content="-line")]),
    )
    with (
        patch("agentic_devtools.cli.azure_devops.review_prompt_generation.get_diff_lines_info", return_value=info),
        patch("agentic_devtools.cli.azure_devops.review_prompt_generation.get_diff_patch", return_value="patch"),
    ):
        result = _load_recovered_file_diff("src/file.py", "origin/main", "src/file.py")

    assert result == (
        False,
        [{"line": 5, "content": "+line"}],
        [{"line": 2, "content": "-line"}],
        "patch",
    )
