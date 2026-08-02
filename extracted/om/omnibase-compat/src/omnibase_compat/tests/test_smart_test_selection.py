# SPDX-FileCopyrightText: 2025 OmniNode.ai Inc.
# SPDX-License-Identifier: MIT
"""Unit tests for change-aware test selection (OMN-10761)."""

from __future__ import annotations

from pathlib import Path

import pytest

from scripts.ci.detect_test_paths import compute_selection, resolve_test_paths
from scripts.ci.test_selection_models import EnumFullSuiteReason, ModelTestSelection

ADJACENCY = Path(__file__).parent.parent.parent.parent / "scripts/ci/test_selection_adjacency.yaml"


@pytest.mark.unit
def test_adjacency_yaml_loads() -> None:
    from scripts.ci.test_selection_loader import load_adjacency_map

    config = load_adjacency_map(ADJACENCY)
    assert config.schema_version == 1
    assert "enums" in config.adjacency
    assert "primitives" in config.adjacency


@pytest.mark.unit
def test_source_change_maps_to_unit_tests() -> None:
    paths = resolve_test_paths(
        ["src/omnibase_compat/adapters/some_adapter.py"],
        ADJACENCY,
    )
    assert "src/omnibase_compat/tests/adapters/" in paths


@pytest.mark.unit
def test_shared_module_change_triggers_full_suite() -> None:
    sel = compute_selection(
        changed_files=["src/omnibase_compat/enums/some_enum.py"],
        adjacency_path=ADJACENCY,
        ref_name="jonah/feature-branch",
        event_name="pull_request",
        feature_flag_enabled=True,
    )
    assert sel.is_full_suite is True
    assert sel.full_suite_reason == EnumFullSuiteReason.SHARED_MODULE


@pytest.mark.unit
def test_main_branch_triggers_full_suite() -> None:
    sel = compute_selection(
        changed_files=["src/omnibase_compat/adapters/foo.py"],
        adjacency_path=ADJACENCY,
        ref_name="main",
        event_name="push",
        feature_flag_enabled=True,
    )
    assert sel.is_full_suite is True
    assert sel.full_suite_reason == EnumFullSuiteReason.MAIN_BRANCH


@pytest.mark.unit
def test_merge_group_triggers_full_suite() -> None:
    sel = compute_selection(
        changed_files=["src/omnibase_compat/adapters/foo.py"],
        adjacency_path=ADJACENCY,
        ref_name="gh-readonly-queue/main/pr-42-abc123",
        event_name="merge_group",
        feature_flag_enabled=True,
    )
    assert sel.is_full_suite is True
    assert sel.full_suite_reason == EnumFullSuiteReason.MERGE_GROUP


@pytest.mark.unit
def test_feature_flag_off_triggers_full_suite() -> None:
    sel = compute_selection(
        changed_files=["src/omnibase_compat/adapters/foo.py"],
        adjacency_path=ADJACENCY,
        ref_name="jonah/feature-branch",
        event_name="pull_request",
        feature_flag_enabled=False,
    )
    assert sel.is_full_suite is True
    assert sel.full_suite_reason == EnumFullSuiteReason.FEATURE_FLAG_OFF


@pytest.mark.unit
def test_pyproject_change_triggers_infra_full_suite() -> None:
    sel = compute_selection(
        changed_files=["pyproject.toml"],
        adjacency_path=ADJACENCY,
        ref_name="jonah/feature-branch",
        event_name="pull_request",
        feature_flag_enabled=True,
    )
    assert sel.is_full_suite is True
    assert sel.full_suite_reason == EnumFullSuiteReason.TEST_INFRASTRUCTURE


@pytest.mark.unit
def test_leaf_module_smart_selection() -> None:
    sel = compute_selection(
        changed_files=["src/omnibase_compat/concurrency/util.py"],
        adjacency_path=ADJACENCY,
        ref_name="jonah/feature-branch",
        event_name="pull_request",
        feature_flag_enabled=True,
    )
    assert sel.is_full_suite is False
    assert sel.full_suite_reason is None
    assert any("concurrency" in p for p in sel.selected_paths)


@pytest.mark.unit
def test_unrelated_file_gets_conservative_fallback() -> None:
    sel = compute_selection(
        changed_files=["README.md"],
        adjacency_path=ADJACENCY,
        ref_name="jonah/feature-branch",
        event_name="pull_request",
        feature_flag_enabled=True,
    )
    assert sel.is_full_suite is False
    assert sel.selected_paths == ["tests/"]


@pytest.mark.unit
def test_model_test_selection_invariant() -> None:
    sel = ModelTestSelection(
        selected_paths=["tests/"],
        split_count=2,
        is_full_suite=False,
        full_suite_reason=None,
        matrix=[1, 2],
    )
    assert len(sel.matrix) == sel.split_count


@pytest.mark.unit
def test_model_test_selection_rejects_mismatched_matrix() -> None:
    with pytest.raises(ValueError):
        ModelTestSelection(
            selected_paths=["tests/"],
            split_count=2,
            is_full_suite=False,
            full_suite_reason=None,
            matrix=[1],  # wrong length
        )
