"""Tests for _collect_current_files."""

from agentic_devtools.cli.azure_devops.review_prompt_tracking import _collect_current_files


def test_collects_nonempty_normalized_pr_file_paths() -> None:
    result = _collect_current_files(
        {"files": [{"path": "/src/a.py"}, {"path": ""}, {"path": "/src/b.py"}]},
        lambda path: path.lower() if path else None,
    )

    assert result == {"/src/a.py", "/src/b.py"}
