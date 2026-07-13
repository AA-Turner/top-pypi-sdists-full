"""Task Tests: Mobile App Generation

Tests the generation of mobile app boilerplates (React Native, Flutter) across
different clients and verifies them.
"""

from __future__ import annotations

import pytest
from sage.tests.functional.harnesses import run_test_with_verification

MODEL = "cloud:qwen3-coder"

class TestTaskMobile:
    
    def test_cli_react_native(self):
        req = {
            "cli_request": "sage ask 'Create a React Native app boilerplate with a package.json and an App.js that displays a fitness tracker UI.' --agent",
            "description": "CLI React Native",
        }
        res, verify = run_test_with_verification("cli", req, MODEL)
        
        assert res.exit_code == 0
        assert verify.install_ok, f"Install failed: {verify.details.get('install')}"
        assert verify.build_ok, f"Build failed: {verify.details.get('build')}"
        assert verify.run_ok, f"Run failed: {verify.details.get('run')}"
        assert verify.tests_ok, f"Tests failed: {verify.details.get('tests')}"
        
        if res.artifact_path and res.artifact_path.is_dir():
            assert (res.artifact_path / "package.json").exists()
            assert (res.artifact_path / "App.js").exists() or (res.artifact_path / "App.tsx").exists()

    def test_sms_flutter(self):
        req = {
            "sms_request": "@run Create a Flutter weather app boilerplate with a pubspec.yaml and a main.dart.",
            "description": "SMS Flutter",
        }
        res, verify = run_test_with_verification("sms", req, MODEL, language="dart")
        
        assert res.exit_code == 0
        assert verify.install_ok, f"Install failed: {verify.details.get('install')}"
        assert verify.build_ok, f"Build failed: {verify.details.get('build')}"
        assert verify.run_ok, f"Run failed: {verify.details.get('run')}"
        assert verify.tests_ok, f"Tests failed: {verify.details.get('tests')}"
        
        if res.artifact_path and res.artifact_path.is_dir():
            assert (res.artifact_path / "pubspec.yaml").exists()
            # Dart code might be in lib/
            dart_files = list(res.artifact_path.rglob("*.dart"))
            assert dart_files
