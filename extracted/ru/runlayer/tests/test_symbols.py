"""Tests for terminal-safe symbol constants."""

import importlib
import io
import sys
from unittest.mock import patch

import runlayer_cli.symbols as sym


def test_unicode_symbols_on_utf8():
    """Symbols resolve to Unicode when stdout supports it."""
    fake_stdout = io.TextIOWrapper(io.BytesIO(), encoding="utf-8")
    with patch.object(sys, "stdout", fake_stdout):
        importlib.reload(sym)
        assert sym.OK == "✓"
        assert sym.FAIL == "✗"
        assert sym.WARN == "⚠"


def test_ascii_fallback_on_cp1252():
    """Symbols fall back to ASCII when stdout can't encode Unicode."""
    fake_stdout = io.TextIOWrapper(io.BytesIO(), encoding="cp1252")
    with patch.object(sys, "stdout", fake_stdout):
        importlib.reload(sym)
        assert sym.OK == "[ok]"
        assert sym.FAIL == "[error]"
        assert sym.WARN == "[warn]"


def test_ascii_fallback_on_ascii():
    """Symbols fall back to ASCII when stdout encoding is plain ASCII."""
    fake_stdout = io.TextIOWrapper(io.BytesIO(), encoding="ascii")
    with patch.object(sys, "stdout", fake_stdout):
        importlib.reload(sym)
        assert sym.OK == "[ok]"
        assert sym.FAIL == "[error]"
        assert sym.WARN == "[warn]"


def test_ascii_fallback_when_stdout_is_none():
    """Symbols fall back to ASCII when sys.stdout is None (e.g. pythonw.exe)."""
    with patch.object(sys, "stdout", None):
        importlib.reload(sym)
        assert sym.OK == "[ok]"
        assert sym.FAIL == "[error]"
        assert sym.WARN == "[warn]"
