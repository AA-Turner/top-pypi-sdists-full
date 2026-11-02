"""A worker started from inside a live request still carries the witness of the request it re-runs.

Live 2026-10-24 03:55:46Z (conversation 577db529, ``ops.system_error`` d2c0d108): Arman answered his
own turn's vault-capture request on the signed-in page. ``POST /action-requests/complete`` resumed
the parked turn under ``system_app_context("action_request_continuation", ...)``, which, inside that
live request, derives a context that keeps the request's carriers, ``route`` included. A
resumed-run / continued-run witness was only read when the context had NO route, so the door's
route disqualified it, the turn read as background ``system`` and the protected-account guard
refused his own turn ("Not run: this automated run would have run as, and billed, a protected
account").

Locked here: a context that DECLARES ``system`` (a worker) keeps the class its matching witness
records even when it carries another request's route; a machine witness stays machine; a live
request that declares nothing is still its own witness.
"""

from __future__ import annotations

import pytest

from matrx_connect import (
    CONTINUED_RUN_WITNESS_KEY,
    RESUMED_RUN_WITNESS_KEY,
    AppContext,
    clear_app_context,
    OWN_TEXT_WITNESS_KEY,
    continued_run_witness,
    own_text_witness,
    gate_origin_class,
    resumed_run_witness,
    set_app_context,
    system_app_context,
)
from matrx_connect.emitters.console_emitter import ConsoleEmitter

PERSON = "4cf62e4e-2679-484f-b652-034e697418df"
DOOR_ORG = "39c38960-d30c-4840-b0c1-c9960de95582"
TURN_ORG = "5dc930e9-bd65-44a1-8369-af773f6e1a5b"
PARKED_REQUEST = "46ae69a6-b92d-4193-93b2-563a28263c05"
ORIGINAL = {"route": "/ai/conversations/577db529", "auth_type": "token"}


def _door() -> AppContext:
    """The live ``/action-requests/complete`` request the person answered on."""
    return AppContext(
        emitter=ConsoleEmitter("door", accumulate=False),
        user_id=PERSON,
        organization_id=DOOR_ORG,
        route="/action-requests/complete",
        auth_type="token",
        is_authenticated=True,
        origin_class="human",
        request_id="0b0b0b0b-0000-4000-8000-000000000001",
    )


async def _worker_class(metadata: dict) -> str:
    token = set_app_context(_door())
    try:
        async with system_app_context(
            "action_request_continuation", user_id=PERSON, organization_id=TURN_ORG
        ) as base:
            assert base.route == "/action-requests/complete"  # the door's carrier survives
            resumed = base.with_overrides(request_id=PARKED_REQUEST, metadata=metadata)
            return gate_origin_class(resumed)
    finally:
        clear_app_context(token)


@pytest.mark.asyncio
async def test_a_resumed_person_turn_inside_a_live_request_is_theirs() -> None:
    record = resumed_run_witness(request_id=PARKED_REQUEST, user_id=PERSON, origin_class="human", origin_witness=ORIGINAL)
    assert await _worker_class({RESUMED_RUN_WITNESS_KEY: record}) == "human"


@pytest.mark.asyncio
async def test_a_continued_person_turn_inside_a_live_request_is_theirs() -> None:
    record = continued_run_witness(
        request_id=PARKED_REQUEST, user_id=PERSON, origin_class="human", origin_witness=ORIGINAL
    )
    assert await _worker_class({CONTINUED_RUN_WITNESS_KEY: record}) == "human"


@pytest.mark.asyncio
async def test_a_machine_witness_stays_machine_inside_a_live_request() -> None:
    record = resumed_run_witness(request_id=PARKED_REQUEST, user_id=PERSON, origin_class="scheduled", origin_witness={})
    assert await _worker_class({RESUMED_RUN_WITNESS_KEY: record}) == "scheduled"


@pytest.mark.asyncio
async def test_without_a_witness_the_worker_is_system() -> None:
    assert await _worker_class({}) == "system"


def test_a_live_request_that_declares_nothing_is_still_its_own_witness() -> None:
    record = resumed_run_witness(request_id=PARKED_REQUEST, user_id=PERSON, origin_class="human", origin_witness=ORIGINAL)
    live = AppContext(
        emitter=ConsoleEmitter("live", accumulate=False),
        user_id=PERSON,
        route="/ai/chat",
        auth_type="token",
        origin_class="",
        request_id=PARKED_REQUEST,
        metadata={RESUMED_RUN_WITNESS_KEY: record},
    )
    assert gate_origin_class(live) == "api"


@pytest.mark.asyncio
async def test_an_own_text_turn_inside_a_live_request_reads_like_the_other_two() -> None:
    """All three worker readers agree on what a worker context is (``_is_worker_context``)."""
    record = own_text_witness(
        inbound_message_id="11111111-1111-4111-8111-111111111111", user_id=PERSON, channel="sms", claim="spend_desk"
    )
    assert await _worker_class({OWN_TEXT_WITNESS_KEY: record}) == "human"


def test_an_own_text_record_on_a_live_request_that_declares_nothing_is_ignored() -> None:
    record = own_text_witness(
        inbound_message_id="11111111-1111-4111-8111-111111111111", user_id=PERSON, channel="sms", claim="x"
    )
    live = AppContext(
        emitter=ConsoleEmitter("live", accumulate=False),
        user_id=PERSON,
        route="/ai/chat",
        auth_type="token",
        origin_class="",
        request_id=PARKED_REQUEST,
        metadata={OWN_TEXT_WITNESS_KEY: record},
    )
    assert gate_origin_class(live) == "api"


# ── The same-identity branch applies what its caller asked for (review 2026-10-24) ─────────


@pytest.mark.asyncio
async def test_overrides_the_same_identity_branch_drops_are_announced(caplog) -> None:
    """The same-identity branch keeps a live request's own context (an entry point with an HTTP
    and a background caller), so the overrides it does not apply are SAID, once per feature —
    a continuation lost its channel metadata and narrowed authority there, silently."""
    import logging

    from matrx_connect.context import app_context

    app_context._DROPPED_OVERRIDES_ANNOUNCED.discard("override_drop_probe")
    door = _door().with_overrides(organization_id=TURN_ORG)
    token = set_app_context(door)
    try:
        with caplog.at_level(logging.WARNING, logger="matrx_connect.context.app_context"):
            async with system_app_context(
                "override_drop_probe", user_id=PERSON, organization_id=TURN_ORG, metadata={"channel": "web"}
            ) as ctx:
                assert ctx is door
    finally:
        clear_app_context(token)
    assert any("override_drop_probe" in r.getMessage() and "metadata" in r.getMessage() for r in caplog.records)


@pytest.mark.asyncio
async def test_isolated_applies_the_overrides_beside_the_same_identity_request() -> None:
    door = _door().with_overrides(organization_id=TURN_ORG, is_admin=True, admin_surface=True)
    token = set_app_context(door)
    try:
        async with system_app_context(
            "action_request_continuation",
            user_id=PERSON,
            organization_id=TURN_ORG,
            isolated=True,
            metadata={"channel": "web"},
            is_admin=False,
            admin_surface=False,
        ) as ctx:
            assert ctx is not door
            assert ctx.metadata.get("channel") == "web"
            assert ctx.is_admin is False and ctx.admin_surface is False
    finally:
        clear_app_context(token)


@pytest.mark.asyncio
async def test_the_same_identity_branch_without_overrides_is_the_ambient_context() -> None:
    door = _door().with_overrides(organization_id=TURN_ORG)
    token = set_app_context(door)
    try:
        async with system_app_context("probe", user_id=PERSON, organization_id=TURN_ORG) as ctx:
            assert ctx is door
    finally:
        clear_app_context(token)
