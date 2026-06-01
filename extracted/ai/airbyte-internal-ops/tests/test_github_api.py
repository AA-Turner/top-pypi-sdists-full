# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""Tests for GitHub API helpers."""

from __future__ import annotations

from unittest.mock import patch

import pytest

from airbyte_ops_mcp.github_api import resolve_default_github_token


@pytest.mark.unit
def test_resolve_default_github_token_returns_none_when_allowed() -> None:
    with patch(
        "airbyte_ops_mcp.github_api._get_gh_cli_token", return_value=None
    ), patch("airbyte_ops_mcp.github_api.os.getenv", return_value=None):
        token = resolve_default_github_token(allow_none=True)

    assert token is None


@pytest.mark.unit
def test_resolve_default_github_token_raises_by_default() -> None:
    with patch(
        "airbyte_ops_mcp.github_api._get_gh_cli_token", return_value=None
    ), patch("airbyte_ops_mcp.github_api.os.getenv", return_value=None), pytest.raises(
        ValueError, match="No GitHub token found"
    ):
        resolve_default_github_token()
