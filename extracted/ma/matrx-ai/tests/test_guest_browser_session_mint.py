"""mint_guest_browser_session (G2 guest data): the session is KEPT; a blocked visitor never mints."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
from types import SimpleNamespace
from unittest.mock import AsyncMock

import pytest

from matrx_ai.db import _guest_registry_impl as guest_registry


class _Rows:
    def __init__(self, rows: list[object]) -> None:
        self.rows = rows

    async def filter_all_guest_executions(self, **_: object) -> list[object]:
        return self.rows


@pytest.fixture(autouse=True)
def _no_ceiling(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(guest_registry, "_enforce_mint_ceiling", AsyncMock(return_value=None))


async def test_the_browser_gets_the_session_gotrue_minted(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(guest_registry, "_gm", _Rows([]))
    monkeypatch.setattr(
        guest_registry,
        "_gotrue_anonymous_signup",
        AsyncMock(return_value={"user": {"id": "u-1"}, "access_token": "jwt", "refresh_token": "rt", "expires_in": 3600, "expires_at": 7}),
    )
    out = await guest_registry.mint_guest_browser_session("A" * 24, "203.0.113.1")
    assert out == {"user_id": "u-1", "access_token": "jwt", "refresh_token": "rt", "expires_in": 3600, "expires_at": 7, "token_type": "bearer"}


async def test_a_blocked_visitor_is_refused_before_gotrue(monkeypatch: pytest.MonkeyPatch) -> None:
    row = SimpleNamespace(is_blocked=True, blocked_until=datetime.now(UTC) + timedelta(days=1))
    monkeypatch.setattr(guest_registry, "_gm", _Rows([row]))
    signup = AsyncMock()
    monkeypatch.setattr(guest_registry, "_gotrue_anonymous_signup", signup)
    with pytest.raises(guest_registry.GuestBlockedError):
        await guest_registry.mint_guest_browser_session("A" * 24, None)
    signup.assert_not_called()


async def test_a_mint_without_a_session_is_an_outage_never_a_half_guest(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(guest_registry, "_gm", _Rows([]))
    monkeypatch.setattr(guest_registry, "_gotrue_anonymous_signup", AsyncMock(return_value={"user": {"id": "u-2"}}))
    with pytest.raises(guest_registry.GuestIdentityUnavailableError):
        await guest_registry.mint_guest_browser_session("A" * 24, None)
