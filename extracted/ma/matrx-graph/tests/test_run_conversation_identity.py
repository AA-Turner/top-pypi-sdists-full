from __future__ import annotations

import pytest
from matrx_graph.db.run_store import RunStore, _require_optional_uuid


def test_run_conversation_uuid_is_canonicalized() -> None:
    assert (
        _require_optional_uuid(
            "AAAAAAAA-AAAA-4AAA-8AAA-AAAAAAAAAAAA",
            "conversation_id",
        )
        == "aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa"
    )


def test_invalid_run_conversation_uuid_fails_loudly() -> None:
    with pytest.raises(ValueError, match="conversation_id must be a valid UUID"):
        _require_optional_uuid("not-a-conversation-uuid", "conversation_id")


@pytest.mark.asyncio
async def test_standalone_run_model_does_not_require_host_completeness_field(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from matrx_graph.db import run_store as module

    captured: list[dict[str, object]] = []

    class _StandaloneRunModel:
        @classmethod
        async def create(cls, **fields: object) -> None:
            captured.append(fields)

    monkeypatch.setattr(module, "get_model", lambda name: _StandaloneRunModel)
    await RunStore().create(
        definition_id="11111111-1111-4111-8111-111111111111",
        definition_hash="hash",
        # Every workflow run belongs to an organization (Arman, 2026-08-23) —
        # "standalone" describes the HOST, never an org-less run. The package
        # is independent AND opinionated: it ships our structure, and an
        # org-less run is not part of it.
        organization_id="22222222-2222-4222-8222-222222222222",
    )

    assert "request_attribution_complete" not in captured[0]


@pytest.mark.asyncio
async def test_host_can_opt_run_into_complete_request_attribution(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from matrx_graph.db import run_store as module

    captured: list[dict[str, object]] = []

    class _HostRunModel:
        @classmethod
        async def create(cls, **fields: object) -> None:
            captured.append(fields)

    monkeypatch.setattr(module, "get_model", lambda name: _HostRunModel)
    await RunStore().create(
        definition_id="11111111-1111-4111-8111-111111111111",
        definition_hash="hash",
        organization_id="22222222-2222-4222-8222-222222222222",
        request_attribution_complete=True,
    )

    assert captured[0]["request_attribution_complete"] is True


# ── EVERY RUN BELONGS TO AN ORGANIZATION (Arman, 2026-08-23) ────────────────
# "There is no such thing as a detached workflow." The column is NOT NULL, so
# a None never FAILS — `platform.stamp_run_org` silently assigns the owner's
# personal org, and the run becomes invisible to the org that started it with
# nothing recording that a guess was made. The store refuses instead.


@pytest.mark.asyncio
async def test_a_run_with_no_organization_is_refused(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from matrx_graph.db import run_store as module

    created: list[dict[str, object]] = []

    class _Model:
        @classmethod
        async def create(cls, **fields: object) -> None:
            created.append(fields)

    monkeypatch.setattr(module, "get_model", lambda name: _Model)

    from matrx_graph.db.run_store import RunStore

    with pytest.raises(ValueError, match="no organization"):
        await RunStore().create(
            definition_id="11111111-1111-4111-8111-111111111111",
            definition_hash="hash",
        )
    # THE FORCING FUNCTION: refused BEFORE the insert, so the database never
    # gets the chance to stamp a guess.
    assert created == []


@pytest.mark.asyncio
async def test_a_derived_run_inherits_its_parents_organization(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A fork / durable subgraph child / race arm is a CONTINUATION of one run.

    Its org is that run's — never the request context's, which is exactly the
    channel that cannot be trusted on a detached leg (the contextvar trap
    `durable_run_organization` exists for).
    """
    from matrx_graph.db import run_store as module

    parent_id = "33333333-3333-4333-8333-333333333333"
    parent_org = "44444444-4444-4444-8444-444444444444"
    created: list[dict[str, object]] = []

    class _Model:
        @classmethod
        def filter(cls, **_kw: object) -> "_Model":
            return cls()  # type: ignore[return-value]

        async def values(self, *_a: object) -> list[dict[str, object]]:
            return [{"organization_id": parent_org}]

        @classmethod
        async def create(cls, **fields: object) -> None:
            created.append(fields)

    monkeypatch.setattr(module, "get_model", lambda name: _Model)

    from matrx_graph.db.run_store import RunStore

    await RunStore().create(
        definition_id="11111111-1111-4111-8111-111111111111",
        definition_hash="hash",
        parent_run_id=parent_id,
        # organization_id deliberately omitted — the whole point.
    )
    assert str(created[0]["organization_id"]) == parent_org
