"""Every fixable refusal carries its way through as data (no-dead-ends rule 16)."""

from matrx_connect.fix_actions import (
    FIX_ACTION_BY_CODE, PLATFORM_FIX_TOKENS, fix_action_for, with_fix_action,
)
from matrx_connect.org_hold import OrganizationRequired, organization_hold_detail


def test_every_mapped_code_uses_a_declared_token():
    assert set(FIX_ACTION_BY_CODE.values()) <= PLATFORM_FIX_TOKENS


def test_organization_hold_carries_pick_organization_flat_and_in_details():
    detail = organization_hold_detail(what="no org")
    assert detail["fix_action"] == "pick_organization"
    assert detail["details"]["fix_action"] == "pick_organization"
    assert OrganizationRequired(what="x").detail["fix_action"] == "pick_organization"


def test_with_fix_action_adds_for_fixable_and_never_for_unfixable_or_overwrites():
    assert with_fix_action({"code": "not_connected"})["fix_action"] == "connect_integration"
    assert "fix_action" not in with_fix_action({"code": "something_unfixable"})
    assert with_fix_action({"code": "not_connected", "fix_action": "x"})["fix_action"] == "x"
    assert fix_action_for(None) is None
