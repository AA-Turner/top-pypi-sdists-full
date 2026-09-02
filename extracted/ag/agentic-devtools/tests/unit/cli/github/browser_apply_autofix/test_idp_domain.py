"""Tests for _idp_domain."""

from __future__ import annotations

import os
from unittest.mock import patch

from agentic_devtools.cli.github.browser_apply_autofix import (
    DEFAULT_IDP_DOMAIN,
    _idp_domain,
)


class TestIdpDomain:
    """Tests for _idp_domain."""

    def test_returns_env_override(self) -> None:
        with patch.dict("os.environ", {"AGDT_BROWSER_IDP_DOMAIN": "idp.acme.example"}):
            assert _idp_domain() == "idp.acme.example"

    def test_returns_default_when_unset(self) -> None:
        env = {k: v for k, v in os.environ.items() if k != "AGDT_BROWSER_IDP_DOMAIN"}
        with patch.dict("os.environ", env, clear=True):
            assert _idp_domain() == DEFAULT_IDP_DOMAIN

    def test_returns_default_when_blank(self) -> None:
        with patch.dict("os.environ", {"AGDT_BROWSER_IDP_DOMAIN": "   "}):
            assert _idp_domain() == DEFAULT_IDP_DOMAIN
