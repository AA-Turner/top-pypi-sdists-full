"""Tests for _normalize_repository function."""

import pytest

from agentic_devtools.cli.release.commands import _normalize_repository
from agentic_devtools.cli.release.helpers import ReleaseError


class TestNormalizeRepository:
    """Tests for _normalize_repository function."""

    def test_none_defaults_to_pypi(self):
        """Should default to 'pypi' when value is None."""
        assert _normalize_repository(None) == "pypi"

    def test_pypi_lowercase(self):
        """Should accept 'pypi' as valid."""
        assert _normalize_repository("pypi") == "pypi"

    def test_pypi_mixed_case(self):
        """Should normalize 'PyPI' to lowercase."""
        assert _normalize_repository("PyPI") == "pypi"

    def test_testpypi(self):
        """Should accept 'testpypi' as valid."""
        assert _normalize_repository("testpypi") == "testpypi"

    def test_testpypi_mixed_case(self):
        """Should normalize 'TestPyPI' to lowercase."""
        assert _normalize_repository("TestPyPI") == "testpypi"

    def test_unsupported_repository_raises(self):
        """Should raise ReleaseError for unsupported repository."""
        with pytest.raises(ReleaseError, match="Unsupported repository"):
            _normalize_repository("invalid-repo")
