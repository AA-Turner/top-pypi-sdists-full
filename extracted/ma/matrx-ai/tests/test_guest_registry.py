from __future__ import annotations

from datetime import UTC, datetime, timedelta
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


class _RecordingGuestManager:
    def __init__(self, rows: list[object], *, reread: list[object] | None = None) -> None:
        self.rows = rows
        self.reread = reread
        self.reads = 0
        self.created: list[dict[str, object]] = []
        self.updates: list[tuple[str, dict[str, object]]] = []
        self.create_error: Exception | None = None

    async def filter_all_guest_executions(self, *, fingerprint: str) -> list[object]:
        self.reads += 1
        if self.reads > 1 and self.reread is not None:
            return self.reread
        return self.rows

    async def create_guest_executions(self, **data: object) -> None:
        if self.create_error is not None:
            raise self.create_error
        self.created.append(data)

    async def update_guest_executions(self, row_id: str, **updates: object) -> None:
        self.updates.append((row_id, updates))


MINTED = "c6e76caa-d115-4e25-a742-c6a5d43ef06e"


@pytest.mark.asyncio
async def test_first_visit_persists_the_minted_identity_for_the_fingerprint(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    # Break caught: the registry row created without the minted auth user —
    # the next request from this browser would mint a SECOND anonymous user.
    manager = _RecordingGuestManager([])
    monkeypatch.setattr(guest_registry, "_gm", manager)
    monkeypatch.setattr(guest_registry, "_create_anon_auth_user", AsyncMock(return_value=MINTED))

    resolved = await guest_registry.resolve_guest_uuid(
        "browser-fingerprint", ip_address="203.0.113.9", user_agent="UA/1"
    )

    assert resolved == MINTED
    assert manager.created == [
        {
            "fingerprint": "browser-fingerprint",
            "auth_user_id": MINTED,
            "ip_address": "203.0.113.9",
            "user_agent": "UA/1",
            "total_executions": 1,
        }
    ]


@pytest.mark.asyncio
async def test_existing_row_without_identity_is_backfilled_with_the_minted_user(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    # Break caught: the backfill update omitting auth_user_id — the row stays
    # identity-less and every request mints a new anonymous auth user.
    row = SimpleNamespace(
        id="guest-row", auth_user_id=None, is_blocked=False, total_executions=4, first_execution_at=None
    )
    manager = _RecordingGuestManager([row])
    monkeypatch.setattr(guest_registry, "_gm", manager)
    monkeypatch.setattr(guest_registry, "_create_anon_auth_user", AsyncMock(return_value=MINTED))

    resolved = await guest_registry.resolve_guest_uuid("browser-fingerprint")

    assert resolved == MINTED
    assert len(manager.updates) == 1
    row_id, updates = manager.updates[0]
    assert row_id == "guest-row"
    assert updates.get("auth_user_id") == MINTED
    assert updates.get("total_executions") == 5


@pytest.mark.asyncio
async def test_failed_first_insert_with_no_registry_winner_is_refused(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    # Break caught: treating every insert failure as a lost race and returning
    # the orphan anonymous identity that no registry row points to.
    manager = _RecordingGuestManager([], reread=[])
    manager.create_error = RuntimeError("insert failed: permission denied")
    monkeypatch.setattr(guest_registry, "_gm", manager)
    monkeypatch.setattr(guest_registry, "_create_anon_auth_user", AsyncMock(return_value=MINTED))

    with pytest.raises(guest_registry.GuestIdentityUnavailableError) as exc_info:
        await guest_registry.resolve_guest_uuid("browser-fingerprint")

    assert "permission denied" in str(exc_info.value.__cause__)


def _blocked_row(*, auth_user_id: str | None, blocked_until: datetime | None) -> SimpleNamespace:
    # Every column of users.guest_executions the resolver can read.
    return SimpleNamespace(
        id="guest-row",
        fingerprint="browser-fingerprint",
        auth_user_id=auth_user_id,
        is_blocked=True,
        blocked_until=blocked_until,
        blocked_reason="abuse",
        total_executions=7,
        daily_executions=3,
        first_execution_at=None,
        last_execution_at=None,
        converted_to_user_id=None,
    )


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "auth_user_id,blocked_until",
    [
        pytest.param("1f8d19c8-fdb8-49f1-b658-3cdab32d0c6e", None, id="identity_minted_block_indefinite"),
        pytest.param(None, None, id="identity_never_minted_block_indefinite"),
        pytest.param(
            "1f8d19c8-fdb8-49f1-b658-3cdab32d0c6e",
            datetime.now(UTC) + timedelta(days=1),
            id="identity_minted_block_until_tomorrow",
        ),
    ],
)
async def test_blocked_guest_is_refused_before_any_counter_or_identity_write(
    monkeypatch: pytest.MonkeyPatch, auth_user_id: str | None, blocked_until: datetime | None
) -> None:
    # Break caught: the is_blocked branch only logging and falling through — the
    # blocked guest gets its auth.users identity back, its execution counters
    # bumped, or a fresh anonymous user minted for it (blocking did nothing).
    manager = _RecordingGuestManager([_blocked_row(auth_user_id=auth_user_id, blocked_until=blocked_until)])
    mint = AsyncMock(return_value=MINTED)
    monkeypatch.setattr(guest_registry, "_gm", manager)
    monkeypatch.setattr(guest_registry, "_create_anon_auth_user", mint)

    with pytest.raises(guest_registry.GuestBlockedError) as exc_info:
        await guest_registry.resolve_guest_uuid("browser-fingerprint")

    assert not isinstance(exc_info.value, guest_registry.GuestIdentityUnavailableError)
    assert exc_info.value.blocked_until == blocked_until
    assert manager.updates == []
    assert manager.created == []
    assert mint.await_count == 0


@pytest.mark.asyncio
async def test_expired_block_resolves_like_an_unblocked_guest(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    # Positive control, same semantics as public.check_guest_execution_limit:
    # a block whose blocked_until has passed is no longer a block. Break caught:
    # a refusal keyed on is_blocked alone that locks expired blocks out forever.
    auth_user_id = "1f8d19c8-fdb8-49f1-b658-3cdab32d0c6e"
    row = _blocked_row(auth_user_id=auth_user_id, blocked_until=datetime.now(UTC) - timedelta(hours=1))
    manager = _RecordingGuestManager([row])
    monkeypatch.setattr(guest_registry, "_gm", manager)

    resolved = await guest_registry.resolve_guest_uuid("browser-fingerprint")

    assert resolved == auth_user_id
    assert manager.updates[0][1]["total_executions"] == 8


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "status,body",
    [
        pytest.param(200, {"user": {}}, id="signup_ok_without_user_id"),
        pytest.param(422, {"error_code": "anonymous_provider_disabled"}, id="provider_disabled"),
    ],
)
async def test_gotrue_signup_without_a_user_id_never_becomes_an_identity(
    monkeypatch: pytest.MonkeyPatch, status: int, body: dict[str, object]
) -> None:
    """GoTrue is the external dependency (httpx transport stubbed). Break
    caught: accepting a signup response with no ``user.id`` — the string
    ``"None"`` would be stored and served as the guest's auth.users identity."""
    import httpx

    real_client = httpx.AsyncClient
    seen: list[str] = []

    def handler(request: httpx.Request) -> httpx.Response:
        seen.append(str(request.url))
        return httpx.Response(status, json=body)

    monkeypatch.setattr(
        httpx,
        "AsyncClient",
        lambda **kw: real_client(transport=httpx.MockTransport(handler), **kw),
    )
    monkeypatch.setenv("SUPABASE_MATRIX_URL", "https://db.invalid/")
    monkeypatch.setenv("SUPABASE_MATRIX_SECRET_KEY", "service-key")
    manager = _RecordingGuestManager([])
    monkeypatch.setattr(guest_registry, "_gm", manager)

    with pytest.raises(guest_registry.GuestIdentityUnavailableError):
        await guest_registry.resolve_guest_uuid("browser-fingerprint")

    assert seen == ["https://db.invalid/auth/v1/signup"]
    assert manager.created == []
