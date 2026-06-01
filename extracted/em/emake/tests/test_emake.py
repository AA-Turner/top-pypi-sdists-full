# pyright: reportImplicitRelativeImport=false
"""Tests for emake module."""

import os
import sys
from contextlib import redirect_stderr, redirect_stdout
from io import StringIO
from pathlib import Path

from emake.config import diff


def test_venv() -> None:
    """Test venv exists."""
    from emake.venv import get_venv  # noqa: PLC0415

    venv = get_venv()
    assert venv.exists


def test_diff_same_version(tmp_path: Path) -> None:
    """Test when version same - no diff."""
    config_text = """
[project]
name = "test"
license = "MIT"
requires-python = ">=3.11"
authors = [{name = "test", email = "test@localhost"}]

[build-system]
requires = ["setuptools>=77.0", "nuitka>=4.0.6"]
build-backend = "nuitka.distutils.Build"

[project.optional-dependencies]
test = ["pytest"]

[tool.pyright]
exclude = [".venv", "build"]

[tool.ruff]
exclude = [".venv", "build"]
"""
    os.chdir(tmp_path)
    with open("pyproject.toml", "w") as f:
        _ = f.write(config_text)

    stdout = StringIO()
    stderr = StringIO()
    with redirect_stdout(stdout), redirect_stderr(stderr):
        result = diff(False, False)

    stdout_text = stdout.getvalue()
    print(stdout_text)
    stderr_text = stderr.getvalue()
    print(stderr_text, file=sys.stderr)
    assert result == 0
    assert "missing coverage for" not in stderr_text


def test_diff_newer_setuptools(tmp_path: Path) -> None:
    """Test when setuptools newer - ok for grug."""
    config_text = """
[project]
name = "test"
license = "MIT"
requires-python = ">=3.11"
authors = [{name = "test", email = "test@localhost"}]

[build-system]
requires = ["setuptools>=80", "nuitka>=4.0.6"]
build-backend = "nuitka.distutils.Build"

[project.optional-dependencies]
test = ["pytest"]

[tool.pyright]
exclude = [".venv", "build"]

[tool.ruff]
exclude = [".venv", "build"]
"""
    os.chdir(tmp_path)
    with open("pyproject.toml", "w") as f:
        _ = f.write(config_text)

    stdout = StringIO()
    stderr = StringIO()
    with redirect_stdout(stdout), redirect_stderr(stderr):
        result = diff(False, False)

    stdout_text = stdout.getvalue()
    print(stdout_text)
    stderr_text = stderr.getvalue()
    print(stderr_text, file=sys.stderr)
    assert result == 0
    assert "missing coverage for" not in stderr_text


def test_diff_older_setuptools(tmp_path: Path) -> None:
    """Test when setuptools older - grug see diff."""
    config_text = """
[project]
name = "test"
license = "MIT"
requires-python = ">=3.11"
authors = [{name = "test", email = "test@localhost"}]

[build-system]
requires = ["setuptools>=60", "nuitka>=4.0.6"]
build-backend = "nuitka.distutils.Build"

[project.optional-dependencies]
test = ["pytest"]

[tool.pyright]
exclude = [".venv", "build"]

[tool.ruff]
exclude = [".venv", "build"]
"""
    os.chdir(tmp_path)
    with open("pyproject.toml", "w") as f:
        _ = f.write(config_text)

    stdout = StringIO()
    stderr = StringIO()
    with redirect_stdout(stdout), redirect_stderr(stderr):
        result = diff(False, False)

    stdout_text = stdout.getvalue()
    print(stdout_text)
    stderr_text = stderr.getvalue()
    print(stderr_text, file=sys.stderr)
    assert result == 1
    assert "setuptools>=77.0" in stderr_text


def test_diff_exact_version(tmp_path: Path) -> None:
    """Test with exact version == 70.1."""
    config_text = """
[project]
name = "test"
license = "MIT"
requires-python = ">=3.11"
authors = [{name = "test", email = "test@localhost"}]

[build-system]
requires = ["setuptools==77.0", "nuitka>=4.0.6"]
build-backend = "nuitka.distutils.Build"

[project.optional-dependencies]
test = ["pytest"]

[tool.pyright]
exclude = [".venv", "build"]

[tool.ruff]
exclude = [".venv", "build"]
"""
    os.chdir(tmp_path)
    with open("pyproject.toml", "w") as f:
        _ = f.write(config_text)

    stdout = StringIO()
    stderr = StringIO()
    with redirect_stdout(stdout), redirect_stderr(stderr):
        result = diff(False, False)

    stdout_text = stdout.getvalue()
    print(stdout_text)
    stderr_text = stderr.getvalue()
    print(stderr_text, file=sys.stderr)
    # == should also satisfy >=70.1
    assert result == 0
    assert "missing coverage for" not in stdout_text


def test_diff_complex_specifier(tmp_path: Path) -> None:
    """Test complex specifier like nuitka>=4.0.6,!=4.7."""
    config_text = """
[project]
name = "test"
license = "MIT"
requires-python = ">=3.11"
authors = [{name = "test", email = "test@localhost"}]

[build-system]
requires = ["setuptools>=77.0", "nuitka>=4.0.6,!=4.7"]
build-backend = "nuitka.distutils.Build"

[project.optional-dependencies]
test = ["pytest"]

[tool.pyright]
exclude = [".venv", "build"]

[tool.ruff]
exclude = [".venv", "build"]
"""
    os.chdir(tmp_path)
    with open("pyproject.toml", "w") as f:
        _ = f.write(config_text)

    stdout = StringIO()
    stderr = StringIO()
    with redirect_stdout(stdout), redirect_stderr(stderr):
        result = diff(False, False)

    stdout_text = stdout.getvalue()
    print(stdout_text)
    stderr_text = stderr.getvalue()
    print(stderr_text, file=sys.stderr)
    assert result == 0
    assert "missing coverage for" not in stderr_text


def test_diff_nuitka_missing(tmp_path: Path) -> None:
    """Test when nuitka missing - grug report diff."""
    config_text = """
[project]
name = "test"
license = "MIT"
requires-python = ">=3.11"
authors = [{name = "test", email = "test@localhost"}]

[build-system]
requires = ["setuptools>=77.0"]
build-backend = "nuitka.distutils.Build"

[project.optional-dependencies]
test = ["pytest"]

[tool.pyright]
exclude = [".venv", "build"]

[tool.ruff]
exclude = [".venv", "build"]
"""
    os.chdir(tmp_path)
    with open("pyproject.toml", "w") as f:
        _ = f.write(config_text)

    stdout = StringIO()
    stderr = StringIO()
    with redirect_stdout(stdout), redirect_stderr(stderr):
        result = diff(False, False)

    stdout_text = stdout.getvalue()
    print(stdout_text)
    stderr_text = stderr.getvalue()
    print(stderr_text, file=sys.stderr)
    assert result == 1
    assert "missing coverage for nuitka" in stderr_text


def test_diff_python_version_marker(tmp_path: Path) -> None:
    """Test requirement with python_version marker."""
    config_text = """
[project]
name = "test"
license = "MIT"
requires-python = ">=3.11"
authors = [{name = "test", email = "test@localhost"}]

[build-system]
requires = ["setuptools>=77.0; python_version >= '3.11'", "nuitka>=4.0.6"]
build-backend = "nuitka.distutils.Build"

[project.optional-dependencies]
test = ["pytest"]

[tool.pyright]
exclude = [".venv", "build"]

[tool.ruff]
exclude = [".venv", "build"]
"""
    os.chdir(tmp_path)
    with open("pyproject.toml", "w") as f:
        _ = f.write(config_text)

    stdout = StringIO()
    stderr = StringIO()
    with redirect_stdout(stdout), redirect_stderr(stderr):
        result = diff(False, False)

    stdout_text = stdout.getvalue()
    print(stdout_text)
    stderr_text = stderr.getvalue()
    print(stderr_text, file=sys.stderr)
    assert result == 0
    assert "missing coverage for" not in stderr_text


def test_diff_sys_platform_marker(tmp_path: Path) -> None:
    """Test requirement with sys_platform marker."""
    config_text = """
[project]
name = "test"
license = "MIT"
requires-python = ">=3.11"
authors = [{name = "test", email = "test@localhost"}]

[build-system]
requires = ["setuptools>=77.0; sys_platform == 'win32'", "nuitka>=4.0.6"]
build-backend = "nuitka.distutils.Build"

[project.optional-dependencies]
test = ["pytest"]

[tool.pyright]
exclude = [".venv", "build"]

[tool.ruff]
exclude = [".venv", "build"]
"""
    os.chdir(tmp_path)
    with open("pyproject.toml", "w") as f:
        _ = f.write(config_text)

    stdout = StringIO()
    stderr = StringIO()
    with redirect_stdout(stdout), redirect_stderr(stderr):
        result = diff(False, False)

    stdout_text = stdout.getvalue()
    print(stdout_text)
    stderr_text = stderr.getvalue()
    print(stderr_text, file=sys.stderr)
    assert result == 1
    assert "missing coverage for setuptools" in stderr_text


def test_diff_missing_name(tmp_path: Path) -> None:
    """Test when name is missing."""
    config_text = """
[project]
license = "MIT"
requires-python = ">=3.11"
authors = [{name = "test", email = "test@localhost"}]

[build-system]
requires = ["setuptools>=77.0", "nuitka>=4.0.6"]
build-backend = "nuitka.distutils.Build"

[project.optional-dependencies]
test = ["pytest"]

[tool.pyright]
exclude = [".venv", "build"]

[tool.ruff]
exclude = [".venv", "build"]
"""
    os.chdir(tmp_path)
    with open("pyproject.toml", "w") as f:
        _ = f.write(config_text)

    stdout = StringIO()
    stderr = StringIO()
    with redirect_stdout(stdout), redirect_stderr(stderr):
        result = diff(False, False)

    stdout_text = stdout.getvalue()
    print(stdout_text)
    stderr_text = stderr.getvalue()
    print(stderr_text, file=sys.stderr)
    assert result == 1
    assert "does not specify a 'name'" in stderr_text


def test_diff_missing_license(tmp_path: Path) -> None:
    """Test when license is missing."""
    config_text = """
[project]
name = "test"
requires-python = ">=3.11"
authors = [{name = "test", email = "test@localhost"}]

[build-system]
requires = ["setuptools>=77.0", "nuitka>=4.0.6"]
build-backend = "nuitka.distutils.Build"

[project.optional-dependencies]
test = ["pytest"]

[tool.pyright]
exclude = [".venv", "build"]

[tool.ruff]
exclude = [".venv", "build"]
"""
    os.chdir(tmp_path)
    with open("pyproject.toml", "w") as f:
        _ = f.write(config_text)

    stdout = StringIO()
    stderr = StringIO()
    with redirect_stdout(stdout), redirect_stderr(stderr):
        result = diff(False, False)

    stdout_text = stdout.getvalue()
    print(stdout_text)
    stderr_text = stderr.getvalue()
    print(stderr_text, file=sys.stderr)
    assert result == 1
    assert "does not specify a 'license'" in stderr_text


def test_diff_missing_authors(tmp_path: Path) -> None:
    """Test when authors is missing."""
    config_text = """
[project]
name = "test"
license = "MIT"
requires-python = ">=3.11"

[build-system]
requires = ["setuptools>=77.0", "nuitka>=4.0.6"]
build-backend = "nuitka.distutils.Build"

[project.optional-dependencies]
test = ["pytest"]

[tool.pyright]
exclude = [".venv", "build"]

[tool.ruff]
exclude = [".venv", "build"]
"""
    os.chdir(tmp_path)
    with open("pyproject.toml", "w") as f:
        _ = f.write(config_text)

    stdout = StringIO()
    stderr = StringIO()
    with redirect_stdout(stdout), redirect_stderr(stderr):
        result = diff(False, False)

    stdout_text = stdout.getvalue()
    print(stdout_text)
    stderr_text = stderr.getvalue()
    print(stderr_text, file=sys.stderr)
    assert result == 1
    assert "does not specify a 'authors'" in stderr_text


def test_diff_empty_authors(tmp_path: Path) -> None:
    """Test when authors is empty list."""
    config_text = """
[project]
name = "test"
license = "MIT"
requires-python = ">=3.11"
authors = []

[build-system]
requires = ["setuptools>=77.0", "nuitka>=4.0.6"]
build-backend = "nuitka.distutils.Build"

[project.optional-dependencies]
test = ["pytest"]

[tool.pyright]
exclude = [".venv", "build"]

[tool.ruff]
exclude = [".venv", "build"]
"""
    os.chdir(tmp_path)
    with open("pyproject.toml", "w") as f:
        _ = f.write(config_text)

    stdout = StringIO()
    stderr = StringIO()
    with redirect_stdout(stdout), redirect_stderr(stderr):
        result = diff(False, False)

    stdout_text = stdout.getvalue()
    print(stdout_text)
    stderr_text = stderr.getvalue()
    print(stderr_text, file=sys.stderr)
    assert result == 1
    assert "does not specify a 'authors'" in stderr_text


def test_diff_invalid_toml(tmp_path: Path) -> None:
    """Test when pyproject.toml has invalid TOML."""
    config_text = """
[project
name = "test"
"""
    os.chdir(tmp_path)
    with open("pyproject.toml", "w") as f:
        _ = f.write(config_text)

    stdout = StringIO()
    stderr = StringIO()
    with redirect_stdout(stdout), redirect_stderr(stderr):
        result = diff(False, False)

    stdout_text = stdout.getvalue()
    print(stdout_text)
    stderr_text = stderr.getvalue()
    print(stderr_text, file=sys.stderr)
    assert result == 1
    assert "pyproject.toml is invalid" in stderr_text


def test_diff_missing_build_system(tmp_path: Path) -> None:
    """Test when build-system section is missing."""
    config_text = """
[project]
name = "test"
license = "MIT"
requires-python = ">=3.11"
authors = [{name = "test", email = "test@localhost"}]

[project.optional-dependencies]
test = ["pytest"]

[tool.pyright]
exclude = [".venv", "build"]

[tool.ruff]
exclude = [".venv", "build"]
"""
    os.chdir(tmp_path)
    with open("pyproject.toml", "w") as f:
        _ = f.write(config_text)

    stdout = StringIO()
    stderr = StringIO()
    with redirect_stdout(stdout), redirect_stderr(stderr):
        result = diff(False, False)

    stdout_text = stdout.getvalue()
    print(stdout_text)
    stderr_text = stderr.getvalue()
    print(stderr_text, file=sys.stderr)
    assert result == 2
    assert "missing coverage for setuptools" in stderr_text
    assert "expected nuitka.distutils.Build" in stderr_text


def test_diff_mismatched_build_backend(tmp_path: Path) -> None:
    """Test when build-backend differs from template."""
    config_text = """
[project]
name = "test"
license = "MIT"
requires-python = ">=3.11"
authors = [{name = "test", email = "test@localhost"}]

[build-system]
requires = ["setuptools>=77.0", "nuitka>=4.0.6"]
build-backend = "setuptools.build_meta"

[project.optional-dependencies]
test = ["pytest"]

[tool.pyright]
exclude = [".venv", "build"]

[tool.ruff]
exclude = [".venv", "build"]
"""
    os.chdir(tmp_path)
    with open("pyproject.toml", "w") as f:
        _ = f.write(config_text)

    stdout = StringIO()
    stderr = StringIO()
    with redirect_stdout(stdout), redirect_stderr(stderr):
        result = diff(False, False)

    stdout_text = stdout.getvalue()
    print(stdout_text)
    stderr_text = stderr.getvalue()
    print(stderr_text, file=sys.stderr)
    assert result == 1
    assert "build-backend" in stderr_text
    assert "nuitka.distutils.Build" in stderr_text


def test_diff_missing_pyright(tmp_path: Path) -> None:
    """Test when pyright tool section is missing."""
    config_text = """
[project]
name = "test"
license = "MIT"
requires-python = ">=3.11"
authors = [{name = "test", email = "test@localhost"}]

[build-system]
requires = ["setuptools>=77.0", "nuitka>=4.0.6"]
build-backend = "nuitka.distutils.Build"

[project.optional-dependencies]
test = ["pytest"]

[tool.ruff]
exclude = [".venv", "build"]
"""
    os.chdir(tmp_path)
    with open("pyproject.toml", "w") as f:
        _ = f.write(config_text)

    stdout = StringIO()
    stderr = StringIO()
    with redirect_stdout(stdout), redirect_stderr(stderr):
        result = diff(False, False)

    stdout_text = stdout.getvalue()
    print(stdout_text)
    stderr_text = stderr.getvalue()
    print(stderr_text, file=sys.stderr)
    assert result == 1
    assert "tool.pyright.exclude" in stderr_text
    assert "None" in stderr_text


def test_diff_missing_ruff(tmp_path: Path) -> None:
    """Test when ruff tool section is missing."""
    config_text = """
[project]
name = "test"
license = "MIT"
requires-python = ">=3.11"
authors = [{name = "test", email = "test@localhost"}]

[build-system]
requires = ["setuptools>=77.0", "nuitka>=4.0.6"]
build-backend = "nuitka.distutils.Build"

[project.optional-dependencies]
test = ["pytest"]

[tool.pyright]
exclude = [".venv", "build"]
"""
    os.chdir(tmp_path)
    with open("pyproject.toml", "w") as f:
        _ = f.write(config_text)

    stdout = StringIO()
    stderr = StringIO()
    with redirect_stdout(stdout), redirect_stderr(stderr):
        result = diff(False, False)

    stdout_text = stdout.getvalue()
    print(stdout_text)
    stderr_text = stderr.getvalue()
    print(stderr_text, file=sys.stderr)
    assert result == 1
    assert "tool.ruff.exclude" in stderr_text
    assert "None" in stderr_text


def test_diff_mismatched_pyright_exclude(tmp_path: Path) -> None:
    """Test when pyright exclude differs from template."""
    config_text = """
[project]
name = "test"
license = "MIT"
requires-python = ">=3.11"
authors = [{name = "test", email = "test@localhost"}]

[build-system]
requires = ["setuptools>=77.0", "nuitka>=4.0.6"]
build-backend = "nuitka.distutils.Build"

[project.optional-dependencies]
test = ["pytest"]

[tool.pyright]
exclude = [".cache", "dist"]

[tool.ruff]
exclude = [".venv", "build"]
"""
    os.chdir(tmp_path)
    with open("pyproject.toml", "w") as f:
        _ = f.write(config_text)

    stdout = StringIO()
    stderr = StringIO()
    with redirect_stdout(stdout), redirect_stderr(stderr):
        result = diff(False, False)

    stdout_text = stdout.getvalue()
    print(stdout_text)
    stderr_text = stderr.getvalue()
    print(stderr_text, file=sys.stderr)
    assert result == 1
    assert "tool.pyright.exclude" in stderr_text


def test_diff_mismatched_ruff_exclude(tmp_path: Path) -> None:
    """Test when ruff exclude differs from template."""
    config_text = """
[project]
name = "test"
license = "MIT"
requires-python = ">=3.11"
authors = [{name = "test", email = "test@localhost"}]

[build-system]
requires = ["setuptools>=77.0", "nuitka>=4.0.6"]
build-backend = "nuitka.distutils.Build"

[project.optional-dependencies]
test = ["pytest"]

[tool.pyright]
exclude = [".venv", "build"]

[tool.ruff]
exclude = [".cache", "dist"]
"""
    os.chdir(tmp_path)
    with open("pyproject.toml", "w") as f:
        _ = f.write(config_text)

    stdout = StringIO()
    stderr = StringIO()
    with redirect_stdout(stdout), redirect_stderr(stderr):
        result = diff(False, False)

    stdout_text = stdout.getvalue()
    print(stdout_text)
    stderr_text = stderr.getvalue()
    print(stderr_text, file=sys.stderr)
    assert result == 1
    assert "tool.ruff.exclude" in stderr_text


def test_diff_missing_test_extras(tmp_path: Path) -> None:
    """Test when test optional-dependencies group is missing."""
    config_text = """
[project]
name = "test"
license = "MIT"
requires-python = ">=3.11"
authors = [{name = "test", email = "test@localhost"}]

[build-system]
requires = ["setuptools>=77.0", "nuitka>=4.0.6"]
build-backend = "nuitka.distutils.Build"

[project.optional-dependencies]
dev = ["black"]

[tool.pyright]
exclude = [".venv", "build"]

[tool.ruff]
exclude = [".venv", "build"]
"""
    os.chdir(tmp_path)
    with open("pyproject.toml", "w") as f:
        _ = f.write(config_text)

    stdout = StringIO()
    stderr = StringIO()
    with redirect_stdout(stdout), redirect_stderr(stderr):
        result = diff(False, False)

    stdout_text = stdout.getvalue()
    print(stdout_text)
    stderr_text = stderr.getvalue()
    print(stderr_text, file=sys.stderr)
    assert result == 1
    assert "test" in stderr_text
    assert "optional dependency" in stderr_text


def test_diff_empty_test_extras(tmp_path: Path) -> None:
    """Test when test extras is empty list."""
    config_text = """
[project]
name = "test"
license = "MIT"
requires-python = ">=3.11"
authors = [{name = "test", email = "test@localhost"}]

[build-system]
requires = ["setuptools>=77.0", "nuitka>=4.0.6"]
build-backend = "nuitka.distutils.Build"

[project.optional-dependencies]
test = []

[tool.pyright]
exclude = [".venv", "build"]

[tool.ruff]
exclude = [".venv", "build"]
"""
    os.chdir(tmp_path)
    with open("pyproject.toml", "w") as f:
        _ = f.write(config_text)

    stdout = StringIO()
    stderr = StringIO()
    with redirect_stdout(stdout), redirect_stderr(stderr):
        result = diff(False, False)

    stdout_text = stdout.getvalue()
    print(stdout_text)
    stderr_text = stderr.getvalue()
    print(stderr_text, file=sys.stderr)
    assert result == 1
    assert "pytest" in stderr_text


def test_diff_pytest_not_in_test_extras(tmp_path: Path) -> None:
    """Test when test group exists but pytest is not in it."""
    config_text = """
[project]
name = "test"
license = "MIT"
requires-python = ">=3.11"
authors = [{name = "test", email = "test@localhost"}]

[build-system]
requires = ["setuptools>=77.0", "nuitka>=4.0.6"]
build-backend = "nuitka.distutils.Build"

[project.optional-dependencies]
test = ["black", "ruff"]

[tool.pyright]
exclude = [".venv", "build"]

[tool.ruff]
exclude = [".venv", "build"]
"""
    os.chdir(tmp_path)
    with open("pyproject.toml", "w") as f:
        _ = f.write(config_text)

    stdout = StringIO()
    stderr = StringIO()
    with redirect_stdout(stdout), redirect_stderr(stderr):
        result = diff(False, False)

    stdout_text = stdout.getvalue()
    print(stdout_text)
    stderr_text = stderr.getvalue()
    print(stderr_text, file=sys.stderr)
    assert result == 1
    assert "pytest" in stderr_text


def test_diff_multiple_authors(tmp_path: Path) -> None:
    """Test with multiple authors - uses first author."""
    config_text = """
[project]
name = "test"
license = "MIT"
requires-python = ">=3.11"
authors = [{name = "first", email = "first@localhost"}, {name = "second", email = "second@localhost"}]

[build-system]
requires = ["setuptools>=77.0", "nuitka>=4.0.6"]
build-backend = "nuitka.distutils.Build"

[project.optional-dependencies]
test = ["pytest"]

[tool.pyright]
exclude = [".venv", "build"]

[tool.ruff]
exclude = [".venv", "build"]
"""
    os.chdir(tmp_path)
    with open("pyproject.toml", "w") as f:
        _ = f.write(config_text)

    stdout = StringIO()
    stderr = StringIO()
    with redirect_stdout(stdout), redirect_stderr(stderr):
        result = diff(False, False)

    stdout_text = stdout.getvalue()
    print(stdout_text)
    stderr_text = stderr.getvalue()
    print(stderr_text, file=sys.stderr)
    assert result == 0
    assert "missing coverage for" not in stderr_text


def test_diff_no_pyproject(tmp_path: Path) -> None:
    """Test when pyproject.toml does not exist."""
    os.chdir(tmp_path)

    stdout = StringIO()
    stderr = StringIO()
    with redirect_stdout(stdout), redirect_stderr(stderr):
        try:
            _ = diff(False, False)
            assert False, "Should raise FileNotFoundError"

        except FileNotFoundError:
            pass

        stdout_text = stdout.getvalue()
        print(stdout_text)
        stderr_text = stderr.getvalue()
        print(stderr_text, file=sys.stderr)


def test_diff_no_requires_python(tmp_path: Path) -> None:
    """Test when requires-python is missing."""
    config_text = """
[project]
name = "test"
license = "MIT"
authors = [{name = "test", email = "test@localhost"}]

[build-system]
requires = ["setuptools>=77.0", "nuitka>=4.0.6"]
build-backend = "nuitka.distutils.Build"

[project.optional-dependencies]
test = ["pytest"]

[tool.pyright]
exclude = [".venv", "build"]

[tool.ruff]
exclude = [".venv", "build"]
"""
    os.chdir(tmp_path)
    with open("pyproject.toml", "w") as f:
        _ = f.write(config_text)

    stdout = StringIO()
    stderr = StringIO()
    with redirect_stdout(stdout), redirect_stderr(stderr):
        result = diff(False, False)

    stdout_text = stdout.getvalue()
    print(stdout_text)
    stderr_text = stderr.getvalue()
    print(stderr_text, file=sys.stderr)
    assert result == 1
    assert "does not specify a 'requires_python'" in stderr_text


def test_diff_multiple_missing(tmp_path: Path) -> None:
    """Test when multiple required fields are missing."""
    config_text = """
[project]
name = "test"
"""
    os.chdir(tmp_path)
    with open("pyproject.toml", "w") as f:
        _ = f.write(config_text)

    stdout = StringIO()
    stderr = StringIO()
    with redirect_stdout(stdout), redirect_stderr(stderr):
        result = diff(False, False)

    stdout_text = stdout.getvalue()
    print(stdout_text)
    stderr_text = stderr.getvalue()
    print(stderr_text, file=sys.stderr)
    assert result >= 3
    assert "does not specify a 'license'" in stderr_text
    assert "does not specify a 'requires_python'" in stderr_text
    assert "does not specify a 'authors'" in stderr_text
