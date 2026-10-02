"""Shared fixtures for Python integration tests."""

from __future__ import annotations

import shutil
import tempfile

import pytest


@pytest.fixture()
def registry_dir():
    """Create a temporary directory and clean it up after the test."""
    d = tempfile.mkdtemp(prefix="scai-pytest-")
    yield d
    shutil.rmtree(d, ignore_errors=True)
