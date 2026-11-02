"""Tests for _load_branch_file_metadata."""

import json

from agentic_devtools.cli.azure_devops.review_prompt_inventory import _load_branch_file_metadata


def test_load_branch_file_metadata_returns_empty_defaults_when_missing(tmp_path):
    assert _load_branch_file_metadata(tmp_path, {"given.py"}) == ({"given.py"}, {}, {}, None)


def test_load_branch_file_metadata_loads_inventory_and_normalizes_values(tmp_path):
    inventory_path = tmp_path / "files-on-branch.json"
    inventory_path.write_text(
        json.dumps(
            {
                "files": ["inventory.py"],
                "change_types": {"inventory.py": "edit"},
                "rename_sources": {"new.py": "old.py"},
                "diff_base_ref": " origin/develop ",
            }
        ),
        encoding="utf-8",
    )
    assert _load_branch_file_metadata(tmp_path, None) == (
        {"inventory.py"},
        {"inventory.py": "edit"},
        {"new.py": "old.py"},
        "origin/develop",
    )
    assert _load_branch_file_metadata(tmp_path, {"caller.py"}) == (
        {"caller.py"},
        {"inventory.py": "edit"},
        {"new.py": "old.py"},
        "origin/develop",
    )


def test_load_branch_file_metadata_treats_invalid_diff_refs_as_missing(tmp_path):
    inventory_path = tmp_path / "files-on-branch.json"
    for diff_base_ref in (None, "   "):
        inventory_path.write_text(json.dumps({"files": [], "diff_base_ref": diff_base_ref}), encoding="utf-8")
        assert _load_branch_file_metadata(tmp_path, None) == (set(), {}, {}, None)
