"""Tests for _normalize_branch_rename_sources."""

from agentic_devtools.cli.azure_devops.review_prompt_inventory import _normalize_branch_rename_sources


def test_normalize_branch_rename_sources_skips_invalid_paths():
    assert _normalize_branch_rename_sources(
        {
            1: "old.py",
            "wrong-value": 2,
            "  ": "old.py",
            "new.py": "  ",
            r"new\file.py": r"old\file.py",
        }
    ) == {"new/file.py": "old/file.py"}
    assert _normalize_branch_rename_sources([]) == {}
