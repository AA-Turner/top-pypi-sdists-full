"""Tests for the OAuth service-integration framework.

OpenClaw advertises 50+ service integrations (Gmail, GitHub, Spotify, etc.).
Implementing 50 specific clients is a follow-up; THIS module provides the
framework that makes adding each one ~30 LOC:

  1. ServiceIntegration — a single connected service with scoped tokens
  2. IntegrationStore   — persistent secure storage of tokens (~/.sage/integrations.json)
  3. OAuthFlow          — generic 3-leg OAuth code-grant helper

The first concrete integration shipped is **GitHub** (read-only repo + user
scope) — enough to prove the framework. Gmail/Calendar/Spotify follow the
same pattern.

TDD: tests describe contract + GitHub-specific behavior.
"""

from __future__ import annotations

import json
from datetime import datetime, timedelta, timezone
from pathlib import Path
from unittest.mock import MagicMock

import pytest

from sage.core.service_integrations import (
    GitHubIntegration,
    IntegrationStore,
    ServiceIntegration,
    OAuthCallbackError,
)


# ── ServiceIntegration data shape ────────────────────────────────────────────


class TestServiceIntegration:
    def test_carries_access_token(self):
        si = ServiceIntegration(
            service="github",
            access_token="gho_abc123",
            refresh_token=None,
            expires_at=None,
            scope="repo user",
            account_id="laynef",
        )
        assert si.service == "github"
        assert si.access_token == "gho_abc123"
        assert si.account_id == "laynef"

    def test_is_expired_returns_false_when_no_expiry(self):
        """GitHub tokens don't expire; expiry None = always valid."""
        si = ServiceIntegration(
            service="github",
            access_token="x", refresh_token=None,
            expires_at=None, scope="repo", account_id="u",
        )
        assert not si.is_expired()

    def test_is_expired_returns_true_when_past_expiry(self):
        past = datetime.now(timezone.utc) - timedelta(minutes=10)
        si = ServiceIntegration(
            service="google",
            access_token="x", refresh_token="r",
            expires_at=past, scope="gmail.readonly", account_id="me@example.com",
        )
        assert si.is_expired()

    def test_is_expired_returns_false_when_future(self):
        future = datetime.now(timezone.utc) + timedelta(hours=1)
        si = ServiceIntegration(
            service="google",
            access_token="x", refresh_token="r",
            expires_at=future, scope="gmail.readonly", account_id="u",
        )
        assert not si.is_expired()


# ── IntegrationStore: persistence ───────────────────────────────────────────


class TestIntegrationStore:
    def test_save_and_load_round_trip(self, tmp_path):
        store = IntegrationStore(state_path=tmp_path / "ints.json")
        si = ServiceIntegration(
            service="github", access_token="t",
            refresh_token=None, expires_at=None,
            scope="repo", account_id="laynef",
        )
        store.save(si)
        loaded = store.get("github", "laynef")
        assert loaded is not None
        assert loaded.access_token == "t"

    def test_get_unknown_returns_none(self, tmp_path):
        store = IntegrationStore(state_path=tmp_path / "ints.json")
        assert store.get("github", "nobody") is None

    def test_remove_drops_integration(self, tmp_path):
        store = IntegrationStore(state_path=tmp_path / "ints.json")
        store.save(ServiceIntegration(
            service="github", access_token="t",
            refresh_token=None, expires_at=None,
            scope="repo", account_id="laynef",
        ))
        store.remove("github", "laynef")
        assert store.get("github", "laynef") is None

    def test_list_returns_all_integrations(self, tmp_path):
        store = IntegrationStore(state_path=tmp_path / "ints.json")
        store.save(ServiceIntegration(
            service="github", access_token="t1",
            refresh_token=None, expires_at=None,
            scope="repo", account_id="laynef",
        ))
        store.save(ServiceIntegration(
            service="google", access_token="t2",
            refresh_token="r2", expires_at=None,
            scope="gmail.readonly", account_id="me@x.com",
        ))
        assert len(store.list()) == 2

    def test_file_perms_are_owner_only(self, tmp_path):
        """Tokens are secrets. File mode must be 0600 (owner read+write only)."""
        store = IntegrationStore(state_path=tmp_path / "ints.json")
        store.save(ServiceIntegration(
            service="github", access_token="t",
            refresh_token=None, expires_at=None,
            scope="repo", account_id="laynef",
        ))
        # On Unix, check the perm bits
        stat = (tmp_path / "ints.json").stat()
        mode = stat.st_mode & 0o777
        # Owner-only: 0o600. We allow 0o400 (read-only) as well in case
        # the OS upgraded perms.
        assert mode in (0o600, 0o400)


# ── GitHubIntegration: concrete client ───────────────────────────────────────


class TestGitHubIntegration:
    def test_authorize_url_contains_required_params(self):
        gh = GitHubIntegration(client_id="cid", client_secret="csec")
        url = gh.build_authorize_url(state="xyz", redirect_uri="http://localhost:9999/cb")
        assert "https://github.com/login/oauth/authorize" in url
        assert "client_id=cid" in url
        assert "state=xyz" in url
        assert "scope=" in url
        assert "redirect_uri=" in url

    def test_exchange_code_returns_integration(self):
        gh = GitHubIntegration(
            client_id="cid", client_secret="csec",
            http_client=_FakeHttp(post_response={
                "access_token": "gho_token",
                "scope": "repo,user",
                "token_type": "bearer",
            }, get_response={"login": "laynef", "id": 12345}),
        )
        si = gh.exchange_code(code="abc", redirect_uri="http://localhost:9999/cb")
        assert si.service == "github"
        assert si.access_token == "gho_token"
        assert si.account_id == "laynef"
        assert si.scope == "repo,user"

    def test_exchange_code_raises_on_oauth_error(self):
        gh = GitHubIntegration(
            client_id="cid", client_secret="csec",
            http_client=_FakeHttp(post_response={
                "error": "bad_verification_code",
                "error_description": "The code passed is incorrect or expired.",
            }),
        )
        with pytest.raises(OAuthCallbackError, match="bad_verification_code"):
            gh.exchange_code(code="bad", redirect_uri="http://localhost:9999/cb")

    def test_request_uses_bearer_token(self):
        http = _FakeHttp(get_response={"name": "test-repo"})
        gh = GitHubIntegration(client_id="cid", client_secret="csec", http_client=http)
        si = ServiceIntegration(
            service="github", access_token="gho_xyz",
            refresh_token=None, expires_at=None,
            scope="repo", account_id="u",
        )
        gh.request(si, "GET", "/repos/owner/test-repo")
        # Verify Authorization header was set
        call = http.last_get
        assert call["headers"]["Authorization"] == "token gho_xyz"


# ── Test helpers ────────────────────────────────────────────────────────────


class _FakeHttp:
    """Minimal HTTP client stand-in. Records calls for assertions."""

    def __init__(self, post_response=None, get_response=None):
        self._post = post_response or {}
        self._get = get_response or {}
        self.last_post: dict | None = None
        self.last_get: dict | None = None

    def post(self, url, **kwargs):
        self.last_post = {"url": url, **kwargs}
        return _FakeResponse(self._post)

    def get(self, url, **kwargs):
        self.last_get = {"url": url, **kwargs}
        return _FakeResponse(self._get)


class _FakeResponse:
    def __init__(self, body):
        self._body = body
        self.status_code = 200

    def json(self):
        return self._body

    def raise_for_status(self):
        pass
