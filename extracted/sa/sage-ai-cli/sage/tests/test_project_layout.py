"""Tests for the project_layout module.

The layout module is the *only* place that knows about directory
conventions. The invariants it enforces are exactly the bugs the user
flagged:

  - Frontend lives under `frontend/`, NEVER mixed at the project root.
  - Backend lives under `backend/`, NEVER mixed at the project root.
  - `.github/workflows/` lives ONLY at the project root, NEVER nested
    inside `frontend/` or `backend/`.
  - Python projects always pair `requirements.txt` and `pyproject.toml`.
"""

from __future__ import annotations

import pytest

from sage.core.project_layout import (
    LayoutPlan,
    assign_paths,
    plan_layout,
)
from sage.core.spec_decomposer import Feature, ProjectPlan, StackProfile


def _make_plan(
    features: list[Feature],
    *,
    frontend: str | None = None,
    backend: str | None = None,
    database: str | None = None,
) -> ProjectPlan:
    return ProjectPlan(
        title="test",
        features=features,
        stack=StackProfile(frontend=frontend, backend=backend, database=database),
    )


class TestLayoutInvariants:
    def test_frontend_files_live_under_frontend_dir(self) -> None:
        plan = _make_plan(
            [Feature(name="login", description="x", layer="frontend", acceptance=[])],
            frontend="react",
            backend="fastapi",
        )
        layout = plan_layout(plan)
        front_files = [f for f in layout.files if f.path.startswith("frontend/")]
        assert front_files, "frontend feature must produce files under frontend/"
        # Critical: every file tied to a frontend feature must live under frontend/.
        for f in layout.files:
            if f.feature == "login":
                assert f.path.startswith("frontend/"), (
                    f"frontend feature file {f.path!r} must live under frontend/"
                )

    def test_backend_files_live_under_backend_dir(self) -> None:
        plan = _make_plan(
            [Feature(name="auth", description="x", layer="backend", acceptance=[])],
            frontend="react",
            backend="fastapi",
        )
        layout = plan_layout(plan)
        back_files = [f for f in layout.files if f.path.startswith("backend/")]
        assert back_files

    def test_github_only_at_root_never_nested(self) -> None:
        plan = _make_plan(
            [
                Feature(name="auth", description="x", layer="backend", acceptance=[]),
                Feature(name="login", description="x", layer="frontend", acceptance=[]),
            ],
            frontend="react",
            backend="fastapi",
        )
        layout = plan_layout(plan)
        # This is the exact bug the user flagged. Backend has its own CI,
        # frontend has its own — must NEVER produce nested .github/ dirs.
        for f in layout.files:
            assert "/.github/" not in f.path, (
                f"nested .github not allowed: {f.path}"
            )
            assert not f.path.startswith("backend/.github/"), f.path
            assert not f.path.startswith("frontend/.github/"), f.path

    def test_root_ci_workflow_exists(self) -> None:
        plan = _make_plan(
            [Feature(name="auth", description="x", layer="backend", acceptance=[])],
            backend="fastapi",
        )
        layout = plan_layout(plan)
        paths = [f.path for f in layout.files]
        assert ".github/workflows/ci.yml" in paths

    def test_python_backend_has_both_requirements_and_pyproject(self) -> None:
        plan = _make_plan(
            [Feature(name="auth", description="x", layer="backend", acceptance=[])],
            backend="fastapi",
        )
        layout = plan_layout(plan)
        paths = [f.path for f in layout.files]
        # Both must exist — the spec calls this out as a hard invariant
        # because Docker/CI workflows may expect either format.
        assert "backend/requirements.txt" in paths
        assert "backend/pyproject.toml" in paths

    def test_node_frontend_has_package_json(self) -> None:
        plan = _make_plan(
            [Feature(name="login", description="x", layer="frontend", acceptance=[])],
            frontend="react",
        )
        layout = plan_layout(plan)
        paths = [f.path for f in layout.files]
        assert "frontend/package.json" in paths

    def test_root_files_present(self) -> None:
        plan = _make_plan(
            [Feature(name="auth", description="x", layer="backend", acceptance=[])],
            backend="fastapi",
        )
        layout = plan_layout(plan)
        paths = [f.path for f in layout.files]
        assert "README.md" in paths
        assert ".gitignore" in paths
        assert ".env.example" in paths


class TestAssignPaths:
    def test_backend_feature_gets_api_and_test_paths(self) -> None:
        paths = assign_paths(
            Feature(name="campaigns", description="x", layer="backend", acceptance=["x"]),
            backend="fastapi",
            frontend=None,
        )
        path_strs = [p[0] for p in paths]
        assert any("backend/app/api/campaigns" in p for p in path_strs)
        # TDD: test file paired with impl
        assert any("backend/tests/test_campaigns" in p for p in path_strs)

    def test_frontend_feature_gets_screen_and_test(self, monkeypatch) -> None:
        monkeypatch.delenv("SAGE_TESTING", raising=False)
        paths = assign_paths(
            Feature(name="login", description="x", layer="frontend", acceptance=["x"]),
            backend=None,
            frontend="react-native-web",
        )
        path_strs = [p[0] for p in paths]
        # RN+Web uses expo-router → app/login.tsx
        assert any("frontend/app/" in p and "login" in p for p in path_strs)
        assert any("frontend/__tests__/" in p and "login" in p for p in path_strs)

    def test_react_web_uses_src_directory(self) -> None:
        paths = assign_paths(
            Feature(name="login", description="x", layer="frontend", acceptance=["x"]),
            backend=None,
            frontend="react",
        )
        path_strs = [p[0] for p in paths]
        assert any("frontend/src/" in p for p in path_strs)

    def test_unknown_backend_falls_back_safely(self) -> None:
        # Unknown framework must NOT crash — produces a generic layout.
        paths = assign_paths(
            Feature(name="x", description="y", layer="backend", acceptance=[]),
            backend="some-future-framework",
            frontend=None,
        )
        assert paths  # must produce at least one file


class TestLayoutPlanShape:
    def test_layout_plan_has_root_directories(self) -> None:
        plan = _make_plan(
            [Feature(name="x", description="y", layer="backend", acceptance=[])],
            backend="fastapi",
            frontend="react",
        )
        layout = plan_layout(plan)
        assert "frontend" in layout.directories
        assert "backend" in layout.directories

    def test_no_files_lie_outside_planned_directories(self) -> None:
        plan = _make_plan(
            [
                Feature(name="auth", description="x", layer="backend", acceptance=[]),
                Feature(name="login", description="x", layer="frontend", acceptance=[]),
            ],
            backend="fastapi",
            frontend="react",
        )
        layout = plan_layout(plan)
        allowed_prefixes = {"frontend/", "backend/", ".github/", "docs/"}
        for f in layout.files:
            # Files at the project root are OK (README, .gitignore, etc.)
            if "/" not in f.path:
                continue
            assert any(f.path.startswith(p) for p in allowed_prefixes), (
                f"file outside allowed dirs: {f.path}"
            )
