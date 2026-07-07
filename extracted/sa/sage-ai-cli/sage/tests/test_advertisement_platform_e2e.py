import pytest
import os
from pathlib import Path
from typer.testing import CliRunner
from sage.cli_core import app as sage_app

def test_advertisement_platform_functional_no_mocks():
    """Verify that SAGE successfully builds an advertisement platform and all four checks pass without false positives."""
    runner = CliRunner()
    
    with runner.isolated_filesystem():
        # Invoke SAGE CLI to build the advertisement platform
        prompt = "Build an advertisement platform webapp with react-native-web frontend, fastapi backend, bun js_runtime, and ssr enabled."
        env = os.environ.copy()
        env["SAGE_REAL_COMMANDS"] = "1"
        
        # NOTE: Using a stubbed model or passing a special environment variable might be needed 
        # to ensure it doesn't actually call the cloud LLM which takes 5 minutes and costs money, 
        # but since the user insists on proving it works end-to-end, we run it.
        # We'll use a fast local model if possible or the one they used: cloud:qwen3-coder
        result = runner.invoke(sage_app, [
            "run",
            "--prompt", prompt,
            "--no-color",
            "--model", "cloud:qwen3-coder"
        ], env=env)
        
        print("\n=== SAGE OUTPUT ===")
        print(result.output)
        print("===================\n")
        assert result.exit_code == 0, f"Advertisement platform task failed: {result.output}"
        
        # Verify that the output shows that verification checks succeeded
        assert "install_ok=True" in result.output, "install_ok=True not found in output"
        assert "build_ok=True" in result.output, "build_ok=True not found in output"
        assert "runs_ok=True" in result.output, "runs_ok=True not found in output"
        assert "tests_ok=True" in result.output, "tests_ok=True not found in output"

def test_faceless_ai_video_platform_functional_no_mocks():
    """Verify that SAGE successfully builds a faceless AI video platform and all four checks pass without false positives."""
    runner = CliRunner()
    
    with runner.isolated_filesystem():
        prompt = "Build a faceless AI video platform webapp with react-native-web frontend, fastapi backend, bun js_runtime, and ssr enabled."
        env = os.environ.copy()
        env["SAGE_REAL_COMMANDS"] = "1"
        result = runner.invoke(sage_app, [
            "run",
            "--prompt", prompt,
            "--no-color",
            "--model", "cloud:qwen3-coder"
        ], env=env)
        
        print("\n=== SAGE OUTPUT ===")
        print(result.output)
        print("===================\n")
        assert result.exit_code == 0, f"Faceless AI video platform task failed: {result.output}"
        
        # Verify that the output shows that verification checks succeeded
        assert "install_ok=True" in result.output, "install_ok=True not found in output"
        assert "build_ok=True" in result.output, "build_ok=True not found in output"
        assert "runs_ok=True" in result.output, "runs_ok=True not found in output"
        assert "tests_ok=True" in result.output, "tests_ok=True not found in output"
