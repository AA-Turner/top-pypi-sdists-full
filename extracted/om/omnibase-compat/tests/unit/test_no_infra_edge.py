# SPDX-FileCopyrightText: 2025 OmniNode.ai Inc.
# SPDX-License-Identifier: MIT

"""No-infra-edge invariant for the compat compatibility gate (OMN-12599).

Durability-plan Task 3.1: ``omnibase_compat`` must validate without importing,
installing, or resolving ``omnibase_infra``. These tests prove independence
(infra absent from the real dependency closure) AND prove the guard fires on a
synthetic infra edge, so the gate fails on coupling rather than silently passing.
"""

from __future__ import annotations

import importlib.util
from pathlib import Path
from types import ModuleType

import pytest

# Repo root is two levels up from this test file:
# tests/unit/test_no_infra_edge.py -> tests/ -> <repo_root>
REPO_ROOT = Path(__file__).resolve().parents[2]


def _load_guard() -> ModuleType:
    """Import the guard module from scripts/ without packaging it."""
    guard_path = REPO_ROOT / "scripts" / "check_no_infra_edge.py"
    spec = importlib.util.spec_from_file_location("check_no_infra_edge", guard_path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.mark.unit
@pytest.mark.timeout(30)
class TestNoInfraEdge:
    def test_real_repo_closure_has_no_infra_edge(self) -> None:
        """The shipped pyproject + uv.lock must contain no upstream omnibase edge."""
        guard = _load_guard()
        violations = guard.scan_dependency_closure(REPO_ROOT)
        assert violations == [], f"unexpected upstream edges: {violations}"

    def test_self_package_is_not_a_violation(self) -> None:
        """omnibase-compat itself appears in uv.lock and must never be flagged."""
        guard = _load_guard()
        violations = guard.scan_dependency_closure(REPO_ROOT)
        assert not any("omnibase-compat" in v for v in violations)

    def test_synthetic_pyproject_infra_dependency_fails(self, tmp_path: Path) -> None:
        """A declared omnibase_infra dependency must make the guard fail."""
        guard = _load_guard()
        (tmp_path / "pyproject.toml").write_text(
            "[project]\n"
            'name = "omnibase-compat"\n'
            'version = "0.0.0"\n'
            "dependencies = [\n"
            '    "pydantic>=2.11.7",\n'
            '    "omnibase-infra>=0.36.0",\n'
            "]\n",
            encoding="utf-8",
        )
        violations = guard.scan_dependency_closure(tmp_path)
        assert any("omnibase-infra" in v and "pyproject" in v for v in violations), (
            f"expected pyproject infra edge to fail; got {violations}"
        )

    def test_synthetic_lock_infra_package_fails(self, tmp_path: Path) -> None:
        """An omnibase_infra package resolved into uv.lock must make the guard fail."""
        guard = _load_guard()
        (tmp_path / "pyproject.toml").write_text(
            "[project]\n"
            'name = "omnibase-compat"\n'
            'version = "0.0.0"\n'
            'dependencies = ["pydantic>=2.11.7"]\n',
            encoding="utf-8",
        )
        (tmp_path / "uv.lock").write_text(
            "version = 1\n\n"
            "[[package]]\n"
            'name = "omnibase-compat"\n'
            'version = "0.0.0"\n\n'
            "[[package]]\n"
            'name = "omnibase-infra"\n'
            'version = "0.36.0"\n',
            encoding="utf-8",
        )
        violations = guard.scan_dependency_closure(tmp_path)
        assert any("omnibase-infra" in v and "uv.lock" in v for v in violations), (
            f"expected uv.lock infra edge to fail; got {violations}"
        )

    def test_underscore_name_normalization_is_caught(self, tmp_path: Path) -> None:
        """An underscore-spelled omnibase_infra edge must still be detected."""
        guard = _load_guard()
        (tmp_path / "pyproject.toml").write_text(
            "[project]\n"
            'name = "omnibase-compat"\n'
            'version = "0.0.0"\n'
            'dependencies = ["omnibase_infra>=0.36.0"]\n',
            encoding="utf-8",
        )
        violations = guard.scan_dependency_closure(tmp_path)
        assert any("omnibase-infra" in v for v in violations), (
            f"underscore-named infra edge must be caught; got {violations}"
        )

    def test_dependency_group_infra_edge_fails(self, tmp_path: Path) -> None:
        """An omnibase_infra edge hidden in a dependency-group must fail."""
        guard = _load_guard()
        (tmp_path / "pyproject.toml").write_text(
            "[project]\n"
            'name = "omnibase-compat"\n'
            'version = "0.0.0"\n'
            'dependencies = ["pydantic>=2.11.7"]\n\n'
            "[dependency-groups]\n"
            'dev = ["pytest>=8.0", "omnibase-infra>=0.36.0"]\n',
            encoding="utf-8",
        )
        violations = guard.scan_dependency_closure(tmp_path)
        assert any("omnibase-infra" in v for v in violations), (
            f"dependency-group infra edge must be caught; got {violations}"
        )

    def test_clean_synthetic_closure_passes(self, tmp_path: Path) -> None:
        """A clean compat-only closure produces zero violations."""
        guard = _load_guard()
        (tmp_path / "pyproject.toml").write_text(
            "[project]\n"
            'name = "omnibase-compat"\n'
            'version = "0.0.0"\n'
            'dependencies = ["pydantic>=2.11.7", "typing-extensions>=4.5.0"]\n',
            encoding="utf-8",
        )
        (tmp_path / "uv.lock").write_text(
            "version = 1\n\n"
            "[[package]]\n"
            'name = "omnibase-compat"\n'
            'version = "0.0.0"\n\n'
            "[[package]]\n"
            'name = "pydantic"\n'
            'version = "2.11.7"\n',
            encoding="utf-8",
        )
        violations = guard.scan_dependency_closure(tmp_path)
        assert violations == [], f"clean closure should pass; got {violations}"
