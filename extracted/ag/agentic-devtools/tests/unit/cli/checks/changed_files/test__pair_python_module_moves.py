"""Tests for pairing removed content with new source modules."""

from unittest.mock import patch

from agentic_devtools.cli.checks.changed_files import _pair_python_module_moves


def test_pairs_only_content_backed_addition(tmp_path):
    (tmp_path / "new.py").write_text("def load():\n    tasks = []\n    return tasks\n", encoding="utf-8")
    (tmp_path / "unrelated.py").write_text("other = 1\n", encoding="utf-8")
    with patch(
        "agentic_devtools.cli.checks.changed_files._removed_python_lines",
        return_value={"def load():", "tasks = []", "return tasks"},
    ):
        assert _pair_python_module_moves(
            ["old.py"], ["new.py", "unrelated.py"], ["git", "diff"], "main...HEAD", tmp_path
        ) == {("old.py", "new.py")}
