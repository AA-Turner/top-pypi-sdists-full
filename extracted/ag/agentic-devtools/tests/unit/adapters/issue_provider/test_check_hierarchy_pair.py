"""Tests for the module-level ``check_hierarchy_pair`` function (issue #2118)."""

from __future__ import annotations

import pytest

from agentic_devtools.adapters.exceptions import AdapterValidationError
from agentic_devtools.adapters.issue_provider import check_hierarchy_pair


class TestCheckHierarchyPair:
    """The shared module-level pair check used by every provider."""

    @pytest.mark.parametrize(
        "child,parent",
        [("feature", "epic"), ("subtask", "feature"), ("task", "epic"), ("bug", "epic")],
    )
    def test_valid_pairs_pass(self, child, parent):
        assert check_hierarchy_pair(child, parent) is None

    def test_is_case_insensitive(self):
        assert check_hierarchy_pair("Feature", "Epic") is None

    @pytest.mark.parametrize(
        "child,parent",
        [("feature", "feature"), ("epic", "feature"), ("epic", "subtask"), ("task", "bug")],
    )
    def test_invalid_pairs_raise(self, child, parent):
        with pytest.raises(AdapterValidationError):
            check_hierarchy_pair(child, parent)

    def test_unsupported_child_raises(self):
        with pytest.raises(AdapterValidationError, match="child"):
            check_hierarchy_pair("saga", "epic")

    def test_unsupported_parent_raises(self):
        with pytest.raises(AdapterValidationError, match="parent"):
            check_hierarchy_pair("feature", "saga")
