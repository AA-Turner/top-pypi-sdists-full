"""Forcing contract tests for explicitly owned non-HTTP tenant contexts."""

from __future__ import annotations

import asyncio
import contextvars
import dataclasses

import pytest

from matrx_connect import (
    AppContext,
    ConsoleEmitter,
    OrganizationFreeAppContext,
    TenantAppContext,
    get_app_context,
    organization_free_context,
    require_tenant_context,
    set_app_context,
    tenant_system_context,
    try_get_app_context,
)

ORG_ID = "11111111-1111-4111-8111-111111111111"
OTHER_ORG_ID = "22222222-2222-4222-8222-222222222222"


async def _in_empty_context(coro_fn):
    loop = asyncio.get_running_loop()
    return await loop.create_task(coro_fn(), context=contextvars.Context())


@pytest.mark.asyncio
async def test_mints_explicit_system_tenant_with_existing_system_defaults() -> None:
    async def work() -> str:
        async with tenant_system_context(
            "tenant-worker", user_id="user-1", organization_id=f"  {ORG_ID.upper()}  "
        ) as ctx:
            assert isinstance(ctx, TenantAppContext)
            assert ctx.organization_id == ORG_ID
            assert ctx.organization_admission == "none"
            assert ctx.claimed_organization_id is None
            assert ctx._organization_admission_binding == ORG_ID
            assert ctx._organization_admission_provenance_binding == "none"
            assert ctx.origin_class == "system"
            assert ctx.store is True
            assert ctx.is_internal_agent is True
            assert get_app_context() is ctx
            inherited = await asyncio.create_task(asyncio.sleep(0, result=get_app_context()))
            assert inherited is ctx
            return ctx.request_id

    assert await _in_empty_context(work)


@pytest.mark.asyncio
async def test_rejects_invalid_org_and_illegal_admission_before_installing_context() -> None:
    async def work() -> None:
        with pytest.raises(ValueError, match="organization_id"):
            async with tenant_system_context("worker", user_id="u", organization_id="bad"):
                pass
        with pytest.raises(ValueError, match="cannot claim"):
            async with tenant_system_context(
                "worker", user_id="u", organization_id=ORG_ID, organization_admission="verified"
            ):
                pass
        assert try_get_app_context() is None

    await _in_empty_context(work)


@pytest.mark.asyncio
async def test_reuses_same_tenant_and_rejects_different_ambient_organization() -> None:
    async def work() -> None:
        async with tenant_system_context("outer", user_id="u", organization_id=ORG_ID) as outer:
            async with tenant_system_context("inner", user_id="u", organization_id=ORG_ID) as inner:
                assert inner is outer
            with pytest.raises(ValueError, match="principal does not match"):
                async with tenant_system_context("wrong-user", user_id="different", organization_id=ORG_ID):
                    pass
            with pytest.raises(ValueError, match="does not match"):
                async with tenant_system_context("wrong", user_id="u", organization_id=OTHER_ORG_ID):
                    pass
            assert get_app_context() is outer

    await _in_empty_context(work)


@pytest.mark.asyncio
async def test_concurrent_system_tenants_do_not_cross_contextvars() -> None:
    async def work(organization_id: str) -> str:
        async with tenant_system_context("worker", user_id="u", organization_id=organization_id):
            await asyncio.sleep(0)
            return get_app_context().organization_id

    first, second = await asyncio.gather(
        _in_empty_context(lambda: work(ORG_ID)),
        _in_empty_context(lambda: work(OTHER_ORG_ID)),
    )
    assert (first, second) == (ORG_ID, OTHER_ORG_ID)


@pytest.mark.asyncio
async def test_promotes_verified_base_temporarily_and_rejects_unverified_or_free_ambient_context() -> None:
    verified_base = AppContext(
        emitter=ConsoleEmitter("test", accumulate=False),
        user_id="u",
        is_authenticated=True,
        organization_id=ORG_ID,
        organization_admission="verified",
    )
    token = set_app_context(verified_base)
    try:
        async with tenant_system_context("worker", user_id="u", organization_id=ORG_ID) as promoted:
            assert isinstance(promoted, TenantAppContext)
            assert promoted.organization_admission == "verified"
            assert get_app_context() is promoted
        assert get_app_context() is verified_base
    finally:
        from matrx_connect import clear_app_context

        clear_app_context(token)

    for rejected in (
        AppContext(emitter=ConsoleEmitter("test", accumulate=False), organization_id=ORG_ID),
        organization_free_context(
            AppContext(
                emitter=ConsoleEmitter("test", accumulate=False),
                organization_id=ORG_ID,
                organization_admission="verified",
            )
        ),
    ):
        token = set_app_context(rejected)
        try:
            with pytest.raises(ValueError):
                async with tenant_system_context("worker", user_id="u", organization_id=ORG_ID):
                    pass
        finally:
            from matrx_connect import clear_app_context

            clear_app_context(token)


@pytest.mark.asyncio
async def test_tenant_admission_provenance_is_sealed_through_copies_and_round_trip() -> None:
    async with tenant_system_context("worker", user_id="u", organization_id=ORG_ID) as system_tenant:
        assert require_tenant_context(system_tenant) is system_tenant
        assert system_tenant.with_execution_attribution(
            "workflow_run", "33333333-3333-4333-8333-333333333333"
        ).organization_admission == "none"
        assert system_tenant.fork_for_child_agent(
            "44444444-4444-4444-8444-444444444444"
        ).organization_admission == "none"
        assert system_tenant.fork_for_workflow_step(
            "55555555-5555-4555-8555-555555555555"
        ).organization_admission == "none"
        with pytest.raises(ValueError, match="typed admitted provenance"):
            TenantAppContext(**dataclasses.asdict(system_tenant))
        with pytest.raises(ValueError, match="provenance"):
            dataclasses.replace(system_tenant, organization_admission="verified")
        with pytest.raises(ValueError, match="provenance"):
            system_tenant.with_overrides(organization_admission="verified")
        with pytest.raises(AttributeError, match="not overrideable"):
            system_tenant.with_overrides(_tenant_context_seal=None)
        with pytest.raises(ValueError, match="organization admission binding is required"):
            dataclasses.replace(system_tenant, _organization_admission_binding=None)
        with pytest.raises(ValueError, match="provenance binding is required"):
            dataclasses.replace(system_tenant, _organization_admission_provenance_binding=None)
    with pytest.raises(ValueError, match="organization admission binding is required"):
        TenantAppContext(
            emitter=ConsoleEmitter("test", accumulate=False),
            user_id="u",
            organization_id=ORG_ID,
            organization_admission="none",
        )


@pytest.mark.asyncio
async def test_tenant_system_context_restores_after_error_and_cancellation() -> None:
    async def error_work() -> None:
        with pytest.raises(ValueError, match="boom"):
            async with tenant_system_context("worker", user_id="u", organization_id=ORG_ID):
                raise ValueError("boom")
        assert try_get_app_context() is None

    async def cancellation_work() -> None:
        with pytest.raises(asyncio.CancelledError):
            async with tenant_system_context("worker", user_id="u", organization_id=ORG_ID):
                raise asyncio.CancelledError()
        assert try_get_app_context() is None

    await _in_empty_context(error_work)
    await _in_empty_context(cancellation_work)


@pytest.mark.asyncio
async def test_organization_free_clears_system_tenant_provenance_binding() -> None:
    async with tenant_system_context("worker", user_id="u", organization_id=ORG_ID) as tenant:
        free = organization_free_context(tenant)
        assert isinstance(free, OrganizationFreeAppContext)
        assert free._organization_admission_provenance_binding is None
        assert free._tenant_provenance is None
        with pytest.raises(ValueError, match="organization-free"):
            require_tenant_context(free)
