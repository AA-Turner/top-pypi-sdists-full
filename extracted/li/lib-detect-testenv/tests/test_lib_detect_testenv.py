"""Comprehensive tests for the core lib_detect_testenv module.

This module tests all test environment detection functions to ensure they
correctly identify pytest, doctest, setup.py, and other test environments.
"""

from __future__ import annotations

import pathlib
import sys
from typing import TYPE_CHECKING

import pytest

from lib_detect_testenv import (
    PathLikeOrString,
    add_path_to_syspath,
    is_doctest_active,
    is_doctest_in_arg_string,
    is_pytest_active,
    is_setup_active,
    is_setup_test_active,
    is_testenv_active,
)

if TYPE_CHECKING:
    from collections.abc import Generator


# ============================================================================
# Tests for is_testenv_active()
# ============================================================================


@pytest.mark.os_agnostic
def test_is_testenv_active_with_pytest() -> None:
    """is_testenv_active() should return True when pytest is detected."""
    assert is_testenv_active(arg_string="pytest.py") is True
    assert is_testenv_active(arg_string="/pytest/__main__.py") is True
    assert is_testenv_active(arg_string="python -m pytest") is True


@pytest.mark.os_agnostic
def test_is_testenv_active_with_doctest() -> None:
    """is_testenv_active() should return True when doctest is detected."""
    assert is_testenv_active(arg_string="docrunner.py") is True
    assert is_testenv_active(arg_string="doctest.py") is True
    assert is_testenv_active(arg_string="/path/to/docrunner.py") is True


@pytest.mark.os_agnostic
def test_is_testenv_active_with_setup_test() -> None:
    """is_testenv_active() should return True when setup.py test is detected."""
    assert is_testenv_active(arg_string="setup.py test") is True
    assert is_testenv_active(arg_string="python setup.py test") is True


@pytest.mark.os_agnostic
def test_is_testenv_active_without_test_env() -> None:
    """is_testenv_active() should return False when no test env is detected."""
    assert is_testenv_active(arg_string="") is False
    assert is_testenv_active(arg_string="python script.py") is False
    assert is_testenv_active(arg_string="setup.py build") is False


@pytest.mark.os_agnostic
def test_is_testenv_active_uses_sys_argv_by_default() -> None:
    """is_testenv_active() should use sys.argv when arg_string is None."""
    # When running under pytest, this should return True
    result = is_testenv_active()
    # We're running under pytest, so this should be True
    assert result is True


# ============================================================================
# Tests for is_pytest_active()
# ============================================================================


@pytest.mark.os_agnostic
def test_is_pytest_active_with_pytest_py() -> None:
    """is_pytest_active() should return True when pytest.py is in args."""
    assert is_pytest_active(arg_string="pytest.py") is True
    assert is_pytest_active(arg_string="/path/to/pytest.py") is True


@pytest.mark.os_agnostic
def test_is_pytest_active_with_pytest_main() -> None:
    """is_pytest_active() should return True when /pytest/__main__.py is in args."""
    assert is_pytest_active(arg_string="/pytest/__main__.py") is True
    assert is_pytest_active(arg_string="/usr/lib/pytest/__main__.py") is True


@pytest.mark.os_agnostic
def test_is_pytest_active_with_python_m_pytest() -> None:
    """is_pytest_active() should return True when 'python -m pytest' is detected."""
    assert is_pytest_active(arg_string="python -m pytest") is True
    assert is_pytest_active(arg_string="['python', '-m', 'pytest', 'test.py']") is True


@pytest.mark.os_agnostic
def test_is_pytest_active_without_pytest() -> None:
    """is_pytest_active() should return False when pytest is not detected."""
    assert is_pytest_active(arg_string="") is False
    assert is_pytest_active(arg_string="python test.py") is False
    assert is_pytest_active(arg_string="doctest.py") is False


@pytest.mark.os_agnostic
def test_is_pytest_active_with_pytest_env_var(monkeypatch: pytest.MonkeyPatch) -> None:
    """is_pytest_active() should return True when PYTEST_IS_RUNNING is set."""
    monkeypatch.setenv("PYTEST_IS_RUNNING", "1")
    assert is_pytest_active(arg_string="") is True


# ============================================================================
# Tests for is_doctest_active()
# ============================================================================


@pytest.mark.os_agnostic
def test_is_doctest_active_with_docrunner() -> None:
    """is_doctest_active() should return True when docrunner.py is detected."""
    assert is_doctest_active(arg_string="docrunner.py") is True
    assert is_doctest_active(arg_string="/path/to/docrunner.py") is True


@pytest.mark.os_agnostic
def test_is_doctest_active_with_doctest() -> None:
    """is_doctest_active() should return True when doctest.py is detected."""
    assert is_doctest_active(arg_string="doctest.py") is True
    assert is_doctest_active(arg_string="/usr/lib/python3/doctest.py") is True


@pytest.mark.os_agnostic
def test_is_doctest_active_without_doctest() -> None:
    """is_doctest_active() should return False when doctest is not detected."""
    assert is_doctest_active(arg_string="") is False
    assert is_doctest_active(arg_string="pytest.py") is False
    assert is_doctest_active(arg_string="test.py") is False


# ============================================================================
# Tests for is_setup_active()
# ============================================================================


@pytest.mark.os_agnostic
def test_is_setup_active_with_setup_py() -> None:
    """is_setup_active() should return True when setup.py is detected."""
    assert is_setup_active(arg_string="setup.py") is True
    assert is_setup_active(arg_string="python setup.py") is True
    assert is_setup_active(arg_string="setup.py build") is True


@pytest.mark.os_agnostic
def test_is_setup_active_without_setup() -> None:
    """is_setup_active() should return False when setup.py is not detected."""
    assert is_setup_active(arg_string="") is False
    assert is_setup_active(arg_string="pytest.py") is False
    assert is_setup_active(arg_string="build.py") is False


# ============================================================================
# Tests for is_setup_test_active()
# ============================================================================


@pytest.mark.os_agnostic
def test_is_setup_test_active_with_setup_test() -> None:
    """is_setup_test_active() should return True when 'setup.py test' is detected."""
    assert is_setup_test_active(arg_string="setup.py test") is True
    assert is_setup_test_active(arg_string="python setup.py test") is True
    assert is_setup_test_active(arg_string="setup.py test --verbose") is True


@pytest.mark.os_agnostic
def test_is_setup_test_active_with_just_setup() -> None:
    """is_setup_test_active() should return False when only setup.py is detected."""
    assert is_setup_test_active(arg_string="setup.py") is False
    assert is_setup_test_active(arg_string="setup.py build") is False
    assert is_setup_test_active(arg_string="setup.py install") is False


@pytest.mark.os_agnostic
def test_is_setup_test_active_without_setup() -> None:
    """is_setup_test_active() should return False when setup.py is not detected."""
    assert is_setup_test_active(arg_string="") is False
    assert is_setup_test_active(arg_string="pytest.py") is False


# ============================================================================
# Tests for is_doctest_in_arg_string()
# ============================================================================


@pytest.mark.os_agnostic
def test_is_doctest_in_arg_string_with_docrunner() -> None:
    """is_doctest_in_arg_string() should return True when docrunner.py is present."""
    assert is_doctest_in_arg_string("test/docrunner.py::::test") is True
    assert is_doctest_in_arg_string("docrunner.py") is True
    assert is_doctest_in_arg_string("/path/to/docrunner.py") is True


@pytest.mark.os_agnostic
def test_is_doctest_in_arg_string_without_docrunner() -> None:
    """is_doctest_in_arg_string() should return False when docrunner.py is not present."""
    assert is_doctest_in_arg_string("test") is False
    assert is_doctest_in_arg_string("pytest.py") is False
    assert is_doctest_in_arg_string("") is False


# ============================================================================
# Tests for add_path_to_syspath()
# ============================================================================


@pytest.fixture
def temp_test_dir(tmp_path: pathlib.Path) -> Generator[pathlib.Path, None, None]:
    """Create a temporary test directory and clean up sys.path after test."""
    test_dir = tmp_path / "test_syspath"
    test_dir.mkdir()
    original_syspath = sys.path.copy()

    yield test_dir

    # Restore original sys.path
    sys.path[:] = original_syspath


@pytest.mark.os_agnostic
def test_add_path_to_syspath_adds_directory(temp_test_dir: pathlib.Path) -> None:
    """add_path_to_syspath() should add a directory to sys.path."""
    add_path_to_syspath(temp_test_dir)
    assert str(temp_test_dir) in sys.path


@pytest.mark.os_agnostic
def test_add_path_to_syspath_adds_at_beginning(temp_test_dir: pathlib.Path) -> None:
    """add_path_to_syspath() should add path at the beginning of sys.path."""
    add_path_to_syspath(temp_test_dir)
    assert sys.path[0] == str(temp_test_dir)


@pytest.mark.os_agnostic
def test_add_path_to_syspath_prevents_duplicates(temp_test_dir: pathlib.Path) -> None:
    """add_path_to_syspath() should not add duplicate paths."""
    original_len = len(sys.path)
    add_path_to_syspath(temp_test_dir)
    first_add_len = len(sys.path)
    assert first_add_len == original_len + 1

    # Adding again should not increase length
    add_path_to_syspath(temp_test_dir)
    second_add_len = len(sys.path)
    assert second_add_len == first_add_len


@pytest.mark.os_agnostic
def test_add_path_to_syspath_handles_file_path(temp_test_dir: pathlib.Path) -> None:
    """add_path_to_syspath() should add parent directory when given a file path."""
    test_file = temp_test_dir / "test_file.py"
    test_file.touch()

    add_path_to_syspath(test_file)

    # Should add the parent directory, not the file itself
    assert str(temp_test_dir) in sys.path
    assert str(test_file) not in sys.path


@pytest.mark.os_agnostic
def test_add_path_to_syspath_handles_string_path(temp_test_dir: pathlib.Path) -> None:
    """add_path_to_syspath() should accept string paths."""
    add_path_to_syspath(str(temp_test_dir))
    assert str(temp_test_dir) in sys.path


@pytest.mark.os_agnostic
def test_add_path_to_syspath_handles_pathlike(temp_test_dir: pathlib.Path) -> None:
    """add_path_to_syspath() should accept PathLike objects."""
    add_path_to_syspath(temp_test_dir)
    assert str(temp_test_dir) in sys.path


@pytest.mark.os_agnostic
def test_add_path_to_syspath_resolves_relative_paths(tmp_path: pathlib.Path) -> None:
    """add_path_to_syspath() should resolve relative paths to absolute paths."""
    import os

    original_cwd = os.getcwd()
    original_syspath = sys.path.copy()

    try:
        # Create a test directory and change to it
        test_dir = tmp_path / "relative_test"
        test_dir.mkdir()
        os.chdir(test_dir)

        # Add a relative path
        sub_dir = test_dir / "subdir"
        sub_dir.mkdir()

        # Use relative path
        rel_path = pathlib.Path("subdir")
        add_path_to_syspath(rel_path)

        # Should add absolute path, not relative
        assert str(sub_dir) in sys.path
        assert "subdir" not in sys.path or any(str(sub_dir) in p for p in sys.path)
    finally:
        os.chdir(original_cwd)
        sys.path[:] = original_syspath


# ============================================================================
# Tests for PathLikeOrString type alias
# ============================================================================


@pytest.mark.os_agnostic
def test_pathlike_or_string_type_exists() -> None:
    """PathLikeOrString type alias should be importable."""
    # This test just verifies the import works
    assert PathLikeOrString is not None
