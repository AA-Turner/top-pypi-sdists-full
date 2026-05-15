"""Shared pytest fixtures for sage/tests.

Provides the project-root fixtures that test_runtime_validation_integration
and others rely on. Resolved at import time so they're cheap.
"""

from __future__ import annotations

from pathlib import Path

import pytest


# This file lives at <project_root>/sage/tests/conftest.py
_HERE = Path(__file__).resolve().parent          # .../sage/tests
_SAGE_MODULE = _HERE.parent                       # .../sage
_PROJECT_ROOT = _SAGE_MODULE.parent               # .../ai-platform


@pytest.fixture
def sage_project_root() -> Path:
    """The ai-platform/ directory — contains pyproject.toml, sage/, backend/."""
    return _PROJECT_ROOT


@pytest.fixture
def sage_module_root() -> Path:
    """The sage/ module directory — contains main.py, __init__.py, tests/."""
    return _SAGE_MODULE


@pytest.fixture
def sage_tests_dir() -> Path:
    """The sage/tests/ directory."""
    return _HERE
