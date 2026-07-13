import pytest
import sys
import os
from pathlib import Path

# Add functional tests to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))
from sage.tests.functional.harnesses import run_test_with_verification
from sage.tests.functional.validators import validate_file

def test_file(test_case):
    # Execute the request
    result, verify = run_test_with_verification(
        channel=test_case["channel"],
        request=test_case["request"],
        model=test_case["model"]
    )

    # Basic sanity checks
    # Invalid combinations might exit non-zero, which is expected
    invalid_flag = any(
        v in [invalid_val for f in test_case["entry"].get("flags", []) for invalid_val in f["values"].get("invalid", [])]
        for v in test_case["flag_set"].values()
    )
    
    if invalid_flag:
        assert result.exit_code != 0 or not result.artifact_path, f"Expected failure for invalid flags, got success: {result.logs}"
        return
        
    assert result.exit_code == 0, f"Non-zero exit code: {result.logs}"
    assert result.artifact_path is not None and result.artifact_path.exists(), f"Artifact not created. Logs: {result.logs}"
    
    assert verify.install_ok, f"Install failed: {verify.details.get('install')}"
    assert verify.build_ok, f"Build failed: {verify.details.get('build')}"
    assert verify.run_ok, f"Run failed: {verify.details.get('run')}"
    assert verify.tests_ok, f"Tests failed: {verify.details.get('tests')}"

    # Validate according to success criteria
    validate_file(result.artifact_path, test_case["request"]["success_criteria"])
