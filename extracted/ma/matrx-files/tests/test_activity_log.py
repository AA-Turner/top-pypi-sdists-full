"""File activity events land in the canonical ``platform.log_activity`` RPC.

The RPC call IS the contract (the DB boundary): its positional arguments are the
row that gets written. Expected values are literals, never derived from the SUT.

The event's ORGANIZATION is carried, never defaulted: the caller names it, else
it is read off the active request context, else the event is DROPPED with a
remedy — it is never filed in an organization picked for the actor
(common-docs/policies/context-is-carried-never-rebuilt.md).
"""

from __future__ import annotations

from unittest.mock import AsyncMock

import pytest

from matrx_files.cloud_sync.db import DatabaseClient


def _carry_organization(organization_id: str | None) -> None:
    """Install the host context seam; ``None`` = a context with no organization."""
    from matrx_utils import ctx as matrx_ctx

    matrx_ctx._context_getter = lambda: matrx_ctx.SimpleUserContext(
        user_id="user-1",
        is_authenticated=True,
        organization_id=organization_id,
    )


@pytest.mark.asyncio
async def test_append_event_uses_canonical_activity_log(monkeypatch) -> None:
    client = object.__new__(DatabaseClient)
    rpc = AsyncMock(return_value=None)
    monkeypatch.setattr(client, "_rpc", rpc)
    _carry_organization("org-1")

    await client.append_event_async(
        "file.deleted",
        actor_id="user-1",
        actor_type="user",
        resource_type="file",
        resource_id="file-1",
        payload={"reason": "request"},
        request_id="req-1",
        ip_address="127.0.0.1",
    )

    rpc.assert_awaited_once_with(
        "platform",
        "log_activity",
        "org-1",
        "file.deleted",
        "file",
        "file-1",
        {
            "reason": "request",
            "actor_id": "user-1",
            "actor_type": "user",
            "request_id": "req-1",
            "ip_address": "127.0.0.1",
        },
        "user-1",
        mode="none",
    )


@pytest.mark.asyncio
async def test_append_event_stamps_the_callers_organization_not_the_carried_one(
    monkeypatch,
) -> None:
    client = object.__new__(DatabaseClient)
    rpc = AsyncMock(return_value=None)
    monkeypatch.setattr(client, "_rpc", rpc)
    _carry_organization("org-of-the-request")

    await client.append_event_async(
        "file.shared",
        actor_id="user-1",
        organization_id="org-team",
        resource_type="file",
        resource_id="file-1",
    )

    assert rpc.await_args.args[:3] == ("platform", "log_activity", "org-team")


@pytest.mark.asyncio
async def test_append_event_never_files_the_row_in_an_organization_picked_for_the_actor(
    monkeypatch,
) -> None:
    """No organization named, none carried → the row is DROPPED, not re-tenanted.

    Before 2026-09-17 this resolved a per-user assumed organization and filed
    the row there, where the organization the action happened in can never
    see it.
    """
    client = object.__new__(DatabaseClient)
    rpc = AsyncMock(return_value=None)
    monkeypatch.setattr(client, "_rpc", rpc)
    _carry_organization(None)

    await client.append_event_async("file.deleted", actor_id="user-1")

    rpc.assert_not_awaited()
    # There is no per-user organization lookup left to reach for.
    assert not [name for name in dir(DatabaseClient) if "organization" in name and "ensure" in name]


@pytest.mark.asyncio
async def test_append_event_payload_cannot_override_the_recorded_actor(monkeypatch) -> None:
    client = object.__new__(DatabaseClient)
    rpc = AsyncMock(return_value=None)
    monkeypatch.setattr(client, "_rpc", rpc)
    _carry_organization("org-1")

    await client.append_event_async(
        "file.deleted",
        actor_id="user-1",
        payload={"actor_id": "someone-else", "actor_type": "system", "reason": "request"},
    )

    assert rpc.await_args.args[6] == {
        "actor_id": "user-1",
        "actor_type": "user",
        "reason": "request",
        "request_id": None,
        "ip_address": None,
    }
    assert rpc.await_args.args[7] == "user-1"


@pytest.mark.asyncio
async def test_append_event_without_actor_drops_instead_of_writing_unscoped(
    monkeypatch,
) -> None:
    client = object.__new__(DatabaseClient)
    rpc = AsyncMock(return_value=None)
    monkeypatch.setattr(client, "_rpc", rpc)
    _carry_organization("org-1")

    await client.append_event_async("system.tick", actor_id=None)

    rpc.assert_not_awaited()
