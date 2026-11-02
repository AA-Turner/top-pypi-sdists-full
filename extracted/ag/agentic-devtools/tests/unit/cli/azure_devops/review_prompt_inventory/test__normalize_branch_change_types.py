"""Tests for _normalize_branch_change_types."""

from agentic_devtools.cli.azure_devops.review_prompt_inventory import _normalize_branch_change_types


def test_normalize_branch_change_types_handles_supported_and_invalid_values():
    assert _normalize_branch_change_types(
        {
            1: "add",
            "wrong-value": 1,
            "   ": "add",
            "new.py": " A ",
            "removed.py": "delete",
            "renamed.py": "R098",
            "edited.py": "modify",
            "ignored.py": "copy",
        }
    ) == {
        "new.py": "add",
        "removed.py": "delete",
        "renamed.py": "rename",
        "edited.py": "edit",
    }
    assert _normalize_branch_change_types(None) == {}
