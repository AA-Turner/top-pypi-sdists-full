"""Tests for build_branch_name."""

import pytest

from agentic_devtools.cli.git.branch_naming import build_branch_name


class TestBuildBranchName:
    """Tests for build_branch_name."""

    def test_builds_feature_branch_with_normalized_key_and_description(self):
        """Branch names use the default feature prefix, normalized key, and sanitized description."""
        assert build_branch_name("#1900", "Add focused unit tests") == "feature/1900/focused-unit-tests"

    def test_uses_implementation_when_description_sanitizes_empty(self):
        """An empty sanitized description is replaced by implementation."""
        assert build_branch_name("PROJECT-1234", "!!!") == "feature/PROJECT-1234/implementation"

    def test_uses_custom_prefix(self):
        """A caller-supplied branch prefix is used verbatim."""
        assert build_branch_name("1900", "Add tests", prefix="fix") == "fix/1900/tests"

    def test_propagates_value_error_for_bad_issue_key(self):
        """Invalid issue keys raise ValueError from normalize_issue_key."""
        with pytest.raises(ValueError):
            build_branch_name("bad/key", "Add tests")
