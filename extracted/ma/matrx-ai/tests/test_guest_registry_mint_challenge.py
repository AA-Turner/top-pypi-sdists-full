"""Both guest mint doors (the header lane's ``resolve_guest_uuid`` and the browser session's
``mint_guest_browser_session``) pass ``_enforce_mint_ceiling``; the host's human challenge
(``guest_mint_challenge``, FREE-ALLOWANCE.md §5) runs there — only for a NEW identity, after the
per-IP ceiling admits the mint and before GoTrue, also for an uncountable address."""

from __future__ import annotations

import pytest

from matrx_ai import _ext
from matrx_ai.db import _guest_registry_impl as reg


@pytest.mark.asyncio
async def test_the_registry_asks_the_challenge_only_for_a_new_identity(monkeypatch):
    """Both mint doors pass ``_enforce_mint_ceiling``: the challenge runs there, after the per-IP
    ceiling admits the mint and before GoTrue — and also for an uncountable address."""
    asked: list[str | None] = []

    async def _challenge(ip: str | None) -> None:
        asked.append(ip)
        raise reg.GuestMintChallengeError("missing")

    async def _limits(ip: str | None) -> tuple[int, int] | None:
        return None if ip == "127.0.0.1" else (30, 60)

    monkeypatch.setitem(_ext._registry, "guest_mint_challenge", _challenge)
    monkeypatch.setitem(_ext._registry, "guest_mint_limit_reader", _limits)
    monkeypatch.setattr(reg, "_schedule_seed", lambda *_a: None)
    for ip in ("198.51.100.4", "127.0.0.1"):
        with pytest.raises(reg.GuestMintChallengeError):
            await reg._enforce_mint_ceiling(ip)
    assert asked == ["198.51.100.4", "127.0.0.1"]
    assert reg._mint_log.get("198.51.100.4", []) == []  # a refused mint is not counted
