import pytest
import os
import shutil
import tempfile
from pathlib import Path
from typer.testing import CliRunner
from sage.cli_core import app as sage_app

@pytest.fixture
def real_commands_env(monkeypatch):
    """Ensure SAGE runs with real commands and real cloud LLM instead of mocks."""
    # Use SAGE_DISABLE_LLM_MOCK=1 so auth/billing skips still apply but LLM is real
    monkeypatch.setenv("SAGE_DISABLE_LLM_MOCK", "1")
    monkeypatch.setenv("SAGE_TESTING", "1")    # Force real commands
    monkeypatch.setenv("SAGE_REAL_COMMANDS", "1")
    # For local test against the cloud model
    monkeypatch.setenv("SAGE_API_BASE", "http://127.0.0.1:8091")
    
def test_advertisement_platform_functional_no_mocks(real_commands_env):
    """Verify that SAGE successfully builds an advertisement platform and all four checks pass strictly."""
    runner = CliRunner()
    
    with runner.isolated_filesystem():
        prompt = "Build an advertisement platform webapp with react-native-web frontend, fastapi backend, bun js_runtime, and ssr enabled."
        # We invoke SAGE to run against the cloud LLM using qwen3-coder
        result = runner.invoke(sage_app, [
            "run",
            "--prompt", prompt,
            "--no-color",
            "--model", "cloud:qwen3-coder"
        ])
        
        print("\n=== SAGE OUTPUT ===")
        print(result.output)
        print("===================\n")
        assert result.exit_code == 0, f"Advertisement platform task failed: {result.output}"
        
        # Verify that the output shows that verification checks succeeded
        assert "install_ok=True" in result.output, "install_ok=True not found in output"
        assert "build_ok=True" in result.output, "build_ok=True not found in output"
        assert "runs_ok=True" in result.output, "runs_ok=True not found in output"
        assert "tests_ok=True" in result.output, "tests_ok=True not found in output"

def test_faceless_ai_video_platform_functional_no_mocks(real_commands_env):
    """Verify that SAGE successfully builds a faceless AI video platform and all four checks pass strictly."""
    runner = CliRunner()
    
    with runner.isolated_filesystem():
        prompt = "Build a faceless AI video platform webapp with react-native-web frontend, fastapi backend, bun js_runtime, and ssr enabled."
        result = runner.invoke(sage_app, [
            "run",
            "--prompt", prompt,
            "--no-color",
            "--model", "cloud:qwen3-coder"
        ])
        
        print("\n=== SAGE OUTPUT ===")
        print(result.output)
        print("===================\n")
        assert result.exit_code == 0, f"Faceless AI video platform task failed: {result.output}"
        
        # Verify that the output shows that verification checks succeeded
        assert "install_ok=True" in result.output, "install_ok=True not found in output"
        assert "build_ok=True" in result.output, "build_ok=True not found in output"
        assert "runs_ok=True" in result.output, "runs_ok=True not found in output"
        assert "tests_ok=True" in result.output, "tests_ok=True not found in output"
