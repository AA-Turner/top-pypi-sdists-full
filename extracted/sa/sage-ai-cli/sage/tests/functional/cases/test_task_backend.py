"""Task Tests: Backend System Generation

Tests the generation of REST APIs and database integrations across
different clients and verifies them using the 4-gate system.
"""

from __future__ import annotations

import pytest
from sage.tests.functional.harnesses import run_test_with_verification

MODEL = "cloud:gemini-flash"

class TestTaskBackend:
    
    def test_cli_fastapi(self):
        req = {
            "cli_request": "sage ask 'Create a FastAPI REST API with SQLite for managing users. Include requirements.txt and a test_main.py.' --agent",
            "description": "CLI FastAPI",
        }
        res, verify = run_test_with_verification("cli", req, MODEL, language="python")
        
        assert res.exit_code == 0
        assert verify.install_ok, f"Install failed: {verify.details.get('install')}"
        assert verify.build_ok, f"Build failed: {verify.details.get('build')}"
        assert verify.run_ok, f"Run failed: {verify.details.get('run')}"
        assert verify.tests_ok, f"Tests failed: {verify.details.get('tests')}"
        
        if res.artifact_path:
            project_dir = res.artifact_path if res.artifact_path.is_dir() else res.artifact_path.parent
            assert (project_dir / "requirements.txt").exists(), "requirements.txt missing"
            assert list(project_dir.glob("*.py")), "No python files found"

    def test_sms_express(self):
        req = {
            "sms_request": "@run Create an Express.js API with a package.json and a health check route in app.js.",
            "description": "SMS Express",
        }
        res, verify = run_test_with_verification("sms", req, MODEL, language="javascript")
        
        assert res.exit_code == 0
        assert verify.install_ok, f"Install failed: {verify.details.get('install')}"
        assert verify.build_ok, f"Build failed: {verify.details.get('build')}"
        assert verify.run_ok, f"Run failed: {verify.details.get('run')}"
        assert verify.tests_ok, f"Tests failed: {verify.details.get('tests')}"
        
        if res.artifact_path:
            project_dir = res.artifact_path if res.artifact_path.is_dir() else res.artifact_path.parent
            assert (project_dir / "package.json").exists(), "package.json missing"
            assert (project_dir / "app.js").exists() or (project_dir / "index.js").exists(), "Entrypoint missing"

    def test_web_go_gin(self):
        req = {
            "web_request": {"task": "Create a Go API using Gin with a go.mod file. Include a main.go."},
            "description": "Web Go Gin",
        }
        res, verify = run_test_with_verification("web", req, MODEL, language="go")
        
        assert res.exit_code == 0
        assert verify.install_ok, f"Install failed: {verify.details.get('install')}"
        assert verify.build_ok, f"Build failed: {verify.details.get('build')}"
        assert verify.run_ok, f"Run failed: {verify.details.get('run')}"
        assert verify.tests_ok, f"Tests failed: {verify.details.get('tests')}"
        
        if res.artifact_path:
            project_dir = res.artifact_path if res.artifact_path.is_dir() else res.artifact_path.parent
            assert (project_dir / "go.mod").exists(), "go.mod missing"
            assert list(project_dir.glob("*.go")), "No go files found"
