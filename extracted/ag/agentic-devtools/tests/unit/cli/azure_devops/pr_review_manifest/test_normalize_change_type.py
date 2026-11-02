"""Tests for normalize_change_type."""

from agentic_devtools.cli.azure_devops.pr_review_manifest import normalize_change_type


class TestNormalizeChangeType:
    def test_add_codes(self):
        assert normalize_change_type("A") == "add"
        assert normalize_change_type("add") == "add"

    def test_delete_codes(self):
        assert normalize_change_type("D") == "delete"
        assert normalize_change_type("delete") == "delete"

    def test_rename_codes(self):
        assert normalize_change_type("R") == "rename"
        assert normalize_change_type("R100") == "rename"
        assert normalize_change_type("rename") == "rename"

    def test_edit_codes(self):
        assert normalize_change_type("M") == "edit"
        assert normalize_change_type("edit") == "edit"
        assert normalize_change_type("modify") == "edit"

    def test_empty_defaults_to_edit(self):
        assert normalize_change_type("") == "edit"
        assert normalize_change_type(None) == "edit"

    def test_unknown_defaults_to_edit(self):
        assert normalize_change_type("zzz") == "edit"
