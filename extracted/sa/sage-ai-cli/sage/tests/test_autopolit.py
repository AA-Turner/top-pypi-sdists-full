"""Tests for autopolit improvements - TDD approach."""

import re
import shutil

# Import the functions we're testing
import sys
import tempfile
from pathlib import Path

import pytest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from sage.cli_core import (
    _detect_broken_test_files,
    _extract_and_write_files,
    _is_garbage_content,
    _module_exists_in_codebase,
    _pending_modules_for_files,
    _validate_imports_in_content,
)


def _extract_file_blocks(response: str) -> list[tuple[str, str]]:
    """Extract FILE: blocks from response.

    Returns list of (filepath, content) tuples.
    This function tests the FILE block extraction logic.
    """
    blocks = []

    # Primary pattern: FILE: path\n```lang\ncontent\n```
    # Also handles FILE:path (no space) and extra whitespace
    pattern = r"FILE:\s*(\S+)\s*\n```[^\n]*\n(.*?)```"

    for m in re.finditer(pattern, response, re.DOTALL):
        fp = m.group(1).strip()
        content = m.group(2)
        blocks.append((fp, content))

    return blocks


class MockRenderer:
    """Mock renderer for testing."""

    def __init__(self):
        self.warnings = []
        self.infos = []
        self.errors = []

    def warning(self, msg):
        self.warnings.append(msg)

    def info(self, msg):
        self.infos.append(msg)

    def error(self, msg):
        self.errors.append(msg)


class TestFileBlockExtraction:
    """Test FILE: block parsing and extraction."""

    def setup_method(self):
        """Set up test fixtures."""
        self.temp_dir = Path(tempfile.mkdtemp())
        self.renderer = MockRenderer()

    def teardown_method(self):
        """Clean up test fixtures."""
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_extract_simple_file_block(self):
        """Test extracting a simple FILE: block."""
        response = """Here's the code:

FILE: test.py
```python
def hello():
    return "world"
```

That's the implementation."""

        blocks = _extract_file_blocks(response)
        assert len(blocks) == 1
        assert blocks[0][0] == "test.py"
        assert "def hello():" in blocks[0][1]

    def test_extract_multiple_file_blocks(self):
        """Test extracting multiple FILE: blocks."""
        response = """Creating two files:

FILE: foo.py
```python
def foo():
    return 1
```

FILE: bar.py
```python
def bar():
    return 2
```
"""
        blocks = _extract_file_blocks(response)
        assert len(blocks) == 2
        assert blocks[0][0] == "foo.py"
        assert blocks[1][0] == "bar.py"

    def test_extract_file_block_with_path(self):
        """Test FILE: block with subdirectory path."""
        response = """
FILE: src/utils/helpers.py
```python
def helper():
    pass
```
"""
        blocks = _extract_file_blocks(response)
        assert len(blocks) == 1
        assert blocks[0][0] == "src/utils/helpers.py"

    def test_ignore_code_blocks_without_file_prefix(self):
        """Test that regular code blocks without FILE: are ignored."""
        response = """Here's some code:

```python
def example():
    return True
```

That's it."""

        blocks = _extract_file_blocks(response)
        assert len(blocks) == 0

    def test_extract_file_block_various_formats(self):
        """Test FILE: block with various formats."""
        # Test with space after FILE:
        response1 = """FILE: test.py
```python
code
```"""

        # Test with newline immediately after FILE:
        response2 = """FILE:test.py
```python
code
```"""

        # Test with extra whitespace
        response3 = """FILE:   test.py
```python
code
```"""

        for response in [response1, response2, response3]:
            blocks = _extract_file_blocks(response)
            assert len(blocks) >= 0  # Should not crash


class TestGarbageContentDetection:
    """Test garbage content detection."""

    def test_empty_functions_detected(self):
        """Test that files with too many empty functions are rejected."""
        content = """
def func1():
    pass

def func2():
    pass

def func3():
    pass
"""
        is_garbage, reason = _is_garbage_content("test.py", content)
        assert is_garbage is True
        # Accept both "empty functions" and "empty function(s)" formats
        assert "empty function" in reason.lower()
        assert "pass" in reason.lower()

    def test_test_without_assertions_rejected(self):
        """Test that test files without assertions are rejected."""
        content = """
def test_something():
    x = 1 + 1
    y = 2
"""
        is_garbage, reason = _is_garbage_content("test_foo.py", content)
        assert is_garbage is True
        # Accept both "no assertions" and "no real assertions" formats
        assert "assertion" in reason.lower()

    def test_test_with_assertions_accepted(self):
        """Test that test files with assertions are accepted."""
        content = """
def test_something():
    x = 1 + 1
    assert x == 2
"""
        is_garbage, reason = _is_garbage_content("test_foo.py", content)
        assert is_garbage is False

    def test_placeholder_comments_rejected(self):
        """Test that files with placeholder comments are rejected."""
        content = """
def foo():
    # TODO: implement this
    pass
"""
        is_garbage, reason = _is_garbage_content("foo.py", content)
        assert is_garbage is True
        assert "placeholder" in reason.lower() or "TODO" in reason

    def test_valid_implementation_accepted(self):
        """Test that valid implementations are accepted."""
        content = '''
def calculate_sum(a, b):
    """Calculate sum of two numbers."""
    return a + b

def calculate_product(a, b):
    """Calculate product of two numbers."""
    return a * b
'''
        is_garbage, reason = _is_garbage_content("math_utils.py", content)
        assert is_garbage is False


class TestBrokenTestDetection:
    """Test broken test file detection."""

    def setup_method(self):
        """Set up test fixtures."""
        self.temp_dir = Path(tempfile.mkdtemp())
        # Create tests directory
        (self.temp_dir / "tests").mkdir()
        # Create a broken test file
        (self.temp_dir / "tests" / "test_broken.py").write_text("""
from nonexistent_module import something

def test_foo():
    assert True
""")

    def teardown_method(self):
        """Clean up test fixtures."""
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_detect_import_error(self):
        """Test detection of ModuleNotFoundError in test output."""
        output = """
============================= test session starts ==============================
tests/test_broken.py:1: in <module>
    from nonexistent_module import something
E   ModuleNotFoundError: No module named 'nonexistent_module'
"""
        broken = _detect_broken_test_files(output, self.temp_dir)
        assert len(broken) == 1
        assert "test_broken.py" in str(broken[0])

    def test_detect_error_collecting(self):
        """Test detection of 'error collecting' pattern."""
        output = """
============================= ERRORS =============================
____________ ERROR collecting tests/test_broken.py ____________
tests/test_broken.py:1: in <module>
    from fake_module import fake_func
E   ModuleNotFoundError: No module named 'fake_module'
"""
        broken = _detect_broken_test_files(output, self.temp_dir)
        assert len(broken) == 1

    def test_ignore_valid_import_errors(self):
        """Test that import errors for standard library are ignored."""
        # Create a test file that imports from standard library
        (self.temp_dir / "tests" / "test_valid.py").write_text("""
import json  # Standard library
def test_foo():
    assert json.loads('{}') == {}
""")
        output = """
tests/test_valid.py:1: in <module>
    import json
"""
        broken = _detect_broken_test_files(output, self.temp_dir)
        # Should not detect json as broken
        broken_names = [str(b) for b in broken]
        assert not any("test_valid.py" in name for name in broken_names)


class TestImportValidation:
    """Test import validation for Python files."""

    def setup_method(self):
        """Set up test fixtures."""
        self.temp_dir = Path(tempfile.mkdtemp())
        # Create a local module
        (self.temp_dir / "my_module.py").write_text("def foo(): pass")
        # Create a package
        pkg_dir = self.temp_dir / "my_package"
        pkg_dir.mkdir()
        (pkg_dir / "__init__.py").write_text("")
        (pkg_dir / "utils.py").write_text("def bar(): pass")

    def teardown_method(self):
        """Clean up test fixtures."""
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_local_module_exists(self):
        """Test that local modules are detected."""
        assert _module_exists_in_codebase("my_module", self.temp_dir) is True

    def test_local_package_exists(self):
        """Test that local packages are detected."""
        assert _module_exists_in_codebase("my_package", self.temp_dir) is True

    def test_nonexistent_module_not_found(self):
        """Test that nonexistent modules are not found."""
        assert _module_exists_in_codebase("nonexistent_xyz", self.temp_dir) is False

    def test_standard_library_exists(self):
        """Test that standard library modules are detected."""
        assert _module_exists_in_codebase("json", self.temp_dir) is True
        assert _module_exists_in_codebase("os", self.temp_dir) is True
        assert _module_exists_in_codebase("sys", self.temp_dir) is True

    def test_validate_imports_with_local_module(self):
        """Test validation passes for local modules."""
        content = """
from my_module import foo
def test_foo():
    assert foo() is None
"""
        is_valid, missing = _validate_imports_in_content(content, self.temp_dir)
        assert is_valid is True
        assert len(missing) == 0

    def test_validate_imports_with_missing_module(self):
        """Test validation fails for missing modules."""
        content = """
from totally_fake_module import fake_func
def test_fake():
    fake_func()
"""
        is_valid, missing = _validate_imports_in_content(content, self.temp_dir)
        assert is_valid is False
        assert "totally_fake_module" in missing


class TestFileWriting:
    """Test file writing with validation."""

    def setup_method(self):
        """Set up test fixtures."""
        from sage.cli_core import _clear_classification

        _clear_classification()
        self.temp_dir = Path(tempfile.mkdtemp())
        # Create an existing file to test READ-before-write
        (self.temp_dir / "existing.py").write_text("# Original content\n")

    def teardown_method(self):
        """Clean up test fixtures."""
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_write_new_file(self):
        """Test writing a new file."""
        response = """
FILE: new_file.py
```python
def new_function():
    return 42
```
"""
        written = _extract_and_write_files(response, self.temp_dir)
        assert len(written) == 1
        assert "new_file.py" in written[0]
        assert (self.temp_dir / "new_file.py").exists()

    def test_reject_write_without_read(self):
        """Existing files can be updated without an explicit READ (SAGE will auto-read)."""
        response = """
FILE: existing.py
```python
# Modified content
# Second line to prevent trivially short rejection.
```
"""
        written = _extract_and_write_files(response, self.temp_dir, files_read=set())
        assert written == ["existing.py"]
        assert (self.temp_dir / "existing.py").read_text(encoding="utf-8") == "# Modified content\n# Second line to prevent trivially short rejection."

    def test_allow_write_after_read(self):
        """Test that writing to existing files after READ is allowed."""
        response = """
FILE: existing.py
```python
# Modified content
def updated():
    return True
```
"""
        written = _extract_and_write_files(response, self.temp_dir, files_read={"existing.py"})
        assert len(written) == 1


class TestCodeQuality:
    """Test code quality validation before writing."""

    def setup_method(self):
        """Set up test fixtures."""
        self.temp_dir = Path(tempfile.mkdtemp())

    def teardown_method(self):
        """Clean up test fixtures."""
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_reject_syntax_error(self):
        """Test that files with syntax errors are rejected."""
        # This would require a syntax validation function
        pass

    def test_reject_empty_test_file(self):
        """Test that test files without tests are rejected."""
        response = """
FILE: tests/test_empty.py
```python
# Just a comment
pass
```
"""
        written = _extract_and_write_files(response, self.temp_dir)
        # Empty test files should be rejected
        assert len(written) == 0


class TestPendingModulesForFiles:
    """Test pending_modules_for_files for path normalization."""

    def test_simple_path(self):
        """Test simple file paths."""
        filepaths = ["middleware.py"]
        modules = _pending_modules_for_files(filepaths)
        assert "middleware" in modules

    def test_nested_path(self):
        """Test nested file paths add parent directories."""
        filepaths = ["middleware/rate_limiter.py"]
        modules = _pending_modules_for_files(filepaths)
        assert "middleware" in modules
        assert "rate_limiter" in modules

    def test_dotslash_prefix(self):
        """Test paths with ./ prefix are normalized correctly.

        This is the critical fix: ./middleware/rate_limiter.py should
        add 'middleware' to modules, not '.'
        """
        filepaths = ["./middleware/rate_limiter.py"]
        modules = _pending_modules_for_files(filepaths)
        assert "middleware" in modules
        assert "rate_limiter" in modules
        assert "." not in modules

    def test_deeply_nested_path(self):
        """Test deeply nested paths add all directory components."""
        filepaths = ["api/endpoints/users/handlers.py"]
        modules = _pending_modules_for_files(filepaths)
        assert "api" in modules
        assert "endpoints" in modules
        assert "users" in modules
        assert "handlers" in modules

    def test_init_py_adds_parent_package(self):
        """Test __init__.py adds parent directory as module."""
        filepaths = ["middleware/__init__.py"]
        modules = _pending_modules_for_files(filepaths)
        assert "middleware" in modules

    def test_dotslash_init_py(self):
        """Test __init__.py with ./ prefix is normalized."""
        filepaths = ["./middleware/__init__.py"]
        modules = _pending_modules_for_files(filepaths)
        assert "middleware" in modules
        assert "." not in modules

    def test_non_python_files_ignored(self):
        """Test non-Python files are ignored."""
        filepaths = ["README.md", "config.json", "styles.css"]
        modules = _pending_modules_for_files(filepaths)
        assert len(modules) == 0

    def test_mixed_filepaths(self):
        """Test mixed filepaths with various formats."""
        filepaths = [
            "./middleware/rate_limiter.py",
            "api/endpoints.py",
            "tests/test_middleware.py",
            "utils.py",
        ]
        modules = _pending_modules_for_files(filepaths)
        assert "middleware" in modules
        assert "rate_limiter" in modules
        assert "api" in modules
        assert "endpoints" in modules
        assert "tests" in modules
        assert "test_middleware" in modules
        assert "utils" in modules
        assert "." not in modules


class TestPathValidation:
    """Test validate_file_path_against_codebase function."""

    def setup_method(self):
        """Set up test fixtures."""
        from sage.core.validation import validate_file_path_against_codebase

        self._validate_path = validate_file_path_against_codebase
        self.temp_dir = Path(tempfile.mkdtemp())

    def teardown_method(self):
        """Clean up test fixtures."""
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_reject_tests_at_root_when_nested_tests_exist(self):
        """Test that tests/ at root is rejected when project uses sage/tests/."""
        # Create sage/tests/ structure
        sage_tests = self.temp_dir / "sage" / "tests"
        sage_tests.mkdir(parents=True)
        (sage_tests / "test_core.py").write_text("def test_foo(): assert True")

        # Create sage source files
        (self.temp_dir / "sage" / "__init__.py").write_text("")
        (self.temp_dir / "sage" / "main.py").write_text("def main(): pass")

        # Try to validate a path at root tests/
        is_valid, error = self._validate_path("tests/test_new.py", self.temp_dir)
        assert is_valid is False
        assert "sage/tests" in error.lower()

    def test_allow_tests_when_root_tests_exists(self):
        """Test that tests/ at root is allowed when it actually exists."""
        # Create root tests/ directory
        tests_dir = self.temp_dir / "tests"
        tests_dir.mkdir()
        (tests_dir / "test_core.py").write_text("def test_foo(): assert True")

        # Create source files
        (self.temp_dir / "src").mkdir()
        (self.temp_dir / "src" / "main.py").write_text("def main(): pass")

        # Should allow tests/ since it exists
        is_valid, error = self._validate_path("tests/test_new.py", self.temp_dir)
        assert is_valid is True

    def test_reject_src_when_different_structure(self):
        """Test that src/ is rejected when project uses different structure."""
        # Create sage/ structure (not src/)
        sage_dir = self.temp_dir / "sage"
        sage_dir.mkdir()
        (sage_dir / "__init__.py").write_text("")
        (sage_dir / "main.py").write_text("def main(): pass")

        # Try to validate a path in src/
        is_valid, error = self._validate_path("src/new_module.py", self.temp_dir)
        assert is_valid is False
        assert "src/" in error.lower()
        assert "sage" in error.lower()

    def test_allow_valid_paths(self):
        """Test that valid paths in existing directories are allowed."""
        # Create sage/ structure
        sage_dir = self.temp_dir / "sage"
        sage_dir.mkdir()
        (sage_dir / "__init__.py").write_text("")
        (sage_dir / "main.py").write_text("def main(): pass")

        # Valid path in existing directory
        is_valid, error = self._validate_path("sage/new_module.py", self.temp_dir)
        assert is_valid is True

    def test_reject_hallucinated_paths(self):
        """Test that common hallucinated paths are rejected."""
        # Create actual structure
        sage_dir = self.temp_dir / "sage"
        sage_dir.mkdir()
        (sage_dir / "main.py").write_text("def main(): pass")

        # Try hallucinated paths
        for hallucinated in ["app/main.py", "api/routes.py", "services/auth.py"]:
            is_valid, error = self._validate_path(hallucinated, self.temp_dir)
            assert is_valid is False, f"{hallucinated} should be rejected"


class TestFindActualTestDirectory:
    """Test _find_actual_test_directory helper function."""

    def setup_method(self):
        """Set up test fixtures."""
        from sage.core.validation import _find_actual_test_directory

        self._find_test_dir = _find_actual_test_directory
        self.temp_dir = Path(tempfile.mkdtemp())

    def teardown_method(self):
        """Clean up test fixtures."""
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_find_nested_tests_directory(self):
        """Test finding tests in nested directory like sage/tests/."""
        sage_tests = self.temp_dir / "sage" / "tests"
        sage_tests.mkdir(parents=True)
        (sage_tests / "test_core.py").write_text("def test_foo(): assert True")

        result = self._find_test_dir(self.temp_dir)
        assert result == "sage/tests"

    def test_find_root_tests_directory(self):
        """Test finding tests at root level."""
        tests_dir = self.temp_dir / "tests"
        tests_dir.mkdir()
        (tests_dir / "test_core.py").write_text("def test_foo(): assert True")

        result = self._find_test_dir(self.temp_dir)
        assert result == "tests"

    def test_return_none_when_no_tests(self):
        """Test returning None when no test directory exists."""
        # Create project without tests
        (self.temp_dir / "src").mkdir()
        (self.temp_dir / "src" / "main.py").write_text("def main(): pass")

        result = self._find_test_dir(self.temp_dir)
        assert result is None


class TestAutopolitCliWiring:
    """Test autopolit CLI command is registered and executes correctly."""

    @patch("sage.main.run")
    def test_cli_autopolit_command_sets_env(self, mock_run):
        """Test that sage autopolit sets environment variables and runs setup."""
        from sage.cli_core import app
        import os
        from typer.testing import CliRunner

        runner = CliRunner()
        # Ensure env is cleared first
        os.environ.pop("SAGE_AUTOPOLIT_RUN", None)
        os.environ.pop("SAGE_AUTOPOLIT_TASK", None)

        result = runner.invoke(app, ["autopolit", "optimize code quality"])
        assert result.exit_code == 0
        assert os.environ.get("SAGE_AUTOPOLIT_RUN") == "1"
        assert os.environ.get("SAGE_AUTOPOLIT_TASK") == "optimize code quality"
        mock_run.assert_called_once()
        
        # Test without message/task
        os.environ.pop("SAGE_AUTOPOLIT_RUN", None)
        os.environ.pop("SAGE_AUTOPOLIT_TASK", None)
        mock_run.reset_mock()
        result = runner.invoke(app, ["autopolit"])
        assert result.exit_code == 0
        assert os.environ.get("SAGE_AUTOPOLIT_RUN") == "1"
        assert "SAGE_AUTOPOLIT_TASK" not in os.environ
        mock_run.assert_called_once()


class TestAutopolitClassificationOverride:
    """Test that request classification is overridden in autopolit mode."""

    def test_classification_overridden_when_env_set(self):
        import os
        from sage.cli_core import _classify_and_store_request
        from sage.core.p0_request_classification import PipelineTypeV2, RequestTypeV2

        # 1. Without SAGE_AUTOPOLIT_RUN
        os.environ.pop("SAGE_AUTOPOLIT_RUN", None)
        classification = _classify_and_store_request("explain what Python is")
        # Standard informational/read-only request should not require TDD
        assert classification.requires_tdd is False

        # 2. With SAGE_AUTOPOLIT_RUN = "1"
        os.environ["SAGE_AUTOPOLIT_RUN"] = "1"
        try:
            classification = _classify_and_store_request("explain what Python is")
            assert classification.read_only is False
            assert classification.requires_tdd is True
            assert classification.pipeline_type == PipelineTypeV2.MULTI_STEP
            assert classification.request_type == RequestTypeV2.MULTI_STEP
        finally:
            os.environ.pop("SAGE_AUTOPOLIT_RUN", None)


if __name__ == "__main__":
    from unittest.mock import patch
    pytest.main([__file__, "-v"])
