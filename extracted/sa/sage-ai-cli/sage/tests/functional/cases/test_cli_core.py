import pytest
import os
import sys
from pathlib import Path

# Add functional tests to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))
from sage.tests.functional.harnesses import run_test_with_verification

MODEL = "cloud:qwen3-coder"

@pytest.mark.timeout(300)
def test_cli_basic_code_generation():
    req = {
        "cli_request": "sage ask 'Write a python script hello.py that prints hello and stop'",
        "success_criteria": {"extension": ".py", "contains": "print", "type": "code"}
    }
    result, verify = run_test_with_verification("cli", req, MODEL)
    assert result.exit_code == 0
    assert result.artifact_path and result.artifact_path.exists()
    assert ".py" in result.artifact_path.name
    assert "print" in result.artifact_path.read_text()

@pytest.mark.timeout(300)
def test_cli_asset_generation():
    req = {
        "cli_request": "sage ask 'generate a simple SVG image of a red circle and save it as circle.svg and stop'",
        "success_criteria": {"extension": ".svg", "type": "document"}
    }
    result, verify = run_test_with_verification("cli", req, MODEL)
    assert result.exit_code == 0
    assert result.artifact_path and result.artifact_path.exists()
    assert ".svg" in result.artifact_path.name
    with open(result.artifact_path, "r") as f:
        assert "<svg" in f.read().lower()

@pytest.mark.timeout(300)
def test_cli_file_generation_document():
    req = {
        "cli_request": "sage ask 'create a text file doc.txt with the exact content important data and stop'",
        "success_criteria": {"extension": ".txt", "contains": "important data"}
    }
    result, verify = run_test_with_verification("cli", req, MODEL)
    assert result.exit_code == 0
    assert result.artifact_path and result.artifact_path.exists()
    assert "important data" in result.artifact_path.read_text()
