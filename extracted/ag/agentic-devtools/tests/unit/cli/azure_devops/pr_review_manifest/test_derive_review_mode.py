"""Tests for derive_review_mode."""

from agentic_devtools.cli.azure_devops.pr_review_manifest import derive_review_mode


class TestDeriveReviewMode:
    def test_deleted(self):
        assert derive_review_mode("D", False, 0, 0) == "deleted"

    def test_deleted_takes_precedence_over_binary(self):
        assert derive_review_mode("delete", True, 0, 0) == "deleted"

    def test_binary(self):
        assert derive_review_mode("M", True, 5, 0) == "binary"

    def test_renamed_with_no_changes(self):
        assert derive_review_mode("R", False, 0, 0) == "renamed"

    def test_rename_with_changes_is_diff(self):
        assert derive_review_mode("R", False, 2, 0) == "diff"

    def test_metadata_only(self):
        assert derive_review_mode("M", False, 0, 0) == "metadata-only"

    def test_none_line_counts_treated_as_zero(self):
        assert derive_review_mode("M", False, None, None) == "metadata-only"

    def test_diff(self):
        assert derive_review_mode("M", False, 3, 1) == "diff"
