"""Tests for _github_enterprise_slug."""

from __future__ import annotations

import os
from unittest.mock import patch

from agentic_devtools.cli.github.browser_apply_autofix import (
    DEFAULT_GH_ENTERPRISE,
    _github_enterprise_slug,
)


class TestGithubEnterpriseSlug:
    """Tests for _github_enterprise_slug."""

    def test_returns_env_override(self) -> None:
        with patch.dict("os.environ", {"AGDT_BROWSER_GH_ENTERPRISE": "acme"}):
            assert _github_enterprise_slug() == "acme"

    def test_returns_default_when_unset(self) -> None:
        env = {k: v for k, v in os.environ.items() if k != "AGDT_BROWSER_GH_ENTERPRISE"}
        with patch.dict("os.environ", env, clear=True):
            assert _github_enterprise_slug() == DEFAULT_GH_ENTERPRISE

    def test_returns_default_when_blank(self) -> None:
        with patch.dict("os.environ", {"AGDT_BROWSER_GH_ENTERPRISE": "   "}):
            assert _github_enterprise_slug() == DEFAULT_GH_ENTERPRISE
