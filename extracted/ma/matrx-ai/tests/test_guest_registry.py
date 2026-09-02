from __future__ import annotations

from types import SimpleNamespace
from unittest.mock import AsyncMock

import pytest

from matrx_ai.db import _guest_registry_impl as guest_registry


class _GuestManager:
    def __init__(self, auth_user_id: str) -> None:
        self.row = SimpleNamespace(
            id="guest-row",
            auth_user_id=auth_user_id,
            is_blocked=False,
            total_executions=2,
            first_execution_at=None,
        )
        self.filter_calls: list[str] = []
        self.updates: list[tuple[str, dict[str, object]]] = []

    async def filter_all_guest_executions(self, *, fingerprint: str) -> list[object]:
        self.filter_calls.append(fingerprint)
        return [self.row]

    async def update_guest_executions(self, row_id: str, **updates: object) -> None:
        self.updates.append((row_id, updates))


class _FailingGuestManager:
    async def filter_all_guest_executions(self, *, fingerprint: str) -> list[object]:
        raise RuntimeError("guest registry unavailable")


class _FirstVisitRaceManager:
    def __init__(self, winner_auth_user_id: str) -> None:
        self.winner_auth_user_id = winner_auth_user_id
        self.reads = 0

    async def filter_all_guest_executions(self, *, fingerprint: str) -> list[object]:
        self.reads += 1
        if self.reads == 1:
            return []
        return [SimpleNamespace(auth_user_id=self.winner_auth_user_id)]

    async def create_guest_executions(self, **data: object) -> None:
        raise RuntimeError("unique fingerprint race")


@pytest.mark.asyncio
async def test_existing_guest_uses_generated_manager_filter(monkeypatch: pytest.MonkeyPatch) -> None:
    auth_user_id = "1f8d19c8-fdb8-49f1-b658-3cdab32d0c6e"
    manager = _GuestManager(auth_user_id)
    monkeypatch.setattr(guest_registry, "_gm", manager)

    resolved = await guest_registry.resolve_guest_uuid("browser-fingerprint")

    assert resolved == auth_user_id
    assert manager.filter_calls == ["browser-fingerprint"]
    assert manager.updates[0][0] == "guest-row"
    assert manager.updates[0][1]["total_executions"] == 3
    assert manager.updates[0][1]["first_execution_at"] is not None
    assert manager.updates[0][1]["last_execution_at"] is not None


@pytest.mark.asyncio
async def test_existing_guest_preserves_original_first_execution(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    auth_user_id = "1f8d19c8-fdb8-49f1-b658-3cdab32d0c6e"
    manager = _GuestManager(auth_user_id)
    first_execution = "2026-08-01T12:00:00+00:00"
    manager.row.first_execution_at = first_execution
    monkeypatch.setattr(guest_registry, "_gm", manager)

    await guest_registry.resolve_guest_uuid("browser-fingerprint")

    assert manager.updates[0][1]["first_execution_at"] == first_execution


@pytest.mark.asyncio
async def test_guest_resolution_never_returns_synthetic_user_id(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(guest_registry, "_gm", _FailingGuestManager())

    with pytest.raises(guest_registry.GuestIdentityUnavailableError) as exc_info:
        await guest_registry.resolve_guest_uuid("browser-fingerprint")

    assert "auth.users" in str(exc_info.value)


@pytest.mark.asyncio
async def test_concurrent_first_visit_adopts_the_registry_winner(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    winner_auth_user_id = "219ce851-a7f6-4c03-bf62-55c18420945d"
    manager = _FirstVisitRaceManager(winner_auth_user_id)
    monkeypatch.setattr(guest_registry, "_gm", manager)
    monkeypatch.setattr(
        guest_registry,
        "_create_anon_auth_user",
        AsyncMock(return_value="c6e76caa-d115-4e25-a742-c6a5d43ef06e"),
    )

    resolved = await guest_registry.resolve_guest_uuid("browser-fingerprint")

    assert resolved == winner_auth_user_id
    assert manager.reads == 2
