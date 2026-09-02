"""Tests for _require_pypi_value function."""

import pytest

from agentic_devtools.cli.release.commands import _require_pypi_value


class TestRequirePypiValue:
    """Tests for _require_pypi_value function."""

    def test_returns_value_when_present(self):
        """Should return the value unchanged when it's truthy."""
        result = _require_pypi_value("my-package", "package_name", "agdt-set pypi.package_name <name>")
        assert result == "my-package"

    def test_exits_when_value_is_none(self):
        """Should sys.exit(1) when value is None."""
        with pytest.raises(SystemExit) as exc_info:
            _require_pypi_value(None, "package_name", "agdt-set pypi.package_name <name>")
        assert exc_info.value.code == 1

    def test_exits_when_value_is_empty_string(self):
        """Should sys.exit(1) when value is an empty string."""
        with pytest.raises(SystemExit) as exc_info:
            _require_pypi_value("", "version", "agdt-set pypi.version <version>")
        assert exc_info.value.code == 1
