"""Tests for _browser_tier_enabled."""

from __future__ import annotations

import os
from unittest.mock import patch

from agentic_devtools.cli.ci.pipeline.discovery.orchestrator import _browser_tier_enabled


class TestBrowserTierEnabled:
    """Tests for _browser_tier_enabled."""

    def test_enabled_for_truthy_values(self) -> None:
        for val in ["1", "true", "TRUE", "Yes", " yes "]:
            with patch.dict("os.environ", {"ENABLE_BROWSER_APPLY_SUGGESTIONS": val}):
                assert _browser_tier_enabled() is True

    def test_disabled_for_false_value(self) -> None:
        with patch.dict("os.environ", {"ENABLE_BROWSER_APPLY_SUGGESTIONS": "false"}):
            assert _browser_tier_enabled() is False

    def test_disabled_when_unset(self) -> None:
        env = {k: v for k, v in os.environ.items() if k != "ENABLE_BROWSER_APPLY_SUGGESTIONS"}
        with patch.dict("os.environ", env, clear=True):
            assert _browser_tier_enabled() is False
