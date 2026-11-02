"""Unit tests for provider-verified hierarchy discovery and runtime input generation."""

from __future__ import annotations

from pathlib import Path

import pytest

from agentic_devtools.hierarchy.models import HierarchyLevel
from agentic_devtools.orchestration.hierarchy.runtime_inputs import (
    HierarchyChain,
    ProviderIssueRelationship,
    generate_runtime_hierarchy_input,
    read_runtime_hierarchy_input,
)


def _rel(
    key: str,
    parent: str | None = None,
    resolvable: bool = True,
    level: HierarchyLevel | None = None,
) -> ProviderIssueRelationship:
    return ProviderIssueRelationship(issue_key=key, parent_key=parent, resolvable=resolvable, level=level)


def test_generate_and_read_runtime_hierarchy_input_round_trip(tmp_path: Path) -> None:
    chain = HierarchyChain(subtask_key="3", feature_key="2", epic_key="1")
    path = generate_runtime_hierarchy_input(tmp_path, "run-1", chain)
    assert path.exists()
    loaded = read_runtime_hierarchy_input(path)
    assert loaded == chain


def test_read_runtime_hierarchy_input_rejects_non_object_json(tmp_path: Path) -> None:
    input_path = tmp_path / "bad.json"
    input_path.write_text("[]", encoding="utf-8")
    with pytest.raises(ValueError, match="JSON object"):
        read_runtime_hierarchy_input(input_path)
