"""Tests for _require_sync_playwright."""

from __future__ import annotations

import builtins
import sys
from types import ModuleType
from unittest.mock import patch

import pytest

from agentic_devtools.cli.github.browser_apply_autofix import (
    BrowserAutofixUnavailable,
    _require_sync_playwright,
)


class TestRequireSyncPlaywright:
    """Tests for the lazy Playwright import helper."""

    def test_returns_sync_playwright_when_importable(self) -> None:
        playwright_mod = ModuleType("playwright")
        sync_api_mod = ModuleType("playwright.sync_api")
        sentinel = object()
        setattr(sync_api_mod, "sync_playwright", sentinel)
        with patch.dict(sys.modules, {"playwright": playwright_mod, "playwright.sync_api": sync_api_mod}):
            assert _require_sync_playwright() is sentinel

    def test_raises_when_missing(self) -> None:
        real_import = builtins.__import__

        def fake_import(name, *args, **kwargs):
            if name == "playwright.sync_api":
                raise ImportError("no playwright")
            return real_import(name, *args, **kwargs)

        with patch("builtins.__import__", side_effect=fake_import):
            with pytest.raises(BrowserAutofixUnavailable, match="playwright is not installed"):
                _require_sync_playwright()
