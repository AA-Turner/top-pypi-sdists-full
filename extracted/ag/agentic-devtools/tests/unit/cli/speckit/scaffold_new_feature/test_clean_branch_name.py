"""Tests for ``clean_branch_name``."""

from agentic_devtools.cli.speckit.scaffold_new_feature import clean_branch_name


def test_clean_branch_name_removes_non_alnum_chars() -> None:
    assert clean_branch_name("Add user auth!!!") == "add-user-auth"
