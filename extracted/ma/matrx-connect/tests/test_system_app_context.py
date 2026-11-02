"""system_app_context — an ambient AppContext for work outside a request.

Background work (detached_task, queue worker, NOTIFY listener, scheduled run)
starts with EMPTY contextvars. Anything downstream that calls get_app_context()
— every agent run does — then dies with "No AppContext is set. Ensure
AuthMiddleware is registered and running…", an error that blames middleware for
a request that never existed. This primitive is the sanctioned fix; these tests
pin its load-bearing properties: it WORKS in an empty context, it REFUSES to
mint a context without an organization (the record's, never a default), it is
a NO-OP when the ambient context already IS the requested identity, and it
HONORS a different requested identity instead of silently dropping it.
"""

from __future__ import annotations

import asyncio
import contextvars
import uuid

import pytest

from matrx_connect import (
    AppContext,
    ConsoleEmitter,
    get_app_context,
    set_app_context,
    system_app_context,
    try_get_app_context,
)

ORG_A = str(uuid.uuid4())
ORG_B = str(uuid.uuid4())


async def _in_empty_context(coro_fn):
    """Run coro_fn the way detached_task does — in a brand-new, EMPTY Context,
    so nothing is inherited from the caller."""
    loop = asyncio.get_running_loop()
    return await loop.create_task(coro_fn(), context=contextvars.Context())


@pytest.mark.asyncio
async def test_establishes_context_in_an_empty_contextvars_context():
    """The actual regression: an agent-shaped call inside a detached task."""

    async def work():
        assert try_get_app_context() is None  # the failing precondition, reproduced

        async with system_app_context(
            "auto_ingest", user_id="user-1", organization_id=ORG_A.upper(), source_app="aidream"
        ):
            ctx = get_app_context()  # would have raised RuntimeError before
            assert ctx.user_id == "user-1"
            assert ctx.organization_id == ORG_A  # canonicalized
            assert ctx.source_feature == "auto_ingest"
            assert ctx.is_internal_agent is True
            assert ctx.store is True  # every AI run keeps its history (2026-10-05)
            return ctx.request_id

    request_id = await _in_empty_context(work)
    assert request_id


def _request_context(**overrides) -> AppContext:
    fields = dict(
        emitter=ConsoleEmitter("test", accumulate=False),
        user_id="real-user",
        auth_type="token",
        is_authenticated=True,
        organization_id=ORG_A,
        request_id="req-abc",
        store=True,
    )
    fields.update(overrides)
    return AppContext(**fields)


@pytest.mark.asyncio
async def test_is_a_no_op_when_the_ambient_context_is_the_requested_identity():
    """Safe to wrap an entry point with BOTH an HTTP caller and a background
    caller: a real request for the SAME actor and organization keeps its own
    context (auth, emitter, store) — overrides are not applied to it."""
    request_ctx = _request_context()
    token = set_app_context(request_ctx)
    try:
        async with system_app_context(
            "auto_ingest", user_id="real-user", organization_id=ORG_A, store=False
        ) as ctx:
            assert ctx is request_ctx
            assert get_app_context() is request_ctx
            assert get_app_context().store is True
        # …and it is still installed afterwards — we never tore down a caller's context.
        assert get_app_context() is request_ctx
    finally:
        from matrx_connect import clear_app_context

        clear_app_context(token)


@pytest.mark.asyncio
async def test_a_different_requested_identity_is_installed_not_dropped():
    """THE 2026-09-17 CLASS: a record's organization differs from the one the
    triggering request selected. The record wins for the block; the request
    carriers (emitter, request id) survive; the ambient context is restored."""
    request_ctx = _request_context()
    token = set_app_context(request_ctx)
    try:
        async with system_app_context(
            "sweep", user_id="real-user", organization_id=ORG_B, system_run=True
        ) as ctx:
            assert ctx is not request_ctx
            assert ctx.organization_id == ORG_B
            assert ctx.user_id == "real-user"
            assert ctx.organization_admission == "none"
            assert ctx.emitter is request_ctx.emitter
            assert ctx.request_id == "req-abc"
            assert ctx.system_run is True
            assert ctx.source_feature == "sweep"
            assert get_app_context() is ctx
        assert get_app_context() is request_ctx
    finally:
        from matrx_connect import clear_app_context

        clear_app_context(token)


@pytest.mark.asyncio
async def test_a_different_actor_never_inherits_the_ambient_admin_tier():
    request_ctx = _request_context(
        is_admin=True, admin_level="super_admin", token="jwt", email="admin@example.com"
    )
    token = set_app_context(request_ctx)
    try:
        async with system_app_context("replay", user_id="owner-2", organization_id=ORG_A) as ctx:
            assert ctx.user_id == "owner-2"
            assert ctx.is_admin is False
            assert ctx.admin_level is None
            assert ctx.token is None
            assert ctx.email is None
    finally:
        from matrx_connect import clear_app_context

        clear_app_context(token)


@pytest.mark.asyncio
async def test_refuses_to_mint_without_an_organization():
    """NO NULL ORG. The record being processed carries its organization; a
    system context without one is how work landed in the wrong tenant."""

    async def work():
        with pytest.raises(ValueError, match="organization_id is required"):
            async with system_app_context("auto_ingest", user_id="user-1", organization_id=None):  # type: ignore[arg-type]
                pass
        with pytest.raises(ValueError, match="organization_id is required"):
            async with system_app_context("auto_ingest", user_id="user-1", organization_id="not-an-id"):
                pass
        assert try_get_app_context() is None

    await _in_empty_context(work)


@pytest.mark.asyncio
async def test_context_is_torn_down_after_the_block():
    async def work():
        async with system_app_context("auto_ingest", user_id="user-1", organization_id=ORG_A):
            assert try_get_app_context() is not None
        assert try_get_app_context() is None

    await _in_empty_context(work)


@pytest.mark.asyncio
async def test_teardown_survives_an_exception_in_the_body():
    async def work():
        with pytest.raises(ValueError, match="boom"):
            async with system_app_context("auto_ingest", user_id="user-1", organization_id=ORG_A):
                raise ValueError("boom")
        assert try_get_app_context() is None

    await _in_empty_context(work)


@pytest.mark.asyncio
async def test_overrides_reach_the_context():
    """A caller that needs the cost spine persisted (system_run) or a specific
    conversation_type passes it straight through."""

    async def work():
        async with system_app_context(
            "content_processing_upload_hook",
            user_id="user-1",
            organization_id=ORG_A,
            conversation_type="auto",
            system_run=True,
        ) as ctx:
            assert ctx.conversation_type == "auto"
            assert ctx.system_run is True

    await _in_empty_context(work)


@pytest.mark.asyncio
async def test_isolated_mints_a_separate_context_for_the_SAME_identity():
    """THE SIDE-COMPUTATION CASE: an in-process pass (auto-ingest NER) fired
    from a live save hook runs as the same person in the same organization, but
    must not emit into their stream, persist into their conversation, or borrow
    their persistence intent. ``isolated=True`` turns the same-identity no-op
    off: a derived context is installed for the block and torn down after."""
    request_ctx = _request_context(conversation_id="user-live-conversation")
    token = set_app_context(request_ctx)
    sink_emitter = ConsoleEmitter("auto-ingest-ner", accumulate=False)
    try:
        async with system_app_context(
            "auto_ingest_ner",
            user_id="real-user",
            organization_id=ORG_A,
            source_app="aidream",
            isolated=True,
            emitter=sink_emitter,
            conversation_id="ner-sink-conversation",
            system_run=True,
            store=True,
            agent_id="agent-1",
        ) as ctx:
            assert ctx is not request_ctx
            # identity is unchanged — same actor, same organization
            assert ctx.user_id == "real-user"
            assert ctx.organization_id == ORG_A
            # …but every carrier the side computation named is its own
            assert ctx.emitter is sink_emitter
            assert ctx.emitter is not request_ctx.emitter
            assert ctx.conversation_id == "ner-sink-conversation"
            assert ctx.system_run is True
            assert ctx.store is True
            assert ctx.agent_id == "agent-1"
            assert ctx.is_internal_agent is True
            assert ctx.source_feature == "auto_ingest_ner"
            assert ctx.operation_id != request_ctx.operation_id
            # attribution back to the request that caused it survives
            assert ctx.request_id == "req-abc"
            assert get_app_context() is ctx
        # the person's own context is untouched and still installed
        assert get_app_context() is request_ctx
        assert request_ctx.conversation_id == "user-live-conversation"
        assert request_ctx.store is True
    finally:
        from matrx_connect import clear_app_context

        clear_app_context(token)


@pytest.mark.asyncio
async def test_isolated_defaults_to_off_so_every_existing_caller_is_unchanged():
    """The no-op is the DEFAULT — only an explicit isolated=True opts out."""
    request_ctx = _request_context()
    token = set_app_context(request_ctx)
    try:
        async with system_app_context(
            "auto_ingest", user_id="real-user", organization_id=ORG_A, store=False
        ) as ctx:
            assert ctx is request_ctx
        async with system_app_context(
            "auto_ingest",
            user_id="real-user",
            organization_id=ORG_A,
            isolated=False,
            store=False,
        ) as ctx:
            assert ctx is request_ctx
        assert get_app_context() is request_ctx
    finally:
        from matrx_connect import clear_app_context

        clear_app_context(token)


@pytest.mark.asyncio
async def test_isolated_does_not_unlock_the_identity_refusals():
    """isolated=True is about WHERE the work streams, never about who it runs
    as: the private tenant bindings stay un-overrideable."""
    request_ctx = _request_context()
    token = set_app_context(request_ctx)
    try:
        for private_field in (
            "_tenant_provenance",
            "_tenant_context_seal",
            "_organization_admission_binding",
            "_organization_admission_provenance_binding",
        ):
            with pytest.raises(ValueError, match="not overrideable"):
                async with system_app_context(
                    "auto_ingest_ner",
                    user_id="real-user",
                    organization_id=ORG_A,
                    isolated=True,
                    **{private_field: None},
                ):
                    pass
        with pytest.raises(ValueError, match="organization_id is required"):
            async with system_app_context(
                "auto_ingest_ner", user_id="real-user", organization_id=None, isolated=True  # type: ignore[arg-type]
            ):
                pass
        assert get_app_context() is request_ctx
    finally:
        from matrx_connect import clear_app_context

        clear_app_context(token)


@pytest.mark.asyncio
async def test_isolated_in_an_empty_context_still_mints_a_fresh_one():
    async def work():
        async with system_app_context(
            "auto_ingest_ner", user_id="user-1", organization_id=ORG_A, isolated=True
        ) as ctx:
            assert ctx.user_id == "user-1"
            assert ctx.organization_id == ORG_A
        assert try_get_app_context() is None

    await _in_empty_context(work)
