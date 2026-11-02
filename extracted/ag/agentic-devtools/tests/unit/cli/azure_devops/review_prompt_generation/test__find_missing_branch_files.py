"""Tests for _find_missing_branch_files."""

from agentic_devtools.cli.azure_devops.review_prompt_generation import _find_missing_branch_files


def test_returns_missing_paths_with_normalized_metadata() -> None:
    missing, change_types, rename_sources = _find_missing_branch_files(
        [{"path": "/src/known.py"}],
        {"/src/known.py", "/src/new.py"},
        {"src/known.py", "src/new.py"},
        {"/src/new.py": "add"},
        {"/src/new.py": "/src/old.py"},
    )

    assert missing == ["/src/new.py"]
    assert change_types == {"src/new.py": "add"}
    assert rename_sources == {"src/new.py": "/src/old.py"}
