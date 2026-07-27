"""Task Tests: Code Generation in 25 Languages

Tests code generation for a wide variety of programming languages.
"""

from __future__ import annotations

import pytest
from sage.tests.functional.harnesses import run_test_with_verification

MODEL = "cloud:qwen3-coder"

LANGUAGES = [
    ("python", ".py"), ("go", ".go"), ("rust", ".rs"), ("java", ".java"),
    ("javascript", ".js"), ("typescript", ".ts"), ("c++", ".cpp"), ("c#", ".cs"),
    ("swift", ".swift"), ("kotlin", ".kt"), ("ruby", ".rb"), ("php", ".php"),
    ("perl", ".pl"), ("dart", ".dart"), ("scala", ".scala"), ("elixir", ".ex"),
    ("haskell", ".hs"), ("clojure", ".clj"), ("r", ".r"), ("lua", ".lua"),
    ("fortran", ".f90"), ("cobol", ".cob"), ("pascal", ".pas"), ("ada", ".adb"),
    ("lisp", ".lisp"),
]

class TestTaskCodeLanguages:
    
    @pytest.mark.parametrize("lang,ext", LANGUAGES)
    def test_cli_language_fibonacci(self, lang, ext):
        req = {
            "cli_request": f"sage ask 'Write a fibonacci function in {lang} and save it to fib{ext} and stop' --agent",
            "description": f"CLI Code {lang}",
        }
        res, verify = run_test_with_verification("cli", req, MODEL, language=lang)
        
        assert res.exit_code == 0
        assert verify.install_ok, f"Install failed: {verify.details.get('install')}"
        assert verify.build_ok, f"Build failed: {verify.details.get('build')}"
        assert verify.run_ok, f"Run failed: {verify.details.get('run')}"
        assert verify.tests_ok, f"Tests failed: {verify.details.get('tests')}"
        
        if res.artifact_path and res.artifact_path.is_dir():
            files = list(res.artifact_path.rglob(f"*{ext}"))
            assert files, f"No {ext} file found for {lang}"
            content = files[0].read_text().lower()
            assert "fib" in content or "function" in content or "func" in content or "def " in content or "fn " in content
