"""Smoke tests for principal_builder — the end-to-end orchestrator."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Callable
from unittest.mock import patch

import pytest

from sage.core.principal_builder import build_project_principal


def _stub_gen() -> Callable[[str], str]:
    def gen(prompt: str) -> str:
        if "decomposing a software" in prompt.lower():
            return json.dumps([
                {"name": "auth_system", "description": "JWT auth",
                 "layer": "backend",
                 "acceptance": ["POST /auth/login returns JWT"]},
                {"name": "user_dashboard", "description": "Main dashboard UI",
                 "layer": "frontend",
                 "acceptance": ["Renders KPI cards"]},
            ])
        if "choosing the technical stack" in prompt.lower():
            return json.dumps(
                {"frontend": "react-native-web", "backend": "fastapi",
                 "database": "postgres", "cache": "redis", "queue": "celery"}
            )
        if "list the packages" in prompt.lower():
            return json.dumps({"python": [], "node": []})
        if "score each criterion" in prompt.lower():
            return json.dumps({"score": 8.0, "gaps": [], "notes": "ok"})
        # All file-generation prompts get a tiny non-empty body
        return "# generated\npass\n"
    return gen


class TestPrincipalBuilderSmoke:
    def test_writes_full_principal_layout(self, tmp_path: Path) -> None:
        """Smoke: principal builder produces architecture + multi-file features."""
        from sage.core.code_doctors import DoctorReport
        from sage.core.integrity_pass import IntegrityReport
        with patch(
            "sage.core.principal_builder._verify_iterate_until_green",
            return_value=[],
        ), patch(
            "sage.core.principal_builder.run_bootstrap",
            return_value=[],  # skip real CLI scaffolders in tests
        ), patch(
            "sage.core.principal_builder.run_code_doctors",
            return_value=DoctorReport(),  # skip mechanical fixers in test
        ), patch(
            "sage.core.principal_builder.run_integrity_pass",
            return_value=IntegrityReport(),  # skip ruff+LLM repair in tests
        ):
            report = build_project_principal(
                "Build a FastAPI + RN Web auth + dashboard app",
                tmp_path,
                _stub_gen(),
                progress=lambda _: None,
                enable_review=False,  # skip review in smoke test
                enable_heal=False,    # stub-generated code can't pass real install
            )

        # Layout invariants
        assert (tmp_path / "frontend").is_dir()
        assert (tmp_path / "backend").is_dir()
        assert (tmp_path / ".github" / "workflows" / "ci.yml").is_file()
        assert not (tmp_path / "backend" / ".github").exists()

        # Architecture modules MUST be present (this is the big upgrade)
        assert (tmp_path / "backend" / "app" / "db" / "base.py").is_file()
        assert (tmp_path / "backend" / "app" / "db" / "session.py").is_file()
        assert (tmp_path / "backend" / "app" / "auth" / "dependencies.py").is_file()
        assert (tmp_path / "backend" / "app" / "core" / "config.py").is_file()
        assert (tmp_path / "backend" / "app" / "core" / "exceptions.py").is_file()
        assert (tmp_path / "backend" / "app" / "middleware" / "rate_limit.py").is_file()
        assert (tmp_path / "backend" / "app" / "ai" / "client.py").is_file()
        assert (tmp_path / "backend" / "app" / "tasks" / "celery_app.py").is_file()
        assert (tmp_path / "backend" / "worker.py").is_file()
        assert (tmp_path / "backend" / "alembic.ini").is_file()

        # Multi-file per feature (auth_system → 8+ files)
        assert (tmp_path / "backend" / "app" / "models" / "auth.py").is_file() or \
               (tmp_path / "backend" / "app" / "models" / "auth_system.py").is_file()
        assert (tmp_path / "backend" / "app" / "schemas").is_dir()
        assert (tmp_path / "backend" / "app" / "repositories").is_dir()
        assert (tmp_path / "backend" / "app" / "services").is_dir()
        assert (tmp_path / "backend" / "app" / "api" / "v1").is_dir()

        # Frontend infra
        assert (tmp_path / "frontend" / "src" / "shared" / "api.ts").is_file()
        assert (tmp_path / "frontend" / "src" / "shared" / "auth.tsx").is_file()
        assert (tmp_path / "frontend" / "src" / "components" / "ui" / "Button.tsx").is_file()
        assert (tmp_path / "frontend" / "app" / "_layout.tsx").is_file()

        # Multi-file per frontend feature
        assert (tmp_path / "frontend" / "src" / "components" / "dashboard").is_dir() or \
               (tmp_path / "frontend" / "src" / "components" / "user_dashboard").is_dir()

        # Deployment artifacts
        assert (tmp_path / "deploy" / "k8s" / "backend.yaml").is_file()
        assert (tmp_path / "deploy" / "terraform" / "main.tf").is_file()

        # Reports persisted
        assert (tmp_path / ".sage" / "PROJECT_PLAN.json").is_file()
        assert (tmp_path / ".sage" / "BUILD_REPORT.json").is_file()

        assert report.feature_count == 2
