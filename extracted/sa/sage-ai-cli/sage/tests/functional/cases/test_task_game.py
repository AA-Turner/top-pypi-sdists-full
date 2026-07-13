"""Task Tests: Video Game Generation

Tests the generation of simple video games (Pygame, HTML5 Canvas) across
different clients and verifies them.
"""

from __future__ import annotations

import pytest
from sage.tests.functional.harnesses import run_test_with_verification

MODEL = "cloud:qwen3-coder"

class TestTaskGame:
    
    def test_cli_pygame(self):
        req = {
            "cli_request": "sage ask 'Create a simple Pygame space shooter. Include requirements.txt and main.py.' --agent",
            "description": "CLI Pygame",
        }
        res, verify = run_test_with_verification("cli", req, MODEL, language="python")
        
        assert res.exit_code == 0
        assert verify.install_ok, f"Install failed: {verify.details.get('install')}"
        assert verify.build_ok, f"Build failed: {verify.details.get('build')}"
        assert verify.run_ok, f"Run failed: {verify.details.get('run')}"
        assert verify.tests_ok, f"Tests failed: {verify.details.get('tests')}"
        
        if res.artifact_path and res.artifact_path.is_dir():
            assert (res.artifact_path / "requirements.txt").exists()
            assert (res.artifact_path / "main.py").exists()

    def test_web_html5_game(self):
        req = {
            "web_request": {"task": "Create a simple snake game using HTML5 Canvas and JavaScript in a single index.html file."},
            "description": "Web HTML5 Game",
        }
        res, verify = run_test_with_verification("web", req, MODEL)
        
        assert res.exit_code == 0
        assert verify.install_ok, f"Install failed: {verify.details.get('install')}"
        assert verify.build_ok, f"Build failed: {verify.details.get('build')}"
        assert verify.run_ok, f"Run failed: {verify.details.get('run')}"
        assert verify.tests_ok, f"Tests failed: {verify.details.get('tests')}"
        
        if res.artifact_path and res.artifact_path.is_dir():
            assert (res.artifact_path / "index.html").exists()
            content = (res.artifact_path / "index.html").read_text()
            assert "<canvas" in content.lower()
            assert "requestanimationframe" in content.lower()
