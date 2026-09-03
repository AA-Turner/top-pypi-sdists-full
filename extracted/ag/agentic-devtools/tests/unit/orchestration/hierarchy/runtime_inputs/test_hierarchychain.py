"""Unit tests for provider-verified hierarchy discovery and runtime input generation."""

from __future__ import annotations

import pytest

from agentic_devtools.orchestration.hierarchy.runtime_inputs import (
    HierarchyChain,
)


def test_levels_found_for_epic_subtask_topology() -> None:
    chain = HierarchyChain(subtask_key="2", feature_key=None, epic_key="1")
    assert chain.levels_found == ["subtask", "epic"]


def test_hierarchy_chain_from_dict_rejects_null_subtask_key() -> None:
    with pytest.raises(ValueError, match="subtask_key"):
        HierarchyChain.from_dict({"subtask_key": None})


def test_hierarchy_chain_from_dict_rejects_empty_subtask_key() -> None:
    with pytest.raises(ValueError, match="subtask_key"):
        HierarchyChain.from_dict({"subtask_key": ""})


def test_hierarchy_chain_from_dict_rejects_whitespace_only_subtask_key() -> None:
    with pytest.raises(ValueError, match="subtask_key"):
        HierarchyChain.from_dict({"subtask_key": "   "})


def test_hierarchy_chain_from_dict_rejects_non_string_feature_key() -> None:
    with pytest.raises(ValueError, match="feature_key"):
        HierarchyChain.from_dict({"subtask_key": "3", "feature_key": 42})


def test_hierarchy_chain_from_dict_rejects_empty_feature_key() -> None:
    with pytest.raises(ValueError, match="feature_key"):
        HierarchyChain.from_dict({"subtask_key": "3", "feature_key": ""})


def test_hierarchy_chain_from_dict_rejects_non_string_epic_key() -> None:
    with pytest.raises(ValueError, match="epic_key"):
        HierarchyChain.from_dict({"subtask_key": "3", "epic_key": 99})


def test_hierarchy_chain_from_dict_rejects_whitespace_only_epic_key() -> None:
    with pytest.raises(ValueError, match="epic_key"):
        HierarchyChain.from_dict({"subtask_key": "3", "epic_key": "   "})


def test_hierarchy_chain_from_dict_rejects_string_divergence_notes() -> None:
    with pytest.raises(ValueError, match="divergence_notes"):
        HierarchyChain.from_dict({"subtask_key": "3", "divergence_notes": "not-a-list"})


def test_hierarchy_chain_from_dict_accepts_valid_chain() -> None:
    chain = HierarchyChain.from_dict({"subtask_key": "3", "feature_key": "2", "epic_key": "1", "divergence_notes": []})
    assert chain.subtask_key == "3"
    assert chain.feature_key == "2"
    assert chain.epic_key == "1"


def test_hierarchy_chain_from_dict_rejects_non_string_divergence_note() -> None:
    with pytest.raises(ValueError, match="divergence_notes\\[0\\]"):
        HierarchyChain.from_dict({"subtask_key": "3", "divergence_notes": [1]})
