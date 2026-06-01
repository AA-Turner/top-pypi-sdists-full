"""Tests for authority guards (require_authorities, require_any_authority)."""

import pytest
from fastapi import HTTPException

from csrd.auth._guards import (
    _get_current_claims,
    require_any_authority,
    require_authorities,
)
from csrd.context.platform import user_info_context
from csrd.models.claims import UserClaims


@pytest.fixture(autouse=True)
def _clear_context():
    """Reset user_info_context before each test."""
    token = user_info_context.set(None)
    yield
    user_info_context.reset(token)


def _set_claims(**kwargs) -> UserClaims:
    claims = UserClaims(**kwargs)
    user_info_context.set(claims)
    return claims


# ── _get_current_claims ──────────────────────────────────────────────────


class TestGetCurrentClaims:
    def test_returns_claims_when_set(self):
        _set_claims(sub="user1", authorities=["ADMIN"])
        claims = _get_current_claims()
        assert claims.sub == "user1"

    def test_raises_403_when_no_claims(self):
        with pytest.raises(HTTPException) as exc_info:
            _get_current_claims()
        assert exc_info.value.status_code == 403
        assert "No authenticated user" in exc_info.value.detail

    def test_raises_403_when_not_user_claims(self):
        user_info_context.set("not a UserClaims object")
        with pytest.raises(HTTPException) as exc_info:
            _get_current_claims()
        assert exc_info.value.status_code == 403


# ── require_authorities ──────────────────────────────────────────────────


class TestRequireAuthorities:
    @pytest.mark.asyncio
    async def test_passes_with_matching_authority(self):
        _set_claims(sub="user1", authorities=["ADMIN"])
        guard = require_authorities("ADMIN")
        await guard()  # should not raise

    @pytest.mark.asyncio
    async def test_passes_with_all_matching_authorities(self):
        _set_claims(sub="user1", authorities=["ADMIN", "MANAGER", "USER"])
        guard = require_authorities("ADMIN", "MANAGER")
        await guard()  # should not raise

    @pytest.mark.asyncio
    async def test_passes_with_superset_of_authorities(self):
        _set_claims(sub="user1", authorities=["ADMIN", "MANAGER", "USER", "SUPER"])
        guard = require_authorities("ADMIN")
        await guard()  # should not raise

    @pytest.mark.asyncio
    async def test_fails_when_missing_one(self):
        _set_claims(sub="user1", authorities=["USER"])
        guard = require_authorities("ADMIN")
        with pytest.raises(HTTPException) as exc_info:
            await guard()
        assert exc_info.value.status_code == 403
        assert "Insufficient authorities" in exc_info.value.detail

    @pytest.mark.asyncio
    async def test_fails_when_missing_some(self):
        _set_claims(sub="user1", authorities=["USER"])
        guard = require_authorities("ADMIN", "MANAGER")
        with pytest.raises(HTTPException) as exc_info:
            await guard()
        assert exc_info.value.status_code == 403
        assert "Insufficient authorities" in exc_info.value.detail

    @pytest.mark.asyncio
    async def test_fails_with_empty_authorities(self):
        _set_claims(sub="user1", authorities=[])
        guard = require_authorities("ADMIN")
        with pytest.raises(HTTPException) as exc_info:
            await guard()
        assert exc_info.value.status_code == 403

    @pytest.mark.asyncio
    async def test_fails_when_no_claims_in_context(self):
        guard = require_authorities("ADMIN")
        with pytest.raises(HTTPException) as exc_info:
            await guard()
        assert exc_info.value.status_code == 403

    def test_raises_on_no_arguments(self):
        with pytest.raises(ValueError, match="at least one"):
            require_authorities()


# ── require_any_authority ────────────────────────────────────────────────


class TestRequireAnyAuthority:
    @pytest.mark.asyncio
    async def test_passes_with_one_match(self):
        _set_claims(sub="user1", authorities=["USER"])
        guard = require_any_authority("ADMIN", "USER")
        await guard()  # should not raise

    @pytest.mark.asyncio
    async def test_passes_with_all_matching(self):
        _set_claims(sub="user1", authorities=["ADMIN", "USER"])
        guard = require_any_authority("ADMIN", "USER")
        await guard()  # should not raise

    @pytest.mark.asyncio
    async def test_fails_with_no_match(self):
        _set_claims(sub="user1", authorities=["VIEWER"])
        guard = require_any_authority("ADMIN", "MANAGER")
        with pytest.raises(HTTPException) as exc_info:
            await guard()
        assert exc_info.value.status_code == 403
        assert "Insufficient authorities" in exc_info.value.detail

    @pytest.mark.asyncio
    async def test_fails_with_empty_authorities(self):
        _set_claims(sub="user1", authorities=[])
        guard = require_any_authority("ADMIN")
        with pytest.raises(HTTPException) as exc_info:
            await guard()
        assert "Insufficient authorities" in exc_info.value.detail

    def test_raises_on_no_arguments(self):
        with pytest.raises(ValueError, match="at least one"):
            require_any_authority()
