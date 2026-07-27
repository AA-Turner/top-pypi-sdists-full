"""Tests for the dynamic_builder orchestrator.

These tests use stub generators so they run without any LLM. They
verify the pipeline wiring, not the LLM output quality.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Callable
from unittest.mock import patch

import pytest

from sage.core.dynamic_builder import build_project_dynamic


def _make_stub_generator(
    features_response: str | None = None,
    stack_response: str | None = None,
    deps_response: str = '{"python": [], "node": []}',
    default_content: str = "# stub\npass\n",
) -> Callable[[str], str]:
    """Return a generate() that responds to each prompt type appropriately."""

    def gen(prompt: str) -> str:
        if "decomposing" in prompt.lower() or "decompose a software" in prompt.lower():
            return features_response or json.dumps(
                [
                    {
                        "name": "health",
                        "description": "Health check endpoint",
                        "layer": "backend",
                        "acceptance": ["GET /health returns 200"],
                    }
                ]
            )
        if "choosing the technical stack" in prompt.lower():
            return stack_response or json.dumps(
                {"frontend": None, "backend": "fastapi", "database": None}
            )
        if "list the packages required" in prompt.lower():
            return deps_response
        if "write a failing test" in prompt.lower():
            return "def test_x():\n    assert True\n"
        if "fix" in prompt.lower() and "json" in prompt.lower():
            return "{}"
        # default impl response
        return default_content

    return gen


class TestBuildProjectDynamicSmoke:
    def test_writes_layout_files(self, tmp_path: Path) -> None:
        """Smoke test: pipeline produces frontend/ + backend/ + root .github/."""
        # Skip the expensive verify pass for this smoke test
        with patch("sage.core.dynamic_builder._verify_iterate_until_green", return_value=[]):
            report = build_project_dynamic(
                "Build a FastAPI + React Native Web auth app",
                tmp_path,
                _make_stub_generator(
                    features_response=json.dumps(
                        [
                            {
                                "name": "login",
                                "description": "login screen",
                                "layer": "frontend",
                                "acceptance": ["renders email + password fields"],
                            },
                            {
                                "name": "auth",
                                "description": "JWT auth",
                                "layer": "backend",
                                "acceptance": ["POST /auth/login returns JWT"],
                            },
                        ]
                    ),
                    stack_response=json.dumps(
                        {"frontend": "react-native-web", "backend": "fastapi"}
                    ),
                ),
                progress=lambda _: None,
                enable_tdd_loop=False,
            )

        # The user's two big invariants
        assert (tmp_path / "frontend").is_dir()
        assert (tmp_path / "backend").is_dir()
        assert (tmp_path / ".github" / "workflows" / "ci.yml").is_file()
        # No nested .github
        assert not (tmp_path / "backend" / ".github").exists()
        assert not (tmp_path / "frontend" / ".github").exists()
        # Both Python dep files
        assert (tmp_path / "backend" / "requirements.txt").is_file()
        assert (tmp_path / "backend" / "pyproject.toml").is_file()
        # package.json for the frontend
        assert (tmp_path / "frontend" / "package.json").is_file()
        # Build report persisted
        assert (tmp_path / ".sage" / "BUILD_REPORT.json").is_file()
        assert (tmp_path / ".sage" / "PROJECT_PLAN.json").is_file()
        # Report shape
        assert report.title
        assert report.feature_count == 2

    def test_15_section_spec_produces_features_per_section(self, tmp_path: Path) -> None:
        """If the LLM returns 15 features, the build emits files for ALL 15.

        This is the user's core complaint: a 15-section spec must not
        collapse into 2 generic auth files.
        """
        big_features = [
            {
                "name": f"feature_{i}",
                "description": f"Feature number {i}",
                "layer": "backend" if i % 2 == 0 else "frontend",
                "acceptance": [f"feature_{i} works"],
            }
            for i in range(1, 16)
        ]
        gen = _make_stub_generator(
            features_response=json.dumps(big_features),
            stack_response=json.dumps(
                {"frontend": "react-native-web", "backend": "fastapi"}
            ),
        )
        import os
        old_val = os.environ.pop("SAGE_TESTING", None)
        try:
            with patch("sage.core.dynamic_builder._verify_iterate_until_green", return_value=[]):
                report = build_project_dynamic(
                    "Build a platform with 15 features",
                    tmp_path,
                    gen,
                    progress=lambda _: None,
                    enable_tdd_loop=False,
                )
        
            plan_file = json.loads((tmp_path / ".sage" / "PROJECT_PLAN.json").read_text())
            assert len(plan_file["features"]) == 15
            # Every feature must produce at least one impl file under its layer
            for feat in plan_file["features"]:
                slug = feat["name"]
                layer_dir = tmp_path / feat["layer"]
                matches = list(layer_dir.rglob(f"*{slug}*"))
                assert matches, f"no files generated for feature {slug}"
        finally:
            if old_val is not None:
                os.environ["SAGE_TESTING"] = old_val
