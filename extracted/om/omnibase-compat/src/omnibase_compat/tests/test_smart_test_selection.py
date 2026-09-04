# SPDX-FileCopyrightText: 2025 OmniNode.ai Inc.
# SPDX-License-Identifier: MIT
"""Unit tests for change-aware test selection (OMN-10761)."""

from __future__ import annotations

import tomllib
from pathlib import Path

import pytest

from scripts.ci.detect_test_paths import (
    collected_test_roots,
    compute_selection,
    resolve_test_paths,
)
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
    # OMN-15541: "conservative" must mean every collected root, not the
    # hardcoded ["tests/"] this used to assert — which silently excluded all
    # 141 tests under src/omnibase_compat/tests/.
    assert sel.selected_paths == collected_test_roots()


@pytest.mark.unit
def test_collected_test_roots_is_sourced_from_pyproject_testpaths() -> None:
    """OMN-15541: the selector reads testpaths; it does not carry its own list."""
    roots = collected_test_roots()
    pyproject = Path(__file__).parent.parent.parent.parent / "pyproject.toml"
    declared = tomllib.loads(pyproject.read_text(encoding="utf-8"))["tool"]["pytest"][
        "ini_options"
    ]["testpaths"]
    assert roots == [str(p).rstrip("/") + "/" for p in declared]
    # Both real roots of this repo, so a regression to one of them is caught.
    assert "tests/" in roots
    assert "src/omnibase_compat/tests/" in roots


@pytest.mark.unit
@pytest.mark.parametrize(
    ("changed_files", "ref_name", "event_name", "feature_flag_enabled"),
    [
        (["src/omnibase_compat/adapters/foo.py"], "main", "push", True),
        (
            ["src/omnibase_compat/adapters/foo.py"],
            "gh-readonly-queue/main/pr-42-abc",
            "merge_group",
            True,
        ),
        (["src/omnibase_compat/enums/some_enum.py"], "jonah/feat", "pull_request", True),
        (["src/omnibase_compat/adapters/foo.py"], "jonah/feat", "pull_request", False),
        (["src/omnibase_compat/adapters/foo.py"], "jonah/feat", "schedule", True),
    ],
    ids=["main_branch", "merge_group", "shared_module", "flag_off", "scheduled"],
)
def test_every_full_suite_escalation_covers_both_roots(
    changed_files: list[str],
    ref_name: str,
    event_name: str,
    feature_flag_enabled: bool,
) -> None:
    """OMN-15541 regression: no escalation may omit a collected test root.

    Before the fix, `_full_suite()` returned the hardcoded `["tests/"]` while
    ci.yml ran `pytest src/omnibase_compat/tests/` — two DISJOINT lists, so the
    fail-closed escalation collected 141 tests and none of the 277 under
    `tests/`, including the OMN-15373 policy gate. Asserting equality with
    `testpaths` (not merely non-emptiness) is what makes this falsifiable.
    """
    sel = compute_selection(
        changed_files=changed_files,
        adjacency_path=ADJACENCY,
        ref_name=ref_name,
        event_name=event_name,
        feature_flag_enabled=feature_flag_enabled,
    )
    assert sel.is_full_suite is True
    assert sel.selected_paths == collected_test_roots()


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
