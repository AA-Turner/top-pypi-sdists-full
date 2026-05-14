"""Tests for dep_resolver.

The resolver turns a ProjectPlan + feature list into pinned dependency
files. Hard invariants:

  - Python backends ALWAYS emit both requirements.txt AND pyproject.toml
    with the same dep union (the user explicitly demanded this).
  - Known libraries are pinned to CURRENT_VERSIONS from
    principal_engineer (defeats stale LLM knowledge).
  - Duplicate deps across features are deduplicated.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Callable

import pytest

from sage.core.dep_resolver import (
    DepSet,
    emit_node_package_json,
    emit_python_dep_files,
    parse_deps_json,
    resolve_dependencies,
)
from sage.core.spec_decomposer import Feature, ProjectPlan, StackProfile


def _stub_gen(responses: list[str]) -> Callable[[str], str]:
    iterator = iter(responses)
    return lambda _: next(iterator, "")


def _plan(features: list[Feature], **stack_kwargs) -> ProjectPlan:
    return ProjectPlan(
        title="t",
        features=features,
        stack=StackProfile(**stack_kwargs),
    )


class TestParseDepsJson:
    def test_parses_object_with_keys(self) -> None:
        raw = json.dumps({"python": ["fastapi", "sqlmodel"], "node": ["axios"]})
        deps = parse_deps_json(raw)
        assert "fastapi" in deps["python"]
        assert "axios" in deps["node"]

    def test_returns_empty_on_garbage(self) -> None:
        deps = parse_deps_json("garbage")
        assert deps == {"python": [], "node": []}

    def test_extracts_from_prose(self) -> None:
        raw = "Sure, here:\n```json\n" + json.dumps({"python": ["x"]}) + "\n```"
        assert "x" in parse_deps_json(raw)["python"]


class TestResolveDependencies:
    def test_baseline_python_backend_includes_framework(self) -> None:
        plan = _plan(
            [Feature(name="auth", description="x", layer="backend", acceptance=[])],
            backend="fastapi",
        )
        # Even with no LLM response, the resolver MUST include the framework
        # because the stack baseline ships with it.
        dep_set = resolve_dependencies(plan, _stub_gen(["", "", ""]))
        assert any("fastapi" in p for p in dep_set.python_runtime)

    def test_baseline_react_native_web_includes_expo(self) -> None:
        plan = _plan(
            [Feature(name="x", description="y", layer="frontend", acceptance=[])],
            frontend="react-native-web",
        )
        dep_set = resolve_dependencies(plan, _stub_gen(["", "", ""]))
        assert any("expo" in p for p in dep_set.node_runtime)

    def test_pins_known_python_lib_from_current_versions(self) -> None:
        plan = _plan([], backend="fastapi")
        dep_set = resolve_dependencies(plan, _stub_gen(["", "", ""]))
        # fastapi is in CURRENT_VERSIONS["python"] → must be pinned
        fastapi_specs = [p for p in dep_set.python_runtime if p.startswith("fastapi")]
        assert fastapi_specs
        assert "==" in fastapi_specs[0]

    def test_llm_adds_feature_deps(self) -> None:
        # Feature LLM responses → adds redis + celery to backend
        responses = [
            json.dumps({"python": ["redis", "celery"], "node": []}),
        ]
        plan = _plan(
            [Feature(name="queue", description="x", layer="backend", acceptance=[])],
            backend="fastapi",
        )
        dep_set = resolve_dependencies(plan, _stub_gen(responses))
        assert any("redis" in p for p in dep_set.python_runtime)
        assert any("celery" in p for p in dep_set.python_runtime)

    def test_deduplicates_across_features(self) -> None:
        responses = [
            json.dumps({"python": ["redis"], "node": []}),
            json.dumps({"python": ["redis"], "node": []}),
        ]
        plan = _plan(
            [
                Feature(name="a", description="x", layer="backend", acceptance=[]),
                Feature(name="b", description="x", layer="backend", acceptance=[]),
            ],
            backend="fastapi",
        )
        dep_set = resolve_dependencies(plan, _stub_gen(responses))
        redis_count = sum(1 for p in dep_set.python_runtime if p.startswith("redis"))
        assert redis_count == 1


class TestEmitFiles:
    def test_emits_both_requirements_and_pyproject(self, tmp_path: Path) -> None:
        backend_root = tmp_path / "backend"
        backend_root.mkdir()
        dep_set = DepSet(
            python_runtime=["fastapi==0.115.6", "redis==5.0.1"],
            python_dev=["pytest==8.3.4"],
            node_runtime=[],
            node_dev=[],
        )
        emit_python_dep_files(dep_set, backend_root, project_name="test-app")
        req = (backend_root / "requirements.txt").read_text()
        pyproj = (backend_root / "pyproject.toml").read_text()
        # Both must contain the same runtime deps
        assert "fastapi==0.115.6" in req
        assert "fastapi==0.115.6" in pyproj
        assert "redis==5.0.1" in req
        assert "redis==5.0.1" in pyproj
        # Dev deps live in pyproject's optional-dependencies
        assert "pytest==8.3.4" in pyproj
        # Sanity: pyproject is TOML-parseable
        import tomllib
        parsed = tomllib.loads(pyproj)
        assert parsed["project"]["name"] == "test-app"

    def test_requirements_txt_is_sorted_and_deduped(self, tmp_path: Path) -> None:
        backend_root = tmp_path / "backend"
        backend_root.mkdir()
        dep_set = DepSet(
            python_runtime=["b==1.0", "a==1.0", "b==1.0"],
            python_dev=[],
            node_runtime=[],
            node_dev=[],
        )
        emit_python_dep_files(dep_set, backend_root, project_name="x")
        lines = (backend_root / "requirements.txt").read_text().strip().splitlines()
        # Sorted + deduped
        assert lines.count("b==1.0") == 1
        assert lines.index("a==1.0") < lines.index("b==1.0")

    def test_emits_package_json_with_scripts(self, tmp_path: Path) -> None:
        frontend_root = tmp_path / "frontend"
        frontend_root.mkdir()
        dep_set = DepSet(
            python_runtime=[],
            python_dev=[],
            node_runtime=["expo@^52.0.0", "react@18.3.1"],
            node_dev=["jest@^29.7.0"],
        )
        emit_node_package_json(
            dep_set, frontend_root, framework="react-native-web", project_name="myapp"
        )
        pkg = json.loads((frontend_root / "package.json").read_text())
        assert pkg["name"] == "myapp"
        # Scripts the user explicitly asked for: install/test/typecheck/lint
        assert "test" in pkg["scripts"]
        assert "typecheck" in pkg["scripts"]
        assert "lint" in pkg["scripts"]
        # Deps included
        assert "expo" in pkg["dependencies"]
        assert "jest" in pkg["devDependencies"]
