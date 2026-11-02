"""Tests for _require_pyotp."""

from __future__ import annotations

import builtins
import sys
from types import ModuleType
from unittest.mock import patch

import pytest

from agentic_devtools.cli.github.browser_apply_autofix import BrowserAutofixUnavailable, _require_pyotp


class TestRequirePyotp:
    """Tests for the lazy pyotp import helper."""

    def test_returns_module_when_importable(self) -> None:
        fake = ModuleType("pyotp")
        with patch.dict(sys.modules, {"pyotp": fake}):
            assert _require_pyotp() is fake

    def test_raises_when_missing(self) -> None:
        real_import = builtins.__import__

        def fake_import(name, *args, **kwargs):
            if name == "pyotp":
                raise ImportError("no pyotp")
            return real_import(name, *args, **kwargs)

        with patch("builtins.__import__", side_effect=fake_import):
            with pytest.raises(BrowserAutofixUnavailable, match="pyotp is not installed"):
                _require_pyotp()
