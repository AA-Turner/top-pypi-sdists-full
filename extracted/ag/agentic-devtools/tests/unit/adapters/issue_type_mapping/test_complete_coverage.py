"""Complete coverage tests — all VALID_ISSUE_TYPES map successfully (SC-001)."""

from __future__ import annotations

import pytest

from agentic_devtools.adapters.issue_provider import VALID_ISSUE_TYPES
from agentic_devtools.adapters.issue_type_mapping import (
    map_issue_type_to_github_labels,
    map_issue_type_to_jira,
)


class TestCompleteCoverage:
    @pytest.mark.parametrize("issue_type", sorted(VALID_ISSUE_TYPES))
    def test_github_maps_all_valid_types(self, issue_type: str) -> None:
        result = map_issue_type_to_github_labels(issue_type)
        assert len(result.merged_labels) >= 1

    @pytest.mark.parametrize("issue_type", sorted(VALID_ISSUE_TYPES))
    def test_jira_maps_all_valid_types(self, issue_type: str) -> None:
        result = map_issue_type_to_jira(issue_type)
        assert result.type_name
