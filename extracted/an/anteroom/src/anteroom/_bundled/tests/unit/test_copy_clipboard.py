"""Tests for the CLI clipboard helper _copy_text_to_clipboard()."""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest

from anteroom.cli.repl import _ClipboardUnavailableError, _copy_text_to_clipboard


class TestCopyTextToClipboard:
    """Verify _copy_text_to_clipboard behavior."""

    def test_copy_success(self) -> None:
        """Happy path: pyperclip.copy is called with the text."""
        mock_pyperclip = MagicMock()
        with patch.dict("sys.modules", {"pyperclip": mock_pyperclip}):
            _copy_text_to_clipboard("hello world")
        mock_pyperclip.copy.assert_called_once_with("hello world")

    def test_copy_import_error(self) -> None:
        """When pyperclip is not installed, raises _ClipboardUnavailableError."""
        with patch.dict("sys.modules", {"pyperclip": None}):
            with pytest.raises(_ClipboardUnavailableError, match="pyperclip"):
                _copy_text_to_clipboard("hello")

    def test_copy_pyperclip_exception(self) -> None:
        """When pyperclip.copy raises PyperclipException, wraps it."""
        import pyperclip

        mock_mod = MagicMock()
        mock_mod.copy.side_effect = pyperclip.PyperclipException("no clipboard")
        mock_mod.PyperclipException = pyperclip.PyperclipException
        with patch.dict("sys.modules", {"pyperclip": mock_mod}):
            with pytest.raises(_ClipboardUnavailableError, match="no clipboard"):
                _copy_text_to_clipboard("hello")
