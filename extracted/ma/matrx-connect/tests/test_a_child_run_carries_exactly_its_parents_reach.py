"""A child run carries EXACTLY the reach its parent turn had — never less, never more.

Lane P, 2026-11-17 (agent-build report gap G1: "admin reach is lost in helper runs"). The context law
(common-docs/policies/context-is-carried-never-rebuilt.md): actor and reach are minted at the boundary
and CARRIED by every hop. Every helper, ``staff_escalate`` / ``mandate_call`` holder and nested helper is
minted by ``child_agent_context`` (``run_agent`` → ``fork_for_child_agent``), and a machine child of a
turn by ``with_overrides(system_run=True)``. This pins, through those real mints:

* an admin parent's child (and grandchild, and machine child) is still that admin — an admin-only tool
  (``admin_tool_authorized``) and an admin-surface reach (``admin_lane_active``) answer as they did
  for the parent;
* a non-admin parent's child gains nothing;
* a delegated member (SMS / voice) stays a delegated member with no admin tier, at every depth.
"""

from __future__ import annotations

import pytest

from matrx_connect.context.app_context import (
    AppContext,
    admin_lane_active,
    admin_tool_authorized,
    child_agent_context,
    clear_app_context,
    get_app_context,
    set_app_context,
)

USER = "22222222-2222-4222-8222-222222222222"
ORG = "66666666-6666-4666-8666-666666666666"


def _turn(**overrides: object) -> AppContext:
    from matrx_connect.emitters import SilentEmitter

    fields: dict[str, object] = {
        "emitter": SilentEmitter(),
        "user_id": USER,
        "organization_id": ORG,
        "request_id": "11111111-1111-4111-8111-111111111111",
        "conversation_id": "1507ab15-d721-49d6-a92e-db73880f2a8e",
        "origin_class": "human",
    }
    fields.update(overrides)
    return AppContext(**fields)  # type: ignore[arg-type]


async def _reach_in_children(parent: AppContext) -> list[tuple[bool, bool, str | None]]:
    """(admin tool, admin lane, tier) seen by a child, a grandchild and a machine child."""
    seen: list[tuple[bool, bool, str | None]] = []
    token = set_app_context(parent)
    try:
        async with child_agent_context("helper", emit_lifecycle=False):
            child = get_app_context()
            seen.append((admin_tool_authorized(), admin_lane_active(), child.admin_level))
            async with child_agent_context("helper-of-helper", emit_lifecycle=False):
                seen.append((admin_tool_authorized(), admin_lane_active(), get_app_context().admin_level))
            machine = child.with_overrides(system_run=True)
            seen.append((admin_tool_authorized(machine), admin_lane_active(machine), machine.admin_level))
    finally:
        clear_app_context(token)
    return seen


@pytest.mark.asyncio
async def test_an_admins_helpers_keep_the_admin_reach_of_the_turn() -> None:
    parent = _turn(is_admin=True, admin_level="super_admin", admin_surface=True)
    assert (admin_tool_authorized(parent), admin_lane_active(parent)) == (True, True)
    assert await _reach_in_children(parent) == [(True, True, "super_admin")] * 3


@pytest.mark.asyncio
async def test_the_admin_header_lane_is_carried_too() -> None:
    parent = _turn(is_admin=True, admin_level="super_admin", metadata={"organization_admitted_by": "admin_lane"})
    assert await _reach_in_children(parent) == [(True, True, "super_admin")] * 3


@pytest.mark.asyncio
async def test_an_admin_in_a_normal_chat_carries_the_tool_reach_but_never_gains_the_lane() -> None:
    parent = _turn(is_admin=True, admin_level="super_admin")
    assert await _reach_in_children(parent) == [(True, False, "super_admin")] * 3


@pytest.mark.asyncio
async def test_a_members_helpers_gain_nothing() -> None:
    parent = _turn()
    assert await _reach_in_children(parent) == [(False, False, None)] * 3


@pytest.mark.asyncio
async def test_a_delegated_member_stays_a_delegated_member_at_every_depth() -> None:
    from matrx_connect import delegated_member_context

    async def prove(user_id: str, organization_id: str) -> str:
        return organization_id

    async with delegated_member_context(
        USER,
        ORG,
        reason="a test text from the person's own verified phone",
        channel="sms",
        prove_membership=prove,
        prover_id="test.prover",
        feature="test.feature",
        conversation_id="1507ab15-d721-49d6-a92e-db73880f2a8e",
        request_id="11111111-1111-4111-8111-111111111111",
    ) as turn:
        assert type(turn).__name__ == "DelegatedMemberAppContext"
        async with child_agent_context("helper", emit_lifecycle=False):
            child = get_app_context()
            assert type(child).__name__ == "DelegatedMemberAppContext"
            assert (admin_tool_authorized(), admin_lane_active(), child.admin_level) == (False, False, None)
            machine = child.with_overrides(system_run=True)
            assert type(machine).__name__ == "DelegatedMemberAppContext"
            assert admin_tool_authorized(machine) is False
