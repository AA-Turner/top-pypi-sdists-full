"""Verification Checks Meta-Tests

Tests the 4-gate verification system itself to ensure it correctly identifies
passing and failing codebase constraints.
"""

from __future__ import annotations

import tempfile
import json
from pathlib import Path

from sage.tests.functional.validators import (
    validate_install,
    validate_build,
    validate_run,
    validate_tests
)

class TestVerificationMeta:
    
    def test_validate_install_success(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            p = Path(tmpdir)
            (p / "package.json").write_text(json.dumps({"name": "test"}))
            # Just having the manifest is enough for validate_install (it checks if it CAN be installed)
            res = validate_install(p, "javascript")
            assert res is True
            
    def test_validate_install_failure(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            p = Path(tmpdir)
            res = validate_install(p, "javascript")
            assert res is False
            
    def test_validate_run_python(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            p = Path(tmpdir)
            main_file = p / "main.py"
            main_file.write_text("print('hello')\n")
            
            res = validate_run(p, "python")
            assert res is True
            
    def test_validate_run_failure(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            p = Path(tmpdir)
            main_file = p / "main.py"
            main_file.write_text("import missing_module\n")
            
            res = validate_run(p, "python")
            assert res is False

    def test_validate_tests_python(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            p = Path(tmpdir)
            test_file = p / "test_main.py"
            test_file.write_text("def test_ok():\n    assert True\n")
            
            res = validate_tests(p, "python")
            assert res is True
            
    def test_validate_tests_failure(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            p = Path(tmpdir)
            test_file = p / "test_main.py"
            test_file.write_text("def test_fail():\n    assert False\n")
            
            res = validate_tests(p, "python")
            assert res is False
