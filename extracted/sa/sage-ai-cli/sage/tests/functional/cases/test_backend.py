import pytest
import sys
import os
from pathlib import Path

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))
from sage.tests.functional.harnesses import run_test
from sage.tests.functional.validators import validate_file

def test_backend(test_case):
    result = run_test(
        channel=test_case["channel"],
        request=test_case["request"],
        model=test_case["model"]
    )

    invalid_flag = any(
        v in [invalid_val for f in test_case["entry"].get("flags", []) for invalid_val in f["values"].get("invalid", [])]
        for v in test_case["flag_set"].values()
    )
    
    if invalid_flag:
        assert result.exit_code != 0 or not result.artifact_path, f"Expected failure for invalid flags, got success: {result.logs}"
        return
        
    assert result.exit_code == 0, f"Non-zero exit code: {result.logs}"
    assert result.artifact_path is not None and result.artifact_path.exists(), f"Artifact not created. Logs: {result.logs}"

    validate_file(result.artifact_path, test_case["request"]["success_criteria"])
