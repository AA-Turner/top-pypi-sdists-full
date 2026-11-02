"""Tests for github_provider._reset_read_token_pool()."""

from unittest.mock import Mock

import pytest

import agentic_devtools.cli.ci.github_provider as github_provider
from agentic_devtools.cli.ci.read_token_pool import ReadTokenPool


def test_clears_cached_pool_and_repository(monkeypatch: pytest.MonkeyPatch) -> None:
    pool = ReadTokenPool(
        repo="owner/repo",
        secrets_json=None,
        request=lambda _endpoint, _token, _identity: ("{}", None),
        on_rate_limit=Mock(),
    )
    monkeypatch.setattr(github_provider, "_READ_TOKEN_POOL", pool)
    monkeypatch.setattr(github_provider, "_READ_TOKEN_POOL_REPO", "owner/repo")

    github_provider._reset_read_token_pool()

    assert github_provider._READ_TOKEN_POOL is None
    assert github_provider._READ_TOKEN_POOL_REPO == ""
