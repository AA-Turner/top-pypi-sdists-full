"""Tests for agentic_devtools.cli.issue_template.exceptions.PresetLoadError."""

from __future__ import annotations

import agentic_devtools.cli.issue_template as issue_template_pkg
from agentic_devtools.cli.issue_template import PresetLoadError as ExportedPresetLoadError
from agentic_devtools.cli.issue_template.exceptions import PresetLoadError


class TestPresetLoadError:
    """Tests for the PresetLoadError exception class."""

    def test_is_direct_exception_subclass(self) -> None:
        """PresetLoadError inherits directly from Exception."""
        assert issubclass(PresetLoadError, Exception)
        assert PresetLoadError.__bases__ == (Exception,)

    def test_can_be_raised_and_caught(self) -> None:
        """PresetLoadError can be raised and caught with its message intact."""
        try:
            raise PresetLoadError("preset.yml not found")
        except PresetLoadError as exc:
            assert str(exc) == "preset.yml not found"

    def test_message_preserved(self) -> None:
        """The error message is preserved in the exception."""
        exc = PresetLoadError("Could not parse preset.yml at /tmp/preset.yml")
        assert "Could not parse preset.yml" in str(exc)


class TestPresetLoadErrorPackageExport:
    """Tests that PresetLoadError is re-exported from the package."""

    def test_reexported_symbol_is_same_class(self) -> None:
        """The package-level PresetLoadError is the exceptions module class."""
        assert ExportedPresetLoadError is PresetLoadError

    def test_appears_in_dunder_all(self) -> None:
        """PresetLoadError is listed in the package __all__."""
        assert "PresetLoadError" in issue_template_pkg.__all__
