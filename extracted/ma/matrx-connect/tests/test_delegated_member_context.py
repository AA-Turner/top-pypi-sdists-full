"""Forcing contract tests for the delegated member boundary.

Every test here is a door somebody will try. The boundary admits a worker as a
MEMBER — the strongest tenant admission the platform has — so each refusal is
pinned by a test that fails if the refusal is ever relaxed, and the one
permission it grants is pinned by a test that fails if it stops working.
"""

from __future__ import annotations

import asyncio
import contextvars
import dataclasses
from datetime import UTC, datetime

import pytest

from matrx_connect import ConsoleEmitter
from matrx_connect.context import (
    AppContext,
    DelegatedMemberAppContext,
    DelegatedMemberTenantProvenance,
    DelegatedMembershipDenied,
    DelegatedMembershipUnverifiable,
    MembershipProof,
    TenantAppContext,
    delegated_member_admission,
    delegated_member_context,
    get_app_context,
    is_delegated_member_context,
    require_interactive_human,
    require_tenant_context,
    set_app_context,
    tenant_system_context,
    try_get_app_context,
)
from matrx_connect.context.delegated_member import DelegatedMemberAdmissionError
from matrx_connect.context.provenance import (
    ATTESTED_ORIGIN_CLASSES,
    MACHINE_ORIGIN_CLASSES,
    ORIGIN_CLASS_DELEGATED_MEMBER,
    reconcile_origin,
)

ORG_ID = "11111111-1111-4111-8111-111111111111"
OTHER_ORG_ID = "22222222-2222-4222-8222-222222222222"
USER_ID = "87a6e699-3622-4869-8843-d0867456c0dd"


async def _in_empty_context(coro_fn):
    loop = asyncio.get_running_loop()
    return await loop.create_task(coro_fn(), context=contextvars.Context())


async def _member(user_id: str, organization_id: str) -> str:
    return organization_id


def _open(**kwargs):
    params = {
        "reason": "answering an inbound text to the Personal Staff number",
        "channel": "sms",
        "prove_membership": _member,
        "prover_id": "test.membership",
    }
    params.update(kwargs)
    return delegated_member_context(USER_ID, ORG_ID, **params)


# ── What it grants ───────────────────────────────────────────────────────────


@pytest.mark.asyncio
async def test_a_proved_member_turn_is_admitted_as_a_member_and_says_it_is_delegated() -> None:
    async def work() -> None:
        async with _open() as ctx:
            assert isinstance(ctx, DelegatedMemberAppContext)
            assert isinstance(ctx, TenantAppContext)
            assert ctx.user_id == USER_ID
            assert ctx.organization_id == ORG_ID
            # The whole point: the three staff gates read exactly these.
            assert ctx.organization_admission == "verified"
            assert ctx.is_authenticated is True
            assert ctx.origin_class == ORIGIN_CLASS_DELEGATED_MEMBER
            assert ctx.system_run is False
            assert get_app_context() is ctx
        assert try_get_app_context() is None

    await _in_empty_context(work)


@pytest.mark.asyncio
async def test_the_admission_is_audited_with_reason_channel_and_proof_id() -> None:
    async def work() -> None:
        async with _open() as ctx:
            record = delegated_member_admission(ctx)
            assert record is not None
            assert record["reason"] == "answering an inbound text to the Personal Staff number"
            assert record["channel"] == "sms"
            assert record["prover_id"] == "test.membership"
            assert record["membership_proof_id"]
            assert datetime.fromisoformat(record["verified_at"]).tzinfo is not None
            # The persistence witness carries the audit onto every row the turn writes.
            _, witness = reconcile_origin(ctx)
            assert witness["delegated_member_admission"] == record

    await _in_empty_context(work)


@pytest.mark.asyncio
async def test_the_origin_class_survives_the_persistence_witness() -> None:
    async def work() -> None:
        async with _open() as ctx:
            final, _ = reconcile_origin(ctx)
            assert final == ORIGIN_CLASS_DELEGATED_MEMBER
            # Even with the label stripped, the TYPE still answers honestly —
            # never the plain 'system' that made the staff turn refuse.
            stripped = dataclasses.replace(ctx, origin_class="")
            final_stripped, _ = reconcile_origin(stripped)
            assert final_stripped == ORIGIN_CLASS_DELEGATED_MEMBER

    await _in_empty_context(work)
    assert ORIGIN_CLASS_DELEGATED_MEMBER in MACHINE_ORIGIN_CLASSES


# ── It cannot be minted without a live proof ─────────────────────────────────


@pytest.mark.asyncio
async def test_no_prover_means_no_context() -> None:
    async def work() -> None:
        with pytest.raises(TypeError):
            async with delegated_member_context(
                USER_ID, ORG_ID, reason="r", channel="sms", prover_id="p"
            ):
                pass
        with pytest.raises(ValueError, match="prove_membership is required"):
            async with _open(prove_membership="not callable"):
                pass
        assert try_get_app_context() is None

    await _in_empty_context(work)


@pytest.mark.asyncio
async def test_a_proved_non_member_is_denied_and_nothing_is_installed() -> None:
    async def deny(user_id: str, organization_id: str) -> None:
        return None

    async def work() -> None:
        with pytest.raises(DelegatedMembershipDenied, match="not an active member"):
            async with _open(prove_membership=deny):
                pass
        assert try_get_app_context() is None

    await _in_empty_context(work)


@pytest.mark.asyncio
async def test_a_resolver_outage_is_unverifiable_and_never_falls_back_to_system() -> None:
    async def blow_up(user_id: str, organization_id: str) -> str:
        raise RuntimeError("pool exhausted")

    async def work() -> None:
        with pytest.raises(DelegatedMembershipUnverifiable, match="could not confirm"):
            async with _open(prove_membership=blow_up):
                pass
        assert try_get_app_context() is None

    await _in_empty_context(work)


@pytest.mark.asyncio
async def test_a_resolver_that_verifies_another_organization_is_refused() -> None:
    async def elsewhere(user_id: str, organization_id: str) -> str:
        return OTHER_ORG_ID

    async def work() -> None:
        with pytest.raises(DelegatedMembershipDenied, match="DIFFERENT organization"):
            async with _open(prove_membership=elsewhere):
                pass

    await _in_empty_context(work)


def test_a_membership_proof_cannot_be_forged_from_outside_the_boundary() -> None:
    with pytest.raises(ValueError, match="only be minted by the delegated member boundary"):
        MembershipProof(
            organization_id=ORG_ID,
            principal=USER_ID,
            proof_id="33333333-3333-4333-8333-333333333333",
            prover_id="attacker",
            verified_at=datetime.now(UTC),
        )
    with pytest.raises(ValueError, match="typed membership proof"):
        DelegatedMemberTenantProvenance(
            proof={"organization_id": ORG_ID, "principal": USER_ID},  # type: ignore[arg-type]
            reason="r",
            channel="sms",
        )


def test_a_delegated_context_cannot_be_hand_built() -> None:
    # No provenance at all.
    with pytest.raises(ValueError, match="tenant organization admission binding is required"):
        DelegatedMemberAppContext(
            emitter=ConsoleEmitter("x", accumulate=False),
            user_id=USER_ID,
            organization_id=ORG_ID,
            is_authenticated=True,
            organization_admission="verified",
        )
    # Membership provenance wearing the delegated type: refused, because the
    # two are one thing.
    from matrx_connect.context.app_context import _context_init_fields, _mint_tenant_context
    from matrx_connect.context.tenant_provenance import MembershipTenantProvenance

    base = AppContext(
        emitter=ConsoleEmitter("x", accumulate=False),
        user_id=USER_ID,
        organization_id=ORG_ID,
        is_authenticated=True,
        organization_admission="verified",
    )
    minted = _mint_tenant_context(
        _context_init_fields(base), MembershipTenantProvenance(ORG_ID, USER_ID)
    )
    assert type(minted) is TenantAppContext
    assert not is_delegated_member_context(minted)
    with pytest.raises(ValueError, match="delegated member context and delegated member provenance"):
        DelegatedMemberAppContext(**_context_init_fields(minted))


# ── It is not a signed-in session ────────────────────────────────────────────


@pytest.mark.asyncio
async def test_it_carries_no_token_no_jwt_claims_and_no_admin_tier() -> None:
    async def work() -> None:
        async with _open() as ctx:
            assert ctx.token is None
            assert ctx.metadata.get("jwt_claims") is None
            assert ctx.is_admin is False
            assert ctx.admin_level is None

    await _in_empty_context(work)


@pytest.mark.asyncio
async def test_a_session_credential_cannot_be_pasted_onto_it() -> None:
    async def work() -> None:
        for field in ("token", "is_admin", "admin_level", "auth_type", "origin_class"):
            with pytest.raises(ValueError, match="not overrideable"):
                async with _open(**{field: "x"}):
                    pass
        # Nor after the fact: the frozen copy re-validates.
        async with _open() as ctx:
            with pytest.raises(ValueError, match="carries no session token"):
                dataclasses.replace(ctx, token="eyJhbGciOi")
            with pytest.raises(ValueError, match="carries no JWT claims"):
                dataclasses.replace(ctx, metadata={**ctx.metadata, "jwt_claims": {"amr": []}})
            with pytest.raises(ValueError, match="never carries an admin tier"):
                dataclasses.replace(ctx, is_admin=True, admin_level="super_admin")
            with pytest.raises(ValueError, match="may not claim origin_class"):
                # Read back, never stamped: the attested vocabulary is
                # derivation-only (scripts/check_origin_provenance.py).
                dataclasses.replace(ctx, origin_class=ATTESTED_ORIGIN_CLASSES[0])

    await _in_empty_context(work)


@pytest.mark.asyncio
async def test_anything_needing_a_person_present_refuses() -> None:
    async def work() -> None:
        async with _open() as ctx:
            with pytest.raises(DelegatedMemberAdmissionError, match="nobody is at a keyboard"):
                require_interactive_human(ctx, "Revealing this password")

    await _in_empty_context(work)
    # An ordinary signed-in context sails through the same call.
    require_interactive_human(
        AppContext(emitter=ConsoleEmitter("x", accumulate=False), user_id=USER_ID),
        "Revealing this password",
    )


@pytest.mark.asyncio
async def test_it_cannot_open_a_credential_filling_context() -> None:
    async def work() -> None:
        for capability in ("credential_fill", "credential_login", "vault_reveal"):
            with pytest.raises(ValueError, match="its own consented capability"):
                async with _open(capabilities=[capability, "send_text"]):
                    pass

    await _in_empty_context(work)


# ── Tenancy cannot be moved ──────────────────────────────────────────────────


@pytest.mark.asyncio
async def test_the_admitted_tenant_cannot_be_repointed_or_downgraded() -> None:
    async def work() -> None:
        async with _open() as ctx:
            with pytest.raises(ValueError, match="tenant organization cannot be replaced"):
                dataclasses.replace(ctx, organization_id=OTHER_ORG_ID)
            with pytest.raises(ValueError, match="tenant admission provenance cannot be replaced"):
                dataclasses.replace(ctx, organization_admission="none")
            with pytest.raises(AttributeError, match="not overrideable"):
                ctx.with_overrides(_tenant_provenance=None)
            # Forks keep both the type and the admission.
            child = ctx.fork_for_child_agent("44444444-4444-4444-8444-444444444444")
            assert isinstance(child, DelegatedMemberAppContext)
            assert child.organization_admission == "verified"
            assert child.origin_class == "child_agent"

    await _in_empty_context(work)


@pytest.mark.asyncio
async def test_only_a_channel_that_proves_the_speaker_may_open_one() -> None:
    async def work() -> None:
        for channel in ("email", "web", "", "SMS"):
            with pytest.raises(ValueError, match="channel must be one of"):
                async with _open(channel=channel):
                    pass
        with pytest.raises(ValueError, match="reason must be a nonempty string"):
            async with _open(reason="  "):
                pass

    await _in_empty_context(work)


@pytest.mark.asyncio
async def test_it_refuses_to_open_inside_another_tenants_admitted_work() -> None:
    async def work() -> None:
        async with tenant_system_context("other-worker", user_id="someone-else", organization_id=OTHER_ORG_ID):
            with pytest.raises(DelegatedMemberAdmissionError, match="channel ingress"):
                async with _open():
                    pass

    await _in_empty_context(work)


@pytest.mark.asyncio
async def test_a_system_context_is_still_not_a_member_and_still_not_delegated() -> None:
    """The RED half stays red: nothing here loosened the system context."""

    async def work() -> None:
        async with tenant_system_context(
            "sms-assistant", user_id=USER_ID, organization_id=ORG_ID
        ) as ctx:
            assert ctx.organization_admission == "none"
            assert ctx.origin_class == "system"
            assert not is_delegated_member_context(ctx)
            assert delegated_member_admission(ctx) is None

    await _in_empty_context(work)


@pytest.mark.asyncio
async def test_a_system_block_inside_a_delegated_turn_keeps_the_member_admission() -> None:
    """The adoption path: existing system_app_context calls under the boundary.

    ``tenant_system_context`` yields an ambient tenant context for the same
    actor untouched, so code already wrapped in one does NOT silently fall back
    to ``organization_admission="none"`` once the ingress opens the delegated
    boundary around it.
    """

    async def work() -> None:
        async with _open() as delegated:
            async with tenant_system_context(
                "sms-assistant", user_id=USER_ID, organization_id=ORG_ID
            ) as inner:
                assert inner is delegated
                assert inner.organization_admission == "verified"
            assert require_tenant_context(delegated) is delegated

    await _in_empty_context(work)


@pytest.mark.asyncio
async def test_the_boundary_never_inherits_an_ambient_request_context() -> None:
    """A carrier webhook is an anonymous HTTP request; nothing of it leaks in."""

    async def work() -> None:
        webhook = AppContext(
            emitter=ConsoleEmitter("webhook", accumulate=False),
            user_id="",
            auth_type="anonymous",
            route="/communications/sms/inbound",
            token="carrier-bearer",
            metadata={"jwt_claims": {"amr": [{"timestamp": 1}]}},
        )
        token = set_app_context(webhook)
        try:
            async with _open() as ctx:
                assert ctx.token is None
                assert ctx.metadata.get("jwt_claims") is None
                assert ctx.emitter is not webhook.emitter
                assert ctx.user_id == USER_ID
        finally:
            from matrx_connect.context import clear_app_context

            clear_app_context(token)

    await _in_empty_context(work)


@pytest.mark.asyncio
async def test_a_parentless_fork_under_a_member_turn_records_the_member_not_the_platform() -> None:
    """A mandate the staff turn starts with no conversation was started on the verified member's
    word: its record reads ``delegated_member``, never ``system`` (2026-10-16)."""

    async def work() -> None:
        async with _open() as ctx:
            child = ctx.fork_for_child_agent("44444444-4444-4444-8444-444444444444")
            assert child.parent_conversation_id is None
            assert reconcile_origin(child)[0] == ORIGIN_CLASS_DELEGATED_MEMBER

    await _in_empty_context(work)
